class Categoria:
    """
    Modelo que representa uma categoria de contatos.
    """
    def __init__(self, id=None, nome=None, descricao=None):
        """
        Inicializa uma nova categoria.
        
        Args:
            id (int): Identificador único da categoria
            nome (str): Nome da categoria
            descricao (str): Descrição da categoria
        """
        self.id = id
        self.nome = nome
        self.descricao = descricao
    
    def to_dict(self):
        """
        Converte o objeto categoria para um dicionário.
        
        Returns:
            dict: Dicionário com os dados da categoria
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Cria um objeto Categoria a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados da categoria
            
        Returns:
            Categoria: Uma nova instância de Categoria
        """
        return cls(
            id=data.get('id'),
            nome=data.get('nome'),
            descricao=data.get('descricao')
        )