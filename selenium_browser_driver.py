from selenium import *
import subprocess
import os
from sys import platform
import time
import threading
import signal

class SeleniumServer(threading.Thread):
    out_file = None
    
    def run(self, log_file="./out.txt"):
        self.out_file = open(log_file, mode='a')
        serverJar = os.path.dirname(__file__) + "/lib/selenium-server/selenium-server.jar"
        self.current_process = subprocess.Popen("java -jar %s" %(serverJar), stdout=self.out_file, shell=True)
            
    def stop(self):
        self.out_file.close()
        if platform == 'win32': 
            import ctypes
            ctypes.windll.kernel32.TerminateProcess(int(self.current_process._handle), -1)
        else:
            os.kill(os.getpid(), signal.SIGKILL)

class SeleniumBrowserDriver(object):
    def start(self):
        self.selenium_server = SeleniumServer()
        self.selenium_server.start()
    
    def start_test(self, url = "http://www.someurl.com"):
        self.selenium = selenium("localhost", 4444, "*firefox", url)
        self.selenium.start()
        
    def open(self, url):
        self.selenium.open(url)
    
    def type(self, input_selector, text):
        self.selenium.type(input_selector, text)
        
    def click_button(self, button_selector):
        self.selenium.click(button_selector)
    
    def wait_for_page(self, timeout = 20000):
        self.selenium.wait_for_page_to_load(timeout)
    
    def get_title(self):
        return self.selenium.get_title()
    
    def stop_test(self):
        self.selenium.stop()        
    
    def stop(self):
        self.selenium_server.stop()