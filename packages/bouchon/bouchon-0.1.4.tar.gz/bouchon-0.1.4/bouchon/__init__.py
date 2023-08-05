from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
@app.route("/<path:path>")
def show_subpath(path=""):
    return jsonify(
        {
            "request": {
                "method": request.method,
                "path": request.path,
                "full_path": request.full_path,
                "headers": dict(sorted(request.headers.items())),
            },
            "system": {"env": dict(sorted(os.environ.items()))},
        }
    )
