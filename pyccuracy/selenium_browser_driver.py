from selenium import *
from selenium_server import SeleniumServer
from selenium_element_selector import SeleniumElementSelector
import time
import os
import urllib2

class SeleniumBrowserDriver(object):
    def __init__(self, browser_to_run, tests_dir):
        self.__host = "localhost"
        self.__port = 4444
        self.__browser = browser_to_run
        self.root_dir = tests_dir

    def resolve_element_key(self, context, element_type, element_key):
        if context == None: return element_key

        return SeleniumElementSelector.element(element_type, element_key)

    def __wait_for_server_to_start(self):
        server_started = False
        while server_started == False:
            server_started = self.__is_server_started()
            time.sleep(2)

    def __is_server_started(self):
        timeout = urllib2.socket.getdefaulttimeout()
        try:
            urllib2.socket.setdefaulttimeout(5)
            url = "http://%s:%s/" % (self.__host, self.__port)
            request = urllib2.urlopen(url)
            server_started = True
            request.close()
        except IOError, e:
            server_started = False

        urllib2.socket.setdefaulttimeout(timeout)
        return server_started

    def start(self):
        #if self.__is_server_started():
            #self.selenium_server = None
            #return
        #self.selenium_server = SeleniumServer()
        #self.selenium_server.start()
        #self.__wait_for_server_to_start()
        pass

    def start_test(self, url = "http://www.someurl.com"):
        self.selenium = selenium(self.__host, self.__port, self.__browser, url)
        self.selenium.start()

    def page_open(self, url):
        self.selenium.open(url)

    def type(self, input_selector, text):
        self.selenium.type(input_selector, text)

    def click_element(self, element_selector):
        self.selenium.click(element_selector)

    def is_element_visible(self, element_selector):
        return self.selenium.is_element_present(element_selector) and self.selenium.is_visible(element_selector)

    def wait_for_page(self, timeout = 20000):
        self.selenium.wait_for_page_to_load(timeout)

    def get_title(self):
        return self.selenium.get_title()

    def is_element_enabled(self, element):
        script = """this.page().findElement("%s").disabled;"""
        
        script_return = self.selenium.get_eval(script % element)
        if script_return == "null":
            is_disabled = self.__get_attribute_value(element, "disabled")
        else:
            is_disabled = script_return[0].upper()=="T"
        return not is_disabled

    def checkbox_is_checked(self, checkbox_selector):
        return self.selenium.is_checked(checkbox_selector)

    def checkbox_check(self, checkbox_selector):
        self.selenium.check(checkbox_selector)

    def checkbox_uncheck(self, checkbox_selector):
        self.selenium.uncheck(checkbox_selector)

    def get_selected_index(self, element_selector):
        return int(self.selenium.get_selected_index(element_selector))

    def get_selected_value(self, element_selector):
        return self.selenium.get_selected_value(element_selector)

    def get_selected_text(self, element_selector):
        return self.selenium.get_selected_label(element_selector)

    def get_element_text(self, element_selector):
        text = ""
        
        text = self.__get_attribute_value(element_selector, "value")
        if not text:
            text = self.selenium.get_text(element_selector)
            if not text:
                script = """this.page().findElement("%s").value;"""
                script_return = self.selenium.get_eval(script % element_selector)
            
                if script_return != "null":
                    text = script_return

        return text

    def select_option_by_index(self, checkbox_selector, index):
        self.selenium.select(checkbox_selector, "index=%d" % index)

    def get_link_href(self, link_selector):
        return self.__get_attribute_value(link_selector, "href")

    def get_link_text(self, link_selector):
        return self.selenium.get_text(link_selector)

    def mouseover_element(self, element_selector):
        self.selenium.mouse_over(element_selector)

    def is_element_empty(self, element_selector):
        return self.get_element_text(element_selector) == ""

    def stop_test(self):
        self.selenium.stop()

    def stop(self):
        #if self.selenium_server:
            #self.selenium_server.stop()
        pass

    def __get_attribute_value(self, element, attribute):
        try:
            locator = element + "/@" + attribute
            attr_value = self.selenium.get_attribute(locator)
        except Exception, inst:
            if "Could not find element attribute" in str(inst):
                attr_value = None
            else:
                raise
        return attr_value
