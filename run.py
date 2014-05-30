from flask import Flask
from models import db

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

if __name__ == '__main__':
    app.run()