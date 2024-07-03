from flask import Flask, render_template
from config import Config
from models import db, Vino

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('Index.html')

    @app.route('/tienda')
    def tienda():
        vinos = Vino.query.all()
        return render_template('Tienda.html', vinos=vinos)

    @app.route('/eventos')
    def eventos():
        return render_template('Eventos.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
