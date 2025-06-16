from repositories.contato_repository import ContatoRepository
from models.contato import Contato
from logger_singleton import Logger

class ContatoService:
    def __init__(self):
        """
        Inicializa o serviço de contatos.
        """
        self.logger = Logger.get_instance()
        self.repository = ContatoRepository()
    
    def listar_todos(self):
        """
        Lista todos os contatos.
        
        Returns:
            list: Lista de objetos Contato
        """
        self.logger.info("Listando todos os contatos")
        return self.repository.listar_todos()
    
    def buscar_por_id(self, id):
        """
        Busca um contato pelo ID.
        
        Args:
            id (int): ID do contato
            
        Returns:
            Contato: Objeto contato encontrado ou None
        """
        self.logger.info(f"Buscando contato por ID: {id}")
        return self.repository.buscar_por_id(id)
    
    def buscar_por_nome(self, nome):
        """
        Busca contatos pelo nome (parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado
            
        Returns:
            list: Lista de objetos Contato que correspondem à busca
        """
        if not nome:
            self.logger.warning("Busca por nome vazio")
            return []
        
        self.logger.info(f"Buscando contatos por nome: {nome}")
        return self.repository.buscar_por_nome(nome)
    
    def buscar_por_categoria(self, categoria_id):
        """
        Busca contatos por categoria.
        
        Args:
            categoria_id (int): ID da categoria
            
        Returns:
            list: Lista de objetos Contato que pertencem à categoria
        """
        self.logger.info(f"Buscando contatos por categoria: ID {categoria_id}")
        return self.repository.buscar_por_categoria(categoria_id)
    
    def criar(self, nome, telefone, email=None, categoria_id=None):
        """
        Cria um novo contato.
        
        Args:
            nome (str): Nome do contato
            telefone (str): Telefone do contato
            email (str, optional): Email do contato
            categoria_id (int, optional): ID da categoria
            
        Returns:
            Contato: Contato criado ou None se falhar
        """
        # Validação básica
        if not nome or not telefone:
            self.logger.warning("Dados insuficientes para criar contato")
            return None
        
        # Cria o contato
        contato = Contato(
            nome=nome,
            telefone=telefone,
            email=email,
            categoria_id=categoria_id
        )
        
        self.logger.info(f"Criando novo contato: {nome}")
        return self.repository.criar(contato)
    
    def atualizar(self, id, nome, telefone, email=None, categoria_id=None):
        """
        Atualiza um contato existente.
        
        Args:
            id (int): ID do contato
            nome (str): Novo nome do contato
            telefone (str): Novo telefone do contato
            email (str, optional): Novo email do contato
            categoria_id (int, optional): Novo ID da categoria
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        # Validação básica
        if not id or not nome or not telefone:
            self.logger.warning("Dados inválidos para atualização de contato")
            return False
        
        # Busca o contato
        contato = self.repository.buscar_por_id(id)
        if not contato:
            self.logger.warning(f"Contato não encontrado para atualização: ID {id}")
            return False
        
        # Atualiza os dados
        contato.nome = nome
        contato.telefone = telefone
        contato.email = email
        contato.categoria_id = categoria_id
        
        self.logger.info(f"Atualizando contato: ID {id}")
        return self.repository.atualizar(contato)
    
    def excluir(self, id):
        """
        Exclui um contato pelo ID.
        
        Args:
            id (int): ID do contato a ser excluído
            
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        self.logger.info(f"Excluindo contato: ID {id}")
        return self.repository.excluir(id)