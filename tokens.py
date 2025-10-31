import logging

from skale.contracts.erc20_contract import Erc20Contract
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet

from agent.configs import get_config
from agent.logger import init_logger
from agent.web3_tools import get_ima_mainnet, get_ima_schain
from tools.dev_configs import get_dev_config
from tools.hardhat_tokens import TokenType, deploy_erc20_m2s_token_pair

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    init_logger()
    config = get_config()
    dev_config = get_dev_config()

    web3_mainnet = init_web3(config.mainnet_endpoint)
    wallet_mainnet = Web3Wallet(dev_config.eth_private_key, web3_mainnet)

    web3_schain = init_web3(config.schain_endpoint)
    wallet_schain = Web3Wallet(dev_config.eth_private_key, web3_schain)

    ima_schain = get_ima_schain(config, wallet_schain)
    ima_mainnet = get_ima_mainnet(config, wallet_mainnet)

    if not dev_config.erc20_mainnet_address or not dev_config.erc20_schain_address:
        mainnet_address, schain_address = deploy_erc20_m2s_token_pair(
            config, dev_config, ima_mainnet, ima_schain, TokenType.ERC20
        )
    else:
        mainnet_address = dev_config.erc20_mainnet_address
        schain_address = dev_config.erc20_schain_address

    token_mainnet = Erc20Contract(web3_mainnet, mainnet_address, wallet_mainnet)
    token_schain = Erc20Contract(web3_schain, schain_address, wallet_schain)

    balance_mainnet = token_mainnet.balance_of(wallet_mainnet.address)
    balance_schain = token_schain.balance_of(wallet_schain.address)

    logger.info(f'ERC20 Mainnet Token Balance: {balance_mainnet}')
    logger.info(f'ERC20 Schain Token Balance: {balance_schain}')
