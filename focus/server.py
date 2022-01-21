from flask import Flask

application = Flask(__name__)


@application.route("/status/health")
def status_health():
    return "OK", 200


if __name__ == "__main__":
    application.run()
