
import time
import pyautogui
from selenium import webdriver

def search_place(query) :

    global driver

    #query 입력, 추후 복수의 검색어로 지정해서 반복문으로 감쌀예정~
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
    
    # 스크롤, 페이지가 일반적인 셀레니움 스크롤 함수나 여러가지 스크롤 관련 이런거 다 안먹혀서 존나 빡쳐서 절대좌표로 억지로 내리게 함 불편한사람 알아서 바꾸셈,,
    scroll = driver.find_element_by_xpath('//*[@id="reviewSort"]')
    scroll.click()
    pyautogui.moveTo(480, 490)
    pyautogui.click()
    # 동적으로 페이지가 바껴서,,, 리뷰 긁고 싶은 만큼 미리 스크롤 내려줘야하므,,,,,,,정확한 개수처림 힘듬,, 더 좋은 방법있으면 바꿔셈,,
    # 예를 들어 어느정도 내리고 긁고 내리고 긁고 근데 이러면 중복으로 안긁는 루틴이나 중복값 안들어가는 루틴 짜야할듯?
    for i in range(size):

        pyautogui.scroll(-2000)
        time.sleep(0.5)
    time.sleep(2)
    

def review_crawl():
    global driver, user, rating, date, review

    #리뷰 크롤링
    origin_divs = driver.find_elements_by_css_selector('#reviewSort > div')
    print(len(origin_divs)) #크롤하는 리뷰 갯수확인, 만약 이 len값이 5면 리뷰 50개임

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

# 긁어야하는 핵심 데이터 웹구조 설명,,더 좋게 바꾸고 싶은사람 찾고해서 바꾸셈.. 인생 쓰다
#---------------------------------------------------------------------
# [origin_divs]
# 	div : 10개짜리 리뷰, 페이지 같은 개념
# 	div
# 	div
#   ...   >> origin_div
#---------------------------------------------------------------------
# [origin_div]
# div
# div 
# 	div : 한사람의 리뷰
# 	div
# 	div
# 	div
# 	div
# 	div
# 	div
# 	div
# 	div
# 	div  >> lv1_div
#---------------------------------------------------------------------
# [final_div]
# a
# div.jxjCjc
# 	div.TSUbDb =lv4s
# 		a >> 유저이름 잇음
# 	div.fglxyd
# 	div style
# 		div.puahbe
# 			g-review-stars
# 				span.fTKmHE99XE4__star-s >> aria-label에 rating 잇음
# 			span.dehysf >> date 있음
# 			span
# 			span
# 		div.jtu6td
# 			span, 리뷰 있음
# 		div
# div
#---------------------------------------------------------------------