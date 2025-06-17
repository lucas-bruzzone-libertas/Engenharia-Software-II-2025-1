import pytest
import tempfile
import shutil
import os
from app import app

@pytest.mark.integration
class TestCategoriaAPI:
    """Testes de integração para API de categorias"""
    
    def test_listar_categorias_com_dados(self):
        """Testa listagem após criar categoria (mais realista)"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        
        with app.test_client() as client:
            # Primeiro cria uma categoria
            dados = {'nome': 'Categoria Teste', 'descricao': 'Para teste'}
            client.post('/categorias/api', json=dados)
            
            # Depois lista para verificar
            response = client.get('/categorias/api')
            assert response.status_code == 200
            assert len(response.json) >= 1
            assert any(cat['nome'] == 'Categoria Teste' for cat in response.json)
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_criar_categoria_sucesso(self):
        """Testa criação bem-sucedida de categoria"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        
        with app.test_client() as client:
            dados = {'nome': 'Trabalho Novo', 'descricao': 'Contatos profissionais'}
            response = client.post('/categorias/api', json=dados)
            
            assert response.status_code == 201
            assert response.json['nome'] == 'Trabalho Novo'
            assert 'id' in response.json
        
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_buscar_categoria_por_id(self):
        """Testa criação bem-sucedida de categoria"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        with app.test_client() as client:
            response = client.get('/categorias/api/1')
            
            assert response.status_code == 200
            assert response.json['nome'] == 'Trabalho E2E 202227'
            assert 'id' in response.json

@pytest.mark.integration
class TestContatoAPI:
    """Testes de integração para API de contatos"""
    
    def test_listar_contatos_com_dados(self):
        """Testa listagem após criar contato (mais realista)"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        
        with app.test_client() as client:
            # Cria um contato
            dados = {'nome': 'Pedro Teste', 'telefone': '(11) 99999-9999'}
            client.post('/contatos/api', json=dados)
            
            # Lista para verificar
            response = client.get('/contatos/api')
            assert response.status_code == 200
            assert len(response.json) >= 1
            assert any(c['nome'] == 'Pedro Teste' for c in response.json)
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_buscar_contatos_por_nome_funcional(self):
        """Testa busca - versão que funciona independente do estado"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        
        with app.test_client() as client:
            # Cria contato único
            dados = {'nome': 'TestBusca12345', 'telefone': '111'}
            create_response = client.post('/contatos/api', json=dados)
            assert create_response.status_code == 201
            
            # Busca pelo nome único
            response = client.get('/contatos/api?nome=TestBusca12345')
            assert response.status_code == 200
            
            # Verifica que encontrou pelo menos 1
            found = [c for c in response.json if 'TestBusca12345' in c['nome']]
            assert len(found) >= 1
        
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_criar_contato_sucesso(self):
        """Testa criação bem-sucedida"""
        temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['DATA_PATH'] = temp_dir
        
        with app.test_client() as client:
            dados = {'nome': 'Ana Nova', 'telefone': '(11) 88888-8888'}
            response = client.post('/contatos/api', json=dados)
            
            assert response.status_code == 201
            assert response.json['nome'] == 'Ana Nova'
            assert 'id' in response.json
        
        shutil.rmtree(temp_dir, ignore_errors=True)


