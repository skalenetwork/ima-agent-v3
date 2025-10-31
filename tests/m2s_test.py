from eth_typing import ChecksumAddress
from skale import SchainIma, SkaleIma
from skale.contracts.erc20_contract import Erc20Contract

from agent.configs import Config

TRANSFER_AMOUNT = 0.01


def test_eth_transfer(ima_mainnet: SkaleIma, ima_schain: SchainIma, config: Config) -> None:
    transfer_amount_wei = ima_mainnet.web3.to_wei(TRANSFER_AMOUNT, 'ether')
    mainnet_balance_before = ima_mainnet.web3.eth.get_balance(ima_mainnet.wallet.address)
    schain_balance_before = ima_schain.eth_erc20.balance_of(ima_schain.wallet.address)
    expected_schain_balance = schain_balance_before + transfer_amount_wei

    ima_mainnet.deposit_box_eth.deposit(config.schain_name, value=transfer_amount_wei)
    ima_schain.eth_erc20.wait_for_balance_change(
        ima_schain.wallet.address, schain_balance_before, poll_interval=1
    )

    mainnet_balance_after = ima_mainnet.web3.eth.get_balance(ima_mainnet.wallet.address)
    schain_balance_after = ima_schain.eth_erc20.balance_of(ima_schain.wallet.address)

    assert mainnet_balance_after < mainnet_balance_before
    assert schain_balance_after == expected_schain_balance


def test_erc20_transfer(
    ima_mainnet: SkaleIma,
    ima_schain: SchainIma,
    config: Config,
    erc20_token_addresses: tuple[ChecksumAddress, ChecksumAddress],
) -> None:
    mainnet_token_address, schain_token_address = erc20_token_addresses
    token_mainnet = Erc20Contract(ima_mainnet.web3, mainnet_token_address, ima_mainnet.wallet)
    token_schain = Erc20Contract(ima_schain.web3, schain_token_address, ima_schain.wallet)

    transfer_amount_wei = ima_mainnet.web3.to_wei(TRANSFER_AMOUNT, 'ether')
    mainnet_balance_before = token_mainnet.balance_of(ima_mainnet.wallet.address)
    schain_balance_before = token_schain.balance_of(ima_schain.wallet.address)
    expected_schain_balance = schain_balance_before + transfer_amount_wei
    expected_mainnet_balance = mainnet_balance_before - transfer_amount_wei

    token_mainnet.approve(ima_mainnet.deposit_box_erc20.address, transfer_amount_wei)
    ima_mainnet.deposit_box_erc20.deposit_erc20(
        config.schain_name, mainnet_token_address, transfer_amount_wei
    )

    token_schain.wait_for_balance_change(
        ima_schain.wallet.address, schain_balance_before, poll_interval=1
    )

    mainnet_balance_after = token_mainnet.balance_of(ima_mainnet.wallet.address)
    schain_balance_after = token_schain.balance_of(ima_schain.wallet.address)

    assert mainnet_balance_after == expected_mainnet_balance
    assert schain_balance_after == expected_schain_balance
