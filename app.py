from flask import Flask, request, jsonify
from autoshopify import stormxcc  # Module installed via pip

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Autoshopify API is running!"

@app.route("/check", methods=["GET"])
def check():
    cc = request.args.get("cc")
    site = request.args.get("site")
    proxy = request.args.get("proxy", "")
    tries = int(request.args.get("tries", 1))
    timeout = int(request.args.get("timeout", 30))

    if not cc or not site:
        return jsonify({"error": "Missing required parameters: cc and site"}), 400

    try:
        resp = stormxcc(
            site=site,
            cc=cc,
            proxy=proxy,
            tries=tries,
            timeout=timeout
        )

        result = {"status_code": resp.status_code}

        try:
            result["response"] = resp.json()
        except Exception:
            result["response"] = resp.text[:500]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required by Vercel for Flask WSGI apps
def handler(environ, start_response):
    return app(environ, start_response)
