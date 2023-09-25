import time
import datetime
import logging
import util as util
import storage as storage
import downloader as downloader
from scraper import get_scraping_details

STORAGE_PATH =  "/home/zangetsu/Videos/from-scraping/reddit"

if __name__ == '__main__':
    init_datetime = datetime.datetime.now().isoformat()
    starting_time = time.time()

    logging.info(f'initiating script at {init_datetime}')
    
    scraping_details = get_scraping_details()
    dir_storage = f"{STORAGE_PATH}/{scraping_details.get('subreddit_title')}" #title[2:]  redits name come like r/SubRedit...  estamos eliminado los dos primeros caracteres  

    util.create_dir(dir_storage)
    
    last_scraping_details  = storage.load_last_scraping_details(dir_storage)
    storage.save_scraping_details(dir_storage, scraping_details)
    storage.save_scraping_details_to_csv(dir_storage, scraping_details)
    
    downloader.dowload_videos(dir_storage, scraping_details.get("video_posts"), last_scraping_details)
    
    ending_time = time.time()

    logging.info(f'it did take {(starting_time - ending_time) / 60} minutes to run script')
    logging.info(f'started at {init_datetime} and ending script at {datetime.datetime.now().isoformat()}')
