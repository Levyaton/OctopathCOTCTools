# pip install pandas
import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

gameTextCharacterDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextCharacter.csv"
charaPlayerDatabase = "D:\Downloads\DataBase\Character\CharaPlayer.csv"
skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"

charNameDB = pd.read_csv(gameTextCharacterDatabase)
charDataDB = pd.read_csv(charaPlayerDatabase)

charDataDB["formattedSkills"] = charDataDB['m_InfoCommandSkills'].str.replace("[", "").replace("]", "")
skills = charDataDB["formattedSkills"].str.split(pat=',', expand=True)
for x in range(0, 9):
    charDataDB["Skill" + str(x + 1)] = skills[x]


def generateJoinSkillNameString(index):
    dbName = "sd" + str(index + 1)
    return " join skillNameDB AS " + dbName + " on " + dbName + ".m_id = cd.Skill" + str(index + 1) + " "


def generateSkillColumnsForSelect():
    result = ""
    for x in range(0, 9):
        result = result + ", sd" + str(x + 1) + ".m_gametext " + "Skill" + str(x + 1) + " "
    return result


def generateSkillNameJoins():
    result = ""
    for x in range(0, 9):
        result = result + generateJoinSkillNameString(x)
    return result


charDataDB['m_InfoCommandSkills'].str.split(pat=',', expand=True)
# print(pysqldf("SELECT  FROM charDataDB"))
skillNameDB = pd.read_csv(skillNameDatabase)
select = "SELECT charNameDB.m_gametext Name " + generateSkillColumnsForSelect() + " FROM charDataDB cd join charNameDB on cd.m_Name = charNameDB.m_id " + generateSkillNameJoins()
#skillSelect = "SELECT cd.m_id" + generateSkillColumnsForSelect() + " FROM charDataDB cd " + generateSkillDBNames() + generateSkillNameJoins()
test = "SELECT sd1.m_gametext Skill1 from charDataDB AS cd join skillNameDB AS sd1 on sd1.m_id = cd.Skill1"
print(select)
print(pysqldf(select))
