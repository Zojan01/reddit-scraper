import json
import time
import logging
import requests
import datetime

STORAGE_PATH =  "/home/zangetsu/Videos/from-scraping/reddit"

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def download_specific_videos(dir_name,videos):
    logging.info(f'dowload_videos dir_name={videos}')
    for  counter, video in enumerate(videos):
        title = video.get("title").replace('.', '').replace('/','')
        publish_date = video.get("publish_date")
        url = video.get("url")

        file_name = ""

        if not title or not publish_date:
             file_name = f"{datetime.datetime.now().isoformat()}-{counter}-video"
        else:
             file_name = f"{title}-publish_date"

        try:
            video_page = requests.get(url, proxies=proxies)
            print(f"dowloading video #{counter} - {file_name}")
            with open(f'{dir_name}/{file_name}.mp4', 'wb') as f:
                f.write(video_page.content)
        except:
            continue

        time.sleep(20)


def dowload_videos(dir_name, video_posts, last_details_json):
    logging.info(f'dowload_videos dir_name={dir_name}')

    video_post_saved =  last_details_json.get('video_posts', [])

    for  counter, video in enumerate(video_posts):
        if video.get('url') in video_post_saved:
            continue

        title = video.get("title").replace('.', '').replace('/','')
        publish_date = video.get("publish_date")
        url = video.get("url")
        votes = video.get("votes")

        file_name = f"{title}-{publish_date}"

        try:
            video_page = requests.get(url, proxies=proxies)
            print(f"dowloading video #{counter} - {title} - {votes}")
            with open(f'{dir_name}/{file_name}.mp4', 'wb') as f:
                f.write(video_page.content)
        except:
            continue

        time.sleep(20)


# def init():
#     dir_storage = f"{STORAGE_PATH}/{'Lifeweaver Mains'}"
#     file_path = f"{dir_storage}/details.json"

#     scraping_details = None

#     with open(file_path, 'r') as file:
#             scraping_details = json.load(file)
#             print("scraping details found")

#     videos = scraping_details.get("video_posts")

#     dowload_videos(dir_storage, videos)

# init()