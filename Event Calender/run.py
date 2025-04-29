from flask import Flask
from app.models import db
from app.views import app as application

if __name__ == "__main__":
    application.run(debug=True)
