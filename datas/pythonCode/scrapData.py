# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# ChromeDriver 설치 및 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 헤드리스 모드 (브라우저 창이 뜨지 않음)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 웹 드라이버 초기화
driver = webdriver.Chrome(service=service, options=options)

# 대상 웹사이트 URL
url = 'https://wooparoo-odyssey.hangame.com/probability'
driver.get(url)

# 페이지 로드 대기 (필요에 따라 조정)
time.sleep(5)

# "5" 페이지 버튼 클릭
try:
    page_5_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to page 5"]')
    page_5_button.click()
    time.sleep(2)  # 페이지 로드 대기
except NoSuchElementException:
    print("Could not find the page 5 button")
    driver.quit()
    exit()

# "다음" 버튼을 클릭하여 9페이지로 이동
for _ in range(4):
    try:
        next_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to next page"]')
        next_button.click()
        time.sleep(2)  # 페이지 로드 대기
    except NoSuchElementException:
        print("Could not find the next button")
        driver.quit()
        exit()

# 첫 번째 링크 클릭 (16번째 항목)
try:
    first_link = driver.find_element(By.XPATH, '//table//tr[15]//td[1]//button')
    first_link.click()
    time.sleep(5)  # 페이지 로드 대기
except NoSuchElementException:
    print("Could not find the first link")
    driver.quit()
    exit()

# 데이터를 저장할 리스트
all_data = []

index = 1
while True:
    try:
        # n번째 링크 클릭 (테이블의 특정 항목)
        second_link = driver.find_element(By.XPATH, f'//table//tr[{index}]//td[1]//button')
        second_link.click()
        time.sleep(12)  # 페이지 로드 대기

        # 현재 페이지의 HTML을 파싱
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
        time.sleep(2)  # 페이지 로드 대기

        index += 1

    except NoSuchElementException:
        print(f"No more elements found at index {index}. Ending loop.")
        break
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

# 웹 드라이버 종료
driver.quit()

# pandas DataFrame으로 변환
df = pd.DataFrame(all_data)

# 데이터를 수정하여 확률% 추가 및 인덱스 번호 추가
new_data = []
for i, row in df.iterrows():
    if len(row) >= 3:
        left = row[0]
        right = row[1]
        probability = row[2]

        # '확률%' 추가
        if '%' in probability:
            new_row = [i + 1, left, right, probability]  # 인덱스 번호 추가
        else:
            new_row = [i + 1, left, right, f"{probability}%"]  # 인덱스 번호 추가
        new_data.append(new_row)

# 수정된 데이터프레임 생성
new_df = pd.DataFrame(new_data, columns=['Index', 'Left', 'Right', 'Probability'])

# 수정된 데이터프레임을 CSV 파일로 저장
new_df.to_csv('outputData.csv', index=False, encoding='utf-8-sig')

print("completed")
