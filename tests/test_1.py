
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from fitlink.models import User,TipoPlano
from django.test import Client
from django.contrib.auth.models import Group
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class TestBrowser(LiveServerTestCase):
    serv = Service("C:\\Users\\Nuno\\Documents\\UNI\\as\\fitlink\\geckodriver.exe")
    driver = webdriver.Firefox(service = serv)
    client = Client()
    
    Token = None

    def test_login(self):
        #self.token()
        User.objects.create_user(username='nuno', password='admin') #to be able login
        self.driver.get(self.live_server_url + '/login')
        
        user = self.driver.find_element(By.ID , "id_username")
        user.send_keys("nuno")

        password = self.driver.find_element(By.ID , "id_password")
        password.send_keys("admin")

        button = self.driver.find_element(By.XPATH , "//button[@type='submit']")
    
        button.click()

        try:
            element = WebDriverWait(driver , 20).until(
                lambda d: d.find_element(By.XPATH , "//img[@alt='profile_image']")
            )
        except:
            assert False , "Login provavelmente falhou"

        assert True

    def test_login(self):
        self.initUser()
        
        try:
            element = WebDriverWait(self.driver , 20).until(
                lambda d: d.find_element(By.XPATH , "//img[@alt='profile_image']")
            )
        except:
            assert False , "Login provavelmente falhou"

        assert True

    def test_planAdd(self):
        self.test_login()
        TipoPlano.objects.create(tipo="Compra única")
        self.driver.get(self.live_server_url + '/planMaker')

        tipo = Select(self.driver.find_element(By.ID , "tipoPlano"))
        tipo.select_by_visible_text("Compra única")

        preco = self.driver.find_element(By.ID , "precoPlano")
        preco.send_keys("50")

        titulo = self.driver.find_element(By.ID , "titulo")
        titulo.send_keys("Selenium test")

        descricao = self.driver.find_element(By.ID , "descricao")
        descricao.send_keys("aaa")

        requisitos = self.driver.find_element(By.ID , "requisitos")
        requisitos.send_keys("bbb")
        
        nrBlocos = self.driver.find_element(By.ID , "nrBlocos")
        nrBlocos.clear()
        nrBlocos.send_keys("1")

        duracaoBloco = self.driver.find_element(By.ID , "duracaoBloco")
        duracaoBloco.clear()
        duracaoBloco.send_keys("1")

        button = self.driver.find_element(By.ID , "nextPhase")
    
        button.click()

        wait=WebDriverWait(self.driver, 20)
        wait.until(EC.element_to_be_clickable((By.ID, "submeterEspecifico"))).click()


        try:
            element = WebDriverWait(self.driver , 20).until(
                lambda d: d.find_element(By.XPATH , "//div[@role='alert']")
            )
        except:
            assert False , "Erro criacao plano"



        assert True


    def initUser(self):
        user = User.objects.create_user(username='nuno', password='admin') #to be able login
       
        my_group, created = Group.objects.get_or_create(name='Personal Trainer') 
        my_group.user_set.add(user)

        self.driver.get(self.live_server_url + '/login')
        
        user = self.driver.find_element(By.ID , "id_username")
        user.send_keys("nuno")

        password = self.driver.find_element(By.ID , "id_password")
        password.send_keys("admin")

        button = self.driver.find_element(By.XPATH , "//button[@type='submit']")
    
        button.click()
