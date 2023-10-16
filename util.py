import os
import logging

def create_dir(dir):
    logging.info(f'scrap_sub_redit dir={dir}')
    if not os.path.exists(dir):
        logging.info(f'scrap_sub_redit dir={dir} doesn"t exits ')
        os.makedirs(dir)
