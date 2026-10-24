from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import json
import os

# Tell Flask that the static files are in the parent directory
app = Flask(__name__, static_folder='../', static_url_path='')

# 1. Serve the frontend
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# 2. Handle the AI chat
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

    if not API_KEY:
        return jsonify({"error": "API Key missing in Vercel settings"}), 500

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": "google/gemma-2-9b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        }).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://vercel.app",
            "X-Title": "Study Tracker"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            ai_text = result['choices'][0]['message']['content']
            return jsonify({"text": ai_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

handler = app