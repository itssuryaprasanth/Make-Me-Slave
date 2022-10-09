import time
import unittest

from appium import webdriver


class sut_test_via_jenkins(unittest.TestCase):

    def setUp(self) -> None:
        _desired_capabilities = dict(app='Notepad.exe')
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723',
                                       desired_capabilities=_desired_capabilities)
        self.driver.implicitly_wait(time_to_wait=30)

    def test_sut(self):
        self.driver.maximize_window()
        time.sleep(15)

    def tearDown(self) -> None:
        self.driver.quit()
