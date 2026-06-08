import json
import os
import requests

def handler(event, context):
    # CORS headers - නැත්තම් browser එක block කරනවා
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # OPTIONS request එකට reply - CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    if event['httpMethod']!= 'POST':
        return {'statusCode': 405, 'headers': headers, 'body': json.dumps({"reply": "POST method use කරපන්"})}

    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    if not GROQ_API_KEY:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({"reply": "Error: Vercel/Netlify එකේ GROQ_API_KEY env variable එක සෙට් කරපන්"})}

    try:
        body = json.loads(event['body'])
        user_msg = body.get('message', '')

        url = "https://api.groq.com/openai/v1/chat/completions"
        req_headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_msg}],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        res = requests.post(url, headers=req_headers, json=payload, timeout=30)
        ai_reply = res.json()['choices'][0]['message']['content']

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"reply": ai_reply})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({"reply": "AI reply එක ගන්න බැරි උනා"})}
