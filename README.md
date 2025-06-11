# TextToToon

## Description

A web application that leverages AI (Stability AI) to transform text prompts into structured comic panel sequences. Users can specify prompts, art styles, and panel layouts.

## Features

- Text-to-image generation using Stability AI
- Multiple art styles selection (Japanese, American, Egyptian)
- Selectable grid layouts for comic panels
- Real-time preview of panel layouts
- Responsive design for various screen sizes

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **AI:** Stability AI API

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- A Stability AI API key (get one from https://stability.ai/)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a file named `.env` in the project root directory with your Stability AI API key:
   ```
   STABILITY_API_KEY=your_actual_key
   ```

5. **Run the backend server:**
   ```bash
   python -m uvicorn comic_backend:app --reload
   ```
   The server will start at `http://localhost:8000`

### Frontend Setup

1. **Open the frontend:**
   - Simply open `index.html` in your web browser
   - Or use a local server (recommended):
     ```bash
     # Using Python's built-in server
     python -m http.server 8080
     ```
     Then visit `http://localhost:8080`

## API Documentation

### Generate Comic Endpoint

**Endpoint:** `POST /generate-comic`

**Request Body:**
```json
{
    "prompt": "string",      // Text description for the comic
    "style": "string",      // Art style (Japanese, American, Egyptian)
    "grid_type": "number",    // Grid layout type (0-2)
    "num_panels": "number"    // Number of panels to generate (default: 4)
}
```

**Response:**
```json
{
    "images": [
        "base64_image_data_1",
        "base64_image_data_2",
        "base64_image_data_3",
        "base64_image_data_4"
    ]
}
```

**Error Response:**
```json
{
    "error": "Error message"
}
```

## Project Structure

```
TextToToon/
├── comic_backend.py      # FastAPI backend
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── index.html           # Homepage
├── craft.html           # Comic creation page
├── style.css            # Styles
├── js/
│   └── craft.js         # Frontend JavaScript
└── Images/              # Static images
```

## Team Members 

- Thangamma.K.C
- Veeraj.G
- Thrisha.M.K
- Yahashwi Mahaveer

## Challenges & Future Work

- **Narrative Coherence Tools:** Implementing features to maintain character consistency across panels
- **Advanced User Options:** 
  - Voice prompt input
  - Control over AI model parameters (CFG scale, steps, seed)
- **User Accounts and Project Management:** Save generated comics and manage projects
- **Expanded Content Library:** More diverse grid layouts and panel templates
- **Community Features:** Share creations and explore others' comics

---

