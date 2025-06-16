import pytest
from unittest.mock import Mock, patch
from services.contato_service import ContatoService
from services.categoria_service import CategoriaService
from models.contato import Contato
from models.categoria import Categoria

@pytest.mark.unit
class TestContatoService:
    """Testes unitários para ContatoService"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        with patch('services.contato_service.Logger.get_instance'):
            self.service = ContatoService()
        self.service.repository = Mock()
    
    def test_listar_todos_contatos(self):
        """Testa listagem de todos os contatos"""
        # Arrange
        contatos_mock = [
            Contato(id=1, nome="João", telefone="123"),
            Contato(id=2, nome="Maria", telefone="456")
        ]
        self.service.repository.listar_todos.return_value = contatos_mock
        
        # Act
        resultado = self.service.listar_todos()
        
        # Assert
        assert resultado == contatos_mock
        self.service.repository.listar_todos.assert_called_once()
    
    def test_buscar_contato_por_id_existente(self):
        """Testa busca de contato por ID existente"""
        # Arrange
        contato_mock = Contato(id=1, nome="João", telefone="123")
        self.service.repository.buscar_por_id.return_value = contato_mock
        
        # Act
        resultado = self.service.buscar_por_id(1)
        
        # Assert
        assert resultado == contato_mock
        self.service.repository.buscar_por_id.assert_called_once_with(1)
    
    def test_criar_contato_valido(self):
        """Testa criação de contato com dados válidos"""
        # Arrange
        contato_criado = Contato(id=1, nome="Pedro", telefone="789", email="pedro@test.com")
        self.service.repository.criar.return_value = contato_criado
        
        # Act
        resultado = self.service.criar("Pedro", "789", "pedro@test.com", 1)
        
        # Assert
        assert resultado == contato_criado
        self.service.repository.criar.assert_called_once()
        
        # Verifica se o contato passado tem os dados corretos
        contato_passado = self.service.repository.criar.call_args[0][0]
        assert contato_passado.nome == "Pedro"
        assert contato_passado.telefone == "789"
        assert contato_passado.email == "pedro@test.com"
        assert contato_passado.categoria_id == 1
    
    def test_criar_contato_sem_nome(self):
        """Testa criação de contato sem nome (deve falhar)"""
        # Act
        resultado = self.service.criar("", "123456789")
        
        # Assert
        assert resultado is None
        self.service.repository.criar.assert_not_called()
    
    def test_criar_contato_sem_telefone(self):
        """Testa criação de contato sem telefone (deve falhar)"""
        # Act
        resultado = self.service.criar("João", "")
        
        # Assert
        assert resultado is None
        self.service.repository.criar.assert_not_called()
    
    def test_atualizar_contato_sucesso(self):
        """Testa atualização bem-sucedida de contato"""
        # Arrange
        contato_existente = Contato(id=1, nome="João", telefone="123")
        self.service.repository.buscar_por_id.return_value = contato_existente
        self.service.repository.atualizar.return_value = True
        
        # Act
        resultado = self.service.atualizar(1, "João Silva", "987654321", "joao@novo.com", 2)
        
        # Assert
        assert resultado is True
        self.service.repository.buscar_por_id.assert_called_once_with(1)
        self.service.repository.atualizar.assert_called_once()
    
    def test_atualizar_contato_inexistente(self):
        """Testa atualização de contato que não existe"""
        # Arrange
        self.service.repository.buscar_por_id.return_value = None
        
        # Act
        resultado = self.service.atualizar(999, "João", "123")
        
        # Assert
        assert resultado is False
        self.service.repository.atualizar.assert_not_called()
    
    def test_excluir_contato(self):
        """Testa exclusão de contato"""
        # Arrange
        self.service.repository.excluir.return_value = True
        
        # Act
        resultado = self.service.excluir(1)
        
        # Assert
        assert resultado is True
        self.service.repository.excluir.assert_called_once_with(1)

@pytest.mark.unit
class TestCategoriaService:
    """Testes unitários para CategoriaService"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        with patch('services.categoria_service.Logger.get_instance'):
            self.service = CategoriaService()
        self.service.repository = Mock()
    
    def test_listar_todas_categorias(self):
        """Testa listagem de todas as categorias"""
        # Arrange
        categorias_mock = [
            Categoria(id=1, nome="Trabalho"),
            Categoria(id=2, nome="Família")
        ]
        self.service.repository.listar_todas.return_value = categorias_mock
        
        # Act
        resultado = self.service.listar_todas()
        
        # Assert
        assert resultado == categorias_mock
        self.service.repository.listar_todas.assert_called_once()
    
    def test_criar_categoria_valida(self):
        """Testa criação de categoria com dados válidos"""
        # Arrange
        categoria_criada = Categoria(id=1, nome="Amigos", descricao="Contatos pessoais")
        self.service.repository.criar.return_value = categoria_criada
        
        # Act
        resultado = self.service.criar("Amigos", "Contatos pessoais")
        
        # Assert
        assert resultado == categoria_criada
        self.service.repository.criar.assert_called_once()
        
        # Verifica dados da categoria passada
        categoria_passada = self.service.repository.criar.call_args[0][0]
        assert categoria_passada.nome == "Amigos"
        assert categoria_passada.descricao == "Contatos pessoais"
    
    def test_criar_categoria_sem_nome(self):
        """Testa criação de categoria sem nome (deve falhar)"""
        # Act
        resultado = self.service.criar("")
        
        # Assert
        assert resultado is None
        self.service.repository.criar.assert_not_called()
    
    def test_criar_categoria_nome_none(self):
        """Testa criação de categoria com nome None (deve falhar)"""
        # Act
        resultado = self.service.criar(None)
        
        # Assert
        assert resultado is None
        self.service.repository.criar.assert_not_called()
    
    def test_atualizar_categoria_sucesso(self):
        """Testa atualização bem-sucedida de categoria"""
        # Arrange
        categoria_existente = Categoria(id=1, nome="Trabalho")
        self.service.repository.buscar_por_id.return_value = categoria_existente
        self.service.repository.atualizar.return_value = True
        
        # Act
        resultado = self.service.atualizar(1, "Trabalho Atualizado", "Nova descrição")
        
        # Assert
        assert resultado is True
        self.service.repository.buscar_por_id.assert_called_once_with(1)
        self.service.repository.atualizar.assert_called_once()
    
    def test_buscar_categoria_por_id(self):
        """Testa busca de categoria por ID"""
        # Arrange
        categoria_mock = Categoria(id=5, nome="Emergência")
        self.service.repository.buscar_por_id.return_value = categoria_mock
        
        # Act
        resultado = self.service.buscar_por_id(5)
        
        # Assert
        assert resultado == categoria_mock
        self.service.repository.buscar_por_id.assert_called_once_with(5)