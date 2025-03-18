from flask import Flask, render_template, redirect, url_for, request
from controllers.contato_controller import contato_bp
from controllers.categoria_controller import categoria_bp
from logger_singleton import Logger
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Para flash messages

# Registra os blueprints
app.register_blueprint(contato_bp)
app.register_blueprint(categoria_bp)

# Configura o logger
logger = Logger.get_instance()

@app.route('/')
def index():
    """Página inicial que redireciona para a lista de contatos"""
    logger.info("Página inicial acessada")
    return render_template('index.html')

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    """Tratamento para página não encontrada"""
    logger.warning(f"Página não encontrada: {request.path}")
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Certifica-se de que o diretório de dados existe
    os.makedirs('data', exist_ok=True)
    
    # Log de inicialização
    logger.info("Aplicação Agenda de Contatos iniciada")
    
    # Inicie o aplicativo Flask
    app.run(debug=True)