import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Core Environment Variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STOREFRONT_URL = "https://mustapha3536.github.io/veramustello/"

# The product catalog used for both customer chat and video scripts
PRODUCT_CATALOG = """
OFFICIAL REAL-TIME PRICE CATALOG:
1. Chelated Cal-Mag with 500 IU Vitamin D3 - 90 Tablets
   - Price: ₦24,750.00
   - Benefits: Highly bioavailable calcium and magnesium to boost bone strength, nerve function, and deep muscle relaxation.
2. Carotenoid Complex - 90 Capsules
   - Price: ₦80,280.00
   - Benefits: Elite whole-food antioxidant shield proven to augment immune capacity by 37% in just 20 days.
3. Aloe Vera Plus
   - Price: ₦22,750.00
   - Benefits: Refreshing herbal blend designed to calm the digestive tract and assist with sustained energy layout.
4. Chewable All-C - 90 Tablets
   - Price: ₦35,050.00
   - Benefits: Delicious daily dose of premium vitamin C to support skin cells and robust body defenses.
5. CoQ10 - 60 Capsules
   - Price: ₦64,250.00
   - Benefits: Delivers targeted energy infrastructure straight to your heart cells for optimal natural stamina.
6. Feminine Herbal Complex - 60 Tablets
   - Price: ₦56,240.00
   - Benefits: Proprietary blend of distinct botanicals calibrated for modern women's balance and health wellness.
7. Fibre Tablets - 120 Tablets
   - Price: ₦30,910.00
   - Benefits: Sourced from broad natural plants to aid fast digestive transit and internal body cleansing.
8. Flavonoid Complex - 60 Tablets
   - Price: ₦40,350.00
   - Benefits: Water-soluble cellular protection to shield vascular pathways and improve system protection.
"""

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
                    <span class="text-sm font-mono text-emerald-400">Content Engine Active</span>
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
        user_text = update["message"]["text"].strip()
        
        openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # ROUTER LOGIC: Check if you are requesting a content script
        if user_text.lower().startswith('/script'):
            # Switch system behavior to Creative Content Director
            system_content = (
                "You are the expert Creative Content Director and Viral Growth Hacker for Vera Mustello. "
                "Your job is to write high-converting, punchy, 20-30 second TikTok/Instagram Reels script blueprints based on the product catalog provided.\n\n"
                f"{PRODUCT_CATALOG}\n\n"
                "When a user triggers this mode, choose the specific product they named (or pick one at random if they just said /script) and output the script using exactly this format:\n\n"
                "🎬 **VIRAL TIKTOK BLUEPRINT**\n"
                "📦 **Product Focus:** [Product Name]\n\n"
                "🚨 **ON-SCREEN TEXT HOOK (First 3 Secs):**\n"
                "[Write a bold, pattern-interrupt text hook to layer on the video]\n\n"
                "📸 **VISUAL DIRECTION:**\n"
                "[Describe a clean, aesthetic faceless visual scene or action that matches the audio]\n\n"
                "🎙️ **VOICEOVER SCRIPT (Copy into CapCut AI):**\n"
                "[Write a punchy, problem-led voiceover script. Must mention the benefits and the exact price in Nigerian Naira ₦. Do not use emojis inside the spoken script text, keep it natural for text-to-speech engine generation.]\n\n"
                "🎯 **CALL TO ACTION (CTA):**\n"
                "[Instruct them to click the bio link to run into our automated Telegram bot pipeline]"
            )
            prompt_query = f"Generate a video script blueprint based on this request: {user_text}"
        else:
            # Maintain standard premium customer support assistant logic
            system_content = (
                "You are the professional, highly persuasive senior marketing executive for Vera Mustello wellness brand. "
                f"Your objective is to answer product questions accurately, state real prices in Nigerian Naira (₦), "
                f"and professionally drive users to click our catalog link to order: {STOREFRONT_URL}\n\n"
                "CRITICAL RULES:\n"
                "- ALWAYS quote prices in Nigerian Naira (₦). Never mention US Dollars ($).\n"
                "- Only use the exact naming conventions and sizes listed in the catalog below.\n\n"
                f"{PRODUCT_CATALOG}\n\n"
                f"Conclude responses by cleanly offering to help them complete their selection via our checkout layout: {STOREFRONT_URL}"
            )
            prompt_query = user_text

        payload = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_query}
            ]
        }
        
        try:
            ai_response = requests.post(openrouter_url, json=payload, headers=headers, timeout=10).json()
            reply_text = ai_response['choices'][0]['message']['content']
        except Exception:
            reply_text = f"Hello! Welcome to Vera Mustello. Our automated systems are refreshing. You can view our entire wellness catalog live right here: {STOREFRONT_URL}"

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply_text}, timeout=10)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
