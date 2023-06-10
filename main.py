import glob
import json
import shutil
import sys
from typing import Dict, List
from dotenv import load_dotenv
import os
import logging
import base64
import jsonschema
import pymysql
import requests

__author__ = "Tirthya Kamal Dasgupta"


load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_converted_img_data(new_imgs_list: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Converts a list of image files to base64-encoded strings and returns them as a dictionary.

    Args:
        new_imgs_list (List[str]): A list of image file paths.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are image file paths, and values are nested dictionaries containing the corresponding base64-encoded strings under the key 'converted'.

    Raises:
        FileNotFoundError: If an image file is not found.
        IsADirectoryError: If the provided path is a directory instead of a file.
        base64.binascii.Error: If there is an error encoding the image data as base64.
        UnicodeDecodeError: If there is an error decoding the base64-encoded data to UTF-8.

    Example usage:
        new_imgs_list = ["path/to/image1.jpg", "path/to/image2.png"]
        
        converted_imgs = get_converted_img_data(new_imgs_list)
        
        print(converted_imgs)

    Note:
        - The function assumes that the image files are readable and the necessary file permissions are available.
        - If an error occurs during encoding or decoding, the corresponding image's 'converted' value will be set to None.
        - Logging is used to capture any encountered errors.

    """
    new_imgs_list_len = len(new_imgs_list)

    new_imgs_dict = {}

    for index in range(new_imgs_list_len):
        logging.info(f"converting: '{new_imgs_list[index]}'")

        with open(new_imgs_list[index], "rb") as img_file:
            new_imgs_dict[new_imgs_list[index]] = {}

            try:
                new_imgs_dict[new_imgs_list[index]]["converted"] = base64.b64encode(img_file.read())
            except base64.binascii.Error:
                logging.error(base64.binascii.Error(f"'{new_imgs_list[index]}'"))
                
                new_imgs_dict[new_imgs_list[index]]["converted"] = None

            try:
                new_imgs_dict[new_imgs_list[index]]["converted"] = new_imgs_dict[new_imgs_list[index]]["converted"].decode("utf-8")
            except UnicodeDecodeError:
                logging.error(UnicodeDecodeError(f"'{new_imgs_list[index]}'"))

                new_imgs_dict[new_imgs_list[index]]["converted"] = None

        logging.info(f"converted: '{new_imgs_list[index]}'")

    return new_imgs_dict


def get_new_pan_card_images(pan_card_new_img_dir: str) -> List:
    """
    Retrieves a list of new PAN card image files from the specified directory.

    Parameters:
        pan_card_new_img_dir (str): The directory path where the PAN card images are located.

    Returns:
        List[str]: A list of file paths representing the new PAN card image files.

    Raises:
        None

    Example usage:
        pan_card_new_img_dir = "/path/to/new_pan_card_images/"
        
        new_pan_card_images = get_new_pan_card_images(pan_card_new_img_dir)
        
        print(new_pan_card_images)

    Note:
        - The function assumes that the specified directory exists and contains the new PAN card image files.
        - The function searches for image files with the extension '.webp' in the specified directory.
        - If the specified directory is empty or no new PAN card image files are found, None is returned.
        - Logging is used to capture any encountered errors or to log information about the number of found images.
    """
    if not len(os.listdir(pan_card_new_img_dir)) > 0:
        logging.error(f"dir: '{pan_card_new_img_dir}' is empty")

        return None

    img_extns = [".webp"]
    
    img_files = []

    for ext in img_extns:
        img_files.extend(glob.glob(os.path.join(pan_card_new_img_dir, '*' + ext)))

    if not img_files:
        logging.error(f"no new pan card image(s) found inside dir: '{pan_card_new_img_dir}'")

        return None

    logging.info(f"{len(img_files)} new pan card image(s) found inside dir: '{pan_card_new_img_dir}'")

    return img_files


def get_env_vars(*args: str) -> Dict[str, str]:
    """
    Retrieves environment variables and returns them as a dictionary.

    Args:
        *args: Variable number of environment variable names.

    Returns:
        Dict[str, str]: A dictionary where keys are the environment variable names and values are their corresponding values.

    Raises:
        EnvironmentError: If an environment variable is not found or is empty.

    Example usage:
        env_vars = get_env_vars("VAR1", "VAR2", "VAR3")
        print(env_vars)

    Note:
        The function assumes that the necessary environment variables are defined and accessible.

    """
    env_vars = {}

    for arg in args:
        env_vars[arg] = os.getenv(arg)

        if not env_vars[arg]:
            logging.error(f"failed to load env vars")

            raise EnvironmentError(f"'{arg}'")

    return env_vars


def main():
    """
    The main entry point of the program.
    
    This function performs the following tasks:
    1. Obtains necessary environment variables.
    2. Establishes a database connection.
    3. Loads a schema representing extracted data.
    4. Retrieves a list of new PAN card images from a directory.
    5. Processes the new PAN card images and converts them.
    6. Extracts information from the converted images using an OCR API.
    7. Validates the extracted data against a schema.
    8. Inserts the metadata into a database.
    9. Archives the processed images by moving them to a different directory.

    Note: The function assumes the presence of certain environment variables and file paths.

    Raises:
        NotADirectoryError: If the specified directory for new/archived PAN card images doesn't exist.

    Returns:
        None
    """
    logging.info("obtaining env vars")

    env_vars = get_env_vars(
        "PAN_CARD_NEW_IMGS_DIR",
        "PAN_CARD_ARCHIVED_IMGS_DIR",
        "X_RAPIDAPI_KEY",
        "X_RAPIDAPI_HOST",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_URI",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_TASK_ID",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_GROUP_ID",
        "DB_HOST",
        "DB_USERNAME",
        "DB_PASSWORD",
        "DB_NAME"
    )

    logging.info("obtained env vars")

    DB_HOST = env_vars["DB_HOST"]
    DB_USERNAME = env_vars["DB_USERNAME"]
    DB_PASSWORD = env_vars["DB_PASSWORD"]
    DB_NAME = env_vars["DB_NAME"]

    logging.info("establishing database connection")

    connection = pymysql.connect(
        host= DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
        ssl={
            "ssl": {
                "ca": "/etc/ssl/cert.pem"
            }
        }
    )

    logging.info("database connection established")

    with open("schemas/extracted-data-schema.json", "r") as extracted_data_schema_file:
        extracted_data_schema = json.loads(extracted_data_schema_file.read())

    logging.info("schema representing extracted data loaded")

    PAN_CARD_NEW_IMGS_DIR = env_vars["PAN_CARD_NEW_IMGS_DIR"]
    PAN_CARD_ARCHIVED_IMGS_DIR = env_vars["PAN_CARD_ARCHIVED_IMGS_DIR"]

    logging.info(f"finding dir: '{PAN_CARD_NEW_IMGS_DIR}'")

    if not os.path.exists(PAN_CARD_NEW_IMGS_DIR):
        raise NotADirectoryError(f"'{PAN_CARD_NEW_IMGS_DIR}'")
    
    if not os.path.exists(PAN_CARD_ARCHIVED_IMGS_DIR):
        raise NotADirectoryError(f"'{PAN_CARD_ARCHIVED_IMGS_DIR}'")
    
    logging.info(f"found dir: '{PAN_CARD_NEW_IMGS_DIR}'")

    X_RAPIDAPI_KEY = env_vars["X_RAPIDAPI_KEY"]
    X_RAPIDAPI_HOST = env_vars["X_RAPIDAPI_HOST"]

    PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_URI = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_URI"]
    PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_TASK_ID = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_TASK_ID"]
    PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_GROUP_ID = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_GROUP_ID"]

    new_pan_card_imgs_list = get_new_pan_card_images(PAN_CARD_NEW_IMGS_DIR)

    if not new_pan_card_imgs_list:
        sys.exit()

    new_pan_card_imgs_dict = get_converted_img_data(new_pan_card_imgs_list)

    del new_pan_card_imgs_list

    for new_pan_card_img in new_pan_card_imgs_dict.keys():
        if not new_pan_card_imgs_dict[new_pan_card_img]["converted"]:
            continue

        logging.info(f"extracting info for: '{new_pan_card_img}'")

        try:
            api_resp = requests.post(
                url=PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_URI,
                headers={
                    "content-type": "application/json",
                    "X-RapidAPI-Key": X_RAPIDAPI_KEY,
                    "X-RapidAPI-Host": X_RAPIDAPI_HOST
                },
                json={
                    "task_id": PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_TASK_ID,
                    "group_id": PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_GROUP_ID,
                    "data": {
                        "document1": new_pan_card_imgs_dict[new_pan_card_img]["converted"]
                    }
                },
                timeout=10
            )
        except requests.exceptions.HTTPError as http_err:
            logging.error(http_err)

            logging.error(f"failed to extract info for: '{new_pan_card_img}'")

            continue
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(conn_err)

            logging.error(f"failed to extract info for: '{new_pan_card_img}'")

            continue
        except requests.exceptions.Timeout as timeout_err:
            logging.error(timeout_err)

            logging.error(f"failed to extract info for: '{new_pan_card_img}'")

            continue
        except requests.exceptions.RequestException as err:
            logging.error(err)

            logging.error(f"failed to extract info for: '{new_pan_card_img}'")

            continue

        if not api_resp.status_code == 200:
            try:
                logging.error(api_resp.json())
            except requests.exceptions.JSONDecodeError:
                logging.error(api_resp.text)

            continue
        
        try:
            api_resp_json = api_resp.json()
        except requests.exceptions.JSONDecodeError:
            logging.error(api_resp.text)

            continue

        api_resp_json = {'action': 'extract', 'completed_at': '2023-06-08T15:30:58+05:30', 'created_at': '2023-06-08T15:30:57+05:30', 'group_id': '8e16424a-58fc-4ba4-ab20-5bc8e7c3c41e', 'request_id': '9b8e4660-535b-4463-8361-0b451d31cb10', 'result': {'extraction_output': {'age': 36, 'date_of_birth': '1986-07-16', 'date_of_issue': '', 'fathers_name': 'DURAISAMY', 'id_number': 'BNZPM2501F', 'is_scanned': False, 'minor': False, 'name_on_card': 'D MANIKANDAN', 'pan_type': 'Individual'}}, 'status': 'completed', 'task_id': '74f4c926-250c-43ca-9c53-453e87ceacd1', 'type': 'ind_pan'}

        logging.info(api_resp_json)

        logging.info(f"extracted info for: '{new_pan_card_img}'")

        logging.info(f"validating extracted data against schema for: '{new_pan_card_img}'")

        try:
            jsonschema.validate(
                instance=api_resp_json, schema=extracted_data_schema
            )
        except jsonschema.ValidationError as validation_err:
            logging.error(validation_err)

            logging.error(f"failed to validate extracted data against schema for: '{new_pan_card_img}'")

            continue
        
        logging.info(f"validated extracted data against schema for: '{new_pan_card_img}'")

        api_resp_json["result"]["extraction_output"]["is_scanned"] = 1 if api_resp_json["result"]["extraction_output"]["is_scanned"] else 0
        
        api_resp_json["result"]["extraction_output"]["minor"] = 1 if api_resp_json["result"]["extraction_output"]["minor"] else 0
        
        api_resp_json["result"]["extraction_output"]["date_of_issue"] = api_resp_json["result"]["extraction_output"]["date_of_issue"] if api_resp_json["result"]["extraction_output"]["date_of_issue"] else "0000-00-00"
        
        api_resp_json["result"]["extraction_output"]["verified"] = 0

        logging.info(f"inserting metadata into database for: '{new_pan_card_img}'")

        with connection.cursor() as cursor:
            try:
                statement = "SET SQL_MODE='ALLOW_INVALID_DATES'"

                cursor.execute(statement)

                statement = f"INSERT INTO pan_card_details (`age`, `date_of_birth`, `date_of_issue`, `fathers_name`, `id_number`, `is_scanned`, `minor`, `name_on_card`, `pan_type`, `verified`) VALUES ({api_resp_json['result']['extraction_output']['age']}, STR_TO_DATE('{api_resp_json['result']['extraction_output']['date_of_birth']}', '%Y-%m-%d'), STR_TO_DATE('{api_resp_json['result']['extraction_output']['date_of_issue']}', '%Y-%m-%d'), '{api_resp_json['result']['extraction_output']['fathers_name']}', '{api_resp_json['result']['extraction_output']['id_number']}', {api_resp_json['result']['extraction_output']['is_scanned']}, {api_resp_json['result']['extraction_output']['minor']}, '{api_resp_json['result']['extraction_output']['name_on_card']}', '{api_resp_json['result']['extraction_output']['pan_type']}', 0)"
                
                cursor.execute(statement)
            except pymysql.Error as err:
                logging.error(err)

                logging.error(f"failed to insert metadata into database for: '{new_pan_card_img}'")

                continue
        
        logging.info(f"inserted metadata into database for: '{new_pan_card_img}'")

        new_pan_card_img_file_name = os.path.basename(new_pan_card_img)
        
        archived_pan_card_img = os.path.join(PAN_CARD_ARCHIVED_IMGS_DIR, new_pan_card_img_file_name)

        logging.info(f"moving: '{new_pan_card_img_file_name}' from '{PAN_CARD_NEW_IMGS_DIR}' to '{PAN_CARD_ARCHIVED_IMGS_DIR}'")

        try:
            shutil.move(new_pan_card_img, archived_pan_card_img)
        except FileNotFoundError as fnf_err:
            logging.error(fnf_err)

            logging.error(f"failed to move: '{new_pan_card_img_file_name}' from '{PAN_CARD_NEW_IMGS_DIR}' to '{PAN_CARD_ARCHIVED_IMGS_DIR}'")

            continue

        logging.info(f"moved: '{new_pan_card_img_file_name}' from '{PAN_CARD_NEW_IMGS_DIR}' to '{PAN_CARD_ARCHIVED_IMGS_DIR}'")


if __name__ == "__main__":
    main()
