import logging
import os
import subprocess
from subprocess import PIPE

logger = logging.getLogger(__name__)


def run_cmd(
    cmd: list[str], env: dict[str, str] = {}, shell: bool = False, cwd: str | None = None
) -> subprocess.CompletedProcess:
    logger.info(f'Running: {cmd}')
    res = subprocess.run(
        cmd, shell=shell, stdout=PIPE, stderr=PIPE, env={**os.environ, **env}, cwd=cwd
    )
    if res.returncode:
        logger.error('Error during shell execution:')
        logger.error(res.stderr.decode('UTF-8').rstrip())
        raise subprocess.CalledProcessError(res.returncode, cmd)
    return res
