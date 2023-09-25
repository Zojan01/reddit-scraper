
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

def scrap_sub_redit():
    logging.info('scrapping sub_reddit')
    
    with open('scrapper_script.js', 'r') as scrapper_script:
        js_code = scrapper_script.read()
        scrapper_details_data = driver.execute_script(js_code)

    return {
        **scrapper_details_data,
        "last_date_updated": datetime.datetime.now().isoformat(),
    }   

def get_scraping_details():
    logging.info("getting scrappign details")
    load_all_media()
    scraping_ditails =  scrap_sub_redit()

    driver.quit()
    return scraping_ditails

