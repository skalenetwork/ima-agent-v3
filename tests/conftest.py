import pytest
from eth_typing import ChecksumAddress, HexStr
from skale import MainnetIma, SchainIma
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet
from web3 import Web3

from agent.configs import Config, get_config
from agent.web3_tools import get_ima_mn, get_ima_sc
from tools.dev_configs import DevConfig, get_dev_config
from tools.hardhat_tokens import TokenType, deploy_erc20_m2s_token_pair


@pytest.fixture(scope='session')
def config() -> Config:
    return get_config()


@pytest.fixture(scope='session')
def dev_config() -> DevConfig:
    return get_dev_config()


@pytest.fixture(scope='session')
def eth_private_key(dev_config: DevConfig) -> HexStr:
    return dev_config.eth_private_key


@pytest.fixture(scope='session')
def mainnet_web3(config: Config) -> Web3:
    w3: Web3 = init_web3(config.mainnet_endpoint)
    return w3


@pytest.fixture(scope='session')
def wallet(mainnet_web3: Web3, eth_private_key: HexStr) -> Web3Wallet:
    return Web3Wallet(eth_private_key, mainnet_web3)


@pytest.fixture(scope='session')
def ima_mn(config: Config, wallet: Web3Wallet) -> MainnetIma:
    return get_ima_mn(config, wallet)


@pytest.fixture(scope='session')
def ima_sc(config: Config, wallet: Web3Wallet) -> SchainIma:
    return get_ima_sc(config, wallet)


@pytest.fixture
def erc20_token_addresses(
    config: Config, dev_config: DevConfig, ima_mn: MainnetIma, ima_sc: SchainIma
) -> tuple[ChecksumAddress, ChecksumAddress]:
    mainnet_address = dev_config.erc20_mainnet_address
    schain_address = dev_config.erc20_schain_address
    if not mainnet_address or not schain_address:
        mainnet_address, schain_address = deploy_erc20_m2s_token_pair(
            config, dev_config, ima_mn, ima_sc, TokenType.ERC20
        )
    return mainnet_address, schain_address
