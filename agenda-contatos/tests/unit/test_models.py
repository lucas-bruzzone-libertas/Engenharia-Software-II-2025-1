import pytest
from models.contato import Contato
from models.categoria import Categoria

@pytest.mark.unit
class TestContato:
    """Testes unitários para o modelo Contato"""
    
    def test_criar_contato_com_todos_campos(self):
        """Testa criação de contato com todos os campos"""
        contato = Contato(
            id=1,
            nome="João Silva",
            telefone="(11) 99999-9999",
            email="joao@teste.com",
            categoria_id=1
        )
        
        assert contato.id == 1
        assert contato.nome == "João Silva"
        assert contato.telefone == "(11) 99999-9999"
        assert contato.email == "joao@teste.com"
        assert contato.categoria_id == 1
    
    def test_criar_contato_campos_opcionais_none(self):
        """Testa criação de contato com campos opcionais None"""
        contato = Contato(nome="Maria", telefone="123456789")
        
        assert contato.nome == "Maria"
        assert contato.telefone == "123456789"
        assert contato.id is None
        assert contato.email is None
        assert contato.categoria_id is None
    
    def test_contato_to_dict(self):
        """Testa conversão do contato para dicionário"""
        contato = Contato(
            id=1,
            nome="Pedro",
            telefone="987654321",
            email="pedro@teste.com",
            categoria_id=2
        )
        
        resultado = contato.to_dict()
        esperado = {
            'id': 1,
            'nome': 'Pedro',
            'telefone': '987654321',
            'email': 'pedro@teste.com',
            'categoria_id': 2
        }
        
        assert resultado == esperado
    
    def test_contato_from_dict(self):
        """Testa criação de contato a partir de dicionário"""
        dados = {
            'id': 5,
            'nome': 'Ana Santos',
            'telefone': '(11) 88888-8888',
            'email': 'ana@teste.com',
            'categoria_id': 3
        }
        
        contato = Contato.from_dict(dados)
        
        assert contato.id == 5
        assert contato.nome == 'Ana Santos'
        assert contato.telefone == '(11) 88888-8888'
        assert contato.email == 'ana@teste.com'
        assert contato.categoria_id == 3
    
    def test_contato_from_dict_campos_ausentes(self):
        """Testa criação de contato com campos ausentes no dicionário"""
        dados = {'nome': 'Carlos', 'telefone': '555-1234'}
        
        contato = Contato.from_dict(dados)
        
        assert contato.nome == 'Carlos'
        assert contato.telefone == '555-1234'
        assert contato.id is None
        assert contato.email is None
        assert contato.categoria_id is None

@pytest.mark.unit
class TestCategoria:
    """Testes unitários para o modelo Categoria"""
    
    def test_criar_categoria_completa(self):
        """Testa criação de categoria com todos os campos"""
        categoria = Categoria(
            id=1,
            nome="Trabalho",
            descricao="Contatos profissionais"
        )
        
        assert categoria.id == 1
        assert categoria.nome == "Trabalho"
        assert categoria.descricao == "Contatos profissionais"
    
    def test_criar_categoria_sem_descricao(self):
        """Testa criação de categoria sem descrição"""
        categoria = Categoria(nome="Família")
        
        assert categoria.nome == "Família"
        assert categoria.id is None
        assert categoria.descricao is None
    
    def test_categoria_to_dict(self):
        """Testa conversão da categoria para dicionário"""
        categoria = Categoria(
            id=2,
            nome="Amigos",
            descricao="Contatos pessoais"
        )
        
        resultado = categoria.to_dict()
        esperado = {
            'id': 2,
            'nome': 'Amigos',
            'descricao': 'Contatos pessoais'
        }
        
        assert resultado == esperado
    
    def test_categoria_from_dict(self):
        """Testa criação de categoria a partir de dicionário"""
        dados = {
            'id': 3,
            'nome': 'Emergência',
            'descricao': 'Contatos de emergência'
        }
        
        categoria = Categoria.from_dict(dados)
        
        assert categoria.id == 3
        assert categoria.nome == 'Emergência'
        assert categoria.descricao == 'Contatos de emergência'
    
    def test_categoria_from_dict_apenas_nome(self):
        """Testa criação de categoria com apenas nome no dicionário"""
        dados = {'nome': 'Serviços'}
        
        categoria = Categoria.from_dict(dados)
        
        assert categoria.nome == 'Serviços'
        assert categoria.id is None
        assert categoria.descricao is None