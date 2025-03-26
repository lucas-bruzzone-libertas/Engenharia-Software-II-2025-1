# Agenda de Contatos

Uma aplicação web para gerenciamento de contatos pessoais e profissionais, desenvolvida com Flask seguindo o padrão MVC (Model-View-Controller).

## Características

- Interface web responsiva usando Bootstrap 5
- API REST completa para integração com outras aplicações
- Gerenciamento de contatos com informações como nome, telefone, e-mail
- Categorização de contatos para melhor organização
- Busca e filtragem de contatos por nome ou categoria
- Logging de operações usando padrão Singleton
- Persistência de dados em arquivos JSON

## Estrutura do Projeto

```
agenda-contatos/
│
├── app.py                  # Aplicação Flask principal
├── config.py               # Configurações da aplicação
├── logger_singleton.py     # Logger implementando o padrão Singleton
│
├── models/                 # Camada de Dados
│   ├── __init__.py
│   ├── contato.py          # Modelo de Contato
│   └── categoria.py        # Modelo de Categoria
│
├── services/               # Camada de Negócios
│   ├── __init__.py
│   ├── contato_service.py  # Lógica de negócio para contatos
│   └── categoria_service.py # Lógica de negócio para categorias
│
├── repositories/           # Camada de Acesso a Dados
│   ├── __init__.py
│   ├── contato_repository.py # Acesso a dados de contatos
│   └── categoria_repository.py # Acesso a dados de categorias
│
├── controllers/            # Controladores Flask
│   ├── __init__.py
│   ├── contato_controller.py # Endpoints para contatos
│   └── categoria_controller.py # Endpoints para categorias
│
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   └── style.css       # Estilos CSS
│   ├── js/
│   │   └── scripts.js      # Scripts JavaScript
│   └── img/
│       └── contacts.svg    # Imagens usadas na aplicação
│
├── templates/              # Templates HTML
│   ├── base.html           # Template base
│   ├── index.html          # Página inicial
│   ├── 404.html            # Página de erro 404
│   ├── contatos/           # Templates de contatos
│   │   ├── listar.html
│   │   ├── criar.html
│   │   └── editar.html
│   └── categorias/         # Templates de categorias
│       ├── listar.html
│       ├── criar.html
│       └── editar.html
│
├── logs/                   # Logs da aplicação
│   └── application.log     # Arquivo de log principal
│
└── data/                   # Dados persistidos em JSON
    ├── contatos.json       # Dados de contatos
    └── categorias.json     # Dados de categorias
```

## Padrões de Projeto Utilizados

O projeto implementa vários padrões de design para promover organização, manutenibilidade e extensibilidade do código.

### MVC (Model-View-Controller)
Separa a aplicação em três componentes interconectados, garantindo a separação de responsabilidades:

- **Models (Modelos)**: 
  - Implementados em `models/categoria.py` e `models/contato.py`
  - Representam os dados da aplicação e suas regras de validação
  - Contêm métodos de conversão como `to_dict()` e `from_dict()`
  - Não possuem dependências com outras camadas da aplicação

- **Views (Visões)**: 
  - Implementadas como templates Jinja2 no diretório `templates/`
  - Responsáveis apenas pela apresentação dos dados ao usuário
  - Utilizam herança de templates para manter consistência visual (base.html)
  - Separadas por funcionalidade em diretórios específicos

- **Controllers (Controladores)**: 
  - Implementados como Blueprints Flask em `controllers/`
  - Gerenciam o fluxo da aplicação, processando requisições HTTP
  - Delegam operações de negócio para a camada de serviços
  - Disponibilizam endpoints tanto para API REST quanto para interface web

**Benefícios**: Manutenção simplificada, facilidade para testes, reutilização de código e desenvolvimento paralelo por diferentes membros da equipe.

### Singleton
Um padrão criacional que garante que uma classe tenha apenas uma instância e fornece um ponto global de acesso a ela.

