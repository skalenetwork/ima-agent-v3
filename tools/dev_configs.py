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

import os

from eth_typing import ChecksumAddress, HexStr
from pydantic_settings import BaseSettings, SettingsConfigDict

TEST_TOKENS_DIR = 'test-tokens'
TEST_TOKENS_PATH = os.path.join(os.path.dirname(__file__), '..', TEST_TOKENS_DIR)


class DevConfig(BaseSettings):
    eth_private_key: HexStr

    erc20_mainnet_address: ChecksumAddress | None = None
    erc20_schain_address: ChecksumAddress | None = None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


def get_dev_config() -> DevConfig:
    return DevConfig()  # type: ignore[call-arg]
