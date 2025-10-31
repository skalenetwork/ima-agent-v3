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

from pydantic_settings import BaseSettings, SettingsConfigDict
from skale.types.schain import SchainName


class SgxConfig(BaseSettings):
    sgx_url: str
    ecdsa_key_name: str
    bls_key_name: str
    sgx_ssl_key_path: str
    sgx_ssl_cert_path: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


class Config(BaseSettings):
    mainnet_endpoint: str
    schain_endpoint: str
    ima_contracts: str
    manager_contracts: str
    schain_name: SchainName

    ima_contracts_schain: str = 'predeployed'

    agent_loop_sleep: int = 5
    agent_loop_error_sleep: int = 2

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


def get_config() -> Config:
    return Config()  # type: ignore[call-arg]


def get_sgx_config() -> SgxConfig:
    return SgxConfig()  # type: ignore[call-arg]
