import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
if not STABILITY_API_KEY:
    raise ValueError("STABILITY_API_KEY environment variable not set. Please set it before running the backend.")

app = FastAPI()

# Allow CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize the input prompt to prevent injection attacks and ensure valid content.
    
    Args:
        prompt (str): The input prompt to sanitize
        
    Returns:
        str: Sanitized prompt
        
    Raises:
        HTTPException: If prompt is invalid
    """
    if not prompt or not isinstance(prompt, str):
        raise HTTPException(status_code=400, detail="Prompt must be a non-empty string")
    
    # Remove any potentially harmful characters
    sanitized = re.sub(r'[<>{}[\]\\]', '', prompt)
    
    # Limit prompt length
    if len(sanitized) > 500:
        raise HTTPException(status_code=400, detail="Prompt must be less than 500 characters")
    
    return sanitized.strip()

def generate_image_with_stability(prompt: str, style: str, width: int = 1024, height: int = 1024) -> str:
    """
    Generate an image using Stability AI API.
    
    Args:
        prompt (str): The text prompt for image generation
        style (str): The art style to apply
        width (int): Image width
        height (int): Image height
        
    Returns:
        str: Base64 encoded image data
        
    Raises:
        HTTPException: If API call fails
    """
    engine_id = "stable-diffusion-xl-1024-v1-0"
    url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text_prompts": [{"text": f"{prompt}, {style} comic style"}],
        "cfg_scale": 7,
        "height": height,
        "width": width,
        "samples": 1,
        "steps": 30
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["artifacts"][0]["base64"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Stability AI API: {str(e)}")

@app.options("/generate-comic")
async def options_generate_comic():
    """Handle OPTIONS request for CORS preflight."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "86400",  # Cache preflight response for 24 hours
    }
    return JSONResponse(content={}, headers=headers)

@app.post("/generate-comic")
async def generate_comic(request: Request):
    """
    Generate comic panels based on the provided prompt and style.
    
    Args:
        request (Request): FastAPI request object containing prompt and style information
        
    Returns:
        dict: Dictionary containing generated image data
        
    Raises:
        HTTPException: If request processing fails
    """
    try:
        data = await request.json()
        prompt = sanitize_prompt(data.get("prompt", ""))
        style = data.get("style", "Japanese")
        grid_type = int(data.get("grid_type", 0))
        num_panels = int(data.get("num_panels", 4))
        panel_sizes = data.get("panel_sizes", [])
        
        # Validate grid type
        if grid_type not in [0, 1, 2]:
            raise HTTPException(status_code=400, detail="Invalid grid type")
            
        # Validate number of panels
        if num_panels < 1 or num_panels > 4:
            raise HTTPException(status_code=400, detail="Number of panels must be between 1 and 4")
        
        images = []
        for i in range(num_panels):
            # Use width/height from panel_sizes if provided, else default to 1024
            if i < len(panel_sizes):
                width = int(panel_sizes[i].get("width", 1024))
                height = int(panel_sizes[i].get("height", 1024))
            else:
                width = 1024
                height = 1024

            # Define allowed dimensions
            allowed_dimensions = [
                (1024, 1024), (1152, 896), (1216, 832), (1344, 768),
                (1536, 640), (640, 1536), (768, 1344), (832, 1216),
                (896, 1152)
            ]

            # Check if dimensions are allowed, if not use default
            if (width, height) not in allowed_dimensions:
                width = 1024
                height = 1024

            img_b64 = generate_image_with_stability(prompt, style, width, height)
            images.append(f"data:image/png;base64,{img_b64}")
            
        return {"images": images}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 