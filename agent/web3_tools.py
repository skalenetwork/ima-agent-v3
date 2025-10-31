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

from skale import SchainIma, SkaleIma, SkaleManager
from skale.wallets.common import BaseWallet

from agent.configs import Config

logger = logging.getLogger(__name__)


def get_ima_mainnet(config: Config, wallet: BaseWallet | None = None) -> SkaleIma:
    return SkaleIma(config.mainnet_endpoint, config.ima_contracts, wallet)


def get_ima_schain(config: Config, wallet: BaseWallet | None = None) -> SchainIma:
    return SchainIma(config.schain_endpoint, config.ima_contracts_schain, wallet)


def get_skale_manager(config: Config, wallet: BaseWallet | None = None) -> SkaleManager:
    return SkaleManager(config.mainnet_endpoint, config.manager_contracts, wallet)
