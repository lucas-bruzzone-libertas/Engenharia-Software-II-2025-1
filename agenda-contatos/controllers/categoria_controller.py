from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.categoria_service import CategoriaService
from logger_singleton import Logger

categoria_bp = Blueprint('categorias', __name__, url_prefix='/categorias')
categoria_service = CategoriaService()
logger = Logger.get_instance()

# Rotas para API REST
@categoria_bp.route('/api', methods=['GET'])
def api_listar_categorias():
    """API - Lista todas as categorias"""
    categorias = categoria_service.listar_todas()
    return jsonify([cat.to_dict() for cat in categorias])

@categoria_bp.route('/api/<int:id>', methods=['GET'])
def api_obter_categoria(id):
    """API - Obtém uma categoria pelo ID"""
    categoria = categoria_service.buscar_por_id(id)
    if categoria:
        return jsonify(categoria.to_dict())
    return jsonify({'error': 'Categoria não encontrada'}), 404

@categoria_bp.route('/api', methods=['POST'])
def api_criar_categoria():
    """API - Cria uma nova categoria"""
    dados = request.json
    if not dados or 'nome' not in dados:
        return jsonify({'error': 'Nome da categoria é obrigatório'}), 400
    
    categoria = categoria_service.criar(dados['nome'], dados.get('descricao'))
    if categoria:
        return jsonify(categoria.to_dict()), 201
    return jsonify({'error': 'Falha ao criar categoria'}), 500

@categoria_bp.route('/api/<int:id>', methods=['PUT'])
def api_atualizar_categoria(id):
    """API - Atualiza uma categoria existente"""
    dados = request.json
    if not dados or 'nome' not in dados:
        return jsonify({'error': 'Nome da categoria é obrigatório'}), 400
    
    sucesso = categoria_service.atualizar(id, dados['nome'], dados.get('descricao'))
    if sucesso:
        return jsonify({'message': 'Categoria atualizada com sucesso'})
    return jsonify({'error': 'Falha ao atualizar categoria'}), 404

@categoria_bp.route('/api/<int:id>', methods=['DELETE'])
def api_excluir_categoria(id):
    """API - Exclui uma categoria"""
    sucesso = categoria_service.excluir(id)
    if sucesso:
        return jsonify({'message': 'Categoria excluída com sucesso'})
    return jsonify({'error': 'Falha ao excluir categoria'}), 404

# Rotas para interface web
@categoria_bp.route('/', methods=['GET'])
def listar_categorias():
    """Página web - Lista todas as categorias"""
    logger.info("Acessando página de listagem de categorias")
    categorias = categoria_service.listar_todas()
    return render_template('categorias/listar.html', categorias=categorias)

@categoria_bp.route('/nova', methods=['GET', 'POST'])
def criar_categoria():
    """Página web - Formulário para criar nova categoria"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        
        if not nome:
            flash('Nome da categoria é obrigatório', 'danger')
            return render_template('categorias/criar.html')
        
        categoria = categoria_service.criar(nome, descricao)
        if categoria:
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('categorias.listar_categorias'))
        
        flash('Erro ao criar categoria', 'danger')
    
    return render_template('categorias/criar.html')

@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    """Página web - Formulário para editar categoria"""
    categoria = categoria_service.buscar_por_id(id)
    if not categoria:
        flash('Categoria não encontrada', 'danger')
        return redirect(url_for('categorias.listar_categorias'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        
        if not nome:
            flash('Nome da categoria é obrigatório', 'danger')
            return render_template('categorias/editar.html', categoria=categoria)
        
        sucesso = categoria_service.atualizar(id, nome, descricao)
        if sucesso:
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('categorias.listar_categorias'))
        
        flash('Erro ao atualizar categoria', 'danger')
    
    return render_template('categorias/editar.html', categoria=categoria)

@categoria_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_categoria(id):
    """Página web - Exclui uma categoria"""
    sucesso = categoria_service.excluir(id)
    if sucesso:
        flash('Categoria excluída com sucesso!', 'success')
    else:
        flash('Erro ao excluir categoria', 'danger')
    
    return redirect(url_for('categorias.listar_categorias'))