import pandas as pd
import re

gameTextCharacterDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextCharacter.csv"
charaPlayerDatabase = "D:\Downloads\DataBase\Character\CharaPlayer.csv"
skillNameDatabase = "D:\Downloads\DataBase\GameText\SystemText\GameTextSkill.csv"
skillIdDatabase = "D:\Downloads\DataBase\Skill\SkillID.csv"
skillAvailIdDatabase = "D:\Downloads\DataBase\Skill\SkillAvailID.csv"
skillAilmentDatabase = "D:\Downloads\DataBase\Skill\SkillAilmentType.csv"

charNameDB = pd.read_csv(gameTextCharacterDatabase)

charDataDB = pd.read_csv(charaPlayerDatabase)

skillNameDB = pd.read_csv(skillNameDatabase)

skillIdDB = pd.read_csv(skillIdDatabase)

skillAvailIdDB = pd.read_csv(skillAvailIdDatabase)

skillAilmentDB = pd.read_csv(skillAilmentDatabase)


def extractColumnArrayValues(stringValue):
    return str(stringValue).replace('[', '').replace(']', '').replace('\n', '').replace('\'', '').replace('\"',
                                                                                                          '').split(",")


class Traveller:

    def get_command_skills_exports(self):
        skills = "\n"
        for skill in self.commandSkills:
            skills = skills + skill.export() + ",\n"
        return skills[:-2]

    def get_passive_skills_exports(self):
        skills = "\n"
        for skill in self.passiveSkills:
            skills = skills + skill.export() + ",\n"
        return skills[:-2]

    def export(self):
        return "{\n\"name\" : \"" + self.name + "\"," \
                                                "\n\"job\" : \"" + self.job + "\",\n" \
                                                                              "\n\"commandSkills\" : [" + self.get_command_skills_exports() + "],\n" \
                                                                                                                                              "\n\"passiveSkills\" : [" + self.get_passive_skills_exports() + "]\n}"

    def __pickJob__(self, id):
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
    def export(self):
        return "{\n\"name\" : \"" + self.name + "\",\n" + "\"description\" : \"" + self.description + "\"\n}"

    def __init__(self, id, owner):
        self.id = id
        skillIdDF = skillIdDB.loc[id]
        nameId = skillIdDF["m_Name"]
        self.name = extractColumnArrayValues(skillNameDB.loc[[nameId], ["m_gametext"]].values[0])[0]
        desciption = skillIdDF["m_Detail"]
        self.description = self.__get_formatted_description__(
            avaiidList=[i for i in extractColumnArrayValues(skillIdDF["m_Avails"]) if int(i) != 0],
            description=extractColumnArrayValues(skillNameDB.loc[desciption]["m_gametext"])[0],
            owner=owner)

    def __find_unique_tokens__(self, input_list):
        return list(dict.fromkeys([m.group(1) for s in input_list for m in re.finditer(r'<(.*?)>', s)]))

    def __get_formatted_description__(self, description, avaiidList, owner):
        tokens = self.__find_unique_tokens__([description])
        result = description
        for token in tokens:
            result = self.__token_replacer__("<" + token + ">", result, avaiidList, owner)
        return result

    def __target_type_selector__(self, target_type):
        if target_type == -94:
            return "enemy?"
        if target_type == -91:
            return "proceeding..."
        if target_type == -60:
            return "enemy."
        if target_type == -59:
            return "twice bitten"
        if target_type == -58:
            return "magic thief"
        if target_type == -55:
            return "enemy. heart wrench, plague, precipice of fear"
        if target_type == -42:
            return "penalty turn limit exceeded kill in tower"
        if target_type == 0:
            return "linde and hagen skill type"
        if target_type == 1:
            return "single foe"
        if target_type == 2:
            return "all foes"
        if target_type == 3:
            return "random foe"
        if target_type == 5:
            return "own"
        if target_type == 6:
            return "single ally"
        if target_type == 7:
            return "entire front row"
        if target_type == 8:
            return "enemy self heal"
        if target_type == 9:
            return "Improved Offense on Enemy"
        if target_type == 10:
            return "single ally enemy"
        if target_type == 12:
            return "fallen ally"
        if target_type == 13:
            return "enemy calls for backup"
        if target_type == 14:
            return "Last enemy hit"
        if target_type == 15:
            return "entire front row again. seems to only be used for front/all like lyn switch or raise all"
        if target_type == 16:
            return "for what i must protect, aelfrics affection, light of heaven"
        if target_type == 17:
            return "when in back row, do x for front row"
        if target_type == 18:
            return "paired allies"
        if target_type == 19:
            return "enemy. darkness emits miasma"
        if target_type == 21:
            return "for what i must protect only. most likely moa assist code"
        if target_type == 22:
            return "single ally, excluding self (donate bp)"
        if target_type == 24:
            return "only used for \"encore\""
        if target_type == 25:
            return "single ally, used for reraise"
        if target_type == 52:
            return "single enemy npc?? used for shackle foe, armor corrosive, etc"
        if target_type == 54:
            return "enemy. no idea"
        if target_type == 55:
            return "only used for running slash. no clue."
        if target_type == 62:
            return "single ally. npc?"
        if target_type == 66:
            return "single ally again. also npc?"
        if target_type == 68:
            return "single ally again. also npc?"
        return "<Unknown target type: " + str(target_type) + ">"

    def __token_replacer__(self, token, description, ids, owner):
        token_map = {
            "<skl_ailment_hit_ratio>": "m_HitRatio",
            "<skl_ailment_value>": "m_ValueAilment",  # List of values
            "<skl_attribute_name>": "m_ModifyType",  # not sure if this is the correct column
            "<skl_avail_value>": "m_Values",  # List of values
            "<skl_calc_type>": "m_CalcType",
            "<skl_resist_name>": "m_CalcTypeResist",
            "<skl_modify_status>": "m_ModifyStatus",
            "<skl_hit_ratio>": "m_HitRatio",
            "<skl_effect_use_count>": "m_Counts",
            "<skl_turn_count>": "m_Turns"}  # List of values
        index = [int(s) for s in token.split() if s.isdigit()]
        cleaned_token = ''.join(i for i in token if not i.isdigit())
        if len(list(index)) == 0:
            index = 0
        else:
            index = int(index[0])

        if cleaned_token in token_map.keys():
            i = int(ids[index].strip())
            df = skillAvailIdDB.loc[i]
            column = token_map[cleaned_token]
            value = str(df[column])
            return description.replace(token, value)
        if token == "<skl_user_name>":
            return description.replace(token, owner)
        if token == "<skl_ailment_status>":
            result = ""
            for id in [i for i in extractColumnArrayValues(skillAvailIdDB.loc[int(ids[index])]["m_AddAilment"]) if
                       int(i) != 0]:
                result = result + skillAilmentDB.loc[int(id)]["m_Label"] + " "
                return description.replace(token, result)
        if token == "<skl_target_type>":
            target_type_id = skillAvailIdDB.loc[int(ids[index])]["m_TargetType"]
            target_type = self.__target_type_selector__(target_type_id)
            return description.replace(token, target_type)
        return "Unknown skill mapping for the token: " + token


def getAllTravellers():
    travellers = []
    ids = charDataDB["m_id"]
    charDataDB.set_index("m_id", inplace=True)
    charNameDB.set_index("m_id", inplace=True)
    skillIdDB.set_index("m_id", inplace=True)
    skillNameDB.set_index("m_id", inplace=True)
    skillAvailIdDB.set_index("m_id", inplace=True)
    skillAilmentDB.set_index("m_id", inplace=True)

    for id in ids:
        travellers.append(Traveller(id))
    return travellers


def exportTravellers(travellers):
    json = "["
    for traveller in travellers:
        json = json + "\n" + traveller.export() + ","
    return json[:-1] + "\n]".replace("\\", "").replace("/","")


result = getAllTravellers()
export = exportTravellers(result)
text_file = open("exported.json", "w")
text_file.write(export)
text_file.close()
print(export)
