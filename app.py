import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from openai import OpenAI
from logs.logger import log  # Assuming you've created this file as discussed earlier

# Load environment variables
load_dotenv()

# Create the Flask app
app = Flask(__name__, static_folder='static')

# Configure CORS
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Load API keys
perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize OpenAI client
client = OpenAI()

def get_prompt(level, topic, domain):
    # Implement your prompt generation logic here
    return f"Explain {topic} in {domain} at a {level} level."

def get_image_prompt(level, topic, domain):
    # Implement your image prompt generation logic here
    return f"Create an image representing {topic} in {domain} suitable for a {level} audience."

def generate_explanation(topic, domain, level):
    prompt = get_prompt(level, topic, domain)
    payload = {
        "model": "llama-3-sonar-small-32k-chat",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {perplexity_api_key}"},
            json=payload
        )
        response.raise_for_status()
        explanation = response.json().get("choices")[0].get("message").get("content")
        
        log("INFO", f"Generated explanation for {topic}", domain=domain, level=level, explanation=explanation)
        return explanation
    except requests.exceptions.RequestException as e:
        log("ERROR", f"RequestException in generate_explanation", error=str(e))
        return f"An error occurred: {e}"

def generate_image(topic, domain, level):
    image_prompt = get_image_prompt(level, topic, domain)

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        log("INFO", "Image generated successfully", topic=topic, domain=domain, level=level, image_url=image_url)
        return image_url
    except Exception as e:
        log("ERROR", "Error generating image", error=str(e))
        return None

@app.route('/')
def index():
    log("INFO", "Accessed home page")
    return render_template('index.html')

@app.route('/generate_explanation', methods=['POST'])
def generate_explanation_route():
    data = request.json
    topic = data.get('topic')
    domain = data.get('domain')
    level = data.get('level')
    log("INFO", "Generating explanation", topic=topic, domain=domain, level=level)
    explanation_markdown = generate_explanation(topic, domain, level)
    return jsonify({'explanation': explanation_markdown})

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    data = request.json
    topic = data.get('topic')
    domain = data.get('domain')
    level = data.get('level')
    log("INFO", "Generating image", topic=topic, domain=domain, level=level)
    image_url = generate_image(topic, domain, level)
    return jsonify({'image_url': image_url})

@app.route('/refresh', methods=['GET'])
def refresh():
    log("INFO", "Refreshing page")
    return render_template('index.html')

# Add Content Security Policy
@app.after_request
def add_security_headers(response):
    csp = "default-src 'self'; " \
          "script-src 'self' https://kit.fontawesome.com https://cdn.jsdelivr.net https://cdn.jsdelivr.net/npm/marked/marked.min.js; " \
          "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net https://ka-f.fontawesome.com 'unsafe-inline'; " \
          "font-src 'self' https://fonts.gstatic.com https://kit-free.fontawesome.com https://ka-f.fontawesome.com; " \
          "img-src 'self' data: https:; " \
          "connect-src 'self' https://api.perplexity.ai https://api.openai.com https://ka-f.fontawesome.com; " \
          "frame-src 'none';"
    
    response.headers['Content-Security-Policy'] = csp
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    log("INFO", "Application started", port=port)
    app.run(host='0.0.0.0', port=port, debug=False)