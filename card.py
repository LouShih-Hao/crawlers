from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import requests
import pytesseract


CHROMEDRIVER = 'chromedriver.exe'
URL = 'https://ezweb.easycard.com.tw/search/CardSearch.php'

class Card:
    def __init__(self):
        service = webdriver.ChromeService(executable_path=CHROMEDRIVER)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(service = service, options=options)

    def execute(self):
        self.open_website()
        self.card_number_input()
        self.enter_card_number()
        self.birthday_input()
        self.enter_birthday()
        self.select_radio()
        # self.identify_check()
        # self.enter_identify_check()
        self.wait_for_enter_check()
        self.click_search()
        self.get_data()

    def open_website(self):
        self.driver.get(URL)

    def card_number_input(self):
        print('請輸入外觀卡號:')
        self.CARDNUMBER = input()

    def enter_card_number(self):
        cn_input = self.driver.find_element('id', 'cardIdInput')
        cn_input.send_keys(self.CARDNUMBER)

    def birthday_input(self):
        print('請輸入生日:(如7月10日請輸入0710)')
        self.BIRTHDAY = input()

    def enter_birthday(self):
        bd_input = self.driver.find_element('id', 'birthdayInput')
        bd_input.send_keys(self.BIRTHDAY)

    def select_radio(self):
        botton = self.driver.find_element('id', 'date3m')
        botton.send_keys(Keys.SPACE)

    # def identify_check(self):
    #     ic_num = self.driver.find_element('id', 'imgcode').get_attribute("src")
    #     response = requests.get(ic_num)
    #     if response.status_code == 200:
    #         image_content = BytesIO(response.content)
    #         image = Image.open(image_content)
    #         result = pytesseract.image_to_string(image)

    # def enter_identify_check(self):
    #     ic_input = self.driver.find_element('xpath', '/html/body/form/div/div[1]/div[2]/div[2]/div/ul/li[4]/input')
    #     bd_input.send_keys(self.ic_num)

    def wait_for_enter_check(self):
        input('輸入驗證碼後，請按下Enter鍵')

    def click_search(self):
        self.driver.find_element('id', 'btnSearch').click()

    def get_data(self):
        self.driver.implicitly_wait(5)
        rows = self.driver.find_elements('class name', 'r1')
        for row in rows:
            print(row.text)

if __name__ == '__main__':
    c = Card()
    c.execute()
