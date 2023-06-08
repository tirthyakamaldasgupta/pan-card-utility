import glob
import sys
from typing import List
from dotenv import load_dotenv
import os
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_dir_from_env(dir_env_var_key: str,) -> str:
    """
    Retrieves a directory path from an environment variable.

    Parameters:
        dir_env_var_key (str): The key of the environment variable.

    Returns:
        str: The directory path obtained from the environment variable.

    Raises:
        EnvironmentError: If the environment variable is not set.
        NotADirectoryError: If the directory path does not exist.

    """
    dir_env_var_value = os.getenv(dir_env_var_key)

    if not dir_env_var_value:
        raise EnvironmentError(f"'{dir_env_var_key}'")
    
    if not os.path.exists(dir_env_var_value):
        raise NotADirectoryError(f"'{dir_env_var_value}'")
    
    logging.info(f"found dir: '{dir_env_var_value}'")
    
    return dir_env_var_value


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


def main():
    PAN_CARD_NEW_IMG_DIR = get_dir_from_env("PAN_CARD_NEW_IMG_DIR")
    PAN_CARD_ARCHIVED_IMG_DIR = get_dir_from_env("PAN_CARD_ARCHIVED_IMG_DIR")

    new_pan_card_images = get_new_pan_card_images(PAN_CARD_NEW_IMG_DIR)

    if not new_pan_card_images:
        sys.exit()


if __name__ == "__main__":
    main()
