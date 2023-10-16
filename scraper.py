
import time
import datetime
import logging
import urllib3
import chromedriver_binary
from concurrent import futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

urllib3.PoolManager(pool_connections=1500, pool_maxsize=1500)

logging.basicConfig(level=logging.INFO)

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--disable-notifications")
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
options.add_argument('--disable-gpu')  # Esto puede ser necesario en algunos sistemas

driver = webdriver.Chrome(options=options)

def go_to_subreddit(subreddit_url):
    driver.get(f"{subreddit_url}")
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

def scrap_subreddit(subreddit_url):
    logging.info("getting scrappign details")

    def __init__():
        go_to_subreddit(subreddit_url)
        load_all_media()
    
    def __exit__():
        driver.quit()
    
    return scrap_sub_redit()


