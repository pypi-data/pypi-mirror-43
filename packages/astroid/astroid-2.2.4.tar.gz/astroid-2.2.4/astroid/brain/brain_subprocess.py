# Copyright (c) 2016-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2017 Hugo <hugovk@users.noreply.github.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>

# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/master/COPYING.LESSER

import sys
import textwrap

import six

import astroid


PY37 = sys.version_info >= (3, 7)
PY36 = sys.version_info >= (3, 6)
PY34 = sys.version_info >= (3, 4)
PY33 = sys.version_info >= (3, 3)


def _subprocess_transform():
    if six.PY3:
        communicate = (bytes("string", "ascii"), bytes("string", "ascii"))
        communicate_signature = "def communicate(self, input=None, timeout=None)"
        if PY37:
            init = """
            def __init__(self, args, bufsize=0, executable=None,
                         stdin=None, stdout=None, stderr=None,
                         preexec_fn=None, close_fds=False, shell=False,
                         cwd=None, env=None, universal_newlines=False,
                         startupinfo=None, creationflags=0, restore_signals=True,
                         start_new_session=False, pass_fds=(), *,
                         encoding=None, errors=None, text=None):
                pass
            """
        elif PY36:
            init = """
            def __init__(self, args, bufsize=0, executable=None,
                         stdin=None, stdout=None, stderr=None,
                         preexec_fn=None, close_fds=False, shell=False,
                         cwd=None, env=None, universal_newlines=False,
                         startupinfo=None, creationflags=0, restore_signals=True,
                         start_new_session=False, pass_fds=(), *,
                         encoding=None, errors=None):
                pass
            """
        else:
            init = """
            def __init__(self, args, bufsize=0, executable=None,
                         stdin=None, stdout=None, stderr=None,
                         preexec_fn=None, close_fds=False, shell=False,
                         cwd=None, env=None, universal_newlines=False,
                         startupinfo=None, creationflags=0, restore_signals=True,
                         start_new_session=False, pass_fds=()):
                pass
            """
    else:
        communicate = ("string", "string")
        communicate_signature = "def communicate(self, input=None)"
        init = """
        def __init__(self, args, bufsize=0, executable=None,
                     stdin=None, stdout=None, stderr=None,
                     preexec_fn=None, close_fds=False, shell=False,
                     cwd=None, env=None, universal_newlines=False,
                     startupinfo=None, creationflags=0):
            pass
        """
    if PY34:
        wait_signature = "def wait(self, timeout=None)"
    else:
        wait_signature = "def wait(self)"
    if six.PY3:
        ctx_manager = """
        def __enter__(self): return self
        def __exit__(self, *args): pass
        """
    else:
        ctx_manager = ""
    py3_args = ""
    if PY33:
        py3_args = "args = []"
    code = textwrap.dedent(
        """
    class Popen(object):
        returncode = pid = 0
        stdin = stdout = stderr = file()
        %(py3_args)s

        %(communicate_signature)s:
            return %(communicate)r
        %(wait_signature)s:
            return self.returncode
        def poll(self):
            return self.returncode
        def send_signal(self, signal):
            pass
        def terminate(self):
            pass
        def kill(self):
            pass
        %(ctx_manager)s
       """
        % {
            "communicate": communicate,
            "communicate_signature": communicate_signature,
            "wait_signature": wait_signature,
            "ctx_manager": ctx_manager,
            "py3_args": py3_args,
        }
    )

    init_lines = textwrap.dedent(init).splitlines()
    indented_init = "\n".join(" " * 4 + line for line in init_lines)
    code += indented_init
    return astroid.parse(code)


astroid.register_module_extender(astroid.MANAGER, "subprocess", _subprocess_transform)
