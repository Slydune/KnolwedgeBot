from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import json

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


class TESScrape:

    def __init__(self, driver, filename):
        self.driver = driver
        self.filename = filename
        self.college_links = ''
        self.class_links = ''
        self.class_info = ''
        self.page_list = ''

    def start_scrape(self):
        wait = WebDriverWait(self.driver, 30)
        self.grabbing_college_links()
        while True:
            first = True
            self.next_page()
            for page in self.page_list:
                if page.get_text() == "...":
                    if first:
                        first = False
                    else:
                        page_click = self.driver.find_element_by_xpath(xpath_soup(page))
                        page_click.click()
                        sleep(0.1)
                        break
                else:
                    sleep(0.1)
                    page_click = self.driver.find_element_by_xpath(xpath_soup(page))
                    for college in self.college_links:
                        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_soup(college))))
                        college_click = self.driver.find_element_by_xpath(xpath_soup(college))
                        college_click.click()
                        self.grabbing_class_links()
                        for course in self.class_links:
                            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_soup(course))))
                            course_click = self.driver.find_element_by_xpath(xpath_soup(course))
                            actions = ActionChains(self.driver)
                            actions.move_to_element(course_click).perform()
                            course_click.click()
                            sleep(3)
                            self.grabbing_class_info()
                            try:
                                school1 = self.class_info[2][0].get_text()
                            except IndexError:
                                school1 = ''

                            try:
                                course1 = self.class_info[0][0].get_text()
                            except IndexError:
                                course1 = ''

                            try:
                                desc1 = self.class_info[1][0].get_text()
                            except IndexError:
                                desc1 = ''

                            try:
                                school2 = self.class_info[2][1].get_text()
                            except IndexError:
                                school1 = ''

                            try:
                                course2 = self.class_info[0][1].get_text()
                            except IndexError:
                                course2 = ''

                            try:
                                desc2 = self.class_info[1][1].get_text()
                            except IndexError:
                                desc2 = ''
                            self.json_dump(school1, school2, course1, course2, desc1, desc2)

                            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div[6]/div/div/div/div/div[1]/button")))
                            close = self.driver.find_element_by_xpath("/html/body/div/form/div[6]/div/div/div/div/div[1]/button")
                            close.click()
                        self.driver.execute_script("window.history.go(-1)")
                    page_click = self.driver.find_element_by_xpath(xpath_soup(page))
                    page_click.click()

    def next_page(self):
        soup = bs(self.driver.page_source, 'html5lib')
        next_page = soup.find_all(lambda tag: tag.name == 'a' and tag.has_attr('href') and 'doPostBack' in tag.get('href') and 'Page' in tag.get('href'))
        self.page_list = next_page

    def grabbing_college_links(self):
        self.driver.get(
            'https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=dfbeb9e1-e048-49ca-b901-d8ba6666eb39&aid=39380d65-2ca9-4bd4-8a40-421d48832187')
        soup = bs(self.driver.page_source, 'html5lib')
        college_links = soup.find_all(
            lambda tag: tag.name == 'a' and tag.has_attr('class') and tag['class'][0] == 'gdv_boundfield_uppercase')
        self.college_links = college_links

    def grabbing_class_links(self):
        soup = bs(self.driver.page_source, 'html5lib')
        class_links = soup.find_all(
            lambda tag: tag.name == 'a' and tag.has_attr('class') and len(tag['class']) >= 2 and tag['class'][
                1] == 'btn-glyphicon-color')
        self.class_links = class_links

    def grabbing_class_info(self):
        soup = bs(self.driver.page_source, 'html5lib')
        main_window = soup.find(
            lambda tag: tag.name == 'div' and tag.has_attr('id') and tag.get('id') == 'udpViewCourseEQDetail')
        course_name = main_window.find_all(
            lambda tag: tag.name == 'td' and tag.has_attr('colspan') and tag.has_attr('style'))
        course_text = main_window.find_all(
            lambda tag: tag.name == 'td' and tag.has_attr('colspan') and not tag.has_attr('style'))
        course_school = main_window.find_all(
            lambda tag: tag.name == 'span' and tag.has_attr('id') and tag.has_attr('class') and tag['class'][
                0] == 'institution_name')
        self.class_info = [course_name, course_text, course_school]

    def json_dump(self, school1, school2, course1, course2, desc1, desc2):
        out_file = open(self.filename, "a")
        output = {
            'Equivalency Detail': {
                "School 1": school1,
                "School 1 Course": course1,
                "Course 1 Desc": desc1,
                "School 2": school2,
                "School 2 Course": course2,
                "Course 2 Desc": desc2
            }
        }
        json.dump(output, out_file, indent=6)
        out_file.close()








option = webdriver.ChromeOptions()
option.add_argument('headless')
driver_location = "C:/Users/pamjw/Desktop/chromedriver.exe"
driver = webdriver.Chrome(driver_location)
temp = TESScrape(driver, "temp")
temp.start_scrape()
# driver.get('https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=dfbeb9e1-e048-49ca-b901-d8ba6666eb39&aid=39380d65-2ca9-4bd4-8a40-421d48832187')
# soup = bs(driver.page_source, 'html5lib')
# college_links = soup.find_all(lambda tag: tag.name == 'a' and tag.has_attr('class') and tag['class'][0] == 'gdv_boundfield_uppercase')
# college = driver.find_element_by_xpath(xpath_soup(college_links[0]))
# college.click()
# soup = bs(driver.page_source, 'html5lib')
# class_links = soup.find_all(lambda tag: tag.name == 'a' and tag.has_attr('class') and len(tag['class']) >= 2 and tag['class'][1] == 'btn-glyphicon-color')
# link = driver.find_element_by_xpath(xpath_soup(class_links[0]))
# link.click()
# sleep(3)
# soup = bs(driver.page_source, 'html5lib')
# main_window = soup.find(lambda tag: tag.name == 'div' and tag.has_attr('id') and tag.get('id') == 'udpViewCourseEQDetail')
# course_name = main_window.find_all(lambda tag: tag.name == 'td' and tag.has_attr('colspan') and tag.has_attr('style'))
# # print(course_name)
# course_text = main_window.find_all(lambda tag: tag.name == 'td' and tag.has_attr('colspan') and not tag.has_attr('style'))
# # print(course_text)
# course_school = main_window.find_all(lambda tag: tag.name == 'span' and tag.has_attr('id') and tag.has_attr('class') and tag['class'][0] == 'institution_name')
# # print(course_school)