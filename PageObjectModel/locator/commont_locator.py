from selenium.webdriver.common.by import By

class CommonLocator:
    @staticmethod
    def element_by_contains_text (text):
        return (By.XPATH, f"//*[contains(normalize-space(text()),{text})]")
    @staticmethod
    def element_by_text (text):
        return (By.XPATH, f"//*[text()= '{text}']")
    @staticmethod
    def button_by_type (type):
        return (By.XPATH, f"//button[@type='{type}']")
    @staticmethod
    def element_by_id (id):
        return (By.ID, f"{id}")
    @staticmethod
    def element_by_placeholder(text):
        return (By.XPATH, f"//*[@placeholder='{text}']")
    @staticmethod
    def button_by_text(text):
        return (By.XPATH, f"//button[text()='{text}']")
