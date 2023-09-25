
import time
import datetime
import logging
import urllib3
import chromedriver_binary
from concurrent import futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



# Esto sera un canal para poner people in roads 
# Idiots on the road
PEOPLE_ON_THE_ROAD =[
"https://www.reddit.com/r/IdiotsOnScooters",
# "https://www.reddit.com/r/BadBusDriver",
"https://www.reddit.com/r/BadCycling",
"https://www.reddit.com/r/IdiotsInCars",
"https://www.reddit.com/r/IdiotsOnMotorcycles",
"https://www.reddit.com/r/IdiotsOnBikes/",
"https://www.reddit.com/r/dashcamgifs/",
]

# WordAndItsPeople.
    # Loveds by the word
    # Looks like the word is not with you.
    # When the world hate you
    # Maybe learn from that... and dont dot it again.

# https://www.reddit.com/r/therewasanattempt/
# https://www.reddit.com/r/CrazyFuckingVideos/
# https://www.reddit.com/r/iamatotalpieceofshit/
# https://www.reddit.com/r/OopsThatsDeadly/
# https://www.reddit.com/r/SipsTea/
# https://www.reddit.com/r/ContagiousLaughter/
# https://www.reddit.com/r/ThatsInsane/
# https://www.reddit.com/r/funnyvideos/

WORLD_AND_ITS_PEOPLE =[
    "https://www.reddit.com/r/criticalblunder/",
    "https://www.reddit.com/r/MadeMeSmile/",
    "https://www.reddit.com/r/WhyWomenLiveLonger/",
    "https://www.reddit.com/r/yesyesyesyesno/",
    "https://www.reddit.com/r/nonononoyes/",
    "https://www.reddit.com/r/whatcouldgoright/",
    "https://www.reddit.com/r/Whatcouldgowrong/",
    "https://www.reddit.com/r/WinStupidPrizes/",
    "https://www.reddit.com/r/instantkarma/",
    "https://www.reddit.com/r/watchpeoplesurvive/",
    "https://www.reddit.com/r/CrazyFuckingVideos/",
    "https://www.reddit.com/r/maybemaybemaybe/",
    "https://www.reddit.com/r/nonononoyes/",
    "https://www.reddit.com/r/TerrifyingAsFuck/",
    "https://www.reddit.com/r/instantkarma/",
    "https://www.reddit.com/r/WatchPeopleDieInside/",
    
]

# phara y mei hay que hacerlo de nuevo
# list of subredit para overwatch.
# OVERWATCH_LIFE
# OVERWATCH_ON_POINT
OVERWATCH_VIEV =[
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
    "https://www.reddit.com/r/kirikomains/",# number 14
    "https://www.reddit.com/r/JunkRatMains/",
    "https://www.reddit.com/r/HanzoMain/",
    "https://www.reddit.com/r/GenjiMains/",
    "https://www.reddit.com/r/DvaMains/",
    "https://www.reddit.com/r/doomfistmains/",
    "https://www.reddit.com/r/BastionMains/",
    "https://www.reddit.com/r/BaptisteMainsOW",
    "https://www.reddit.com/r/AsheOWMains/",


    "https://www.reddit.com/r/WinstonMains/",
    "https://www.reddit.com/r/McCreeMains/",
    "https://www.reddit.com/r/ZaryaMains/",
    "https://www.reddit.com/r/BadLifeweaverPulls/",
    "https://www.reddit.com/r/LifeweaverMains/",
    "https://www.reddit.com/r/IllariMains/"
]

# SUBREDDIT_URL = OVERWATCH_VIEV[16]
SUBREDDIT_URL = PEOPLE_ON_THE_ROAD[2]
urllib3.PoolManager(pool_connections=1500, pool_maxsize=1500)

logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--disable-notifications")
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

def get_time_post(post):
    time_ago = ""
    publish_date = ""

    try:
        time_ago_element = post.find_element(By.CSS_SELECTOR, "[data-click-id='timestamp']")
        time_ago = time_ago_element.get_attribute("innerHTML")

        # actions = ActionChains(driver)
        # actions.move_to_element(time_ago_element)
        # time.sleep(2)
        # publish_date = driver.find_element(By.XPATH, '//*[@data-popper-escaped]').get_attribute("innerHTML")


        # trash_string_position =  publish_date.find("<div>")           
        # if trash_string_position != -1:  # Si se encontró "<div>"
        #     time_published = publish_date[:trash_string_position]  
        
    except Exception as error:
        pass
        # return publish_date, time_ago
    
    if time_ago == "":
        try: 
            time_element = post.find_element(By.TAG_NAME, "time") 
            publish_date = time_element.get_attribute("title")
            time_ago = time_element.text
        except Exception as error:
            pass

    return publish_date , time_ago

def process_post_element(post, counter):
    print(f"interation number #{counter} post = {post}")
    title = ""
    video_url = ""
    amount_of_votes = 0
    post_url = ""
    publish_date = ""
    time_ago = ""    

    # try:
    #     title = post.find_element(By.TAG_NAME, "h3").get_attribute("innerHTML")
    #     video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
    #     amount_of_votes = post.find_element(By.CSS_SELECTOR, '[id*="vote"]').find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
    #     post_url = post.find_element(By.TAG_NAME, "h3").find_element(By.XPATH, './ancestor::a').get_attribute("href")
    #     publish_date, time_ago = get_time_post(post) 

    # except Exception as error:
    #     pass
        # logging.error(f"Error when getting element err: {error}")

    # if post_url == "" or title == "":
    try:
        title = post.find_element(By.CSS_SELECTOR, "[slot='title']").text  
        video_url = post.find_element(By.TAG_NAME,"shreddit-player").get_attribute("src")
        post_url = f"https://www.reddit.com{post.get_attribute('permalink')}"
        publish_date, time_ago = get_time_post(post) 
        amount_of_votes = driver.execute_script('return arguments[0].shadowRoot.querySelector("faceplate-number")', post).text
        # amount_of_votes = post.find_element(By.CSS_SELECTOR, '[id*="vote"]').find_element(By.XPATH, '..').text
    except Exception as error:
        return 
        

    return {
        "title": title,
        "publish_date": publish_date,
        "time_ago": time_ago,
        "votes": amount_of_votes,
        "url": video_url,
        "post_url": post_url
        }

def get_subreddit_title():
    try:
        return driver.find_element(By.XPATH, "//div[starts-with(@class, 'font-bold')]").get_attribute("innerHTML").split("/")[-1]
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")

    try:
        return driver.find_element(By.XPATH, "//h1").get_attribute("innerHTML")
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")

    return SUBREDDIT_URL.split("/")[-1]

def get_all_posts():
    posts = []
    
    try:
        posts =  driver.find_elements(By.XPATH, '//shreddit-post') # find all posts
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")

    try:
        if len(posts) == 0:
            posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid="post-container"]') # find all posts
    except Exception as error:
        logging.error(f"Error when getting element err: {error}")
    
    return posts


def scrap_sub_redit():
    logging.info('scrapping sub_reddit')
    amount_of_posts = 0
    video_posts = []
    
    subreddit_title = get_subreddit_title()
    post_container_elements = get_all_posts()
    
    amount_of_posts = len(post_container_elements)
    logging.info(f'scrap_sub_redit - amout of post #{amount_of_posts}')
    
    with futures.ThreadPoolExecutor(max_workers=1000) as executor:
        # Lanzar el bucle en paralelo
        results = list(executor.map(process_post_element, post_container_elements, range(len(post_container_elements))))
        video_posts = [video for video in results if video is not None]
        executor.shutdown()

    return {
        "subreddit_title": subreddit_title,
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

