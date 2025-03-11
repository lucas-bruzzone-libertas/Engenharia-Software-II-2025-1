import datetime
import os

class Logger:
    """
    Implementação do Logger utilizando o padrão Singleton.
    Garante que exista apenas uma instância do Logger em toda a aplicação.
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
    
    def log(self, message, level="INFO"):
        """
        Registra uma mensagem com o nível especificado e timestamp.
        
        Args:
            message (str): A mensagem a ser registrada
            level (str): O nível do log (INFO, WARNING, ERROR)
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)  # Exibe no console
        self.logs.append(log_entry)
        
    def info(self, message):
        """Registra uma mensagem com nível INFO."""
        self.log(message, self.log_levels["INFO"])
        
    def warning(self, message):
        """Registra uma mensagem com nível WARNING."""
        self.log(message, self.log_levels["WARNING"])
        
    def error(self, message):
        """Registra uma mensagem com nível ERROR."""
        self.log(message, self.log_levels["ERROR"])
    
    def save_to_file(self, filename="application.log"):
        """
        Salva todos os logs registrados em um arquivo.
        
        Args:
            filename (str): Nome do arquivo onde os logs serão salvos
        """
        try:
            with open(filename, "w") as file:
                for log_entry in self.logs:
                    file.write(log_entry + "\n")
            return True
        except Exception as e:
            print(f"Erro ao salvar logs: {e}")
            return False
    
    def get_logs(self):
        """Retorna todos os logs registrados."""
        return self.logs


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
    
    # Salvando logs em arquivo
    logger.save_to_file()
    print("\nLogs salvos em 'application.log'")
    
    # Listando todos os logs registrados
    print("\nTodos os logs registrados:")
    for log in logger.get_logs():
        print(f"  {log}")
