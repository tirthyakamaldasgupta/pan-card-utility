import glob
import sys
from typing import Dict, List
from dotenv import load_dotenv
import os
import logging
import base64
import httpx


load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_converted_img_data(new_imgs_list: List) -> Dict:
    """
    Converts a list of image files to base64-encoded strings.

    Args:
        new_imgs_list (List[str]): A list of image file paths.

    Returns:
        Dict[str, str]: A dictionary where keys are image file paths and values are the corresponding base64-encoded strings.

    Raises:
        None

    """
    new_imgs_list_len = len(new_imgs_list)

    new_imgs_dict = {}

    for index in range(new_imgs_list_len):
        with open(new_imgs_list[index], "rb") as img_file:
            new_imgs_dict[new_imgs_list[index]] = base64.b64encode(img_file.read())
            new_imgs_dict[new_imgs_list[index]] = new_imgs_dict[new_imgs_list[index]].decode("utf-8")

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


def get_env_vars(*args) -> Dict[str, str]:
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
            raise EnvironmentError(f"'{arg}'")

    return env_vars


def main():
    env_vars = get_env_vars(
        "PAN_CARD_NEW_IMGS_DIR",
        "PAN_CARD_ARCHIVED_IMGS_DIR",
        "X_RAPIDAPI_KEY",
        "X_RAPIDAPI_HOST",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_URI",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_TASK_ID",
        "PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_GROUP_ID"
    )

    PAN_CARD_NEW_IMGS_DIR = env_vars["PAN_CARD_NEW_IMGS_DIR"]
    PAN_CARD_ARCHIVED_IMGS_DIR = env_vars["PAN_CARD_ARCHIVED_IMGS_DIR"]

    if not os.path.exists(PAN_CARD_NEW_IMGS_DIR):
        raise NotADirectoryError(f"'{PAN_CARD_NEW_IMGS_DIR}'")
    
    logging.info(f"found dir: '{PAN_CARD_NEW_IMGS_DIR}'")

    X_RAPIDAPI_KEY = env_vars["X_RAPIDAPI_KEY"]
    X_RAPIDAPI_HOST = env_vars["X_RAPIDAPI_HOST"]

    PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_URI = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_URI"]
    PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_TASK_ID = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_TASK_ID"]
    PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_GROUP_ID = env_vars["PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_GROUP_ID"]

    new_pan_card_imgs_list = get_new_pan_card_images(PAN_CARD_NEW_IMGS_DIR)

    if not new_pan_card_imgs_list:
        sys.exit()

    new_pan_card_imgs_dict = get_converted_img_data(new_pan_card_imgs_list)

    del new_pan_card_imgs_list

    # resp = httpx.post(
    #     url=PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_URI,
    #     headers={
    #         "content-type": "application/json",
    #         "X-RapidAPI-Key": X_RAPIDAPI_KEY,
    #         "X-RapidAPI-Host": X_RAPIDAPI_HOST
    #     },
    #     data={
    #         "task_id": PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_TASK_ID,
    #         "group_id": PAN_CARD_OCR_EXTRACTION_SCHEDULER_ENDPOINT_GROUP_ID,
    #         "data": {
    #             "document1": "https://5.imimg.com/data5/TP/US/MU/SELLER-51778781/pan-card-500x500.jpg"
    #         }
    #     }
    # )


if __name__ == "__main__":
    main()
