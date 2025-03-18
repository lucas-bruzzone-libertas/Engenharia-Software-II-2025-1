import json
import os
from models.categoria import Categoria
from logger_singleton import Logger

class CategoriaRepository:
    def __init__(self, data_path='data'):
        """
        Inicializa o repositório de categorias.
        
        Args:
            data_path (str): Caminho para o diretório de dados
        """
        self.logger = Logger.get_instance()
        self.data_path = data_path
        self.file_path = os.path.join(data_path, 'categorias.json')
        
        # Cria o diretório de dados se não existir
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            self.logger.info(f"Diretório de dados criado: {data_path}")
        
        # Cria o arquivo de categorias se não existir
        if not os.path.exists(self.file_path):
            self._save_to_file([])
            self.logger.info(f"Arquivo de categorias criado: {self.file_path}")
    
    def _load_from_file(self):
        """
        Carrega categorias do arquivo JSON.
        
        Returns:
            list: Lista de categorias como dicionários
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            self.logger.error(f"Erro ao carregar categorias: {str(e)}")
            return []
    
    def _save_to_file(self, categorias):
        """
        Salva categorias no arquivo JSON.
        
        Args:
            categorias (list): Lista de categorias como dicionários
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(categorias, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar categorias: {str(e)}")
            return False
    
    def _get_next_id(self, categorias):
        """
        Obtém o próximo ID disponível para uma nova categoria.
        
        Args:
            categorias (list): Lista de categorias atuais
            
        Returns:
            int: Próximo ID disponível
        """
        if not categorias:
            return 1
        return max(cat.get('id', 0) for cat in categorias) + 1
    
    def listar_todas(self):
        """
        Lista todas as categorias.
        
        Returns:
            list: Lista de objetos Categoria
        """
        categorias_dict = self._load_from_file()
        return [Categoria.from_dict(cat) for cat in categorias_dict]
    
    def buscar_por_id(self, id):
        """
        Busca uma categoria pelo ID.
        
        Args:
            id (int): ID da categoria
            
        Returns:
            Categoria: Objeto categoria encontrado ou None
        """
        categorias_dict = self._load_from_file()
        for cat in categorias_dict:
            if cat.get('id') == id:
                return Categoria.from_dict(cat)
        return None
    
    def criar(self, categoria):
        """
        Cria uma nova categoria.
        
        Args:
            categoria (Categoria): Objeto categoria a ser criado
            
        Returns:
            Categoria: Categoria criada com ID atribuído
        """
        categorias_dict = self._load_from_file()
        
        # Atribui um novo ID
        novo_id = self._get_next_id(categorias_dict)
        categoria.id = novo_id
        
        # Adiciona à lista e salva
        categorias_dict.append(categoria.to_dict())
        if self._save_to_file(categorias_dict):
            self.logger.info(f"Categoria criada: {categoria.nome} (ID: {categoria.id})")
            return categoria
        
        self.logger.error(f"Falha ao criar categoria: {categoria.nome}")
        return None
    
    def atualizar(self, categoria):
        """
        Atualiza uma categoria existente.
        
        Args:
            categoria (Categoria): Objeto categoria a ser atualizado
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        if not categoria.id:
            self.logger.error("Tentativa de atualizar categoria sem ID")
            return False
        
        categorias_dict = self._load_from_file()
        for i, cat in enumerate(categorias_dict):
            if cat.get('id') == categoria.id:
                categorias_dict[i] = categoria.to_dict()
                if self._save_to_file(categorias_dict):
                    self.logger.info(f"Categoria atualizada: {categoria.nome} (ID: {categoria.id})")
                    return True
                
                self.logger.error(f"Falha ao salvar atualização da categoria: {categoria.nome}")
                return False
        
        self.logger.warning(f"Categoria não encontrada para atualização: ID {categoria.id}")
        return False
    
    def excluir(self, id):
        """
        Exclui uma categoria pelo ID.
        
        Args:
            id (int): ID da categoria a ser excluída
            
        Returns:
            bool: True se excluída com sucesso, False caso contrário
        """
        categorias_dict = self._load_from_file()
        for i, cat in enumerate(categorias_dict):
            if cat.get('id') == id:
                del categorias_dict[i]
                if self._save_to_file(categorias_dict):
                    self.logger.info(f"Categoria excluída: ID {id}")
                    return True
                
                self.logger.error(f"Falha ao salvar após exclusão da categoria: ID {id}")
                return False
        
        self.logger.warning(f"Categoria não encontrada para exclusão: ID {id}")
        return False