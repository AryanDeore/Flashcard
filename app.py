from flask import Flask, request, render_template, url_for
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Get the API key from environment variables
perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')

def generate_explanation(topic, domain, level):
    if level == "5 year old":
        prompt = f"Explain {topic} in {domain} to me like I am a 5 year old."
        payload = {
            "model": "llama-3-sonar-small-32k-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    elif level == "undergrad student":
        prompt = f"Explain {topic} in {domain} to me like I am an undergrad student. Provide a simple explanation, 2 use cases, and 2 advantages and disadvantages if they exist."
        payload = {
            "model": "llama-3-sonar-small-32k-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    elif level == "Subject Matter Expert":
        prompt = f"Explain {topic} and its architecture in {domain} to me like I am a subject matter expert. Provide a detailed technical explanation with step-by-step procedure in 8 steps."
        payload = {
            "model": "llama-3-sonar-small-32k-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {perplexity_api_key}"},
            json=payload,
            stream=True

        )
        response.raise_for_status()
        return response.json().get("choices")[0].get("message").get("content")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    explanation = ""
    if request.method == 'POST':
        topic = request.form['topic']
        domain = request.form['domain']
        level = request.form['level']
        explanation = generate_explanation(topic, domain, level)
    return render_template('index.html', explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)
