import pytest
import json
import os
import tempfile
import shutil
from app import app

@pytest.mark.integration
class TestCategoriaAPI:
    """Testes de integração para API de categorias"""
    
    @pytest.fixture
    def client(self):
        """Cliente de teste com dados temporários isolados"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            yield client
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_listar_categorias_vazio(self, client):
        """Testa listagem quando não há categorias"""
        response = client.get('/categorias/api')
        
        assert response.status_code == 200
        assert response.json == []
    
    def test_criar_categoria_sucesso(self, client):
        """Testa criação bem-sucedida de categoria"""
        dados = {
            'nome': 'Trabalho',
            'descricao': 'Contatos profissionais'
        }
        
        response = client.post('/categorias/api', 
                             json=dados,
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['nome'] == 'Trabalho'
        assert response.json['descricao'] == 'Contatos profissionais'
        assert 'id' in response.json
    
    def test_criar_categoria_sem_nome(self, client):
        """Testa criação de categoria sem nome (deve falhar)"""
        dados = {'descricao': 'Apenas descrição'}
        
        response = client.post('/categorias/api',
                             json=dados,
                             content_type='application/json')
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_obter_categoria_existente(self, client):
        """Testa obter categoria que existe"""
        # Primeiro, cria uma categoria
        dados = {'nome': 'Família', 'descricao': 'Contatos familiares'}
        create_response = client.post('/categorias/api', json=dados)
        categoria_id = create_response.json['id']
        
        # Depois, busca a categoria
        response = client.get(f'/categorias/api/{categoria_id}')
        
        assert response.status_code == 200
        assert response.json['nome'] == 'Família'
        assert response.json['id'] == categoria_id
    
    def test_obter_categoria_inexistente(self, client):
        """Testa obter categoria que não existe"""
        response = client.get('/categorias/api/999')
        
        assert response.status_code == 404
        assert 'error' in response.json
    
    def test_atualizar_categoria_sucesso(self, client):
        """Testa atualização bem-sucedida de categoria"""
        # Cria categoria
        dados = {'nome': 'Amigos'}
        create_response = client.post('/categorias/api', json=dados)
        categoria_id = create_response.json['id']
        
        # Atualiza categoria
        novos_dados = {
            'nome': 'Amigos Próximos',
            'descricao': 'Melhores amigos'
        }
        response = client.put(f'/categorias/api/{categoria_id}', json=novos_dados)
        
        assert response.status_code == 200
        assert 'message' in response.json
        
        # Verifica se foi atualizada
        get_response = client.get(f'/categorias/api/{categoria_id}')
        assert get_response.json['nome'] == 'Amigos Próximos'
        assert get_response.json['descricao'] == 'Melhores amigos'
    
    def test_excluir_categoria_sucesso(self, client):
        """Testa exclusão bem-sucedida de categoria"""
        # Cria categoria
        dados = {'nome': 'Temporária'}
        create_response = client.post('/categorias/api', json=dados)
        categoria_id = create_response.json['id']
        
        # Exclui categoria
        response = client.delete(f'/categorias/api/{categoria_id}')
        
        assert response.status_code == 200
        assert 'message' in response.json
        
        # Verifica se foi excluída
        get_response = client.get(f'/categorias/api/{categoria_id}')
        assert get_response.status_code == 404

@pytest.mark.integration
class TestContatoAPI:
    """Testes de integração para API de contatos"""
    
    @pytest.fixture
    def client_with_categoria(self):
        """Cliente com categoria pré-criada"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            # Cria uma categoria para os testes
            categoria_data = {'nome': 'Teste', 'descricao': 'Categoria de teste'}
            response = client.post('/categorias/api', json=categoria_data)
            categoria_id = response.json['id']
            
            yield client, categoria_id
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture  
    def client_limpo(self):
        """Cliente isolado para testes que precisam começar limpos"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            yield client
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_listar_contatos_vazio(self, client_limpo):
        """Testa listagem quando não há contatos"""
        response = client_limpo.get('/contatos/api')
        
        assert response.status_code == 200
        assert response.json == []
    
    def test_criar_contato_completo(self, client_with_categoria):
        """Testa criação de contato com todos os campos"""
        client, categoria_id = client_with_categoria
        
        dados = {
            'nome': 'João Silva',
            'telefone': '(11) 99999-9999',
            'email': 'joao@teste.com',
            'categoria_id': categoria_id
        }
        
        response = client.post('/contatos/api', json=dados)
        
        assert response.status_code == 201
        assert response.json['nome'] == 'João Silva'
        assert response.json['telefone'] == '(11) 99999-9999'
        assert response.json['email'] == 'joao@teste.com'
        assert response.json['categoria_id'] == categoria_id
        assert 'id' in response.json
    
    def test_criar_contato_sem_nome(self, client_limpo):
        """Testa criação de contato sem nome (deve falhar)"""
        dados = {'telefone': '123456789'}
        
        response = client_limpo.post('/contatos/api', json=dados)
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_criar_contato_sem_telefone(self, client_limpo):
        """Testa criação de contato sem telefone (deve falhar)"""
        dados = {'nome': 'João'}
        
        response = client_limpo.post('/contatos/api', json=dados)
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_buscar_contatos_por_nome(self, client_with_categoria):
        """Testa busca de contatos por nome"""
        client, categoria_id = client_with_categoria
        
        # Cria alguns contatos específicos para este teste
        contatos = [
            {'nome': 'João Silva Teste', 'telefone': '111'},
            {'nome': 'João Santos Teste', 'telefone': '222'},
            {'nome': 'Maria Silva Teste', 'telefone': '333'}
        ]
        
        for contato in contatos:
            client.post('/contatos/api', json=contato)
        
        # Busca por "João Teste" (mais específico)
        response = client.get('/contatos/api?nome=João Teste')
        
        assert response.status_code == 200
        assert len(response.json) == 2
        assert all('João' in contato['nome'] and 'Teste' in contato['nome'] for contato in response.json)
    
    def test_buscar_contatos_por_categoria(self, client_with_categoria):
        """Testa busca de contatos por categoria"""
        client, categoria_id = client_with_categoria
        
        # Cria contatos com e sem categoria
        contatos = [
            {'nome': 'Com Categoria', 'telefone': '111', 'categoria_id': categoria_id},
            {'nome': 'Sem Categoria', 'telefone': '222'}
        ]
        
        for contato in contatos:
            client.post('/contatos/api', json=contato)
        
        # Busca por categoria
        response = client.get(f'/contatos/api?categoria_id={categoria_id}')
        
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['nome'] == 'Com Categoria'
    
    def test_fluxo_completo_crud_contato(self, client_with_categoria):
        """Testa fluxo completo CRUD de contato"""
        client, categoria_id = client_with_categoria
        
        # CREATE - Cria um contato
        dados_criar = {
            'nome': 'Pedro Costa',
            'telefone': '(11) 88888-8888',
            'email': 'pedro@teste.com',
            'categoria_id': categoria_id
        }
        
        create_response = client.post('/contatos/api', json=dados_criar)
        assert create_response.status_code == 201
        contato_id = create_response.json['id']
        
        # READ - Busca o contato criado
        get_response = client.get(f'/contatos/api/{contato_id}')
        assert get_response.status_code == 200
        assert get_response.json['nome'] == 'Pedro Costa'
        
        # UPDATE - Atualiza o contato
        dados_atualizar = {
            'nome': 'Pedro Costa Silva',
            'telefone': '(11) 77777-7777',
            'email': 'pedro.silva@teste.com',
            'categoria_id': categoria_id
        }
        
        update_response = client.put(f'/contatos/api/{contato_id}', json=dados_atualizar)
        assert update_response.status_code == 200
        
        # Verifica se foi atualizado
        get_updated_response = client.get(f'/contatos/api/{contato_id}')
        assert get_updated_response.json['nome'] == 'Pedro Costa Silva'
        assert get_updated_response.json['telefone'] == '(11) 77777-7777'
        
        # DELETE - Exclui o contato
        delete_response = client.delete(f'/contatos/api/{contato_id}')
        assert delete_response.status_code == 200
        
        # Verifica se foi excluído
        get_deleted_response = client.get(f'/contatos/api/{contato_id}')
        assert get_deleted_response.status_code == 404