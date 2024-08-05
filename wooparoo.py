# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# ChromeDriver ����
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # ��׶��忡�� ���� (������ â�� ����� ����)

# �� ����̹� �ʱ�ȭ
driver = webdriver.Chrome(service=service, options=options)

# �������� URL
url = 'https://wooparoo-odyssey.hangame.com/probability'
driver.get(url)

# ������ �ε� ��� (�ʿ�� ����)
time.sleep(5)

# "5" ������ ��ư�� Ŭ��
page_5_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to page 5"]')
page_5_button.click()
time.sleep(2)  # ������ �ε� ���

# "����" ��ư�� Ŭ���Ͽ� 9�� �������� �̵�
for _ in range(4):
    next_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to next page"]')
    next_button.click()
    time.sleep(2)  # ������ �ε� ���

# ù ��° ��ũ�� Ŭ�� (16��° �ε����� ��ũ)
first_link = driver.find_element(By.XPATH, '//table//tr[16]//td[1]//button')
first_link.click()
time.sleep(5)  # ������ �ε� ��� (�ʿ�� ����)

# �����͸� ������ ����Ʈ
all_data = []

index = 1
while True:
    try:
        # �� ��° ��ũ Ŭ�� (���̺��� Ư�� �ε����� ��)
        second_link = driver.find_element(By.XPATH, f'//table//tr[{index}]//td[1]//button')
        second_link.click()
        time.sleep(5)  # ������ �ε� ��� (�ʿ�� ����)

        # �� ��° �������� �����͸� ����
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cells_text = [cell.get_text(strip=True) for cell in cells]
                all_data.append(cells_text)

        # �ڷ� ����
        driver.back()
        time.sleep(5)  # ������ �ε� ��� (�ʿ�� ����)

        index += 1

    except NoSuchElementException:
        print(f"No more elements found at index {index}. Ending loop.")
        break
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

# ����̹� ����
driver.quit()

# pandas DataFrame���� ��ȯ
df = pd.DataFrame(all_data)

# �����͸� �����Ͽ� �� ��° ���� 'x ���ķ�' �߰�
new_data = []
for index, row in df.iterrows():
    left = row[0]
    right = row[1]
    probability = row[2]

    # 'x ���ķ�' �߰�
    new_row = [left, right, f"{right} {probability}"]
    new_data.append(new_row)

# ������ ������������ ����
new_df = pd.DataFrame(new_data, columns=['Left', 'Right', 'Probability'])

# ������ �������������� CSV ���Ϸ� ����
new_df.to_csv('modified_output.csv', index=False, encoding='utf-8-sig')

print("completed")
