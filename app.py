import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Environment variables securely mapped from Render
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STOREFRONT_URL = "https://mustapha3536.github.io/veramustello/"

@app.route('/')
def dashboard():
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
        
        openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Exact product catalog injected directly into memory to prevent hallucinations
        system_content = (
            "You are the professional, highly persuasive senior marketing executive for Vera Mustello wellness brand. "
            f"Your objective is to answer product questions accurately, state real prices in Nigerian Naira (₦), "
            f"and professionally drive users to click our catalog link to order: {STOREFRONT_URL}\n\n"
            "CRITICAL RULES:\n"
            "- ALWAYS quote prices in Nigerian Naira (₦). Never mention US Dollars ($) or invent arbitrary bundle discounts.\n"
            "- Only use the exact naming conventions and sizes listed below.\n\n"
            "OFFICIAL REAL-TIME PRICE CATALOG:\n"
            "1. Chelated Cal-Mag with 500 IU Vitamin D3 - 90 Tablets\n"
            "   - Price: ₦24,750.00\n"
            "   - Benefits: Highly bioavailable calcium and magnesium to boost bone strength, nerve function, and deep muscle relaxation.\n"
            "2. Carotenoid Complex - 90 Capsules\n"
            "   - Price: ₦80,280.00\n"
            "   - Benefits: Elite whole-food antioxidant shield proven to augment immune capacity by 37% in just 20 days.\n"
            "3. Aloe Vera Plus\n"
            "   - Price: ₦22,750.00\n"
            "   - Benefits: Refreshing herbal blend designed to calm the digestive tract and assist with sustained energy layout.\n"
            "4. Chewable All-C - 90 Tablets\n"
            "   - Price: ₦35,050.00\n"
            "   - Benefits: Delicious daily dose of premium vitamin C to support skin cells and robust body defenses.\n"
            "5. CoQ10 - 60 Capsules\n"
            "   - Price: ₦64,250.00\n"
            "   - Benefits: Delivers targeted energy infrastructure straight to your heart cells for optimal natural stamina.\n"
            "6. Feminine Herbal Complex - 60 Tablets\n"
            "   - Price: ₦56,240.00\n"
            "   - Benefits: Proprietary blend of distinct botanicals calibrated for modern women's balance and health wellness.\n"
            "7. Fibre Tablets - 120 Tablets\n"
            "   - Price: ₦30,910.00\n"
            "   - Benefits: Sourced from broad natural plants to aid fast digestive transit and internal body cleansing.\n"
            "8. Flavonoid Complex - 60 Tablets\n"
            "   - Price: ₦40,350.00\n"
            "   - Benefits: Water-soluble cellular protection to shield vascular pathways and improve system protection.\n\n"
            f"Conclude responses by cleanly offering to help them complete their selection via our checkout layout: {STOREFRONT_URL}"
        )
        
        payload = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_text}
            ]
        }
        
        try:
            ai_response = requests.post(openrouter_url, json=payload, headers=headers, timeout=10).json()
            reply_text = ai_response['choices'][0]['message']['content']
        except Exception:
            reply_text = f"Hello! Welcome to Vera Mustello. Our automated catalog system is running a quick refresh. You can browse all live wellness products right here: {STOREFRONT_URL}"

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply_text}, timeout=10)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
