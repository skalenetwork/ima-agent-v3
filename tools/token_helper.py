import logging

from eth_typing import ChecksumAddress
from skale import MainnetIma, SchainIma
from skale.types.schain import SchainName
from skale.utils.constants import ZERO_ADDRESS

from tools.dev_configs import MAINNET_CHAIN_NAME

logger = logging.getLogger(__name__)


def link_erc20_token(
    ima_mn: MainnetIma,
    ima_sc: SchainIma,
    schain_name: SchainName,
    mainnet_token_address: ChecksumAddress,
    schain_token_address: ChecksumAddress,
) -> None:
    if not ima_mn.erc20.is_token_added(schain_name, mainnet_token_address):
        logger.info(f'Linking ERC20 token {mainnet_token_address} to schain {schain_name}')
        ima_mn.erc20.add_erc20_token(schain_name, mainnet_token_address)
    else:
        logger.info(f'ERC20 token {mainnet_token_address} already linked to schain {schain_name}')

    clone_address = ima_sc.erc20.get_clone(MAINNET_CHAIN_NAME, mainnet_token_address)
    if clone_address == ZERO_ADDRESS:
        logger.info(f'Linking ERC20 token {mainnet_token_address} on schain {schain_name}')
        ima_sc.erc20.add_erc20_token(
            MAINNET_CHAIN_NAME, mainnet_token_address, schain_token_address
        )
    else:
        logger.info(f'ERC20 token {mainnet_token_address} already linked on schain {schain_name}')
