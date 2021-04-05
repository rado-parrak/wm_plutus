import json
import logging
from context.market import setup_market
from context.party import setup_portfolio

def configure_run(configmap:dict):

    # (1) High-level configuration
    with open(configmap['run_config']) as f: run_config = json.load(f)
        
    # (2) loggers
    logger = logging.getLogger('plutusLogger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s :: %(name)s | %(levelname)s | %(message)s')

    fileHandler = logging.FileHandler(run_config['logPath'])
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
        
    # (2) Market
    with open(configmap['market_config']) as f: market_config = json.load(f)
    market = setup_market(market_config, run_config, logger)

    # (3) Portfolio
    with open(configmap['portfolio_config']) as f: portfolio_config = json.load(f)
    portfolio = setup_portfolio(portfolio_config, market, logger)

    return run_config, market, portfolio, logger