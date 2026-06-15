import os
import logging
from instagrapi import Client
import config

logger = logging.getLogger(__name__)

def get_instagram_client():
    cl = Client()
    
    # Login or load existing session to avoid getting banned
    if os.path.exists(config.SESSION_FILE):
        try:
            cl.load_settings(config.SESSION_FILE)
            cl.login(config.IG_USERNAME, config.IG_PASSWORD)
            logger.info("Logged in using existing session.")
        except Exception as e:
            logger.warning(f"Failed to login with session, trying normal login: {e}")
            cl.login(config.IG_USERNAME, config.IG_PASSWORD)
            cl.dump_settings(config.SESSION_FILE)
    else:
        try:
            cl.login(config.IG_USERNAME, config.IG_PASSWORD)
            cl.dump_settings(config.SESSION_FILE)
            logger.info("Logged in and saved new session.")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return None
    
    return cl

def publish_post(image_path, caption):
    """Uploads a photo to Instagram."""
    if not config.IG_USERNAME or not config.IG_PASSWORD:
        logger.warning("Instagram credentials not set. Mocking publication.")
        logger.info(f"MOCK PUBLISH:\nImage: {image_path}\nCaption: {caption}")
        return True

    cl = get_instagram_client()
    if not cl:
        return False
        
    try:
        logger.info("Uploading photo to Instagram...")
        media = cl.photo_upload(image_path, caption)
        logger.info(f"Successfully posted! Media ID: {media.id}")
        return True
    except Exception as e:
        logger.error(f"Failed to post: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # publish_post("generated_post.jpg", "Test caption #AI")
