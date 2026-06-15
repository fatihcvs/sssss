import time
import logging
import schedule
import os

from llm_brain import generate_post_idea
from image_generator import generate_image
from instagram_publisher import publish_post
import config

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MAIN")

def execute_post_workflow():
    logger.info("=== Starting New Post Workflow ===")
    
    # 1. Generate Idea & Prompt
    logger.info("Generating post idea from LLM...")
    idea = generate_post_idea()
    if not idea:
        logger.error("Failed to generate idea. Aborting workflow.")
        return

    # 2. Generate Image
    prompt = idea.get("image_prompt", "")
    caption = idea.get("caption", "")
    hashtags = " ".join(idea.get("hashtags", []))
    
    full_caption = f"{caption}\n\n{hashtags}"
    
    logger.info("Generating image...")
    image_path = generate_image(prompt)
    if not image_path or not os.path.exists(image_path):
        logger.error("Failed to generate image. Aborting workflow.")
        return

    # 3. Publish to Instagram
    logger.info("Publishing to Instagram...")
    success = publish_post(image_path, full_caption)
    
    if success:
        logger.info("=== Workflow Completed Successfully ===")
    else:
        logger.error("=== Workflow Failed during Publication ===")

def setup_schedule():
    # Example schedule: Post twice a day at specific times
    schedule.every().day.at("10:00").do(execute_post_workflow)
    schedule.every().day.at("18:00").do(execute_post_workflow)
    logger.info("Schedule configured: 10:00 and 18:00 daily.")

if __name__ == "__main__":
    logger.info(f"Starting AI Influencer Bot for {config.CHARACTER_NAME}...")
    
    # Optional: Run once immediately on startup for testing
    # execute_post_workflow()
    
    setup_schedule()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)
