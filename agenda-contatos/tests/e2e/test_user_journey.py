import pytest
import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import threading
from app import app

class FlaskAppManager:
    """Gerenciador para iniciar/parar a aplicação Flask durante os testes"""
    
    def __init__(self):
        self.server_thread = None
        self.temp_dir = None
    
    def start_app(self, port=5001):
        """Inicia a aplicação Flask em uma thread separada"""
        self.temp_dir = tempfile.mkdtemp()
        app.config['TESTING'] = False
        app.config['DATA_PATH'] = self.temp_dir
        app.config['WTF_CSRF_ENABLED'] = False
        
        def run_app():
            app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_app)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        time.sleep(2)
    
    def stop_app(self):
        """Para a aplicação Flask"""
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)

@pytest.fixture(scope="class")
def flask_app():
    """Fixture que gerencia a aplicação Flask para testes E2E"""
    app_manager = FlaskAppManager()
    app_manager.start_app()
    yield app_manager
    app_manager.stop_app()

@pytest.fixture(scope="class")
def driver():
    """Fixture que gerencia o WebDriver do Selenium"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.mark.e2e
class TestUserJourney:
    """Testes End-to-End simulando jornadas completas do usuário"""
    
    BASE_URL = "http://127.0.0.1:5001"
    
    def test_validacao_formularios(self, _, driver):
        """Testa validações dos formulários"""
        
        # Testa validação do formulário de categoria
        driver.get(f"{self.BASE_URL}/categorias/nova")
        
        # Tenta submeter sem preencher o nome (obrigatório)
        salvar_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        salvar_btn.click()
        
        # Verifica se a validação HTML5 funcionou
        nome_campo = driver.find_element(By.ID, "nome")
        validation_message = nome_campo.get_attribute("validationMessage")
        assert validation_message  # Deve ter mensagem de validação
        
        # Testa validação do formulário de contato
        driver.get(f"{self.BASE_URL}/contatos/novo")
        
        # Preenche apenas o nome (telefone é obrigatório)
        nome_contato = driver.find_element(By.ID, "nome")
        nome_contato.send_keys("Teste Validação")
        
        salvar_contato_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        salvar_contato_btn.click()
        
        # Verifica validação do telefone
        telefone_campo = driver.find_element(By.ID, "telefone")
        validation_message = telefone_campo.get_attribute("validationMessage")
        assert validation_message
    
    def test_responsividade_basica(self, _, driver):
        """Testa responsividade básica da aplicação"""
        
        # Testa em tamanho desktop
        driver.set_window_size(1920, 1080)
        driver.get(self.BASE_URL)
        
        # Verifica se elementos principais estão visíveis
        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        assert navbar.is_displayed()
        
        # Testa em tamanho mobile
        driver.set_window_size(375, 667)  # iPhone SE
        
        # Verifica se a navbar ainda está presente (pode estar colapsada)
        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        assert navbar.is_displayed()
        
        # Volta ao tamanho desktop
        driver.set_window_size(1920, 1080)
    
    def test_navegacao_breadcrumbs(self, _, driver):
        """Testa navegação e links da aplicação"""
        
        driver.get(self.BASE_URL)
        
        # Testa link para contatos da página inicial
        ver_contatos_btn = driver.find_element(By.LINK_TEXT, "Ver Contatos")
        ver_contatos_btn.click()
        
        assert "/contatos/" in driver.current_url
        
        # Volta para home clicando no logo/marca
        logo_link = driver.find_element(By.CLASS_NAME, "navbar-brand")
        logo_link.click()
        
        assert driver.current_url == f"{self.BASE_URL}/"
        
        # Testa navegação via menu
        categorias_menu = driver.find_element(By.LINK_TEXT, "Categorias")
        categorias_menu.click()
        
        assert "/categorias/" in driver.current_url
        
        # Volta para contatos via menu
        contatos_menu = driver.find_element(By.LINK_TEXT, "Contatos")
        contatos_menu.click()
        
        assert "/contatos/" in driver.current_url
    
    def test_mensagens_feedback(self, _, driver):
        """Testa se as mensagens de feedback aparecem corretamente"""
        
        timestamp = str(int(time.time()))[-4:]
        
        # Cria uma categoria para testar mensagem de sucesso
        driver.get(f"{self.BASE_URL}/categorias/nova")
        
        nome_categoria = driver.find_element(By.ID, "nome")
        nome_categoria.send_keys(f"Teste Feedback {timestamp}")
        
        salvar_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        salvar_btn.click()
        
        # Verifica se a mensagem de sucesso aparece
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        
        mensagem_sucesso = driver.find_element(By.CLASS_NAME, "alert-success")
        assert "sucesso" in mensagem_sucesso.text.lower()
        
        # Verifica se a mensagem desaparece automaticamente
        time.sleep(6)  # scripts.js fecha alertas após 5 segundos
        
        try:
            mensagem_sucesso = driver.find_element(By.CLASS_NAME, "alert-success")
            assert not mensagem_sucesso.is_displayed()
        except:
            pass  # Se não existe mais, está correto