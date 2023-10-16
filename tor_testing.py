from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
options.add_argument('--disable-gpu')  # Esto puede ser necesario en algunos sistemas

# Inicialización del navegador
driver = webdriver.Chrome(options=options)

# Navegar a una página de prueba para verificar la conexión Tor
driver.get("http://check.torproject.org")


response = driver.get("http://check.torproject.org")
