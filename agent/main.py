#   -*- coding: utf-8 -*-
#
#   This file is part of ima-agent
#
#   Copyright (C) 2025 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from multiprocessing import SimpleQueue

from agent.executor import JobExecutor
from agent.logger import init_logger
from agent.producers import m2s_loop, s2m_loop, s2s_loop
from agent.thread_group import ThreadGroup

logger = logging.getLogger(__name__)


def run_agent() -> None:
    executor = JobExecutor(workers=6)
    errq: SimpleQueue[BaseException] = SimpleQueue()
    tg = ThreadGroup()
    try:
        tg.go(m2s_loop, executor, errq)
        tg.go(s2m_loop, executor, errq)
        tg.go(s2s_loop, executor, errq)
        tg.join()
    finally:
        executor.shutdown()


if __name__ == '__main__':
    init_logger()
    run_agent()
