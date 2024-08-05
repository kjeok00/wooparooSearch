import chardet

with open('incoding_data111.csv', 'rb') as f:
    result = chardet.detect(f.read())

print(result['encoding'])
