import pandas as pd
import argparse

gameTextCharacterDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextCharacter.csv"
charaPlayerDatabase = "D:\Downloads\DataBase\Character\CharaPlayer.csv"
skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"
skillIdDatabase = "D:\Downloads\DataBase\Skill\SkillID.csv"
classNameDatabase = ""

charNameDB = pd.read_csv(gameTextCharacterDatabase)
charDataDB = pd.read_csv(charaPlayerDatabase)
skillNameDB = pd.read_csv(skillNameDatabase)
skillIdDB = pd.read_csv(skillIdDatabase)

numberOfCommandSkillIdSlots = 15

def getCharacterNames(baseDb):
    extractColumnArrayData(charNameDB, "m_gametext", "CharName")
    return pd.merge(charNameDB, baseDb, right_on="m_Name", left_on="m_id")



def pickJob(id):
    if id == 0:
        return "None"
    if id == 1:
        return "Warrior"
    if id == 2:
        return "Apothecary"
    if id == 3:
        return "Thief"
    if id == 4:
        return "Scholar"
    if id == 5:
        return "Cleric"
    if id == 6:
        return "Hunter"
    if id == 7:
        return "Merchant"
    return "Dancer"


def translateJobNames(baseDb):
    jobs = baseDb["m_JobID"]
    renamed = []
    for x in range(0, len(jobs)):
        renamed.append(pickJob(jobs[x]))
    baseDb["Job"] = renamed
    return baseDb


def extractColumnArrayData(table, column_name, new_column_base_name):
    results = table[column_name].replace("[", "").replace("]", "").str.split(pat=',', expand=True)
    l = len(results.columns.array)
    for x in range(0, l):
        test = results[x]
        for y in range(0, len(results[x])):
            temp = str(results[x][y]).replace("]", "").replace("[", "")
            results[x][y] = str(results[x][y]).replace("]", "").replace("[", "").replace("\'", "").replace("\"", "")
        table[new_column_base_name + str(x + 1)] = results[x]

def extractSkillType(baseDb, columnName, skillNames, skillCount):
    newNames = skillNames.copy()
    for column in newNames.head():
        newNames = newNames.rename(columns={column: (column + "_" + str(skillCount + 1))})
    colName = columnName + str(skillCount + 1)
    baseDb[colName] = baseDb[colName].astype(int)
    merged = pd.merge(baseDb, newNames, right_on="m_id_x_" + str(skillCount + 1), left_on=colName)
    # merged = baseDb.merge(names, right_on="m_id_" + str(x+1), left_on=colName)
    for y in range(0, len(merged["SkillName1_" + str(skillCount + 1)])):
        # First three ids must be skipped, due to them missing from the merge
        baseDb[colName][y + 3] = merged["SkillName1_" + str(skillCount + 1)][y] + ": (\n" + \
                                 merged["SkillName1_Description_" + str(skillCount + 1)][y] + "\n)"

def getCharacterSkills(baseDb):
    print("Merging Skill Tables")
    extractColumnArrayData(baseDb, "m_InfoCommandSkills", "Skill")
    extractColumnArrayData(baseDb, "m_InfoSupportSkills", "SupportSkill")
    extractColumnArrayData(skillNameDB, "m_gametext", "SkillName")
    SkillNames = skillIdDB.merge(skillNameDB, right_on="m_id", left_on="m_Name").merge(skillNameDB.copy(), right_on="m_id",
                                                                                   left_on="m_Detail",
                                                                              suffixes=("", "_Description"))
    print("Exporting Command Skills")
    #Command Skills
    for x in range(0, numberOfCommandSkillIdSlots):
        extractSkillType(baseDb=baseDb, columnName="Skill", skillNames=SkillNames, skillCount=x)

    print("Exporting Support Skills")
    #Support Skills
    for x in range(0,2):
        extractSkillType(baseDb=baseDb, columnName="SupportSkill", skillNames=SkillNames, skillCount=x)
    return baseDb




def exportTable():
    custom = charDataDB
    print("Exporting Character Names")
    custom = getCharacterNames(custom)
    print("Exporting Character Jobs")
    custom = translateJobNames(custom)
    print("Exporting Character Skills")
    custom = getCharacterSkills(custom)
    return custom[["m_id_x", "CharName1", "Job", "Skill1", "Skill2", "Skill3","Skill4", "Skill5","Skill6", "Skill7", "Skill8","Skill9", "SupportSkill1", "SupportSkill2"]]


# result = exportTable()
# extractColumnArrayData(table=result, column_name="m_InfoCommandSkills", new_column_base_name="Skill")
# for x in range(0, numberOfCommandSkillIdSlots):
#     skillIdDB["m_id"] = skillIdDB["m_id"].astype(str)
#     column = result["Skill" + str(x+1)]
#     result = pd.merge(skillIdDB, result, right_on="Skill" + str(x+1), left_on="m_id", suffixes=('', 'Skill' + str(x+1)))

result = exportTable()
result.to_csv("result.csv")

