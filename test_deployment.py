from pathlib import Path
import unittest
import os, signal
import time
import subprocess
from selenium import webdriver
import pytest
import rt


class LocalDevTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app_instance = os.system('python3 rt.py dev')
        

class DevHealthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc_comp_file = 'docker-compose.dev.yml'
        cls.app_name = 'web'
        cls.network_address = "http://0.0.0.0:1337"
        os.system(f"docker-compose -f {cls.doc_comp_file} build")
        cls.container = subprocess.Popen(f"docker-compose -f {cls.doc_comp_file} up", shell=True)
        time.sleep(9)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.container.kill()
        os.system(f"docker kill {cls.app_name}")

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_server_live(self):
        self.browser.get(self.network_address)
        self.assertIn('APAX HRS', self.browser.title, self.browser.title)


class DemoHealthTest(unittest.TestCase):
    # os.system(f"docker-compose -f {cls.docker_file_directory} down -v")
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc_comp_file = 'docker-compose.demo.yml'
        cls.app_names = ['rabbitmq','ngx','web']
        cls.network_address = 'http://0.0.0.0:80'
        os.system(f"docker-compose -f {cls.doc_comp_file} build")
        cls.container = subprocess.Popen(f"docker-compose -f {cls.doc_comp_file} up", shell=True)
        time.sleep(9)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.container.kill()
        for container in ['web']:
            try:
                os.system(f"docker kill {container}")
            finally:
                print(f"Container {container} not killed, possibly not started")


    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_server_live(self):
        self.browser.get(self.network_address)
        self.assertIn('APAX HRS', self.browser.title, self.browser.title)
        self.browser.implicitly_wait(1)



class ProdHealthTest(unittest.TestCase):
    # os.system(f"docker-compose -f {cls.docker_file_directory} down -v")
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc_comp_file = 'docker-compose.prod.yml'
        cls.app_names = ['rabbitmq','ngx','web']
        cls.network_address = 'http://0.0.0.0:80'
        os.system(f"docker-compose -f {cls.doc_comp_file} build")
        cls.container = subprocess.Popen(f"docker-compose -f {cls.doc_comp_file} up", shell=True)
        time.sleep(9)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.container.kill()
        for container in ['web']:
            try:
                os.system(f"docker kill {container}")
            finally:
                print(f"Container {container} not killed, possibly not started")


    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_server_live(self):
        self.browser.get(self.network_address)
        self.assertIn('APAX HRS', self.browser.title, self.browser.title)
        self.browser.implicitly_wait(1)

if __name__ == '__main__': #
    unittest.main(warnings='ignore') #

