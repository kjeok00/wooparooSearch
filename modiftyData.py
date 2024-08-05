# -*- coding: utf-8 -*-
import pandas as pd

# CSV 파일 읽기 (utf-8 인코딩)
df = pd.read_csv('utf8_encoded_wooparooData.csv', header=None, encoding='utf-8')

# 새로운 데이터를 저장할 리스트
new_data = []

# 현재 "결과우파루"를 저장할 변수
current_result_wooparoo = ""

# 데이터를 순회하며 수정
for index, row in df.iterrows():
    if len(row) == 3 and "확률" in row[2]:  # "확률"이 포함된 행 확인
        current_result_wooparoo = row[2].split()[-2]  # "결과우파루" 추출
        new_data.append(row)  # 제목 행을 그대로 추가
    else:
        # 데이터를 수정하여 '결과우파루 확률%' 추가
        new_row = [row[0], row[1], f"{current_result_wooparoo} {row[2]}"]
        new_data.append(new_row)

# 수정된 데이터프레임 생성
new_df = pd.DataFrame(new_data, columns=['Left', 'Right', 'Result Probability'])

# 수정된 데이터프레임을 새로운 CSV 파일로 저장
new_df.to_csv('modified_output.csv', index=False, encoding='utf-8-sig')

print("end")
