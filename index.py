import json
import re
import camelot

from datetime import datetime
from pathlib import Path

file_path = "data\extrato-test-bb3.pdf"
path_destination = ""

# extraindo as tabelas com o camelot
data_frames = camelot.read_pdf(file_path, pages="all", flavor="stream", strip_text='\n')

#variáveis importantes 
sum = 0
sum_credit = 0
sum_debt = 0

# Padrões de regex 
date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
value_pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2}) [CD]')

# extraindo colunas desnecessarias e renomeando as colunas das tabelas 
def extract_columns(df):
    if len(df.columns) >= 5:
        if len(df.columns) == 5: 
            df = df.drop(columns=[2, 4])
        if len(df.columns) == 6: 
            df = df.drop(columns=[1, 3, 5])
        if len(df.columns) == 7: 
            df = df.drop(columns=[1, 2, 4, 6])
        if len(df.columns) == 8: 
            df = df.drop(columns=[1, 2, 4, 5, 7])
        
        df = df.iloc[:, [0, 1, 2]]
        df.columns = ["data", "nome", "valor"]

        return df

# convertendo tabelas em dicionário    
def convert_table(tables):
    obj_list = []

    for table in tables:
        df = table.df
        df = extract_columns(df)

        if df is not None:
            data_dict = df.to_dict(orient="records")
            obj_list.extend(data_dict)
    return obj_list

# função para remover sinal de + das datas
def remove_plus(date_str):
    return date_str.rstrip('+')

# função para ordenar o array pela data
def sort_data(data_list):
    sorted_list = sorted(data_list, key=lambda data: datetime.strptime(remove_plus(data['data']), "%d/%m/%Y").timestamp())
    return sorted_list

# lista de objetos iteráveis com os valores das tabelas para serem tratados
data_list = convert_table(data_frames)

# lista final para adicionar os elementos validos
final_list = []

# processo principal para extrair apenas os valores desejados e ja adicionar seu valor as respectivas variaveis
for data in data_list:       
    data['data'] = str(data['data'])  
    data['valor'] = str(data['valor'])  
    
    if date_pattern.findall(data['data']) and value_pattern.match(data['valor']):            
        final_list.append({'data': data['data'], 'nome': data['nome'], 'valor': data['valor']})
        if data['valor'][-1] == "D":
            sum_debt -= float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))
        else:
            sum_credit += float(data['valor'].replace('.', '').replace(',', '.').replace(' ', '').replace('C', '').replace('D', ''))

#somando valores de crédito, débito e total 
sum_credit = round(sum_credit, 2)
sum_debt = round(sum_debt, 2)
sum = round(sum_credit + sum_debt, 2)

#final_list = sort_data(final_list)
final_list.append({'total de créditos': sum_credit, 'total de débitos': sum_debt, 'total': sum})

# criando json 
result_json = json.dumps(final_list, ensure_ascii=False, indent=4)
print(result_json)