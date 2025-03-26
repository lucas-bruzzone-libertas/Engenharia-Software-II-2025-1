from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.contato_service import ContatoService
from services.categoria_service import CategoriaService
from logger_singleton import Logger

contato_bp = Blueprint('contatos', __name__, url_prefix='/contatos')
contato_service = ContatoService()
categoria_service = CategoriaService()
logger = Logger.get_instance()

# Rotas para API REST
@contato_bp.route('/api', methods=['GET'])
def api_listar_contatos():
    """API - Lista todos os contatos"""
    # Verifica se há filtro por nome ou categoria
    nome = request.args.get('nome')
    categoria_id = request.args.get('categoria_id')
    
    if nome:
        contatos = contato_service.buscar_por_nome(nome)
    elif categoria_id:
        try:
            contatos = contato_service.buscar_por_categoria(int(categoria_id))
        except ValueError:
            return jsonify({'error': 'ID de categoria inválido'}), 400
    else:
        contatos = contato_service.listar_todos()
    
    return jsonify([contato.to_dict() for contato in contatos])

@contato_bp.route('/api/<int:id>', methods=['GET'])
def api_obter_contato(id):
    """API - Obtém um contato pelo ID"""
    contato = contato_service.buscar_por_id(id)
    if contato:
        return jsonify(contato.to_dict())
    return jsonify({'error': 'Contato não encontrado'}), 404

@contato_bp.route('/api', methods=['POST'])
def api_criar_contato():
    """API - Cria um novo contato"""
    dados = request.json
    if not dados or 'nome' not in dados or 'telefone' not in dados:
        return jsonify({'error': 'Nome e telefone são obrigatórios'}), 400
    
    categoria_id = dados.get('categoria_id')
    if categoria_id is not None:
        try:
            categoria_id = int(categoria_id)
        except ValueError:
            return jsonify({'error': 'ID de categoria inválido'}), 400
    
    contato = contato_service.criar(
        dados['nome'],
        dados['telefone'],
        dados.get('email'),
        categoria_id
    )
    
    if contato:
        return jsonify(contato.to_dict()), 201
    return jsonify({'error': 'Falha ao criar contato'}), 500

@contato_bp.route('/api/<int:id>', methods=['PUT'])
def api_atualizar_contato(id):
    """API - Atualiza um contato existente"""
    dados = request.json
    if not dados or 'nome' not in dados or 'telefone' not in dados:
        return jsonify({'error': 'Nome e telefone são obrigatórios'}), 400
    
    categoria_id = dados.get('categoria_id')
    if categoria_id is not None:
        try:
            categoria_id = int(categoria_id)
        except ValueError:
            return jsonify({'error': 'ID de categoria inválido'}), 400
    
    sucesso = contato_service.atualizar(
        id,
        dados['nome'],
        dados['telefone'],
        dados.get('email'),
        categoria_id
    )
    
    if sucesso:
        return jsonify({'message': 'Contato atualizado com sucesso'})
    return jsonify({'error': 'Falha ao atualizar contato'}), 404

@contato_bp.route('/api/<int:id>', methods=['DELETE'])
def api_excluir_contato(id):
    """API - Exclui um contato"""
    sucesso = contato_service.excluir(id)
    if sucesso:
        return jsonify({'message': 'Contato excluído com sucesso'})
    return jsonify({'error': 'Falha ao excluir contato'}), 404

# Rotas para interface web
@contato_bp.route('/', methods=['GET'])
def listar_contatos():
    """Página web - Lista todos os contatos"""
    logger.info("Acessando página de listagem de contatos")
    
    # Verifica se há filtro por nome ou categoria
    nome = request.args.get('nome')
    categoria_id = request.args.get('categoria_id')
    
    if nome:
        contatos = contato_service.buscar_por_nome(nome)
        titulo = f'Resultados para "{nome}"'
    elif categoria_id:
        try:
            categoria_id = int(categoria_id)
            contatos = contato_service.buscar_por_categoria(categoria_id)
            categoria = categoria_service.buscar_por_id(categoria_id)
            titulo = f'Contatos na categoria: {categoria.nome if categoria else "Desconhecida"}'
        except ValueError:
            contatos = []
            titulo = 'Contatos (filtro inválido)'
    else:
        contatos = contato_service.listar_todos()
        titulo = 'Todos os Contatos'
    
    categorias = categoria_service.listar_todas()
    return render_template('contatos/listar.html', 
                          contatos=contatos, 
                          categorias=categorias,
                          titulo=titulo,
                          nome_busca=nome,
                          categoria_id_busca=categoria_id)

@contato_bp.route('/novo', methods=['GET', 'POST'])
def criar_contato():
    """Página web - Formulário para criar novo contato"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        categoria_id = request.form.get('categoria_id')
        
        if not nome or not telefone:
            flash('Nome e telefone são obrigatórios', 'danger')
            categorias = categoria_service.listar_todas()
            return render_template('contatos/criar.html', categorias=categorias)
        
        # Converte categoria_id para int ou None
        if categoria_id:
            try:
                categoria_id = int(categoria_id)
            except ValueError:
                categoria_id = None
        
        contato = contato_service.criar(nome, telefone, email, categoria_id)
        if contato:
            flash('Contato criado com sucesso!', 'success')
            return redirect(url_for('contatos.listar_contatos'))
        
        flash('Erro ao criar contato', 'danger')
    
    categorias = categoria_service.listar_todas()
    return render_template('contatos/criar.html', categorias=categorias)

@contato_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):
    """Página web - Formulário para editar contato"""
    contato = contato_service.buscar_por_id(id)
    if not contato:
        flash('Contato não encontrado', 'danger')
        return redirect(url_for('contatos.listar_contatos'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        categoria_id = request.form.get('categoria_id')
        
        if not nome or not telefone:
            flash('Nome e telefone são obrigatórios', 'danger')
            categorias = categoria_service.listar_todas()
            return render_template('contatos/editar.html', contato=contato, categorias=categorias)
        
        # Converte categoria_id para int ou None
        if categoria_id:
            try:
                categoria_id = int(categoria_id)
            except ValueError:
                categoria_id = None
        
        sucesso = contato_service.atualizar(id, nome, telefone, email, categoria_id)
        if sucesso:
            flash('Contato atualizado com sucesso!', 'success')
            return redirect(url_for('contatos.listar_contatos'))
        
        flash('Erro ao atualizar contato', 'danger')
    
    categorias = categoria_service.listar_todas()
    return render_template('contatos/editar.html', contato=contato, categorias=categorias)

@contato_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_contato(id):
    """Página web - Exclui um contato"""
    sucesso = contato_service.excluir(id)
    if sucesso:
        flash('Contato excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir contato', 'danger')
    
    return redirect(url_for('contatos.listar_contatos'))