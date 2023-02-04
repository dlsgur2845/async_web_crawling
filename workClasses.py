import worksConf
from chromeCrawling import runner


class ManagerInfo:
    def __init__(self, id, pw):
        self.id = id
        self.pw = pw


class Work:
    def __init__(self):
        self.workName = None
        self.LOG_PATH = None
        self.URL = None

    def getURL(self):
        return self.URL

    def getLogPath(self):
        return self.LOG_PATH

    def run(self, driver, managerInfo: ManagerInfo, userInfo):
        driver.get(self.URL)
        runner(self.workName)(driver, managerInfo, userInfo)

        return self.LOG_PATH


class UCMessenger(Work):
    def __init__(self):
        super().__init__()
        self.workName = worksConf.MESSENGER_NAME_ENG
        self.LOG_PATH = worksConf.MESSENGER_LOG_PATH
        self.URL = worksConf.MESSENGER_URL


class Confluence(Work):
    def __init__(self):
        super().__init__()
        self.workName = worksConf.CONFLUENCE_NAME_ENG
        self.LOG_PATH = worksConf.CONFLUENCE_LOG_PATH
        self.URL = worksConf.CONFLUENCE_URL
