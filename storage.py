import os
import csv
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


def save_scraping_details_to_csv(dir,scraping_details):
    logging.info(f'save_scraping_details_to_csv in dir_name={dir}')

    csv_path = f"{dir}/csv_details.csv"
    videos = scraping_details.get('video_posts', [])
    
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='') as csv_file:
            videos = scraping_details.get('video_posts', [])
            
            try:
                csv_writer = csv.writer(csv_file)
                
                headers = videos[0].keys()
                csv_writer.writerow(headers)

                for item in videos:
                    csv_writer.writerow(item.values())

            except Exception as err:
                logging.info(f"there was a error when creating, cvs error = {err}")
    else:
        with open(csv_path, mode='a', newline='') as csv_file:
            videos = scraping_details.get('video_posts', [])
            
            try:
                csv_writer = csv.writer(csv_file)
                
                for item in videos:
                    csv_writer.writerow(item.values())

            except Exception as err:
                logging.info(f"there was a error when appending, to cvs, error = {err}")


        