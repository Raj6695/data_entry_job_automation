from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
import random

FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSeBMHOKFWvGvxz7cJQAVqKOI3RzHPP53t48M4O967dGr4MrZA/viewform'
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122" \
              ".73144760527843%2C%22east%22%3A-122.13521039472157%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%2" \
              "2mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%2" \
              "2beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%" \
              "22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22f" \ 
              "r%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf" \
              "%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"


WEB_DRIVER_PATH = "C:\Develop\chromedriver.exe"
PROPERTY_ADDRESS = []
PROPERTY_PRICE = []
PROPERTY_LINK = []
PROPERTY_LIST = []


class Data_entry_bot:

    def __init__(self):
        self.driver = 0
        self.soup = 0
        self.response = 0

    def zillow_scrape(self):

        global PROPERTY_ADDRESS, PROPERTY_PRICE, PROPERTY_LINK, PROPERTY_LIST

        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]

        for i in range(1, 4):
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            self.response = requests.get(ZILLOW_LINK, headers=headers)
        self.soup = BeautifulSoup(self.response.text, "lxml")
        get_prize = self.soup.find_all("div", class_="list-card-price")
        PROPERTY_PRICE = [item.getText().strip("/mo + 1 bd") for item in get_prize]
        get_address = self.soup.find_all("address", class_="list-card-addr", )
        PROPERTY_ADDRESS = [item.getText() for item in get_address]
        get_link = self.soup.find_all("a", class_="list-card-link")
        PROPERTY_LINK = [item["href"] for item in get_link]
        print(PROPERTY_LINK)

        for num in range(len(PROPERTY_PRICE)):
            lizt = [
                PROPERTY_ADDRESS[num],
                PROPERTY_PRICE[num],
                PROPERTY_LINK[num]
            ]
            PROPERTY_LIST.append(lizt)

    def enter_research_data(self):
        self.driver = webdriver.Chrome(executable_path=WEB_DRIVER_PATH)
        form = self.driver.get(FORM_LINK)

        for item in PROPERTY_LIST:
            addrs = self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

            prize = self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link = self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            time.sleep(1)
            addrs.send_keys(item[0])
            prize.send_keys(item[1])
            link.send_keys(item[2])
            submit= self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
            submit.click()
            time.sleep(1)
            new_res =self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            new_res.click()
            time.sleep(1)
bot = Data_entry_bot()
bot.zillow_scrape()

