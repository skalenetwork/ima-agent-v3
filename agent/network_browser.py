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

from skale import SkaleManager
from skale.types.schain import Schain, SchainHash

logger = logging.getLogger(__name__)


def collect_connected_chains(skale: SkaleManager) -> list[Schain]:
    all_schains_ids = skale.schains_internal.get_all_schains_ids()
    return get_schains(skale, all_schains_ids)


def get_schains(skale: SkaleManager, schain_ids: list[SchainHash]) -> list[Schain]:
    return [skale.schains.get(schain_hash) for schain_hash in schain_ids]
