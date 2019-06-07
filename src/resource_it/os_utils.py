import shutil
import shlex
from subprocess import run as proc_run
from subprocess import PIPE, CompletedProcess
from os.path import expanduser, expandvars

import log_it
log = log_it.logger(__name__)

def run(cmd, cwd=None, fail_msg=None, **kwargs):
    args = shlex.split(cmd)
    args = [expanduser(expandvars(arg)) for arg in args if arg is not None]
    bin_name = args[0]
    args[0] = shutil.which(bin_name)

    try:
        proc_result = proc_run(args=args, cwd=cwd, encoding="utf-8",
                               stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)

        log.debug(
            "Results of executing `{bin}`".format(bin=bin_name),
            extra=dict(
                args=proc_result.args,
                returncode=proc_result.returncode,
                stdout=proc_result.stdout,
                stderr=proc_result.stderr))
    except Exception:
        log.debug(fail_msg, exc_info=True)
        proc_result = CompletedProcess(args, 1)
    return proc_result

def run_output(proc_result):
    return proc_result.stdout.strip()
