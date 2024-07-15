from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from conf import BASE_URL, LOGIN_INFO


class BrowserCrawler:

    def __init__(self, browser='chrome', cookies=None):
        options = Options()
        options.page_load_strategy = 'eager'
        self.cookies = cookies
        if browser.lower() == 'chrome':
            self.browser = webdriver.Chrome(options=options)
        elif browser.lower() == 'firefox':
            self.browser = webdriver.Firefox()
        elif browser.lower() == 'edge':
            self.browser = webdriver.edge()
        else:
            raise Exception('browser webkit not found!!!')

    def  set_cookies(self, cookies):
        self.cookies = cookies

    def login_truecar(self):
        self.browser.get(BASE_URL)
        wait = WebDriverWait(self.browser, 10)
        login_by_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="globalNavSignUp"]')))
        login_by_email_button.click()
        wait = WebDriverWait(self.browser, 10)
        email_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div/div/div/div/div/div[2]/div/form/div/div/div[1]/div/input')))
        email_element.send_keys(LOGIN_INFO['email'])
        email_confirm = self.browser.find_element(
            By.XPATH, '//*[@id="unifiedRegistration"]/div/div/div[2]/div/form/button'
        )
        email_confirm.click()
        wait = WebDriverWait(self.browser, 10)
        password_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div/div/div/div/div/div[2]/div/form/span/div/div/div[1]/div/input')))
        password_element.send_keys(LOGIN_INFO['password'])
        password_confirm = self.browser.find_element(
            By.XPATH, '//*[@id="unifiedRegistration"]/div/div/div[2]/div/form/button[2]'
        )
        password_confirm.click()
        self.cookies = self.browser.get_cookies()


if __name__ == '__main__':
    driver = BrowserCrawler()
    driver.login_truecar()
