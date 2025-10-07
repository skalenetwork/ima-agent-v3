import logging

from skale import SkaleIma
from skale.schain_ima import SchainIma

from agent.configs import config
from agent.logger import init_logger

logger = logging.getLogger(__name__)


def init_ima_mainnet() -> SkaleIma:
    return SkaleIma(config.mainnet_endpoint, config.ima_contracts)


def init_ima_schain() -> SchainIma:
    return SchainIma(config.schain_endpoint, config.ima_contracts_schain)


def run_agent_loop() -> None:
    init_logger()
    logger.info('Starting agent loop')
    ima_mainnet = init_ima_mainnet()
    ima_schain = init_ima_schain()
    logger.info(ima_mainnet.community_pool.address)
    logger.info(ima_schain.community_locker.address)


if __name__ == '__main__':
    run_agent_loop()
