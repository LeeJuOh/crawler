
import time
import pyautogui
from selenium import webdriver

def search_place(query) :

    global driver

    
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(2)
    
    #리뷰 클릭
    place = driver.find_element_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/span[2]/span/a')
    place.click()
    time.sleep(5)

    #리뷰 옵션 - 현재는 최신순, 텍스트 학습데이터 긁을때는 관련성순 ㄱㄱ
    review_option = driver.find_element_by_class_name('dkSGpd.NkCsjc')
    review_option.click()
    time.sleep(2)
    #relevancy = driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[1]')
    #relevancy.click()
    recency = driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[2]')
    recency.click()
    time.sleep(2)
    
def define_crawl_size(size):
    
    global driver
    
  
    scroll = driver.find_element_by_xpath('//*[@id="reviewSort"]')
    scroll.click()
    pyautogui.moveTo(480, 490)
    pyautogui.click()
  
    for i in range(size):

        pyautogui.scroll(-2000)
        time.sleep(0.5)
    time.sleep(2)
    

def review_crawl():
    global driver, user, rating, date, review

    #리뷰 크롤링
    origin_divs = driver.find_elements_by_css_selector('#reviewSort > div')
    print(len(origin_divs)) #크롤하는 리뷰 갯수확인, 만약 이 len값이 5면, 리뷰 50개

    cnt=1
    for origin_div in origin_divs:

        final_divs = origin_div.find_elements_by_css_selector('div.gws-localreviews__general-reviews-block > div')
        for final_div in final_divs:

            id_div = final_divs.find_element_by_class_name('TSUbDb')
            user.append(id_div.text)
            print(id_div.text)

            rating_span = final_divs.find_element_by_class_name('fTKmHE99XE4__star-s').get_attribute('aria-label')
            rating.append(rating_span)
            print(rating_span[7:10])

            date_span = final_divs.find_element_by_class_name('dehysf').text
            date.append(date_span)
            print(date_span)

            review_div = final_divs.find_element_by_class_name('Jtu6Td')
            review_span = review_div.find_element_by_tag_name('span').text
            review.append(review_span)
            print(review_span)
            print('-----------------------------------------', cnt, '--------------------------------------------------')
            cnt+=1

if __name__ == "__main__":

    global driver, user, rating, date, review

    user = list()
    rating = list()
    date = list()
    review = list()

    #driver load
    driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    driver.get('http://www.gogle.com/')
    time.sleep(2)
    
    search_place('제주도 용두암')
    define_crawl_size(20)
    review_crawl()

