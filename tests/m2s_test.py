from eth_typing import ChecksumAddress
from skale import MainnetIma, SchainIma
from skale.contracts.erc20_contract import Erc20Contract

from agent.configs import Config

TRANSFER_AMOUNT = 0.01


def test_eth_transfer(ima_mn: MainnetIma, ima_sc: SchainIma, config: Config) -> None:
    transfer_amount_wei = ima_mn.web3.to_wei(TRANSFER_AMOUNT, 'ether')
    mainnet_balance_1 = ima_mn.web3.eth.get_balance(ima_mn.wallet.address)
    schain_balance_1 = ima_sc.eth_erc20.balance_of(ima_sc.wallet.address)
    expected_schain_balance = schain_balance_1 + transfer_amount_wei

    ima_mn.eth.deposit(config.schain_name, value=transfer_amount_wei)
    ima_sc.eth_erc20.wait_for_balance_change(
        ima_sc.wallet.address, schain_balance_1, poll_interval=1
    )

    mainnet_balance_2 = ima_mn.web3.eth.get_balance(ima_mn.wallet.address)
    schain_balance_2 = ima_sc.eth_erc20.balance_of(ima_sc.wallet.address)

    assert mainnet_balance_2 < mainnet_balance_1
    assert schain_balance_2 == expected_schain_balance


def test_erc20_transfer(
    ima_mn: MainnetIma,
    ima_sc: SchainIma,
    config: Config,
    erc20_token_addresses: tuple[ChecksumAddress, ChecksumAddress],
) -> None:
    mainnet_token_address, schain_token_address = erc20_token_addresses
    token_mainnet = Erc20Contract(ima_mn.web3, mainnet_token_address, ima_mn.wallet)
    token_schain = Erc20Contract(ima_sc.web3, schain_token_address, ima_sc.wallet)

    transfer_amount_wei = ima_mn.web3.to_wei(TRANSFER_AMOUNT, 'ether')
    mainnet_balance_1 = token_mainnet.balance_of(ima_mn.wallet.address)
    schain_balance_1 = token_schain.balance_of(ima_sc.wallet.address)
    expected_schain_balance_1 = schain_balance_1 + transfer_amount_wei
    expected_mainnet_balance_1 = mainnet_balance_1 - transfer_amount_wei

    token_mainnet.approve(ima_mn.erc20.address, transfer_amount_wei)
    ima_mn.erc20.deposit_erc20(config.schain_name, mainnet_token_address, transfer_amount_wei)

    token_schain.wait_for_balance_change(ima_sc.wallet.address, schain_balance_1, poll_interval=1)

    mainnet_balance_2 = token_mainnet.balance_of(ima_mn.wallet.address)
    schain_balance_2 = token_schain.balance_of(ima_sc.wallet.address)

    assert mainnet_balance_2 == expected_mainnet_balance_1
    assert schain_balance_2 == expected_schain_balance_1

    ima_sc.erc20.exit_to_main_erc20(schain_token_address, transfer_amount_wei)
    token_mainnet.wait_for_balance_change(ima_mn.wallet.address, mainnet_balance_2, poll_interval=1)

    mainnet_balance_3 = token_mainnet.balance_of(ima_mn.wallet.address)
    schain_balance_3 = token_schain.balance_of(ima_sc.wallet.address)

    assert mainnet_balance_3 == mainnet_balance_1
    assert schain_balance_3 == schain_balance_1
