import subprocess
import sys
import re
import logging
import errno
import os
from pprint import pformat

from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

from .errors import *

class ExternTool(object):
    def __init__(self, cmd, os_pkg, stderr_ignore=[], encoding='utf-8'):
        self.cmd = cmd
        self.os_pkg = os_pkg
        self.capture_stdout = True
        self.stderr_ignore = stderr_ignore
        self.encoding = encoding

    def __should_ignore(self, line):
        for ignore in self.stderr_ignore:
            if ignore in line:
                return True
        return False

    def run(self, *args, **kw):
        args = list(args)
        args.insert(0, self.cmd)

        kw['stderr'] = subprocess.PIPE
        if self.capture_stdout:
            kw['stdout'] = subprocess.PIPE

        logging.debug("Running " + str(args))
        try:
            p = subprocess.Popen(args, **kw)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise MissingToolError(self.cmd, self.os_pkg)
            raise

        stdout, stderr = p.communicate()
        stdout = stdout.decode(self.encoding)
        stderr = stderr.decode(self.encoding)

        # Hide ignored lines from stderr
        for line in stderr.splitlines(True):
            if self.__should_ignore(line):
                continue
            sys.stderr.write(line)

        if p.returncode != 0:
            raise ToolError(self.cmd, '{} returned {}'.format(self.cmd, p.returncode))

        return stdout




tool_ldd        = ExternTool('ldd', 'binutils')
tool_objcopy    = ExternTool('objcopy', 'binutils')
tool_patchelf   = ExternTool('patchelf', 'patchelf',
                    stderr_ignore = [
                        'working around a Linux kernel bug by creating a hole',
                    ])
tool_strip      = ExternTool('strip', 'binutils')

def get_shobj_deps(path, libpath=[]):
    # TODO: Should we use dict(os.environ) instead?
    #       For now, make sure we always pass a clean environment.
    env = {}

    if libpath:
        # Prepend to LD_LIBRARY_PATH
        assert isinstance(libpath, list)
        old_libpath = env.get('LD_LIBRARY_PATH', '')
        env['LD_LIBRARY_PATH'] = ':'.join(libpath + [old_libpath])

    output = tool_ldd.run(path, env=env)

    # Example:
    #	libc.so.6 => /usr/lib64/libc.so.6 (0x00007f42ac010000)
    #	/lib64/ld-linux-x86-64.so.2 (0x0000557376e75000)
    pat = re.compile('\t([\w./+-]*) (?:=> ([\w./+-]*) )?\((0x[0-9a-fA-F]*)\)')

    ignore_list = [
        'linux-vdso.so',
    ]

    def ignore(p):
        for name in ignore_list:
            if libpath.startswith(name):
                return True
        return False

    for line in output.splitlines():
        m = pat.match(line)
        if not m:
            # Some shared objs might have no DT_NEEDED tags (see issue #67)
            if line == '\tstatically linked':
                break
            raise ToolError('ldd', "Unexpected line in ldd output: " + line)
        libname  = m.group(1)
        libpath  = m.group(2)
        baseaddr = int(m.group(3), 16)

        libpath = libpath or libname

        if ignore(libpath):
            continue
        yield libpath



def elf_add_section(elfpath, secname, secfilename):
    tool_objcopy.run(
        '--add-section', '{}={}'.format(secname, secfilename),
        elfpath)

def patch_elf(path, interpreter=None, rpath=None, force_rpath=False):
    args = []
    if interpreter:
        args += ['--set-interpreter', interpreter]
    if rpath:
        args += ['--set-rpath', rpath]
    if force_rpath:
        args.append('--force-rpath')
    args.append(path)

    tool_patchelf.run(*args)

def strip_elf(path):
    tool_strip.run(path)


################################################################################
# Using pyelftools

class ELFCloser(object):
    def __init__(self, path, mode):
        self.f = open(path, mode)
        self.elf = ELFFile(self.f)

    def __enter__(self):
        return self.elf

    def __exit__(self, *exc_info):
        self.f.close()

def _open_elf(path, mode='rb'):
    try:
        return ELFCloser(path, mode)
    except ELFError as e:
        raise InvalidInputError("{}: Invalid ELF image: {}".format(path, e))


def get_machine(path):
    with _open_elf(path) as elf:
        return elf['e_machine']

def get_prog_interp(path):
    with _open_elf(path) as elf:
        for seg in elf.iter_segments():
            # Amazingly, this is slightly faster than
            # if isinstance(seg, InterpSegment):
            try:
                return seg.get_interp_name()
            except AttributeError:
                continue
        else:
            raise InvalidInputError("{}: not a dynamic executable "
                                    "(no interp segment)".format(path))

