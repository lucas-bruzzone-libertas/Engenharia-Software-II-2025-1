import json
import os
from models.contato import Contato
from logger_singleton import Logger

class ContatoRepository:
    def __init__(self, data_path='data'):
        """
        Inicializa o repositório de contatos.
        
        Args:
            data_path (str): Caminho para o diretório de dados
        """
        self.logger = Logger.get_instance()
        self.data_path = data_path
        self.file_path = os.path.join(data_path, 'contatos.json')
        
        # Cria o diretório de dados se não existir
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            self.logger.info(f"Diretório de dados criado: {data_path}")
        
        # Cria o arquivo de contatos se não existir
        if not os.path.exists(self.file_path):
            self._save_to_file([])
            self.logger.info(f"Arquivo de contatos criado: {self.file_path}")
    
    def _load_from_file(self):
        """
        Carrega contatos do arquivo JSON.
        
        Returns:
            list: Lista de contatos como dicionários
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            self.logger.error(f"Erro ao carregar contatos: {str(e)}")
            return []
    
    def _save_to_file(self, contatos):
        """
        Salva contatos no arquivo JSON.
        
        Args:
            contatos (list): Lista de contatos como dicionários
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(contatos, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar contatos: {str(e)}")
            return False
    
    def _get_next_id(self, contatos):
        """
        Obtém o próximo ID disponível para um novo contato.
        
        Args:
            contatos (list): Lista de contatos atuais
            
        Returns:
            int: Próximo ID disponível
        """
        if not contatos:
            return 1
        return max(contato.get('id', 0) for contato in contatos) + 1
    
    def listar_todos(self):
        """
        Lista todos os contatos.
        
        Returns:
            list: Lista de objetos Contato
        """
        contatos_dict = self._load_from_file()
        return [Contato.from_dict(contato) for contato in contatos_dict]
    
    def buscar_por_id(self, id):
        """
        Busca um contato pelo ID.
        
        Args:
            id (int): ID do contato
            
        Returns:
            Contato: Objeto contato encontrado ou None
        """
        contatos_dict = self._load_from_file()
        for contato in contatos_dict:
            if contato.get('id') == id:
                return Contato.from_dict(contato)
        return None
    
    def buscar_por_nome(self, nome):
        """
        Busca contatos pelo nome (parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado
            
        Returns:
            list: Lista de objetos Contato que correspondem à busca
        """
        contatos_dict = self._load_from_file()
        resultados = []
        
        # Busca case-insensitive
        nome_lower = nome.lower()
        for contato in contatos_dict:
            if nome_lower in contato.get('nome', '').lower():
                resultados.append(Contato.from_dict(contato))
        
        return resultados
    
    def buscar_por_categoria(self, categoria_id):
        """
        Busca contatos por categoria.
        
        Args:
            categoria_id (int): ID da categoria
            
        Returns:
            list: Lista de objetos Contato que pertencem à categoria
        """
        contatos_dict = self._load_from_file()
        resultados = []
        
        for contato in contatos_dict:
            if contato.get('categoria_id') == categoria_id:
                resultados.append(Contato.from_dict(contato))
        
        return resultados
    
    def criar(self, contato):
        """
        Cria um novo contato.
        
        Args:
            contato (Contato): Objeto contato a ser criado
            
        Returns:
            Contato: Contato criado com ID atribuído
        """
        contatos_dict = self._load_from_file()
        
        # Atribui um novo ID
        novo_id = self._get_next_id(contatos_dict)
        contato.id = novo_id
        
        # Adiciona à lista e salva
        contatos_dict.append(contato.to_dict())
        if self._save_to_file(contatos_dict):
            self.logger.info(f"Contato criado: {contato.nome} (ID: {contato.id})")
            return contato
        
        self.logger.error(f"Falha ao criar contato: {contato.nome}")
        return None
    
    def atualizar(self, contato):
        """
        Atualiza um contato existente.
        
        Args:
            contato (Contato): Objeto contato a ser atualizado
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        if not contato.id:
            self.logger.error("Tentativa de atualizar contato sem ID")
            return False
        
        contatos_dict = self._load_from_file()
        for i, contact in enumerate(contatos_dict):
            if contact.get('id') == contato.id:
                contatos_dict[i] = contato.to_dict()
                if self._save_to_file(contatos_dict):
                    self.logger.info(f"Contato atualizado: {contato.nome} (ID: {contato.id})")
                    return True
                
                self.logger.error(f"Falha ao salvar atualização do contato: {contato.nome}")
                return False
        
        self.logger.warning(f"Contato não encontrado para atualização: ID {contato.id}")
        return False
    
    def excluir(self, id):
        """
        Exclui um contato pelo ID.
        
        Args:
            id (int): ID do contato a ser excluído
            
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        contatos_dict = self._load_from_file()
        for i, contato in enumerate(contatos_dict):
            if contato.get('id') == id:
                del contatos_dict[i]
                if self._save_to_file(contatos_dict):
                    self.logger.info(f"Contato excluído: ID {id}")
                    return True
                
                self.logger.error(f"Falha ao salvar após exclusão do contato: ID {id}")
                return False
        
        self.logger.warning(f"Contato não encontrado para exclusão: ID {id}")
        return False