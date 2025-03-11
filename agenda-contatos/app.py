from flask import Flask, render_template
import os

# Importe o Logger
from logger_singleton import Logger

app = Flask(__name__)

# Obtenha a instância do Logger
logger = Logger.get_instance()

@app.route('/')
def index():
    """Rota inicial para testar o logger"""
    logger.info("Página inicial acessada")
    return """
    <html>
        <head>
            <title>Agenda de Contatos</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
                .info { background-color: #e9f7f7; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Agenda de Contatos - Teste</h1>
                <div class="info">
                    <p>Esta é uma página de teste para verificar se o logger está funcionando.</p>
                    <p>Verifique o console para ver as mensagens de log.</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/teste-log')
def teste_log():
    """Rota para testar diferentes níveis de log"""
    logger.info("Teste de INFO")
    logger.warning("Teste de WARNING")
    logger.error("Teste de ERROR")
    logger.save_to_file()
    
    return """
    <html>
        <head>
            <title>Teste de Logs</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
                .success { background-color: #d4edda; padding: 15px; border-radius: 5px; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Teste de Logger</h1>
                <div class="success">
                    <p>Logs gerados com sucesso!</p>
                    <p>Níveis testados: INFO, WARNING, ERROR</p>
                    <p>Os logs foram salvos em <code>application.log</code>.</p>
                    <p><a href="/">Voltar para a página inicial</a></p>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Log de inicialização
    logger.info("Aplicação iniciada")
    
    # Inicie o aplicativo Flask
    app.run(debug=True)