from flask import Flask
from routes.main_routes import main_bp
from routes.analytics_routes import analytics as analytics_bp

app = Flask(__name__)

# registrér dine blueprints
app.register_blueprint(main_bp)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run(debug=True)
