import json
import logging
import time
import requests
import os
import urllib.request
import uuid
import config

logger = logging.getLogger(__name__)

def queue_prompt(prompt_workflow):
    """Sends the workflow JSON to the ComfyUI API."""
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"{config.COMFYUI_API_URL}/prompt", data=data)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())

def get_image(filename, subfolder, folder_type):
    """Downloads the generated image from ComfyUI."""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"{config.COMFYUI_API_URL}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    """Gets the history to find the generated images."""
    with urllib.request.urlopen(f"{config.COMFYUI_API_URL}/history/{prompt_id}") as response:
        return json.loads(response.read())

def generate_image(prompt, output_filename="generated_post.jpg"):
    """
    Calls ComfyUI API with the provided prompt and the IP-Adapter FaceID workflow.
    """
    logger.info(f"Initiating image generation with prompt: {prompt}")
    
    if "127.0.0.1" in config.COMFYUI_API_URL and not os.path.exists("workflow_api.json"):
        logger.warning("Local test detected without workflow. Using MOCK.")
        # Create a dummy image
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1024, 1024), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((50,50), "Mock Generation", fill=(255,255,0))
        img.save(output_filename)
        return output_filename
        
    try:
        # Load the template workflow
        with open("workflow_api.json", "r", encoding="utf-8") as f:
            workflow = json.load(f)
            
        # Update prompt node (ID 6 in our JSON)
        workflow["6"]["inputs"]["text"] = prompt
        
        # Inject seed for randomness
        import random
        workflow["3"]["inputs"]["seed"] = random.randint(1, 10000000)
        
        # We assume FaceID reference image is already loaded in ComfyUI input folder
        # or we update node 10's image input if we handle upload.
        # workflow["10"]["inputs"]["image"] = config.FACE_ID_REFERENCE_IMAGE_URL 
        
        logger.info("Sending workflow to ComfyUI...")
        prompt_response = queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']
        
        logger.info(f"Queued prompt ID: {prompt_id}. Waiting for completion...")
        
        # Polling for completion
        history = {}
        while prompt_id not in history:
            time.sleep(2)
            history = get_history(prompt_id)
            
        history_data = history[prompt_id]
        
        # Download images
        for node_id in history_data['outputs']:
            node_output = history_data['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    with open(output_filename, "wb") as img_file:
                        img_file.write(image_data)
                    logger.info(f"Image successfully downloaded to {output_filename}")
                    return output_filename

        return None
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_image("A beautiful woman sitting in a cafe")
