#!/usr/bin/python3
import pynetbox
import logging
import logging.config
import requests
import sys
import yaml
import emoji
from dotenv import dotenv_values
from pprint import pformat
from importRegions import create_nb_regions

with open('./logging.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('ImportAll')

nb_config = dotenv_values(".env")
api_server = nb_config.get('NETBOX_API_SERVER')
api_token = nb_config.get('NETBOX_API_TOKEN')
REGIONS_DIR = '../organization/regions/'
alert = "\U0001F6A8"
hour_glass = "\U000023F3"
globe = "\U0001F30D"
OK = "\U0001F197"
'''
Validate Netbox API Access
'''
logger.info(f"{hour_glass} Validate Netbox API Access")
try:
    nb = pynetbox.api(api_server, api_token)
    nb.status()
    logging.info(f"{OK} Netbox API Credentials Validated!")
except pynetbox.RequestError as e:
    logger.error(f"{alert} Critical Netbox Error: {e.error}")
    sys.exit(1)

'''Create Netbox Regions'''
logger.info(f"{hour_glass} Creating Netbox Regions...")
create_nb_regions(nb, REGIONS_DIR)
