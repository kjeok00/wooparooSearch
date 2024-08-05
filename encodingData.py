import pandas as pd
import chardet

# 원본 CSV 파일 경로와 변환된 CSV 파일 경로
original_file = 'wooparooData.csv'
utf8_file = 'utf8_encoded_wooparooData.csv'

# 원본 CSV 파일의 인코딩 감지
with open(original_file, 'rb') as f:
    result = chardet.detect(f.read())

original_encoding = result['encoding']
print(f"원본 파일의 인코딩: {original_encoding}")

# 원본 CSV 파일을 읽기 (감지된 인코딩 사용)
df = pd.read_csv(original_file, header=None, encoding=original_encoding)

# UTF-8 인코딩으로 새로운 CSV 파일로 저장
df.to_csv(utf8_file, index=False, encoding='utf-8')

print(f"파일이 {utf8_file}로 UTF-8 인코딩으로 저장되었습니다.")
