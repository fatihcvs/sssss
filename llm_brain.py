import json
import logging
from openai import OpenAI
import config

logger = logging.getLogger(__name__)

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_post_idea():
    """Generates a concept, image prompt, and instagram caption."""
    system_prompt = f"""
    You are the creative director for an AI Influencer named {config.CHARACTER_NAME}.
    Her style/appearance is: {config.CHARACTER_STYLE}.
    
    Your task is to generate a daily post idea. Return ONLY a valid JSON object with the following keys:
    - "concept": A brief description of the situation (e.g. "drinking coffee at a cafe")
    - "image_prompt": A highly detailed prompt for Stable Diffusion (SDXL). It must include her physical description, the setting, lighting, and camera details (e.g. "cinematic lighting, 85mm lens, candid shot"). Do NOT use the word "iPhone".
    - "caption": The Instagram caption for the post, written in a natural, engaging tone, including emojis.
    - "hashtags": A list of 5-10 relevant hashtags.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate a new, unique post idea for today."}
            ],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        idea = json.loads(content)
        logger.info(f"Generated idea: {idea['concept']}")
        return idea
    except Exception as e:
        logger.error(f"Error generating post idea: {e}")
        return None

if __name__ == "__main__":
    # Test the LLM Brain
    logging.basicConfig(level=logging.INFO)
    print(generate_post_idea())
