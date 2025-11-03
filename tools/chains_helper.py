import logging

from eth_typing import ChecksumAddress
from skale import MainnetIma, SchainIma, SkaleManager
from skale.types.schain import SchainName
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet

from agent.configs import get_config
from agent.logger import init_logger
from agent.web3_tools import get_ima_mn, get_ima_sc, get_skale_manager
from tools.dev_configs import get_dev_config

logger = logging.getLogger(__name__)


def grant_linker_role(ima_mn: MainnetIma, address: ChecksumAddress) -> None:
    linker_role = ima_mn.linker.linker_role()
    if not ima_mn.linker.has_role(linker_role, address):
        logger.info(f'Granting linker role to address {address}')
        ima_mn.linker.grant_role(linker_role, address)
    else:
        logger.info(f'Address {address} already has linker role')


def grant_dev_roles(ima_mn: MainnetIma, address: ChecksumAddress) -> None:
    grant_linker_role(ima_mn, address)


def schain_ima_addresses(ima_sc: SchainIma) -> list[ChecksumAddress]:
    return [
        ima_sc.token_manager_linker.address,
        ima_sc.community_locker.address,
        ima_sc.eth.address,
        ima_sc.erc20.address,
        ima_sc.erc721.address,
        ima_sc.erc721_wmt.address,
        ima_sc.erc1155.address,
    ]


def connect_chain_to_mainnet(
    ima_mn: MainnetIma, ima_sc: SchainIma, schain_name: SchainName
) -> None:
    if not ima_mn.message_proxy_for_mainnet.is_connected_chain(schain_name):
        logger.info(f'Connecting schain {schain_name} to mainnet')
        ima_mn.linker.connect_schain(schain_name, schain_ima_addresses(ima_sc))
    else:
        logger.info(f'sChain {schain_name} is already connected to mainnet')


def setup_chains() -> None:
    config = get_config()
    dev_config = get_dev_config()
    web3 = init_web3(config.mainnet_endpoint)
    wallet = Web3Wallet(dev_config.eth_private_key, web3)
    ima_mn = get_ima_mn(config, wallet)
    ima_sc = get_ima_sc(config, wallet)
    skale = get_skale_manager(config, wallet)

    schain_info(skale, config.schain_name)
    grant_dev_roles(ima_mn, ima_mn.wallet.address)
    connect_chain_to_mainnet(ima_mn, ima_sc, config.schain_name)
    ima_mn.erc20.disable_whitelist(config.schain_name)


def schain_info(skale: SkaleManager, schain_name: SchainName) -> None:
    schain = skale.schains.get_by_name(schain_name)
    logger.info(f'Schain info for {schain_name}: {schain}')


if __name__ == '__main__':
    init_logger()
    setup_chains()
