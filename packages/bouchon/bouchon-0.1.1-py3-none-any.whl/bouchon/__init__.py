from flask import Flask, request, jsonify
import os

app = Flask(__name__)
__version__ = "0.1.0"


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

    return Response(
        "\n".join(
            [
                f"{request.method} {request.full_path} HTTP/1.1",
                "",
                "# HTTP Headers",
                *map(": ".join, request.headers.items()),
                "",
                "# System Environment",
                *map(" = ".join, sorted(os.environ.items())),
            ]
        ),
        content_type="text/plain",
    )
