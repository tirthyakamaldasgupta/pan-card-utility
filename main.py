from dotenv import load_dotenv
import os
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO)


def main():
    PAN_CARD_IMAGES_DIR = os.getenv("PAN_CARD_IMAGES_DIR")

    if not PAN_CARD_IMAGES_DIR:
        raise EnvironmentError("'PAN_CARD_IMAGES_DIR'")

    if not os.path.exists(PAN_CARD_IMAGES_DIR):
        raise NotADirectoryError(PAN_CARD_IMAGES_DIR)
    
    logging.info(f"found pan card images dir: '{PAN_CARD_IMAGES_DIR}'")
    
    ARCHIVED_IMAGES_DIR = os.path.join(PAN_CARD_IMAGES_DIR, "archived-images")
    
    if not os.path.exists(ARCHIVED_IMAGES_DIR):
        logging.info(f"'archived-images' dir doesn't exist within '{PAN_CARD_IMAGES_DIR}'")
        logging.info(f"creating 'archived-images' dir within '{PAN_CARD_IMAGES_DIR}'")

        os.mkdir(ARCHIVED_IMAGES_DIR)

        logging.info(f"created 'archived-images' dir within '{PAN_CARD_IMAGES_DIR}'")


if __name__ == "__main__":
    main()
