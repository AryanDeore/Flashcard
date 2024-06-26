from flask import Flask, request, render_template, url_for
import os
from dotenv import load_dotenv
import requests
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Get the API keys from environment variables
perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')

def generate_explanation(topic, domain, level):
    logging.debug(f"Generating explanation for topic: {topic}, domain: {domain}, level: {level}")
    if level == "5 year old":
        prompt = f"""Topic: {topic} in {domain}

I am a 5 year old and have limited vocabulary and limited understanding of the world.

Explain me the above topic in simple words using analogy and anecdotes"""
    elif level == "undergrad student":
        prompt = f"""Topic: {topic} in {domain}

I am an undergrad student and have surface level knowledge of the topic.
Explain me what the topic does in simple language.
Tell me its 2 use cases.
Tell me its 2 advantages and 2 disadvantages if they exist."""
    elif level == "Subject Matter Expert":
        prompt = f"""Topic: {topic} and its architecture in {domain}

I am a subject Matter expert in the topic
Explain me the above topic using relevant technical terms.
Explain the step by step procedure/workflow/process of the topic in 8 steps"""

    logging.debug(f"Prompt: {prompt}")

    # Call Perplexity API
    try:
        response = requests.post(
            "https://api.perplexity.ai/v1/generate",
            headers={"Authorization": f"Bearer {perplexity_api_key}"},
            json={"prompt": prompt, "model": "llama-3-sonar-large-32k-chat"}
        )
        response.raise_for_status()
        logging.debug(f"API Response: {response.json()}")
        return response.json().get("text", "")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "An error occurred while generating the explanation."

@app.route('/', methods=['GET', 'POST'])
def index():
    explanation = ""
    if request.method == 'POST':
        topic = request.form['topic']
        domain = request.form['domain']
        level = request.form['level']
        logging.debug(f"Form data - Topic: {topic}, Domain: {domain}, Level: {level}")
        explanation = generate_explanation(topic, domain, level)
    return render_template('index.html', explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)