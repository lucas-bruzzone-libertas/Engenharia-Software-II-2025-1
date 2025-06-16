// JavaScript para a Agenda de Contatos

// Função executada quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Auto-fechamento de alertas
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            // Cria um novo objeto de Bootstrap para o alerta e o fecha
            const bsAlert = new bootstrap.Alert(alert);
            setTimeout(() => bsAlert.close(), 5000); // Fecha após 5 segundos
        });
    }, 100);

    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Máscara para campos de telefone
    const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
    telefoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                // Formato: (XX) XXXXX-XXXX
                if (value.length <= 2) {
                    value = `(${value}`;
                } else if (value.length <= 7) {
                    value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
                } else if (value.length <= 11) {
                    value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7)}`;
                } else {
                    value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7, 11)}`;
                }
            }
            e.target.value = value;
        });
    });

    // Filtros de pesquisa dinâmicos - APENAS para páginas de listagem
    const nameSearchInput = document.querySelector('input[name="nome"]');
    // Verifica se estamos em uma página de listagem (URL contém apenas /contatos/ ou /categorias/)
    const isListingPage = window.location.pathname.match(/\/(contatos|categorias)\/?$/);
    
    if (nameSearchInput && isListingPage) {
        nameSearchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                e.target.form.submit();
            }
        });
    }

    // Auto-submit do filtro de categoria - APENAS para páginas de listagem
    const categorySelect = document.querySelector('select[name="categoria_id"]');
    if (categorySelect && isListingPage) {
        categorySelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
});

// Função para confirmar exclusão (alternativa ao modal Bootstrap)
function confirmarExclusao(id, nome) {
    if (confirm(`Tem certeza que deseja excluir o contato "${nome}"?`)) {
        document.getElementById(`form-excluir-${id}`).submit();
    }
}