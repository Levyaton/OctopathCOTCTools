import re
import pandas as pd

skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"
skillNameDB = pd.read_csv(skillNameDatabase)


def find_unique_tokens(input_list): return list(dict.fromkeys([m.group(1) for s in input_list for m in re.finditer(r'<(.*?)>', s)]))


descriptions = []
for description in skillNameDB["m_gametext"]:
    descriptions.append(description)

tokens = find_unique_tokens(descriptions)
tokens.sort()
for token in tokens:
    print( "\""+token+"\":\"\",")

print("success!")
