from eth_typing import ChecksumAddress
from skale import MainnetIma, SchainIma
from skale.contracts.erc20_contract import Erc20Contract

from agent.configs import Config

TRANSFER_AMOUNT = 0.01


def test_eth_transfer(ima_mn: MainnetIma, ima_sc: SchainIma, config: Config) -> None:
    transfer_amount_wei = ima_mn.web3.to_wei(TRANSFER_AMOUNT, 'ether')
    mainnet_balance_before = ima_mn.web3.eth.get_balance(ima_mn.wallet.address)
    schain_balance_before = ima_sc.eth_erc20.balance_of(ima_sc.wallet.address)
    expected_schain_balance = schain_balance_before + transfer_amount_wei

    ima_mn.eth.deposit(config.schain_name, value=transfer_amount_wei)
    ima_sc.eth_erc20.wait_for_balance_change(
        ima_sc.wallet.address, schain_balance_before, poll_interval=1
    )

    mainnet_balance_after = ima_mn.web3.eth.get_balance(ima_mn.wallet.address)
    schain_balance_after = ima_sc.eth_erc20.balance_of(ima_sc.wallet.address)

    assert mainnet_balance_after < mainnet_balance_before
    assert schain_balance_after == expected_schain_balance


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
    mainnet_balance_before = token_mainnet.balance_of(ima_mn.wallet.address)
    schain_balance_before = token_schain.balance_of(ima_sc.wallet.address)
    expected_schain_balance = schain_balance_before + transfer_amount_wei
    expected_mainnet_balance = mainnet_balance_before - transfer_amount_wei

    token_mainnet.approve(ima_mn.erc20.address, transfer_amount_wei)
    ima_mn.erc20.deposit_erc20(config.schain_name, mainnet_token_address, transfer_amount_wei)

    token_schain.wait_for_balance_change(
        ima_sc.wallet.address, schain_balance_before, poll_interval=1
    )

    mainnet_balance_after = token_mainnet.balance_of(ima_mn.wallet.address)
    schain_balance_after = token_schain.balance_of(ima_sc.wallet.address)

    assert mainnet_balance_after == expected_mainnet_balance
    assert schain_balance_after == expected_schain_balance
