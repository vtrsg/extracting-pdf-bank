import PyPDF2 as pdf
import tabula
from pathlib import Path

file_path = "C:\\Users\\Vittorio\\Documents\\Projects-2023\\Python\\extracting-pdf-bank\\data\\extrato-test-bb.pdf"

data_frame = tabula.io.read_pdf(file_path, pages="all", encoding="utf-8")
print(data_frame)

