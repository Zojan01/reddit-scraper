
import os
import logging
import storage as storage
import downloader as downloader
from scraper import get_scraping_details

STORAGE_PATH =  "/home/zangetsu/Videos/from-scraping/reddit"

def create_dir(dir):
    logging.info(f'scrap_sub_redit dir={dir}')
    if not os.path.exists(dir):
        logging.info(f'scrap_sub_redit dir={dir} doesn"t exits ')
        os.makedirs(dir)


def init():
    logging.info(f'initiating script')

    scraping_details = get_scraping_details()
    
    dir_storage = f"{STORAGE_PATH}/{scraping_details.get('title_sub_redit')}" #title[2:]  redits name come like r/SubRedit...  estamos eliminado los dos primeros caracteres  

    create_dir(dir_storage)

    last_scraping_details  = storage.load_last_scraping_details(dir_storage)

    storage.save_scraping_details(dir_storage, scraping_details)
    downloader.dowload_videos(dir_storage, scraping_details.get("video_posts"), last_scraping_details)

init()