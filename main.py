
import os
import time
import json
import datetime
import requests
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By

STORAGE_PATH =  "/home/zangetsu/Videos/from-scraping"
SUBREDDIT_URL = "https://www.reddit.com/r/IllariMains/"

options = webdriver.ChromeOptions()
# options.add_argument("--headless")

driver = webdriver.Chrome(options)

driver.get(f"{SUBREDDIT_URL}")

time.sleep(3)

def load_all_media():
    # Define una función de JavaScript para hacer scroll hacia abajo
    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
    amount_of_scrolling_down = 0

    # Inicia un bucle para hacer scroll hasta el final
    while True:
        # Obtiene la posición actual del scroll antes de desplazar
        posicion_anterior = driver.execute_script("return window.scrollY;")
        
        # Ejecuta el script de scroll
        driver.execute_script(scroll_script)
        
        # Espera un momento para que la página se cargue (puedes ajustar el tiempo según sea necesario)
        driver.implicitly_wait(3)
        time.sleep(3)

        # Obtiene la nueva posición del scroll después de desplazar
        nueva_posicion = driver.execute_script("return window.scrollY;")
        
        amount_of_scrolling_down += 1
        print(f"scrolling down for {amount_of_scrolling_down} time")   
        # Si la posición no ha cambiado, significa que llegamos al final
        if nueva_posicion == posicion_anterior:
            break


def scrap_sub_redit():
    amount_of_posts = 0
    video_posts = []

    title_subredit_element = driver.find_element(By.XPATH, "//div[starts-with(@class, 'font-bold')]")
    post_container_elements = driver.find_elements(By.XPATH, '//shreddit-post') # find all posts

    for post in post_container_elements:
        time_element = post.find_element(By.TAG_NAME, "time")
        title_element = post.find_element(By.CSS_SELECTOR, "[slot='title']")

        try:
            video_element = post.find_element(By.TAG_NAME,"shreddit-player")
            video_element.is_displayed()  # Intenta determinar si el elemento de video está presente
        except:
            continue  
        
        title = title_element.text
        time_ago = time_element.text
        video_url = video_element.get_attribute("src")

        amount_of_posts = amount_of_posts + 1


        post = {
            "title": title,
            "time_ago": time_ago,
            "url": video_url
        }

        video_posts.append(post)

    return {
        "title_sub_redit": title_subredit_element.text,
        "amount_of_posts" : amount_of_posts + 1,
        "amount_of_videos_post": len(video_posts),
        "last_date_updated": datetime.datetime.now().isoformat(),
        "video_posts": video_posts
    }   

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def dowload_videos(dir_name, video_posts):
    for  counter, video in enumerate(video_posts):
        title = video.get("title").replace('.', '').replace('/','')
        time_ago = video.get("time_ago").replace('.','')
        url = video.get("url")

        file_name = f"{title}-{time_ago}"

        video_page = requests.get(url)
        print(f"dowloading video #{counter} - {title}")
        with open(f'{dir_name}/{file_name}.mp4', 'wb') as f:
            f.write(video_page.content)

def save_scraping_details(dir,scraping_details):
    with open(f"{dir}/details.json", "w") as archivo:
        json.dump(scraping_details, archivo, indent=4)

def init():
    load_all_media()

    scraping_details = scrap_sub_redit()
    title = scraping_details.get('title_sub_redit')

    dir_storage = f"{STORAGE_PATH}/{title[2:]}" #title[2:]  redits name come like r/SubRedit...  estamos eliminado los dos primeros caracteres  

    create_dir(dir_storage)
    
    dowload_videos(dir_storage, scraping_details.get("video_posts"))

    save_scraping_details(dir_storage, scraping_details)


init()
driver.quit()