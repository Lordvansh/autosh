from flask import Flask, request, jsonify
from autoshopify import stormxcc

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Autoshopify API running on Vercel!"

@app.route("/check", methods=["GET"])
def check_card():
    # --- Get query params ---
    cc = request.args.get("cc")
    site = request.args.get("site")
    proxy = request.args.get("proxy", "")
    tries = int(request.args.get("tries", 2))
    timeout = int(request.args.get("timeout", 120))

    # --- Validate ---
    if not cc or not site:
        return jsonify({"error": "Missing required parameters: cc and site"}), 400

    try:
        # --- Call autoshopify function ---
        resp = stormxcc(
            site=site,
            cc=cc,
            proxy=proxy,
            tries=tries,
            timeout=timeout
        )

        result = {"status_code": resp.status_code}

        # --- Try parsing JSON ---
        try:
            result["response"] = resp.json()
        except Exception:
            result["response"] = resp.text[:500]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Required entrypoint for Vercel ---
def handler(environ, start_response):
    return app(environ, start_response)
