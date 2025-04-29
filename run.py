from app import app
from app.views import app as application

if __name__ == "__main__":
    application.run(debug=True)
