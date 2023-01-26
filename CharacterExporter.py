# pip install pandas
# pip install pandasql
import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

gameTextCharacterDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextCharacter.csv"
charaPlayerDatabase = "D:\Downloads\DataBase\Character\CharaPlayer.csv"
skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"
skillIdDatabase = "D:\Downloads\DataBase\Skill\SkillID.csv"
charNameDB = pd.read_csv(gameTextCharacterDatabase)
charDataDB = pd.read_csv(charaPlayerDatabase)
skillNameDB = pd.read_csv(skillNameDatabase)
skillIdDB = pd.read_csv(skillIdDatabase)
maxSkillCount = 9

charDataDB["formattedSkills"] = charDataDB['m_InfoCommandSkills'].str.replace("[", "").replace("]", "")
skills = charDataDB["formattedSkills"].str.split(pat=',', expand=True)
for x in range(0, maxSkillCount):
    charDataDB["Skill" + str(x + 1)] = skills[x]

def extractArrayFirstValue(db, columnName, extractedName):
    db[extractedName] = db[columnName].str.replace("[", "").replace("]", "").str.split(pat=',', expand=True)[0]

extractArrayFirstValue(charNameDB, "m_gametext", "Name")
extractArrayFirstValue(skillNameDB, "m_gametext", "Name")
def generateJoinSkillNameString(index):
    skillDbName = "sd" + str(index + 1)
    skillDBId = "si" + str(index + 1)
    return " join skillIdDB AS " + skillDBId + " on " + skillDBId + ".m_id = cd.Skill" + str(index + 1) + \
           " join skillNameDB AS " + skillDbName + " on " + skillDbName + ".m_id = " + skillDBId + ".m_Name "


def generateSkillColumnsForSelect():
    result = ""
    for x in range(0, maxSkillCount):
        result = result + ", sd" + str(x + 1) + ".Name " + "Skill" + str(x + 1) + " "
    return result


def generateSkillNameJoins():
    result = ""
    for x in range(0, maxSkillCount):
        result = result + generateJoinSkillNameString(x)
    return result


charDataDB['m_InfoCommandSkills'].str.split(pat=',', expand=True)
# print(pysqldf("SELECT  FROM charDataDB"))

select = "SELECT charNameDB.Name Name " + generateSkillColumnsForSelect() + " FROM charDataDB AS cd join charNameDB on cd.m_Name = charNameDB.m_id " + generateSkillNameJoins()
skillSelect = "SELECT cd.m_id" + generateSkillColumnsForSelect() + " FROM charDataDB cd " + generateSkillNameJoins()
test = "SELECT sd1.m_gametext Skill1 from charDataDB AS cd join skillNameDB AS sd1 on sd1.m_id = cd.Skill1"
print(select)
print(pysqldf(select))
pysqldf(select).to_csv("characters.csv")

