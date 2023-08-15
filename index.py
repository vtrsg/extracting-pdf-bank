
import json
import re
from datetime import datetime
from pathlib import Path

import PyPDF2 as pdf
import tabula

file_path = "data\extrato-test-bb.pdf"
path_destination = ""

data_frames = tabula.io.read_pdf(file_path, pages="all", encoding="utf-8", multiple_tables= True, pandas_options={'header': None})

list = []
sum = 0
sum_credit = 0
sum_debt = 0

date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
valor_pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2}) [CD]')

for data_frame in data_frames:
    data_frame = data_frame.iloc[:, [0, 3, 4, 5]]
    data_frame.columns = ["data", "nome", "doc","valor"]
    
    data_list = data_frame.to_dict(orient="records")
    
    for data in data_list:       
        data['data'] = str(data['data'])  
        data['valor'] = str(data['valor'])  
        
        if data['doc'] == "70":
            list.append({'data': data['data'], 'nome': data['nome'], 'doc': data['doc'], 'valor': data['valor']})
            if data['valor'][-1] == "D":
                sum_debt -= float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))
            else:
                sum_credit += float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))
        else:
            doc_exists = any(item['doc'] == data['doc'] and item['valor'][-1] != data['valor'][-1] for item in list)
            if doc_exists:
                print(data['doc'])
            if date_pattern.findall(data['data']) and valor_pattern.match(data['valor']) and not doc_exists:
                
                list.append({'data': data['data'], 'nome': data['nome'], 'doc': data['doc'], 'valor': data['valor']})
                if data['valor'][-1] == "D":
                    sum_debt -= float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))
                else:
                    sum_credit += float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))

sum_credit = round(sum_credit, 2)
sum_debt = round(sum_debt, 2)
sum = round(sum_credit + sum_debt, 2)

def sort_data(data_list):
    return sorted(data_list, key=lambda data: datetime.strptime(data['data'], "%d/%m/%Y").timestamp())

sorted_result = sort_data(list)
sorted_result.append({'total de créditos': sum_credit, 'total de débitos': sum_debt, 'total': sum})

result_json = json.dumps(sorted_result, ensure_ascii=False, indent=4)
print(result_json)
