import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TestMain:
    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://artoftesting.com/samplesiteforselenium")
        driver.implicitly_wait(5)
        yield driver
        driver.close()
        driver.quit()

    def test_hyperLink(self, test_setup):
        hyperLink = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "This is a link")))
        hyperLink.click()
        time.sleep(3)
        assert driver.current_url == "https://artoftesting.com/samplesiteforselenium"

    def test_textBox(self, test_setup):
        wordToEnter = "`1234567890-=asdfghjkl;'zxcvbnm,./\\|~!@#$%^&*()_+"
        textBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fname")))
        textBox.send_keys(wordToEnter)
        assert textBox.get_attribute("value") == wordToEnter

    def test_button(self, test_setup):
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idOfButton")))
        initialColor = button.value_of_css_property("background")
        button.click()
        time.sleep(1)
        assert initialColor != button.value_of_css_property("background")

    def test_doubleClickAlertBox(self, test_setup):
        alertBoxBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dblClkBtn")))
        action = ActionChains(driver)
        action.double_click(alertBoxBtn)
        action.perform()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            assert True
        except:
            assert False
