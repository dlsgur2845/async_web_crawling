import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import worksConf


def get_chrome_driver():
    if socket.gethostbyname(socket.gethostname()).split(".")[0] == "10":
        return webdriver.Chrome(executable_path="chromedriver")
    else:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver


def runner(case_value):
    return {
        worksConf.MESSENGER_NAME_ENG: UCMessenger_crawling_start,
        worksConf.CONFLUENCE_NAME_ENG: Confluence_crawling_start,
    }.get(case_value, 'default_result')


def UCMessenger_crawling_start(driver, managerInfo, userInfo):
    try:
        # Todo
        if "sign out" in driver.page_source:
            print("User is logged in")
        else:
            print("User is not logged in")

            username = driver.find_element_by_id("username")
            password = driver.find_element_by_id("password")
            username.send_keys(managerInfo.id)
            password.send_keys(managerInfo.pw)

        # Find the button element
        button = driver.find_element_by_id("button-id")

        # Click the button
        button.click()
    except:
        pass


def Confluence_crawling_start(driver, managerInfo, userInfo):
    try:

        # Todo
        pass
    except:
        return