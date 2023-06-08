from dotenv import load_dotenv
import os
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_dir_from_env(
    dir_env_var_key: str,
) -> str:
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


def main():
    PAN_CARD_NEW_IMAGES_DIR = get_dir_from_env("PAN_CARD_NEW_IMAGES_DIR")
    PAN_CARD_ARCHIVED_IMAGES_DIR = get_dir_from_env("PAN_CARD_ARCHIVED_IMAGES_DIR")


if __name__ == "__main__":
    main()
