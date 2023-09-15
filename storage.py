import os
import json
import logging
from shutil import copyfile


def  load_last_scraping_details(dir):
    logging.info(f"loading scraping details from dir={dir}")
    
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

def save_scraping_details(dir,scraping_details):
    logging.info(f'saving_scraping_details in dir_name={dir}')
    with open(f"{dir}/details.json", "w") as archivo:
        json.dump(scraping_details, archivo, indent=4)


