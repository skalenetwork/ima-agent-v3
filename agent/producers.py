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

from __future__ import annotations

import logging
import time
from queue import SimpleQueue
from threading import Event

from agent.configs import get_config
from agent.executor import JobExecutor
from agent.pipeline import run_m2s_pipeline, run_s2s_pipeline
from agent.web3_tools import get_ima_mn, get_ima_sc, get_skale_manager

logger = logging.getLogger(__name__)


def m2s_loop(exe: JobExecutor, errq: SimpleQueue[BaseException], *, cancel: Event) -> None:
    logger.info('Starting m2s producer')
    config = get_config()
    ima_mn = get_ima_mn(config)
    ima_sc = get_ima_sc(config)

    while not cancel.is_set():
        logger.info('gathering all jobs for m2s')
        run_m2s_pipeline(ima_mn, ima_sc)
        if not errq.empty():
            raise errq.get()
        time.sleep(config.agent_loop_sleep)


def s2m_loop(exe: JobExecutor, errq: SimpleQueue[BaseException], *, cancel: Event) -> None:
    logger.info('Starting s2m producer')
    config = get_config()
    while not cancel.is_set():
        logger.info('gathering all jobs for s2m')
        if not errq.empty():
            raise errq.get()
        time.sleep(config.agent_loop_sleep)


def s2s_loop(exe: JobExecutor, errq: SimpleQueue[BaseException], *, cancel: Event) -> None:
    logger.info('Starting s2s producer')
    config = get_config()
    skale = get_skale_manager(config)
    ima_sc = get_ima_sc(config)

    while not cancel.is_set():
        logger.info('gathering all jobs for s2s')
        run_s2s_pipeline(skale, ima_sc)
        if not errq.empty():
            raise errq.get()
        time.sleep(config.agent_loop_sleep)
