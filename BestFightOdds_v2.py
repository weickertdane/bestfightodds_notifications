from selenium import webdriver as uc
from scrapy import Selector
from selenium.webdriver.chrome import webdriver

from Utils_v2 import *
import time



class Scraper:

    def __init__(self):

        path = "/usr/lib/chromium-browser/chromedriver"
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--headless') #if you want to not show remove this if you want to show the browser
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extension')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('start-maximized')

        self.driver = uc.Chrome(path,chrome_options=chrome_options)
        self.cmp = {}

    def start(self):
        x = 0
        self.driver.get(URL)
        while True:
            self.get_data()
            x += 1
            if x > 40:
                x = 0
                self.driver.get(URL)
                time.sleep(1)
        # self.context.close()
        # self.browser.close()
        # print("Completed!")

    def get_response(self):
        while True:
            try:
                return Selector(text=self.driver.page_source)
            except:
                pass

    def get_data(self):
        time.sleep(1)
        response = self.get_response()
        for item in response.xpath(
                "//div[contains(@class, 'table-div') and .//h1[contains(text(), 'UFC')]]//table[@class='odds-table']"):
            indx = 11
            for indx, hd in enumerate(item.xpath(".//thead//th")):
                if " ".join(hd.xpath(".//text()").getall()).strip() == "Ref":
                    break
            chk = 1
            for itm in item.xpath(".//tbody/tr[not(@class)]"):
                if chk == 1:
                    chk = 0
                else:
                    chk = 1
                    continue
                name_1 = " ".join(itm.xpath(".//th//text()").getall())
                name_2 = " ".join(itm.xpath("./following::tr[not(@class)][1]//th//text()").getall()).strip()
                ref_1 = " ".join(itm.xpath(f"./td[{indx}]//text()").getall()).replace("▼", "").replace("▲", "").strip()
                ref_2 = " ".join(itm.xpath(f"./following::tr[not(@class)][1]/td[{indx}]//text()").getall()).replace("▼", "").replace("▲", "").strip()
                data_lst = [ref_1, ref_2]
                ky = f"{name_1}_{name_2}"
                if not self.cmp.get(ky):
                    self.cmp[ky] = data_lst
                else:
                    data = self.cmp.get(ky)
                    if data_lst != data[-2:]:
                        d1 = int(data_lst[-2])
                        d1_orig = int(data[-2])
                        d2 = int(data_lst[-1])
                        d2_orig = int(data[-1])
                        if d1_orig > 0:
                            p1 = get_increase(d1_orig, d1)
                        else:
                            p1 = get_decrease(d1_orig, d1)
                        if d2_orig > 0:
                            p2 = get_increase(d2_orig, d2)
                        else:
                            p2 = get_decrease(d2_orig, d2)
                        if p1 >= 1 or (p1 <= -1):
                            pass
                        elif p2 >= 1 or (p2 <= -1):
                            pass
                        else:
                            self.cmp.get(ky).append(ref_1)
                            self.cmp.get(ky).append(ref_2)
                            continue
                        fnl = {
                            "name_1": name_1,
                            "name_2": name_2,
                            "ref_1": ref_1,
                            "ref_2": ref_2,
                            "refp_1": data[-2],
                            "refp_2": data[-1]
                        }
                        print("Change Occur!")
                        print("Sending Mail..........")
                        send_email(fnl)
                        print("Email Sent!")
                        print()
                        print()
                        print()
                        self.cmp.get(ky).append(ref_1)
                        self.cmp.get(ky).append(ref_2)
                    else:
                        pass
