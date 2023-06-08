import glob
import sys
from typing import Dict, List
from dotenv import load_dotenv
import os
import logging
import base64


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

    new_pan_card_imgs_list = get_new_pan_card_images(PAN_CARD_NEW_IMG_DIR)

    if not new_pan_card_imgs_list:
        sys.exit()

    new_pan_card_imgs_dict = get_converted_img_data(new_pan_card_imgs_list)

    del new_pan_card_imgs_list


if __name__ == "__main__":
    main()
