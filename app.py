from flask import Flask, request, render_template, url_for
import os
from dotenv import load_dotenv
import requests
import markdown  # Import the markdown library
from prompts import get_prompt  # Import the get_prompt function

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Get the API key from environment variables
perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')

def generate_explanation(topic, domain, level):
    prompt = get_prompt(level, topic, domain)
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
            json=payload
        )
        response.raise_for_status()
        return response.json().get("choices")[0].get("message").get("content")
    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException: {e}")
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    explanation = ""
    if request.method == 'POST':
        try:
            topic = request.form['topic']
            domain = request.form['domain']
            level = request.form['level']
            explanation_markdown = generate_explanation(topic, domain, level)
            explanation = markdown.markdown(explanation_markdown)  # Convert markdown to HTML
        except KeyError as e:
            app.logger.error(f"Missing form field: {e}")
            return f"Missing form field: {e}", 400
        except Exception as e:
            app.logger.error(f"Error: {e}")
            return f"An error occurred: {e}", 500
    return render_template('index.html', explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)