- **Implementação**: `logger_singleton.py`
- **Características**:
  - Atributo de classe `_instance` para armazenar a única instância
  - Método `get_instance()` que cria a instância se não existir ou retorna a existente
  - Construtor (`__init__`) que impede a criação direta de novas instâncias
  - Rotação automática de arquivos de log

**Benefícios**: Economia de recursos, acesso centralizado ao log em toda a aplicação, garantia de consistência nos registros.

### Repository Pattern
Um padrão estrutural que isola a camada de domínio da lógica de acesso a dados.

- **Implementação**: `repositories/categoria_repository.py` e `repositories/contato_repository.py`
- **Características**:
  - Abstração completa da fonte de dados (atualmente arquivos JSON)
  - Métodos CRUD bem definidos (listar, buscar, criar, atualizar, excluir)
  - Gerenciamento de IDs automático
  - Tratamento de erros de persistência

**Benefícios**: Facilita mudanças na fonte de dados (ex: migrar de JSON para banco de dados SQL), simplifica testes unitários e promove o princípio de responsabilidade única.

### Service Layer
Um padrão que adiciona uma camada de serviço entre os controladores e os repositórios para encapsular regras de negócio complexas.

- **Implementação**: `services/categoria_service.py` e `services/contato_service.py`
- **Características**:
  - Implementa validações e regras de negócio
  - Orquestra operações que envolvem múltiplos repositórios
  - Mantém os controladores mais limpos e focados em seu papel
  - Registra operações importantes através do logger

**Benefícios**: Código mais testável, lógica de negócio centralizada e reutilizável, separação clara entre regras de negócio e acesso a dados.

### DTO (Data Transfer Object)
Utilizado implicitamente através dos métodos `to_dict()` e `from_dict()` nos modelos.

- **Implementação**: Métodos nas classes de modelo para converter entre objetos e dicionários
- **Características**:
  - Facilita a serialização/deserialização para JSON na API
  - Simplifica a transferência de dados entre camadas

**Benefícios**: Desacopla a representação interna dos dados da sua exposição externa, facilita a evolução da API.

### Front Controller
Implementado naturalmente pelo sistema de rotas do Flask e organizado através de Blueprints.

- **Implementação**: Registro de blueprints em `app.py`
- **Características**:
  - Centraliza o processamento de requisições
  - Organiza rotas por funcionalidade (contatos e categorias)
  - Manipula erros de forma consistente

**Benefícios**: Gerenciamento centralizado de rotas, segurança e tratamento de erros consistente.

## API REST

A aplicação oferece uma API REST completa para operações CRUD de contatos e categorias.

### Endpoints de Categorias

- `GET /categorias/api` - Lista todas as categorias
- `GET /categorias/api/<id>` - Obtém uma categoria pelo ID
- `POST /categorias/api` - Cria uma nova categoria
- `PUT /categorias/api/<id>` - Atualiza uma categoria existente
- `DELETE /categorias/api/<id>` - Exclui uma categoria

### Endpoints de Contatos

- `GET /contatos/api` - Lista todos os contatos (suporta filtros via query params)
- `GET /contatos/api/<id>` - Obtém um contato pelo ID
- `POST /contatos/api` - Cria um novo contato
- `PUT /contatos/api/<id>` - Atualiza um contato existente
- `DELETE /contatos/api/<id>` - Exclui um contato

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/agenda-contatos.git
cd agenda-contatos
```

2. Execute a aplicação:
```bash
python app.py
```

3. Acesse a aplicação em seu navegador:
```
http://localhost:5000
```

## Estrutura de Dados

### Contato
```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "(11) 98765-4321",
  "email": "joao@example.com",
  "categoria_id": 2
}
```

### Categoria
```json
{
  "id": 2,
  "nome": "Trabalho",
  "descricao": "Contatos profissionais"
}
```

## Logging

A aplicação utiliza um sistema de logging próprio implementado com o padrão Singleton. Os logs são salvos no diretório `logs/` e podem ser configurados para diferentes níveis (INFO, WARNING, ERROR).

O sistema implementa rotação automática de logs, limitando cada arquivo a 1MB e mantendo até 10 arquivos de backup.