import logging
import re
import subprocess
from enum import Enum

from eth_typing import ChecksumAddress, HexStr
from skale import MainnetIma, SchainIma
from web3 import Web3

from agent.configs import Config
from tools.dev_configs import TEST_TOKENS_PATH, DevConfig
from tools.helper import run_cmd

logger = logging.getLogger(__name__)


class TokenType(Enum):
    ERC20 = 'erc20'
    ERC721 = 'erc721'
    ERC1155 = 'erc1155'


class NetworkType(Enum):
    MAINNET = 'mainnet'
    SCHAIN = 'schain'


TEST_TOKEN_NAME = 'TestToken'
TEST_TOKEN_SYMBOL = 'TTK'
TEST_MINT_AMOUNT = 1_000_000 * 10**18


def install_dependencies() -> None:
    run_cmd(['bun', 'i'], cwd=TEST_TOKENS_PATH)


def run_hardhat_cmd(
    cmd: list[str],
    endpoint: str,
    private_key: HexStr,
) -> subprocess.CompletedProcess:
    return run_cmd(
        ['npx', 'hardhat'] + cmd,
        env={
            'MAINNET_ENDPOINT': endpoint,
            'PRIVATE_KEY_FOR_ETHEREUM': private_key,
            'PRIVATE_KEY_FOR_SCHAIN': private_key,
            'URL_W3_S_CHAIN': endpoint,
            'URL_W3_ETHEREUM': endpoint,
        },
        cwd=TEST_TOKENS_PATH,
    )


def deploy_token(
    endpoint: str,
    private_key: HexStr,
    token_name: str,
    token_symbol: str,
    token_type: TokenType,
    network_type: NetworkType,
) -> ChecksumAddress:
    res = run_hardhat_cmd(
        [
            token_type.value,
            '--name',
            token_name,
            '--symbol',
            token_symbol,
            '--network',
            network_type.value,
        ],
        endpoint=endpoint,
        private_key=private_key,
    )
    address_search_res = re.search(r'0x[a-fA-F0-9]{40}', res.stdout.decode())
    if not address_search_res:
        raise ValueError('Token address not found in deployment output')
    address = HexStr(address_search_res.group())
    logger.info(f'Deployed {token_type.value} - {token_symbol} token at address: {address}')
    return Web3.to_checksum_address(address)


def add_minter(
    endpoint: str,
    eth_private_key: HexStr,
    token_type: TokenType,
    token_address: HexStr,
    ima_sc: SchainIma,
    network_type: NetworkType,
) -> subprocess.CompletedProcess:
    return run_hardhat_cmd(
        [
            f'add-minter-{token_type.value}',
            '--token-address',
            token_address,
            '--address',
            ima_sc.erc20.address,
            '--network',
            network_type.value,
        ],
        endpoint=endpoint,
        private_key=eth_private_key,
    )


def mint_tokens(
    endpoint: str,
    eth_private_key: HexStr,
    token_type: TokenType,
    token_address: HexStr,
    receiver_address: HexStr,
    amount: int,
    network_type: NetworkType,
) -> subprocess.CompletedProcess:
    return run_hardhat_cmd(
        [
            f'mint-{token_type.value}',
            '--token-address',
            token_address,
            '--receiver-address',
            receiver_address,
            '--amount',
            str(amount),
            '--network',
            network_type.value,
        ],
        endpoint=endpoint,
        private_key=eth_private_key,
    )


def deploy_erc20_m2s_token_pair(
    config: Config,
    dev_config: DevConfig,
    ima_mn: MainnetIma,
    ima_sc: SchainIma,
    token_type: TokenType,
) -> tuple[ChecksumAddress, ChecksumAddress]:
    address_mainnet = deploy_token(
        endpoint=config.mainnet_endpoint,
        private_key=dev_config.eth_private_key,
        token_name=TEST_TOKEN_NAME,
        token_symbol=TEST_TOKEN_SYMBOL,
        token_type=token_type,
        network_type=NetworkType.MAINNET,
    )
    address_schain = deploy_token(
        endpoint=config.schain_endpoint,
        private_key=dev_config.eth_private_key,
        token_name=TEST_TOKEN_NAME,
        token_symbol=TEST_TOKEN_SYMBOL,
        token_type=token_type,
        network_type=NetworkType.SCHAIN,
    )
    add_minter(
        endpoint=config.schain_endpoint,
        eth_private_key=dev_config.eth_private_key,
        token_type=token_type,
        token_address=address_schain,
        ima_sc=ima_sc,
        network_type=NetworkType.SCHAIN,
    )
    mint_tokens(
        endpoint=config.mainnet_endpoint,
        eth_private_key=dev_config.eth_private_key,
        token_type=token_type,
        token_address=address_mainnet,
        receiver_address=ima_mn.wallet.address,
        amount=TEST_MINT_AMOUNT,
        network_type=NetworkType.MAINNET,
    )
    ima_mn.erc20.add_erc20_token(config.schain_name, address_mainnet)
    return address_mainnet, address_schain
