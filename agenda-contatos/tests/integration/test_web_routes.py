import pytest
import tempfile
from app import app

@pytest.mark.integration
class TestWebRoutes:
    """Testes de integração para rotas web da aplicação"""
    
    @pytest.fixture
    def client(self):
        """Cliente de teste com dados temporários"""
        with tempfile.TemporaryDirectory() as temp_dir:
            app.config['TESTING'] = True
            app.config['DATA_PATH'] = temp_dir
            
            with app.test_client() as client:
                yield client
    
    def test_pagina_inicial(self, client):
        """Testa se a página inicial carrega corretamente"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Bem-vindo' in response.data
        assert b'Agenda de Contatos' in response.data
    
    def test_pagina_404(self, client):
        """Testa página de erro 404"""
        response = client.get('/pagina-inexistente')
        
        assert response.status_code == 404
        assert b'404' in response.data
        assert b'encontrada' in response.data

@pytest.mark.integration
class TestCategoriaWebRoutes:
    """Testes de integração para rotas web de categorias"""
    
    @pytest.fixture
    def client(self):
        """Cliente de teste com dados temporários"""
        with tempfile.TemporaryDirectory() as temp_dir:
            app.config['TESTING'] = True
            app.config['DATA_PATH'] = temp_dir
            
            with app.test_client() as client:
                yield client
    
    def test_listar_categorias_pagina(self, client):
        """Testa página de listagem de categorias"""
        response = client.get('/categorias/')
        
        assert response.status_code == 200
        assert b'Categorias' in response.data
        assert b'Nova Categoria' in response.data
    
    def test_pagina_criar_categoria(self, client):
        """Testa página de criação de categoria"""
        response = client.get('/categorias/nova')
        
        assert response.status_code == 200
        assert b'Nova Categoria' in response.data
        assert b'Nome' in response.data
        assert 'Descrição' in response.data.decode('utf-8')
    
    def test_criar_categoria_via_web(self, client):
        """Testa criação de categoria via formulário web"""
        dados = {
            'nome': 'Trabalho Web',
            'descricao': 'Categoria criada via web'
        }
        
        response = client.post('/categorias/nova', data=dados, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Categoria criada com sucesso' in response.data
        assert b'Trabalho Web' in response.data
    
    def test_criar_categoria_sem_nome_via_web(self, client):
        """Testa criação de categoria sem nome via web"""
        dados = {'descricao': 'Apenas descrição'}
        
        response = client.post('/categorias/nova', data=dados)
        
        assert response.status_code == 200
        assert 'obrigatório' in response.data
    
    def test_fluxo_completo_categoria_web(self, client):
        """Testa fluxo completo de categoria via web"""
        # Criar categoria
        dados_criar = {
            'nome': 'Teste Fluxo',
            'descricao': 'Categoria para teste completo'
        }
        
        create_response = client.post('/categorias/nova', data=dados_criar, follow_redirects=True)
        assert create_response.status_code == 200
        assert b'Categoria criada com sucesso' in create_response.data
        
        # Verificar se aparece na listagem
        list_response = client.get('/categorias/')
        assert b'Teste Fluxo' in list_response.data
        
        # Nota: Para testar edição e exclusão, precisaríamos extrair o ID
        # da resposta HTML, o que seria mais apropriado para testes E2E

@pytest.mark.integration
class TestContatoWebRoutes:
    """Testes de integração para rotas web de contatos"""
    
    @pytest.fixture
    def client_with_categoria(self):
        """Cliente com categoria pré-criada para testes de contatos"""
        with tempfile.TemporaryDirectory() as temp_dir:
            app.config['TESTING'] = True
            app.config['DATA_PATH'] = temp_dir
            
            with app.test_client() as client:
                # Cria uma categoria via API para usar nos contatos
                categoria_data = {'nome': 'Teste Web', 'descricao': 'Para testes web'}
                api_response = client.post('/categorias/api', json=categoria_data)
                categoria_id = api_response.json['id']
                
                yield client, categoria_id
    
    def test_listar_contatos_pagina(self, client):
        """Testa página de listagem de contatos"""
        response = client.get('/contatos/')
        
        assert response.status_code == 200
        assert b'Contatos' in response.data
        assert b'Novo Contato' in response.data
    
    def test_pagina_criar_contato(self, client):
        """Testa página de criação de contato"""
        response = client.get('/contatos/novo')
        
        assert response.status_code == 200
        assert b'Novo Contato' in response.data
        assert b'Nome' in response.data
        assert b'Telefone' in response.data
        assert b'Email' in response.data
    
    def test_criar_contato_via_web(self, client_with_categoria):
        """Testa criação de contato via formulário web"""
        client, categoria_id = client_with_categoria
        
        dados = {
            'nome': 'Ana Silva',
            'telefone': '(11) 99999-9999',
            'email': 'ana@teste.com',
            'categoria_id': categoria_id
        }
        
        response = client.post('/contatos/novo', data=dados, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Contato criado com sucesso' in response.data
        assert b'Ana Silva' in response.data
    
    def test_criar_contato_sem_nome_via_web(self, client):
        """Testa criação de contato sem nome via web"""
        dados = {'telefone': '123456789'}
        
        response = client.post('/contatos/novo', data=dados)
        
        assert response.status_code == 200
        assert 'obrigatório' in response.data
    
    def test_criar_contato_sem_telefone_via_web(self, client):
        """Testa criação de contato sem telefone via web"""
        dados = {'nome': 'João Sem Telefone'}
        
        response = client.post('/contatos/novo', data=dados)
        
        assert response.status_code == 200
        assert 'obrigatório' in response.data
    
    def test_filtrar_contatos_por_nome(self, client_with_categoria):
        """Testa filtro de contatos por nome via web"""
        client, categoria_id = client_with_categoria
        
        # Cria alguns contatos
        contatos = [
            {'nome': 'João Silva', 'telefone': '111'},
            {'nome': 'João Santos', 'telefone': '222'},
            {'nome': 'Maria Silva', 'telefone': '333'}
        ]
        
        for contato in contatos:
            client.post('/contatos/novo', data=contato)
        
        # Testa filtro por nome
        response = client.get('/contatos/?nome=João')
        
        assert response.status_code == 200
        assert 'João Silva' in response.data
        assert 'João Santos' in response.data
        assert 'Maria Silva' not in response.data
    
    def test_navegacao_entre_paginas(self, client):
        """Testa navegação entre diferentes páginas"""
        # Página inicial
        response = client.get('/')
        assert response.status_code == 200
        
        # Link para contatos
        response = client.get('/contatos/')
        assert response.status_code == 200
        
        # Link para categorias
        response = client.get('/categorias/')
        assert response.status_code == 200
        
        # Link para criar novo contato
        response = client.get('/contatos/novo')
        assert response.status_code == 200
        
        # Link para criar nova categoria
        response = client.get('/categorias/nova')
        assert response.status_code == 200