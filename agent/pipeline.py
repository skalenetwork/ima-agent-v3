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

from skale import MainnetIma, SchainIma, SkaleManager

from agent.network_browser import collect_connected_chains

logger = logging.getLogger(__name__)


def run_s2s_pipeline(skale: SkaleManager, ima_sc: SchainIma) -> None:
    schains = collect_connected_chains(skale)
    logger.debug(schains)


def run_m2s_pipeline(ima_mn: MainnetIma, ima_sc: SchainIma) -> None:
    pass
