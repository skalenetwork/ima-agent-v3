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
import re
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

from agent.configs import get_config

LOCAL_IPS = ['127.0.0.1', 'localhost']
LOG_FILE_SIZE_MB = 100
LOG_FILE_SIZE_BYTES = LOG_FILE_SIZE_MB * 1000000
LOG_BACKUP_COUNT = 20

LOG_FORMAT = '[%(asctime)s %(levelname)s][%(threadName)s] - %(name)s:%(lineno)d - %(message)s'  # noqa


def compose_hiding_patterns() -> dict:
    config = get_config()
    # sgx_ip = urlparse(SGX_SERVER_URL).hostname
    eth_ip = urlparse(config.mainnet_endpoint).hostname
    patterns = {r'NEK\:\w+': '[SGX_KEY]'}
    # if sgx_ip not in LOCAL_IPS:
    #     patterns.update({rf'{sgx_ip}': '[SGX_IP]'})
    if eth_ip not in LOCAL_IPS:
        patterns.update({rf'{eth_ip}': '[ETH_IP]'})
    return patterns


class HidingFormatter(logging.Formatter):
    def __init__(self, log_format: str, patterns: dict) -> None:
        super().__init__(log_format)
        self._patterns: dict = patterns

    def _filter_sensitive(self, msg: str) -> str:
        for match, replacement in self._patterns.items():
            pat = re.compile(match)
            msg = pat.sub(replacement, msg)
        return msg

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        return self._filter_sensitive(msg)

    def formatException(self, exc_info: tuple) -> str:
        msg = super().formatException(exc_info)
        return self._filter_sensitive(msg)

    def formatStack(self, stack_info: str) -> str:
        msg = super().formatStack(stack_info)
        return self._filter_sensitive(msg)


def init_logger(log_file_path: str | None = None, debug_file_path: str | None = None) -> None:
    handlers: list[logging.Handler] = []

    hiding_patterns = compose_hiding_patterns()
    formatter = HidingFormatter(LOG_FORMAT, hiding_patterns)
    if log_file_path:
        f_handler = RotatingFileHandler(
            log_file_path, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=LOG_BACKUP_COUNT
        )

        f_handler.setFormatter(formatter)
        f_handler.setLevel(logging.INFO)
        handlers.append(f_handler)

    stream_handler = StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    handlers.append(stream_handler)

    if debug_file_path:
        f_handler_debug = RotatingFileHandler(
            debug_file_path, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=LOG_BACKUP_COUNT
        )
        f_handler_debug.setFormatter(formatter)
        f_handler_debug.setLevel(logging.DEBUG)
        handlers.append(f_handler_debug)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)
