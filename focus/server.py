import sys

sys.path.append("..")

from app.server import application

if __name__ == "__main__":
    application.run()
