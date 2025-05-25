import pytest
import tempfile
import shutil
from app import app
from logger_singleton import Logger
from models.contato import Contato
from models.categoria import Categoria
import pytest

def pytest_configure(config):
    """Registra markers customizados"""
    config.addinivalue_line(
        "markers", "unit: Testes unitários"
    )
    config.addinivalue_line(
        "markers", "integration: Testes de integração"
    )
    config.addinivalue_line(
        "markers", "e2e: Testes end-to-end"
    )

@pytest.fixture
def client():
    """Cliente de teste para a aplicação Flask com isolamento completo"""
    # Cria diretório temporário único para cada teste
    temp_dir = tempfile.mkdtemp()
    
    app.config['TESTING'] = True
    app.config['DATA_PATH'] = temp_dir
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        yield client
    
    # Limpa o diretório após o teste
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def temp_data_dir():
    """Diretório temporário isolado para dados de teste"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def sample_categoria():
    """Categoria de exemplo para testes"""
    return Categoria(id=1, nome="Trabalho", descricao="Contatos profissionais")

@pytest.fixture
def sample_contato():
    """Contato de exemplo para testes"""
    return Contato(
        id=1,
        nome="João Silva", 
        telefone="(11) 99999-9999",
        email="joao@teste.com",
        categoria_id=1
    )

@pytest.fixture
def categorias_mock_data():
    """Dados mock para categorias"""
    return [
        {"id": 1, "nome": "Família", "descricao": "Contatos familiares"},
        {"id": 2, "nome": "Trabalho", "descricao": "Contatos profissionais"}
    ]

@pytest.fixture
def contatos_mock_data():
    """Dados mock para contatos"""
    return [
        {
            "id": 1,
            "nome": "Maria Silva",
            "telefone": "(11) 98888-8888",
            "email": "maria@teste.com",
            "categoria_id": 1
        },
        {
            "id": 2,
            "nome": "Pedro Santos",
            "telefone": "(11) 97777-7777",
            "email": "pedro@teste.com",
            "categoria_id": 2
        }
    ]

@pytest.fixture
def mock_logger(mocker):
    """Mock do logger singleton"""
    mock_instance = mocker.Mock()
    mocker.patch.object(Logger, 'get_instance', return_value=mock_instance)
    return mock_instance