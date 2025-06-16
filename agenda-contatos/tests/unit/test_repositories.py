import pytest
import os
import tempfile
from unittest.mock import patch
from repositories.contato_repository import ContatoRepository
from repositories.categoria_repository import CategoriaRepository
from models.contato import Contato
from models.categoria import Categoria

@pytest.mark.unit
class TestContatoRepository:
    """Testes unitários para ContatoRepository"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        with patch('repositories.contato_repository.Logger.get_instance'):
            self.repository = ContatoRepository(self.temp_dir)
    
    def test_inicializacao_repositorio(self):
        """Testa inicialização do repositório"""
        assert self.repository.data_path == self.temp_dir
        assert self.repository.file_path == os.path.join(self.temp_dir, 'contatos.json')
        
        # Verifica se o arquivo foi criado
        assert os.path.exists(self.repository.file_path)
    
    def test_get_next_id_lista_vazia(self):
        """Testa obtenção do próximo ID com lista vazia"""
        next_id = self.repository._get_next_id([])
        assert next_id == 1
    
    def test_get_next_id_com_contatos(self):
        """Testa obtenção do próximo ID com contatos existentes"""
        contatos = [
            {'id': 1, 'nome': 'João'},
            {'id': 3, 'nome': 'Pedro'},
            {'id': 2, 'nome': 'Maria'}
        ]
        next_id = self.repository._get_next_id(contatos)
        assert next_id == 4
    
    def test_listar_todos_arquivo_vazio(self):
        """Testa listagem quando arquivo está vazio"""
        contatos = self.repository.listar_todos()
        assert contatos == []
    
    def test_criar_contato_sucesso(self):
        """Testa criação bem-sucedida de contato"""
        contato = Contato(nome="João", telefone="123456789")
        
        resultado = self.repository.criar(contato)
        
        assert resultado is not None
        assert resultado.id == 1
        assert resultado.nome == "João"
        assert resultado.telefone == "123456789"
        
        # Verifica se foi salvo no arquivo
        contatos = self.repository.listar_todos()
        assert len(contatos) == 1
        assert contatos[0].nome == "João"
    
    def test_buscar_por_id_existente(self):
        """Testa busca por ID de contato existente"""
        # Cria um contato primeiro
        contato = Contato(nome="Maria", telefone="987654321")
        contato_criado = self.repository.criar(contato)
        
        # Busca o contato criado
        contato_encontrado = self.repository.buscar_por_id(contato_criado.id)
        
        assert contato_encontrado is not None
        assert contato_encontrado.id == contato_criado.id
        assert contato_encontrado.nome == "Maria"
    
    def test_buscar_por_id_inexistente(self):
        """Testa busca por ID que não existe"""
        contato = self.repository.buscar_por_id(999)
        assert contato is None
    
    def test_buscar_por_nome_parcial(self):
        """Testa busca por nome parcial"""
        # Cria alguns contatos
        contatos = [
            Contato(nome="João Silva", telefone="111"),
            Contato(nome="João Santos", telefone="222"),
            Contato(nome="Maria Silva", telefone="333")
        ]
        
        for contato in contatos:
            self.repository.criar(contato)
        
        # Busca por "João"
        resultados = self.repository.buscar_por_nome("João")
        
        assert len(resultados) == 2
        assert all("João" in resultado.nome for resultado in resultados)
    
    def test_buscar_por_nome_case_insensitive(self):
        """Testa busca por nome insensível a maiúsculas/minúsculas"""
        contato = Contato(nome="Pedro Costa", telefone="555")
        self.repository.criar(contato)
        
        # Busca com diferentes casos
        resultados_lower = self.repository.buscar_por_nome("pedro")
        resultados_upper = self.repository.buscar_por_nome("PEDRO")
        
        assert len(resultados_lower) == 1
        assert len(resultados_upper) == 1
        assert resultados_lower[0].nome == "Pedro Costa"
    
    def test_buscar_por_categoria(self):
        """Testa busca por categoria"""
        # Cria contatos com diferentes categorias
        contatos = [
            Contato(nome="Trabalho 1", telefone="111", categoria_id=1),
            Contato(nome="Trabalho 2", telefone="222", categoria_id=1),
            Contato(nome="Família 1", telefone="333", categoria_id=2)
        ]
        
        for contato in contatos:
            self.repository.criar(contato)
        
        # Busca contatos da categoria 1
        resultados = self.repository.buscar_por_categoria(1)
        
        assert len(resultados) == 2
        assert all(contato.categoria_id == 1 for contato in resultados)
    
    def test_atualizar_contato_sucesso(self):
        """Testa atualização bem-sucedida de contato"""
        # Cria um contato
        contato = Contato(nome="Ana", telefone="123")
        contato_criado = self.repository.criar(contato)
        
        # Atualiza o contato
        contato_criado.nome = "Ana Silva"
        contato_criado.email = "ana@teste.com"
        
        sucesso = self.repository.atualizar(contato_criado)
        
        assert sucesso is True
        
        # Verifica se foi atualizado
        contato_atualizado = self.repository.buscar_por_id(contato_criado.id)
        assert contato_atualizado.nome == "Ana Silva"
        assert contato_atualizado.email == "ana@teste.com"
    
    def test_excluir_contato_sucesso(self):
        """Testa exclusão bem-sucedida de contato"""
        # Cria um contato
        contato = Contato(nome="Carlos", telefone="456")
        contato_criado = self.repository.criar(contato)
        
        # Exclui o contato
        sucesso = self.repository.excluir(contato_criado.id)
        
        assert sucesso is True
        
        # Verifica se foi excluído
        contato_excluido = self.repository.buscar_por_id(contato_criado.id)
        assert contato_excluido is None

@pytest.mark.unit
class TestCategoriaRepository:
    """Testes unitários para CategoriaRepository"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        with patch('repositories.categoria_repository.Logger.get_instance'):
            self.repository = CategoriaRepository(self.temp_dir)
    
    def test_criar_categoria_sucesso(self):
        """Testa criação bem-sucedida de categoria"""
        categoria = Categoria(nome="Trabalho", descricao="Contatos profissionais")
        
        resultado = self.repository.criar(categoria)
        
        assert resultado is not None
        assert resultado.id == 1
        assert resultado.nome == "Trabalho"
        assert resultado.descricao == "Contatos profissionais"
    
    def test_listar_todas_categorias(self):
        """Testa listagem de todas as categorias"""
        # Cria algumas categorias
        categorias = [
            Categoria(nome="Família"),
            Categoria(nome="Amigos"),
            Categoria(nome="Trabalho")
        ]
        
        for categoria in categorias:
            self.repository.criar(categoria)
        
        # Lista todas
        resultado = self.repository.listar_todas()
        
        assert len(resultado) == 3
        nomes = [cat.nome for cat in resultado]
        assert "Família" in nomes
        assert "Amigos" in nomes
        assert "Trabalho" in nomes
    
    def test_atualizar_categoria_sucesso(self):
        """Testa atualização bem-sucedida de categoria"""
        # Cria categoria
        categoria = Categoria(nome="Test", descricao="Original")
        categoria_criada = self.repository.criar(categoria)
        
        # Atualiza
        categoria_criada.nome = "Teste Atualizado"
        categoria_criada.descricao = "Descrição atualizada"
        
        sucesso = self.repository.atualizar(categoria_criada)
        
        assert sucesso is True
        
        # Verifica atualização
        categoria_atualizada = self.repository.buscar_por_id(categoria_criada.id)
        assert categoria_atualizada.nome == "Teste Atualizado"
        assert categoria_atualizada.descricao == "Descrição atualizada"
    
    def test_excluir_categoria_sucesso(self):
        """Testa exclusão bem-sucedida de categoria"""
        # Cria categoria
        categoria = Categoria(nome="Temporária")
        categoria_criada = self.repository.criar(categoria)
        
        # Exclui
        sucesso = self.repository.excluir(categoria_criada.id)
        
        assert sucesso is True
        
        # Verifica exclusão
        categoria_excluida = self.repository.buscar_por_id(categoria_criada.id)
        assert categoria_excluida is None