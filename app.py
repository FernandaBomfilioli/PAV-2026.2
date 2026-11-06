import os

from flask import Flask, jsonify
from flask_restful import Api

from config.database import init_db
from config.settings import settings
from routes.register_routes import register_routes


def create_app():
    app = Flask(__name__)
    api = Api(app)
    register_routes(api)

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        return jsonify({"erro": "Recurso não encontrado."}), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        return jsonify({"erro": "Erro interno do servidor."}), 500

    with app.app_context():
        try:
            init_db()
        except Exception as erro:  # noqa: BLE001
            # Em produção o banco é inicializado pelo init.sql; não interrompe a API.
            app.logger.warning("Não foi possível inicializar o banco: %s", erro)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.FLASK_DEBUG)
