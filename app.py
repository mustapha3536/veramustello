import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Core Environment Variables safely mapped on Render
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STOREFRONT_URL = "https://mustapha3536.github.io/veramustello/"

@app.route('/')
def dashboard():
    # A sleek, interactive dark-mode dashboard for your marketing metrics
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Vera Mustello — OpenClaw Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex items-center justify-center p-4">
        <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl"></div>
            
            <div class="flex items-center gap-3 mb-6">
                <div class="w-3.5 h-3.5 bg-emerald-500 rounded-full animate-ping absolute"></div>
                <div class="w-3.5 h-3.5 bg-emerald-500 rounded-full"></div>
                <h1 class="text-lg font-bold tracking-tight text-slate-200">OpenClaw Engine Status</h1>
            </div>
            
            <div class="space-y-4">
                <div class="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4">
                    <span class="text-xs text-slate-500 block mb-1 uppercase tracking-wider font-semibold">Gateway Interface</span>
                    <span class="text-sm font-mono text-emerald-400">Telegram Protocol Active</span>
                </div>
                
                <div class="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4">
                    <span class="text-xs text-slate-500 block mb-1 uppercase tracking-wider font-semibold">Sync Target Pipeline</span>
                    <a href="{STOREFRONT_URL}" target="_blank" class="text-sm font-mono text-sky-400 hover:underline break-all">{STOREFRONT_URL}</a>
                </div>
            </div>
            
            <div class="mt-6 pt-4 border-t border-slate-800/60 text-center">
                <p class="text-[11px] text-slate-500">Vera Mustello AI Automation © 2026</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]
        
        # 1. Forward conversational traffic straight to your OpenRouter API Key
        openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # We instruct the AI to know everything about your products using your live setup text
        payload = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [
                {
                    "role": "system", 
                    "content": f"You are the senior marketing executive for Vera Mustello wellness brand. Your goal is to explain products (Tre-en-en, Cal-Mag, Carotenoid Complex) and cleanly send users to purchase on your catalog link: {STOREFRONT_URL}. Be helpful, polite, and persuasive."
                },
                {"role": "user", "content": user_text}
            ]
        }
        
        try:
            ai_response = requests.post(openrouter_url, json=payload, headers=headers, timeout=10).json()
            reply_text = ai_response['choices'][0]['message']['content']
        except Exception:
            # Safe fall-back message if OpenRouter runs out of credits or drops mid-transit
            reply_text = f"Hello! Welcome to Vera Mustello. Our automated catalog system is running a quick refresh. You can browse all live wellness products right here: {STOREFRONT_URL}"

        # 2. Transmit the response message straight back to the user on Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply_text}, timeout=10)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
