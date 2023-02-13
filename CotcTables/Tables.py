import pandas as pd
import argparse

gameTextCharacterDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextCharacter.csv"
charaPlayerDatabase = "D:\Downloads\DataBase\Character\CharaPlayer.csv"
skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"
skillIdDatabase = "D:\Downloads\DataBase\Skill\SkillID.csv"
skillAvailIdDatabase = "D:\Downloads\DataBase\Skill\SkillAvailID.csv"

charNameDB = pd.read_csv(gameTextCharacterDatabase)

charDataDB = pd.read_csv(charaPlayerDatabase)

skillNameDB = pd.read_csv(skillNameDatabase)

skillIdDB = pd.read_csv(skillIdDatabase)

skillAvailIdDB = pd.read_csv(skillAvailIdDatabase)

def extractColumnArrayValues(stringValue):
    return str(stringValue).replace('[','').replace(']','').replace('\n', '').replace('\'','').replace('\"','').split(",")

class Traveller:
    def __pickJob__(self,id):
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

    def __getSkills__(self, charIdDF, columnName):
        skills = []
        skillIds = charIdDF[columnName]
        for id in extractColumnArrayValues(skillIds):
            if int(id) != 0:
                skills.append(Skill(int(id), self.name))
        return skills

    def __init__(self, id):
        self.id = id
        charIdDF = charDataDB.loc[id]
        nameId = charIdDF["m_Name"]
        self.name = extractColumnArrayValues(charNameDB.loc[[nameId], ["m_gametext"]].values[0])[0]
        self.commandSkills = self.__getSkills__(charIdDF, "m_InfoCommandSkills")
        self.passiveSkills = self.__getSkills__(charIdDF, "m_InfoSupportSkills")
        self.job = self.__pickJob__(charIdDF["m_JobID"])


class Skill:
    def __get_formatted_description__(self, skillIdDF, template, owner):
        return template.replace("")

    def __init__(self, id, owner):
        self.id = id
        skillIdDF = skillIdDB.loc[id]
        nameId = skillIdDF["m_Name"]
        self.name = extractColumnArrayValues(skillNameDB.loc[[nameId], ["m_gametext"]].values[0])[0]
        desciption = skillIdDF[["m_Detail"]]
        self.description = self.__get_formatted_description__(skillIdDF=skillIdDF,
                                                              template=extractColumnArrayValues(skillNameDB.loc[[desciption], ["m_gametext"]].values[0])[0],
                                                              owner=owner)

# result = exportTable()
# extractColumnArrayData(table=result, column_name="m_InfoCommandSkills", new_column_base_name="Skill")
# for x in range(0, numberOfCommandSkillIdSlots):
#     skillIdDB["m_id"] = skillIdDB["m_id"].astype(str)
#     column = result["Skill" + str(x+1)]
#     result = pd.merge(skillIdDB, result, right_on="Skill" + str(x+1), left_on="m_id", suffixes=('', 'Skill' + str(x+1)))
def getAllTravellers():
    travellers = []
    ids = charDataDB["m_id"]
    charDataDB.set_index("m_id", inplace=True)
    charNameDB.set_index("m_id", inplace=True)
    skillIdDB.set_index("m_id", inplace=True)
    skillNameDB.set_index("m_id", inplace=True)
    skillAvailIdDB.set_index("m_id", inplace=True)
    for id in ids:
        travellers.append(Traveller(id))
    return travellers
result = getAllTravellers()
print("win")

