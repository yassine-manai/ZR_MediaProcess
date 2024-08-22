import configparser
import os


config_file_path = 'config/config.ini'
config = configparser.ConfigParser()
config.read(config_file_path)


# LOG CONFIGURATION
LEVEL= config.get('DEBUG', 'LEVEL', fallback='DEBUG')
LOG_ON_FILE= config.getboolean('DEBUG', 'LOG_ON_FILE', fallback=False)
FILENAME= config.get('DEBUG', 'FILENAME', fallback='PIC.log')
FILE_SIZE= config.getint('DEBUG', 'FILE_SIZE', fallback=50)


# APP CONFIGURATION
ZR_IP = config.get('APP', 'ZR_IP', fallback='127.0.0.1')
ZR_PORT =  config.getint('APP', 'ZR_PORT', fallback=8000)
TEMPLATE_ID = config.getint('APP', 'TIMOUT', fallback=5)
TIMOUT =  config.getint('APP', 'TIMOUT', fallback=5)

# SHIFT CONFIGURATION
COMPUTER_ID = config.get('SHIFT', 'COMPUTER_ID', fallback=7077)
DEVICE_ID = config.getint('SHIFT', 'DEVICE_ID', fallback=799)
CASHIER_CONTRACT_ID = config.getint('SHIFT', 'CASHIER_CONTRACT_ID', fallback=1)
CASHIER_CONSUMER_ID = config.getint('SHIFT', 'CASHIER_CONSUMER_ID', fallback=13)


