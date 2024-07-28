from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import markdown
from prompts import get_prompt, get_image_prompt
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

os.environ["OPENAI_API_KEY"] = openai_api_key

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
        return response.json().get("choices")[0].get("message").get("content")
    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException: {e}")
        return f"An error occurred: {e}"

def generate_image(topic, domain, level):
    client = OpenAI()
    
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
        app.logger.info(f"Image generated successfully: {image_url}")
        return image_url
    except Exception as e:
        app.logger.error(f"Error generating image: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_explanation', methods=['POST'])
def generate_explanation_route():
    data = request.json
    topic = data.get('topic')
    domain = data.get('domain')
    level = data.get('level')
    explanation_markdown = generate_explanation(topic, domain, level)
    explanation = markdown.markdown(explanation_markdown)
    return jsonify({'explanation': explanation})

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    data = request.json
    topic = data.get('topic')
    domain = data.get('domain')
    level = data.get('level')
    image_url = generate_image(topic, domain, level)
    return jsonify({'image_url': image_url})

@app.route('/refresh', methods=['GET'])
def refresh():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)