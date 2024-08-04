# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# ChromeDriver 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 백그라운드에서 실행 (브라우저 창을 띄우지 않음)

# 웹 드라이버 초기화
driver = webdriver.Chrome(service=service, options=options)

# 웹페이지 URL
url = 'https://wooparoo-odyssey.hangame.com/probability'
driver.get(url)

# 페이지 로드 대기 (필요시 조정)
time.sleep(5)

# "5" 페이지 버튼을 클릭
page_5_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to page 5"]')
page_5_button.click()
time.sleep(2)  # 페이지 로드 대기

# "다음" 버튼을 클릭하여 9번 페이지로 이동
for _ in range(4):
    next_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to next page"]')
    next_button.click()
    time.sleep(2)  # 페이지 로드 대기

# 첫 번째 링크를 클릭
first_link = driver.find_element(By.XPATH, '//button[contains(text(), "2024-07-31 09:00:00")]')
first_link.click()
time.sleep(5)  # 페이지 로드 대기 (필요시 조정)

# 데이터를 저장할 리스트
all_data = []

index = 1
while True:
    try:
        # 두 번째 링크 클릭 (테이블의 특정 인덱스의 셀)
        second_link = driver.find_element(By.XPATH, f'//table//tr[{index}]//td[1]//button')
        second_link.click()
        time.sleep(5)  # 페이지 로드 대기 (필요시 조정)

        # 두 번째 페이지의 데이터를 추출
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cells_text = [cell.get_text(strip=True) for cell in cells]
                all_data.append(cells_text)

        # 뒤로 가기
        driver.back()
        time.sleep(5)  # 페이지 로드 대기 (필요시 조정)

        index += 1

    except NoSuchElementException:
        print(f"No more elements found at index {index}. Ending loop.")
        break
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

# 드라이버 종료
driver.quit()

# pandas DataFrame으로 변환
df = pd.DataFrame(all_data)

# CSV 파일로 저장
df.to_csv('output.csv', index=False, encoding='utf-8-sig')

print("completed")
