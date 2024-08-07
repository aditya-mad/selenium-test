import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        assert True

    def test_radioButtons(self, test_setup):
        radioBtn1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "male")))
        radioBtn2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "female")))
        radioBtn1.click()
        assert radioBtn1.is_selected() and not radioBtn2.is_selected()
        radioBtn2.click()
        assert radioBtn2.is_selected() and not radioBtn1.is_selected()

    def test_checkBox(self, test_setup):
        btn1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Automation")))
        btn2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Performance")))
        btn1.click()
        assert btn1.is_selected() and not btn2.is_selected()
        btn2.click()
        assert btn1.is_selected() and btn2.is_selected()
        btn1.click()
        assert not btn1.is_selected() and btn2.is_selected()
        btn2.click()
        assert not btn1.is_selected() and not btn2.is_selected()

    def test_dropDown(self, test_setup):
        dropdown = Select(driver.find_element(By.ID, "testingDropdown"))
        dropdown.select_by_value("Automation")
        assert dropdown.first_selected_option.text == "Automation Testing"
        dropdown.select_by_value("Performance")
        assert dropdown.first_selected_option.text == "Performance Testing"
        dropdown.select_by_value("Manual")
        assert dropdown.first_selected_option.text == "Manual Testing"
        dropdown.select_by_value("Database")
        assert dropdown.first_selected_option.text == "Database Testing"

    def test_alertBox(self, test_setup):
        alertBoxBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@onclick="generateAlertBox()"]')))
        alertBoxBtn.click()
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        assert True

    def test_confirmBox(self, test_setup):
        confirmBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@onclick="generateConfirmBox()"]')))
        confirmBox.click()
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'demo')))
        assert 'OK' in text.text
        confirmBox.click()
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()
        text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'demo')))
        assert 'Cancel' in text.text
