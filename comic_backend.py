import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64

STABILITY_API_KEY = "sk-RRa9Ur6bhqMsQDdmSgwpI9ZWf3I7OGygL2cKJaubymFxtciB"  # <-- Paste your key here
app = FastAPI()

# Allow CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_image_with_stability(prompt, style):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text_prompts": [{"text": f"{prompt}, {style} comic style"}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }
    response = requests.post(url, headers=headers, json=data)
    print("API status code:", response.status_code)
    print("API response:", response.text)
    response.raise_for_status()
    result = response.json()
    return result["artifacts"][0]["base64"]

@app.post("/generate-comic")
async def generate_comic(request: Request):
    print("Received request at /generate-comic")
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        style = data.get("style", "")
        grid_type = data.get("grid_type", 0)
        num_panels = int(data.get("num_panels", 4))
        images = []
        for i in range(num_panels):
            img_b64 = generate_image_with_stability(prompt, style)
            images.append(f"data:image/png;base64,{img_b64}")
        print("Generated images successfully")
        return {"images": images}
    except Exception as e:
        print("Error in /generate-comic:", e)
        return {"images": []} 