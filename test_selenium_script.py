import unittest
import time
import pyautogui


class sut_test_via_jenkins(unittest.TestCase):

    def setUp(self) -> None:
        pyautogui.hotkey('win','r')
        pyautogui.typewrite('notepad')
        pyautogui.press('enter')
    def test_sut(self):
        pyautogui.hotkey('alt','space','f4')
        pyautogui.typewrite('YOUR SLAVE CONFIGURATION IS SUCCESSFULLY UP AND RUNNING')
        time.sleep(5)

    def tearDown(self) -> None:
        pyautogui.hotkey('alt','f4')
