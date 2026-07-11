from flask import Flask
from flask_cors import CORS
from models import db
from auth_routes import auth_app

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URL"]="sqlite:///lifenice.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET"]= "dev-secret-change-me"

    CORS(app, resources={r"/api/*": {"origin": "http://localhost:5173"}})

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix="/app")

    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True. port=5000)
