import logging

from eth_typing import ChecksumAddress
from skale import SchainIma, SkaleIma, SkaleManager
from skale.types.schain import SchainName
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet

from agent.configs import get_config
from agent.logger import init_logger
from agent.web3_tools import get_ima_mainnet, get_ima_schain, get_skale_manager
from tools.dev_configs import get_dev_config

logger = logging.getLogger(__name__)


def grant_linker_role(ima_mainnet: SkaleIma, address: ChecksumAddress) -> None:
    linker_role = ima_mainnet.linker.linker_role()
    if not ima_mainnet.linker.has_role(linker_role, address):
        logger.info(f'Granting linker role to address {address}')
        ima_mainnet.linker.grant_role(linker_role, address)
    else:
        logger.info(f'Address {address} already has linker role')


def grant_dev_roles(ima_mainnet: SkaleIma, address: ChecksumAddress) -> None:
    grant_linker_role(ima_mainnet, address)


def schain_ima_addresses(ima_schain: SchainIma) -> list[ChecksumAddress]:
    return [
        ima_schain.token_manager_linker.address,
        ima_schain.community_locker.address,
        ima_schain.token_manager_eth.address,
        ima_schain.token_manager_erc20.address,
        ima_schain.token_manager_erc721.address,
        ima_schain.token_manager_erc721_wmt.address,
        ima_schain.token_manager_erc1155.address,
    ]


def connect_chain_to_mainnet(
    ima_mainnet: SkaleIma, ima_schain: SchainIma, schain_name: SchainName
) -> None:
    if not ima_mainnet.message_proxy_for_mainnet.is_connected_chain(schain_name):
        logger.info(f'Connecting schain {schain_name} to mainnet')
        ima_mainnet.linker.connect_schain(schain_name, schain_ima_addresses(ima_schain))
    else:
        logger.info(f'sChain {schain_name} is already connected to mainnet')


def setup_chains() -> None:
    config = get_config()
    dev_config = get_dev_config()
    web3 = init_web3(config.mainnet_endpoint)
    wallet = Web3Wallet(dev_config.eth_private_key, web3)
    ima_mainnet = get_ima_mainnet(config, wallet)
    ima_schain = get_ima_schain(config, wallet)
    skale = get_skale_manager(config, wallet)

    schain_info(skale, config.schain_name)
    grant_dev_roles(ima_mainnet, ima_mainnet.wallet.address)
    connect_chain_to_mainnet(ima_mainnet, ima_schain, config.schain_name)


def schain_info(skale: SkaleManager, schain_name: SchainName) -> None:
    schain = skale.schains.get_by_name(schain_name)
    logger.info(f'Schain info for {schain_name}: {schain}')


if __name__ == '__main__':
    init_logger()
    setup_chains()
