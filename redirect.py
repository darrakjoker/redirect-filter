from flask import Flask, request, redirect
import logging

app = Flask(__name__)

# === CPA OFFER URL ===
CPA_URL = "https://www.clouddamed.com/6T9F9B8/2K3W3FW8/"  # <-- Change this to your CPA link

# === Logging setup ===
logging.basicConfig(filename="clicks.log", level=logging.INFO)

# === Microsoft bot detection ===
def is_microsoft_bot(ip, user_agent):
    ms_ip_prefixes = [
        "13.", "20.", "23.", "40.", "52.", "65.", "104.", "131.", "157.", "168."
    ]
    bot_signatures = [
        "Microsoft", "Office", "Outlook", "Word", "Azure", "Bot", "Crawler", "Scan"
    ]

    ip_match = any(ip.startswith(prefix) for prefix in ms_ip_prefixes)
    ua_match = not user_agent or any(bot in user_agent for bot in bot_signatures)

    return ip_match or ua_match

@app.route("/go")
def go():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")

    if is_microsoft_bot(ip, user_agent):
        logging.info(f"[BOT BLOCKED] IP: {ip} | UA: {user_agent}")
        return "Bot detected — not redirecting."

    logging.info(f"[HUMAN CLICK] IP: {ip} | UA: {user_agent}")
    return redirect(CPA_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
