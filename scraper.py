
import time
import datetime
import logging
import chromedriver_binary
from shutil import copyfile
from selenium import webdriver
from selenium.webdriver.common.by import By

LIST_OF_SUBREDDITS =[
    "https://www.reddit.com/r/WinstonMains/",
    "https://www.reddit.com/r/WidowmakerMains/",
    "https://www.reddit.com/r/ReinhardtMains/",
    "https://www.reddit.com/r/RoadhogMains/",
    "https://www.reddit.com/r/SigmaMains/",
    "https://www.reddit.com/r/Soldier76Mains/",
    "https://www.reddit.com/r/WreckingBallMains/",
    "https://www.reddit.com/r/SymmetraMains/",
    "https://www.reddit.com/r/ReaperMain/",
    "https://www.reddit.com/r/ramattramains/",
    "https://www.reddit.com/r/PharahMains/",
    "https://www.reddit.com/r/orisamains/",
    "https://www.reddit.com/r/MoiraMains/",
    "https://www.reddit.com/r/MeiMains/",
    "https://www.reddit.com/r/TorbjornMains/",
    "https://www.reddit.com/r/TracerMains/",
    "https://www.reddit.com/r/luciomains/",
    "https://www.reddit.com/r/kirikomains/",
    "https://www.reddit.com/r/JunkRatMains/",
    "https://www.reddit.com/r/HanzoMain/",
    "https://www.reddit.com/r/GenjiMains/",
    "https://www.reddit.com/r/DvaMains/",
    "https://www.reddit.com/r/doomfistmains/",
    "https://www.reddit.com/r/BastionMains/",
    "https://www.reddit.com/r/BaptisteMainsOW/",
    "https://www.reddit.com/r/AsheOWMains/",

    "https://www.reddit.com/r/McCreeMains/",
    "https://www.reddit.com/r/ZaryaMains/",
    "https://www.reddit.com/r/BadLifeweaverPulls/",
    "https://www.reddit.com/r/LifeweaverMains/",
    "https://www.reddit.com/r/IllariMains/"
]

SUBREDDIT_URL = LIST_OF_SUBREDDITS[0]

logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
options.add_argument('--disable-gpu')  # Esto puede ser necesario en algunos sistemas

driver = webdriver.Chrome(options=options)
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
        time.sleep(10)
        driver.implicitly_wait(3)

        # Obtiene la nueva posición del scroll después de desplazar
        nueva_posicion = driver.execute_script("return window.scrollY;")
        
        amount_of_scrolling_down += 1
        print(f"scrolling down for {amount_of_scrolling_down} time")   
        # Si la posición no ha cambiado, significa que llegamos al final
        if nueva_posicion == posicion_anterior:
            break



def process_post_element(post):
    # Inserta tu código aquí
    try:
        title = post.find_element(By.TAG_NAME, "h3").get_attribute("innerHTML")
        publish_date = post.find_element(By.CSS_SELECTOR, "[data-click-id='timestamp']").get_attribute("innerHTML")
        video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
        amount_of_votes = post.find_element(By.CSS_SELECTOR, '[id*="vote"]').get_attribute("innerHTML")
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")
        return None

    return (title, video_url, publish_date, amount_of_votes)


def scrap_sub_redit():
    logging.info('scrapping sub_reddit')
    amount_of_posts = 0
    video_posts = []
    title_subredit_element = None
    post_container_elements = None
    
    # try:
    #     title_subredit_element = driver.find_element(By.XPATH, "//div[starts-with(@class, 'font-bold')]")
    #     post_container_elements = driver.find_elements(By.XPATH, '//shreddit-post') # find all posts
    # except Exception as error:
    #     logging.error(f"Error when getting element err: {error}")


    # if title_subredit_element == None or post_container_elements == None:
    try:
        title_subredit_element = driver.find_element(By.XPATH, "//h1")
        post_container_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="post-container"]') # find all posts
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")
    
    
    logging.info(f'scrap_sub_redit - amout of post #{len(post_container_elements)}')

    with ProcessPoolExecutor(max_workers=4) as executor:
    # Lanzar el bucle en paralelo
        results = executor.map(process_post_element, post_container_elements)


    for counter, post in  enumerate(post_container_elements):
        print(f"being in the cicle for {counter} time")
        
        title = ""
        video_url = ""
        publish_date = ""
        amount_of_votes = ""
        
        # try:
        #     title = post.find_element(By.CSS_SELECTOR, "[slot='title']").text   #Worked before
        #     publish_date = post.find_element(By.TAG_NAME, "time").get_attribute("title") #Worked before
        #     video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
        #     amount_of_votes = post.find_element(By.CSS_SELECTOR, '[id*="vote"]').find_element(By.XPATH, '..').text
        # except Exception as error:
        #     logging.error(f"Error when getting element err: {error}")
        
        try:
            title = post.find_element(By.TAG_NAME, "h3").get_attribute("innerHTML")
            publish_date = post.find_element(By.CSS_SELECTOR, "[data-click-id='timestamp']").get_attribute("innerHTML")
            video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
            amount_of_votes = post.find_element(By.CSS_SELECTOR, '[id*="vote"]').get_attribute("innerHTML")
        except Exception as error:
            logging.error(f"Error when getting element err: {error}")
            continue

        amount_of_posts =+ 1
        video_posts.append({
            "title": title,
            "publish_date": publish_date,
            "votes": amount_of_votes,
            "url": video_url
        })

    return {
        "title_sub_redit": title_subredit_element.text,
        "amount_of_posts" : amount_of_posts + 1,
        "amount_of_videos_post": len(video_posts),
        "last_date_updated": datetime.datetime.now().isoformat(),
        "video_posts": video_posts
    }   

def get_scraping_details():
    logging.info("getting scrappign details")
    load_all_media()
    scraping_ditails =  scrap_sub_redit()
    driver.quit()
    return scraping_ditails

