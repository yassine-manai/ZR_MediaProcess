import configparser
from dotenv import load_dotenv
import os

load_dotenv()

config_file_path = 'config/config.ini'
#add_default_section_header(config_file_path)

config = configparser.ConfigParser()
config.read(config_file_path)


LEVEL=str(os.getenv("DEBUG")) if os.getenv("DEBUG") else config.get('DEBUG', 'LEVEL', fallback='DEBUG')
LOG_ON_FILE= str(os.getenv("LOG_ON_FILE")) if os.getenv("LOG_ON_FILE") else config.get('DEBUG', 'LOG_ON_FILE', fallback='True')
FILENAME=str(os.getenv("FILENAME")) if os.getenv("FILENAME") else config.get('DEBUG', 'FILENAME', fallback='PIC.log')
FILE_SIZE=int(os.getenv("FILE_SIZE")) if os.getenv("FILE_SIZE") else config.getint('DEBUG', 'FILE_SIZE', fallback=50)

APP_IP = str(os.getenv("APP_IP")) if os.getenv("APP_IP") else config.get('APP', 'APP_IP', fallback='127.0.0.1')
APP_PORT = int(os.getenv("APP_PORT")) if os.getenv("APP_PORT") else config.getint('APP', 'APP_PORT', fallback=8100)

ZR_IP = str(os.getenv("ZR_IP")) if os.getenv("ZR_IP") else config.get('APP', 'ZR_IP', fallback='127.0.0.1')
ZR_PORT = int(os.getenv("ZR_PORT")) if os.getenv("ZR_PORT") else config.getint('APP', 'ZR_PORT', fallback=8443)

TIMOUT = int(os.getenv("TIMOUT")) if os.getenv("TIMOUT") else config.getint('APP', 'TIMOUT', fallback=5)
