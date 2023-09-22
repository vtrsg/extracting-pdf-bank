import json
import re
import camelot

from datetime import datetime
from pathlib import Path

file_path = "data\mp-extrato.pdf"
path_destination = ""

# extraindo as tabelas com o camelot
data_frames = camelot.read_pdf(file_path, pages="all", flavor="stream", strip_text='\n')

for table in data_frames:
    df = table.df
    print(df)