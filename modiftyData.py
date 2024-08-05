# -*- coding: utf-8 -*-
import pandas as pd

# CSV ���� �б� (utf-8-sig ���ڵ�)
df = pd.read_csv('incoding_data111.csv', header=None, encoding='utf-8-sig')

# ���ο� �����͸� ������ ����Ʈ
new_data = []

# ���� "������ķ�"�� ������ ����
current_result_wooparoo = ""

# �����͸� ��ȸ�ϸ� ����
for index, row in df.iterrows():
    if len(row) == 3 and "Ȯ��" in row[2]:  # "Ȯ��"�� ���Ե� �� Ȯ��
        current_result_wooparoo = row[2].split()[-2]  # "������ķ�" ����
        new_data.append(row)  # ���� ���� �״�� �߰�
    else:
        # �����͸� �����Ͽ� '������ķ� Ȯ��%' �߰�
        new_row = [row[0], row[1], f"{current_result_wooparoo} {row[2]}"]
        new_data.append(new_row)

# ������ ������������ ����
new_df = pd.DataFrame(new_data, columns=['Left', 'Right', 'Result Probability'])

# ������ �������������� ���ο� CSV ���Ϸ� ����
new_df.to_csv('modified_output.csv', index=False, encoding='utf-8-sig')

print("end")
