from django.apps import AppConfig
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    # Run the application with the following line
    app.run(debug=True)

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
