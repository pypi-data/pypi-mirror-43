from flask import Flask, request, Response
import os

app = Flask(__name__)
__version__ = "0.1.0"


@app.route("/")
@app.route("/<path:path>")
def show_subpath(path=""):
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
