class Contato:
    """
    Modelo que representa um contato na agenda.
    """
    def __init__(self, id=None, nome=None, telefone=None, email=None, categoria_id=None):
        """
        Inicializa um novo contato.
        
        Args:
            id (int): Identificador único do contato
            nome (str): Nome do contato
            telefone (str): Número de telefone do contato
            email (str): Endereço de email do contato
            categoria_id (int): ID da categoria à qual o contato pertence
        """
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.categoria_id = categoria_id
    
    def to_dict(self):
        """
        Converte o objeto contato para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do contato
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'categoria_id': self.categoria_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Cria um objeto Contato a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados do contato
            
        Returns:
            Contato: Uma nova instância de Contato
        """
        return cls(
            id=data.get('id'),
            nome=data.get('nome'),
            telefone=data.get('telefone'),
            email=data.get('email'),
            categoria_id=data.get('categoria_id')
        )