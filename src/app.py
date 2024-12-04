import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Task
from routes.tasks import bp

load_dotenv()

# solo si estoy usando sqlite
PATH = os.path.abspath('instance')

app = Flask(__name__, instance_path=PATH)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
Migrate(app, db) # flask db init, db migrate, db upgrade, db downgrade
CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/')
def main():
    return jsonify({ "status": "Server running successfully"}), 200

app.register_blueprint(bp, url_prefix="/api")

with app.app_context():
    #pass
    #'''
    user = User.query.filter_by(username="test").first()
    if not user:
        user = User()
        user.username = "test"
        user.password = "test"

        db.session.add(user)
        db.session.commit()
        print("User test created")
    #'''

if __name__ == '__main__':
    app.run()