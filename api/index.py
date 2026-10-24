from flask import Flask, request, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    API_KEY = os.environ.get("GROQ_API_KEY", "")

    if not API_KEY:
        return jsonify({"error": "API Key missing in Vercel settings"}), 500

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps({
            "model": "gemma2-9b-it",
            "messages": [{"role": "user", "content": prompt}]
        }).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
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