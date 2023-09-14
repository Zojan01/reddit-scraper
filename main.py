
import os
import time
import json
import datetime
import requests
import logging
import chromedriver_binary
from shutil import copyfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions


LIST_OF_SUBREDDITS =[
    "https://www.reddit.com/r/BadLifeweaverPulls/",
    "https://www.reddit.com/r/LifeweaverMains/",
    "https://www.reddit.com/r/IllariMains/",
    "https://www.reddit.com/r/GenjiMains/",
    "https://www.reddit.com/r/McCreeMains/"
]

SUBREDDIT_URL = LIST_OF_SUBREDDITS[1]
STORAGE_PATH =  "/home/zangetsu/Videos/from-scraping/reddit"

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}


logging.basicConfig(level=logging.INFO)

# ------------------SETTING FIREFOX DRIVER----------------------

# options = webdriver.ChromeOptions()
# # options.add_argument("--headless")
# driver = webdriver.Chrome(options)

# geckodriver_path = './driver/geckodriver'
# tor_binary_path_driver = '/home/zangetsu/.local/opt/tor-browser/app/Browser/firefox'

# options = FirefoxOptions()
# profile = webdriver.FirefoxProfile()

# # options.add_argument("--headless")
# profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.socks', '127.0.0.1')
# profile.set_preference('network.proxy.socks_port', 9050)
# profile.set_preference("network.proxy.socks_remote_dns", True)

# options.profile = profile

# service = Service(executable_path=geckodriver_path)
# os.popen(tor_binary_path_driver)
# driver = webdriver.Firefox(options=options, service=service)

options = webdriver.ChromeOptions()

options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
options.add_argument('--disable-gpu')  # Esto puede ser necesario en algunos sistemas

driver = webdriver.Chrome(options=options)

driver.get(f"{SUBREDDIT_URL}")
time.sleep(3)


# ------------------SETTING FIREFOX DRIVER----------------------

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
        time.sleep(10)
        driver.implicitly_wait(3)

        # Obtiene la nueva posición del scroll después de desplazar
        nueva_posicion = driver.execute_script("return window.scrollY;")
        
        amount_of_scrolling_down += 1
        print(f"scrolling down for {amount_of_scrolling_down} time")   
        # Si la posición no ha cambiado, significa que llegamos al final
        if nueva_posicion == posicion_anterior:
            break

def scrap_sub_redit():
    logging.info('scrap_sub_redit')
    amount_of_posts = 0
    video_posts = []
    title_subredit_element = None
    post_container_elements = None
    
    try:
        title_subredit_element = driver.find_element(By.XPATH, "//div[starts-with(@class, 'font-bold')]")
        post_container_elements = driver.find_elements(By.XPATH, '//shreddit-post') # find all posts

    except Exception as error:
        logging.error(f"Error when getting element err: {error}")


    if title_subredit_element == None or post_container_elements == None:
       try:
        title_subredit_element = driver.find_element(By.XPATH, "//h1")
        post_container_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="post-container"]') # find all posts
       except Exception as error:
        logging.error(f"Error when getting element err: {error}")
       
    
    logging.info(f'scrap_sub_redit - amout of post #{len(post_container_elements)}')

    for counter, post in  enumerate(post_container_elements):
        print(f"being in the cicle for {counter} time")
        
        title = ""
        video_url = ""
        publish_date = ""
        
        try:
            title = post.find_element(By.CSS_SELECTOR, "[slot='title']").text   #Worked before
            publish_date = post.find_element(By.TAG_NAME, "time").get_attribute("title") #Worked before
            video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
        except Exception as error:
            print(f"Error when getting element err: {error}")
        
        if not title or not video_url:
            try:
                title = post.find_element(By.TAG_NAME, "h3").text
                publish_date = post.find_element(By.CSS_SELECTOR, "[data-click-id='timestamp']").text
                video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
            except Exception as error:
                print(f"Error when getting element err: {error}")
        
        if not video_url:
            continue

        amount_of_posts =+ 1
        video_posts.append({
            "title": title,
            "publish_date": publish_date,
            "url": video_url
        })

    return {
        "title_sub_redit": title_subredit_element.text,
        "amount_of_posts" : amount_of_posts + 1,
        "amount_of_videos_post": len(video_posts),
        "last_date_updated": datetime.datetime.now().isoformat(),
        "video_posts": video_posts
    }   

def create_dir(dir):
    logging.info(f'scrap_sub_redit dir={dir}')
    if not os.path.exists(dir):
        logging.info(f'scrap_sub_redit dir={dir} doesn"t exits ')
        os.makedirs(dir)

def dowload_videos(dir_name, video_posts, last_details_json):
    logging.info(f'dowload_videos dir_name={dir_name}')

    video_post_saved =  last_details_json.get('video_posts', [])

    for  counter, video in enumerate(video_posts):
        if video.get('url') in video_post_saved:
            continue

        title = video.get("title").replace('.', '').replace('/','')
        publish_date = video.get("publish_date")
        url = video.get("url")

        file_name = f"{title}-{publish_date}"

        try:
            video_page = requests.get(url, proxies=proxies)
            print(f"dowloading video #{counter} - {title}")
            with open(f'{dir_name}/{file_name}.mp4', 'wb') as f:
                f.write(video_page.content)
        except:
            continue

        time.sleep(60)

def save_scraping_details(dir,scraping_details):
    logging.info(f'save_scraping_details dir_name={dir}')
    with open(f"{dir}/details.json", "w") as archivo:
        json.dump(scraping_details, archivo, indent=4)

def init():
    logging.info(f'initiating script')

    load_all_media()
    scraping_details = scrap_sub_redit()
    title = scraping_details.get('title_sub_redit')

    dir_storage = f"{STORAGE_PATH}/{title}" #title[2:]  redits name come like r/SubRedit...  estamos eliminado los dos primeros caracteres  

    create_dir(dir_storage)
    
    last_details_json = load_last_scraping_details(dir_storage)

    dowload_videos(dir_storage, scraping_details.get("video_posts"), last_details_json)

    save_scraping_details(dir_storage, scraping_details)

    time.sleep
    # driver.quit()

def  load_last_scraping_details(dir):
    logging.info("load_scraping_details")
    
    details_json = {}
    file_path = f"{dir}/details.json"
    print("file_path --->", file_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            details_json = json.load(file)
            
            # Crear un backup del archivo
            copyfile(file_path, f'{dir}/details_backup.json')
    else:
        # Si el archivo no existe, continuar
        logging.info("the scraping details file is not present, continuing...")

    return details_json;        

init()