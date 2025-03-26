import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

class Logger:
    """
    Implementação do Logger utilizando o padrão Singleton.
    Garante que exista apenas uma instância do Logger em toda a aplicação.
    Salva logs em arquivo local com rotação automática.
    """
    # Variável de classe para armazenar a instância única
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """
        Método de classe que retorna a instância única do Logger.
        Se a instância não existir, cria uma nova.
        """
        if cls._instance is None:
            cls._instance = Logger()
            print("Nova instância do Logger criada.")
        return cls._instance
    
    def __init__(self):
        """
        Inicializa o Logger e verifica se já existe uma instância.
        Impede a criação direta de múltiplas instâncias.
        """
        if Logger._instance is not None:
            raise Exception("Esta classe é um Singleton. Use Logger.get_instance() para obter a instância.")
        else:
            # Esta linha só é executada quando get_instance() cria a primeira instância
            Logger._instance = self
            self.logs = []
            self.log_levels = {
                "INFO": "INFO",
                "WARNING": "WARNING",
                "ERROR": "ERROR"
            }
            
            # Cria o diretório de logs se não existir
            self.log_dir = 'logs'
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            
            # Configura o logger do Python
            self.logger = logging.getLogger('agenda_contatos')
            self.logger.setLevel(logging.INFO)
            
            # Formata as mensagens de log
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            
            # Handler para console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # Handler para arquivo com rotação
            # Limita o tamanho de cada arquivo a 1MB e mantém até 10 arquivos de backup
            file_handler = RotatingFileHandler(
                os.path.join(self.log_dir, 'application.log'),
                maxBytes=1024 * 1024,  # 1MB
                backupCount=10
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log(self, message, level="INFO"):
        """
        Registra uma mensagem com o nível especificado.
        
        Args:
            message (str): A mensagem a ser registrada
            level (str): O nível do log (INFO, WARNING, ERROR)
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Adiciona à lista interna de logs
        self.logs.append(log_entry)
        
        # Registra usando o logger do Python
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        
    def info(self, message):
        """Registra uma mensagem com nível INFO."""
        self.log(message, self.log_levels["INFO"])
        
    def warning(self, message):
        """Registra uma mensagem com nível WARNING."""
        self.log(message, self.log_levels["WARNING"])
        
    def error(self, message):
        """Registra uma mensagem com nível ERROR."""
        self.log(message, self.log_levels["ERROR"])
    
    def save_to_file(self, filename=None):
        """
        Força o salvamento de todos os logs registrados em um arquivo específico.
        
        Args:
            filename (str, optional): Nome do arquivo onde os logs serão salvos.
                                      Se None, usa 'logs/manual_backup.log'.
        """
        if filename is None:
            filename = os.path.join(self.log_dir, 'manual_backup.log')
            
        try:
            with open(filename, "w") as file:
                for log_entry in self.logs:
                    file.write(log_entry + "\n")
            return True
        except Exception as e:
            print(f"Erro ao salvar logs: {e}")
            return False
    
    def get_logs(self):
        """Retorna todos os logs registrados na sessão atual."""
        return self.logs
    
    def clear_memory_logs(self):
        """Limpa os logs armazenados em memória (lista interna)."""
        self.logs = []
        return True


# Exemplo de uso do Logger
if __name__ == "__main__":
    # Obtendo a instância do Logger
    logger = Logger.get_instance()
    
    # Registrando mensagens de diferentes níveis
    logger.info("Aplicação iniciada com sucesso")
    logger.warning("Espaço em disco está ficando baixo")
    logger.error("Falha ao conectar ao banco de dados")
    
    # Em outra parte do código (simulando outro módulo)
    print("\nEm outro módulo do sistema:")
    outro_logger = Logger.get_instance()  # Obtém a mesma instância
    outro_logger.info("Operação de backup iniciada")
    
    # Verificando se é a mesma instância
    print(f"\nÉ a mesma instância? {logger is outro_logger}")  # Deve retornar True
    
    # Tentando criar uma instância diretamente (vai gerar erro)
    try:
        print("\nTentando criar uma nova instância diretamente:")
        novo_logger = Logger()  # Isso deve lançar uma exceção
    except Exception as e:
        print(f"Erro capturado: {e}")
    
    # Forçando o salvamento manual em um arquivo específico
    logger.save_to_file('logs/teste_manual.log')
    print("\nBackup manual de logs gerado em 'logs/teste_manual.log'")
    
    # Listando todos os logs registrados
    print("\nTodos os logs registrados:")
    for log in logger.get_logs():
        print(f"  {log}")