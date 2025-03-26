from repositories.categoria_repository import CategoriaRepository
from models.categoria import Categoria
from logger_singleton import Logger

class CategoriaService:
    def __init__(self):
        """
        Inicializa o serviço de categorias.
        """
        self.logger = Logger.get_instance()
        self.repository = CategoriaRepository()
    
    def listar_todas(self):
        """
        Lista todas as categorias.
        
        Returns:
            list: Lista de objetos Categoria
        """
        self.logger.info("Listando todas as categorias")
        return self.repository.listar_todas()
    
    def buscar_por_id(self, id):
        """
        Busca uma categoria pelo ID.
        
        Args:
            id (int): ID da categoria
            
        Returns:
            Categoria: Objeto categoria encontrado ou None
        """
        self.logger.info(f"Buscando categoria por ID: {id}")
        return self.repository.buscar_por_id(id)
    
    def criar(self, nome, descricao=None):
        """
        Cria uma nova categoria.
        
        Args:
            nome (str): Nome da categoria
            descricao (str, optional): Descrição da categoria
            
        Returns:
            Categoria: Categoria criada ou None se falhar
        """
        # Validação básica
        if not nome:
            self.logger.warning("Tentativa de criar categoria com nome vazio")
            return None
        
        # Cria a categoria
        categoria = Categoria(nome=nome, descricao=descricao)
        self.logger.info(f"Criando nova categoria: {nome}")
        return self.repository.criar(categoria)
    
    def atualizar(self, id, nome, descricao=None):
        """
        Atualiza uma categoria existente.
        
        Args:
            id (int): ID da categoria
            nome (str): Novo nome da categoria
            descricao (str, optional): Nova descrição da categoria
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        # Validação básica
        if not id or not nome:
            self.logger.warning("Dados inválidos para atualização de categoria")
            return False
        
        # Busca a categoria
        categoria = self.repository.buscar_por_id(id)
        if not categoria:
            self.logger.warning(f"Categoria não encontrada para atualização: ID {id}")
            return False
        
        # Atualiza os dados
        categoria.nome = nome
        categoria.descricao = descricao
        
        self.logger.info(f"Atualizando categoria: ID {id}")
        return self.repository.atualizar(categoria)
    
    def excluir(self, id):
        """
        Exclui uma categoria pelo ID.
        
        Args:
            id (int): ID da categoria a ser excluída
            
        Returns:
            bool: True se excluída com sucesso, False caso contrário
        """
        self.logger.info(f"Excluindo categoria: ID {id}")
        return self.repository.excluir(id)