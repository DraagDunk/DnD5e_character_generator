# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 00:40:59 2021

@author: Jesper
"""

import random
import print_char as pc
from levelup import levelup
from levelup import import_spell_lists
from levelup import choose_feat
from get_equipment import get_equipment
#import matplotlib.pyplot as plt

# Read lines of .txt file into a list


def lst_from_file(file_name):
    # Load in .txt file in read only
    file = open(file_name, "r", encoding="utf-8")
    # Convert to list, split at new lines
    lst = file.read().split("\n")
    # Return the list
    return lst

# Return indices of a list containing exactly a given object


def where(lst, obj):
    # Make empty list of indices
    indices = []
    # Iterate over length of input list
    for i in range(len(lst)):
        # Check if the object is at the current index
        if lst[i] == obj:
            # If it is, append the index to the list of indices
            indices.append(i)
    # Return the indices
    return indices

# Sort stat list by stat priority list. A stat priority list prioritizes each
# index from 0 to N, where N is the number of stats -1.


def sort_by_prio(lst, prio):
    # Make empty prioritized list
    prio_lst = []
    # Sort list from lowest to highest
    sorted_lst = sorted(lst)
    # Iterate over priorities, higher number is higher priority, lowest is 0
    for j in prio:
        # Append the j'th index of the sorted list to the prioritized list
        # j=0 will give the lowest stat, j=N will give the highest stat
        prio_lst.append(sorted_lst[j])
    # Return prioritized list
    return prio_lst

# Remove all occurences of obj from lst


def remove_all(lst, obj):
    try:
        while True:
            lst.remove(obj)
    except ValueError:
        pass
    return lst

# Remove all instances of "none" in a list. If the list only contains a "none"-
# string, return a None-object


def check_none(lst):
    # Iterate over objects in list
    for i in lst:
        # Check if the object is equal to the string "none"
        if i.lower() == "none":
            # Check if the list has more than one object
            if len(lst) > 1:
                # If it does, remove the "none" object. Return the list later
                lst.remove(i)
            else:
                # If it doesn't, return a None-object
                return None
    # The list is only returned if the None-object wasn't returned
    return lst

# Choose a number of objects from the string that do not exist in the list,
# then return the chosen objects in a list


def choose_from(string, lst):
    # Check if the first symbol in the string is a number
    if string[0] in "0123456789":
        # If it is, create an empty output list
        out_lst = []
        # Convert the found number to an integer
        num = int(string[0])
        # Split the rest of the string into a list separated by commas
        pos_lst = string[2:].split(",")
        # Iterate over objects in the input list
        for obj in lst:
            # Remove each object contained in the input list from the
            # string-split list
            try:
                pos_lst.remove(obj)
            except ValueError:
                pass
        # Choose a number of objects from the pos_lst equal to the found number
        # Append each choice to the output list, and remove them from pos_lst
        for i in range(num):
            if len(pos_lst) > 0:
                pick = random.choice(pos_lst)
                out_lst.append(pick)
                pos_lst.remove(pick)
    else:
        # If there's no number, remove "none"-strings from the string, split
        # it into a list, then define it as the output list
        out_lst = check_none(string.split(","))
    # Return the output list
    return out_lst

# Remove all instances of lst2 from lst1


def unique_list(lst1, lst2):
    new_lst = [obj.lower() for obj in lst1 if obj.lower() not in lst2]
    return new_lst

# Roll a number of dice defined by a string on the form "<mod>+<number>d<type>"


def roll_dice(string):
    split1 = string.lower().split("d")
    d_num = int(split1[0])
    split2 = split1[1].lower().split("+")
    d_type = int(split2[0])
    if len(split2) > 1:
        d_mod = int(split2[1])
    else:
        d_mod = 0
    roll = sum([random.randint(1, d_type) for i in range(d_num)]) + d_mod

    return roll

# Convert an integer in inches to a string in feet and inches


def inches_to_feet(inches):
    feet = inches//12
    rest = inches % 12
    ft_string = str(feet) + "'"
    i_string = str(rest) + "\""
    return ft_string + i_string

# Convert inches to cm


def inches_to_cm(inches):
    cm = 2.54 * inches
    return cm

# Convert punds to kg


def lbs_to_kg(lbs):
    kg = 0.4536 * lbs
    return kg

# Put all objects from a list into another list, if they are not already in it


def merge(lst1, lst2):
    if lst2 == None:
        return lst1
    else:
        for obj in lst2:
            if obj[-1] in "01233456789" or obj not in lst1:
                lst1.append(obj)
        return lst1


def check_any(lst):
    new_lst = []
    art_num = 0
    ins_num = 0
    ski_num = 0
    lan_num = 0
    gam_num = 0
    for i in range(len(lst)):
        if "Artisan" in lst[i]:
            art_num += int(lst[i][-1])
        elif "Gaming" in lst[i]:
            gam_num += int(lst[i][-1])
        elif "Instrument" in lst[i]:
            ins_num += int(lst[i][-1])
        elif "Choice" in lst[i]:
            ski_num += int(lst[i][-1])
        elif "Any" in lst[i]:
            lan_num += int(lst[i][-1])
        else:
            new_lst.append(lst[i].lower())

    if art_num > 0:
        artisan_lst = lst_from_file("artisan_tool_list.txt")
        pos_lst = unique_list(artisan_lst, new_lst)
        new_lst += random.sample(pos_lst, art_num)
    if ins_num > 0:
        instrument_lst = lst_from_file("instrument_list.txt")
        pos_lst = unique_list(instrument_lst, new_lst)
        new_lst += random.sample(pos_lst, ins_num)
    if ski_num > 0:
        skill_lst = lst_from_file("skill_list.txt")
        pos_lst = unique_list(skill_lst, new_lst)
        new_lst += random.sample(pos_lst, ski_num)
    if lan_num > 0:
        language_lst = lst_from_file("language_list.txt")
        pos_lst = unique_list(language_lst, new_lst)
        new_lst += random.sample(pos_lst, lan_num)
    if gam_num > 0:
        gaming_lst = lst_from_file("gaming_list.txt")
        pos_lst = unique_list(gaming_lst, new_lst)
        new_lst += random.sample(pos_lst, gam_num)
    return new_lst


class stats:
    def clas_sort(self, character, stat_arr):
        clas_prio_lst = lst_from_file("class_stats_priority.txt")
        if character.clas.subclas == None:
            clas_str = character.clas.clas
        else:
            clas_str = character.clas.subclas + " " + character.clas.clas
        clas_prios = []
        for i in range(len(clas_prio_lst)):
            if clas_str.lower() in clas_prio_lst[i].lower():
                clas_prios.append(clas_prio_lst[i])

        prio_roll = random.choice(clas_prios)
        str_split = prio_roll.split()
        stat_prio = [int(stat) for stat in str_split[-6:]]
        sorted_stats = sort_by_prio(stat_arr, stat_prio)

        character.clas.prio = stat_prio

        self.strength = sorted_stats[0]
        self.dexterity = sorted_stats[1]
        self.constitution = sorted_stats[2]
        self.intelligence = sorted_stats[3]
        self.wisdom = sorted_stats[4]
        self.charisma = sorted_stats[5]

    def roll_stats(self, character, rule8=False, rule70=True, droplowest=True, std_array=False):
        if std_array == True:
            stat_arr = [15, 14, 13, 12, 10, 8]
        else:
            stat_arr = []
            while len(stat_arr) < 6:
                if droplowest == True:
                    stat_roll = [random.randint(1, 6), random.randint(
                        1, 6), random.randint(1, 6), random.randint(1, 6)]
                    stat_roll = sorted(stat_roll)[1:]
                else:
                    stat_roll = [random.randint(1, 6), random.randint(
                        1, 6), random.randint(1, 6)]
                stat_roll_sum = sum(stat_roll)
                if rule8 == True:
                    if stat_roll_sum >= 8:
                        stat_arr.append(stat_roll_sum)
                    else:
                        print("Roll less than 8, rerolling...")
                else:
                    stat_arr.append(stat_roll_sum)
                if rule70 == True:
                    if len(stat_arr) == 6:
                        if sum(stat_arr) < 70:
                            print("Sum less than 70, rerolling...")
                            stat_arr = []

        self.clas_sort(character, stat_arr)

    def __init__(self, character, stats=None, rule8=False, rule70=True,
                 droplowest=True, std_array=False):

        if stats == None:
            self.strength = 10
            self.dexterity = 10
            self.constitution = 10
            self.intelligence = 10
            self.wisdom = 10
            self.charisma = 10

            self.roll_stats(character, rule8=rule8, rule70=rule70,
                            droplowest=droplowest, std_array=std_array)

        else:
            self.strength = stats[0]
            self.dexterity = stats[1]
            self.constitution = stats[2]
            self.intelligence = stats[3]
            self.wisdom = stats[4]
            self.charisma = stats[5]


class statmods:
    def __init__(self):
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0

    def update(self, character):
        mods = list(vars(self).keys())
        for mod in mods:
            new_mod = (getattr(character.stats, mod)-10)//2
            setattr(self, mod, new_mod)


class savingthrows:
    def update(self, character):
        for stat in list(vars(self).keys()):
            setattr(self, stat, getattr(character.statmods, stat) +
                    (character.prof_mod * (stat in character.clas.savingthrows)))

    def __init__(self):
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0


class skills:
    def __init__(self):
        self.acrobatics = 0
        self.animal_handling = 0
        self.arcana = 0
        self.athletics = 0
        self.deception = 0
        self.history = 0
        self.insight = 0
        self.intimidation = 0
        self.investigation = 0
        self.medicine = 0
        self.nature = 0
        self.perception = 0
        self.performance = 0
        self.persuasion = 0
        self.religion = 0
        self.sleight_of_hand = 0
        self.stealth = 0
        self.survival = 0

    def update(self, character):
        mods = list(vars(self).keys())
        str_skills = ["athletics"]
        dex_skills = ["acrobatics", "sleight_of_hand", "stealth"]
        int_skills = ["arcana", "history",
                      "investigation", "nature", "religion"]
        wis_skills = ["animal_handling", "insight",
                      "medicine", "perception", "survival"]
        cha_skills = ["deception", "intimidation", "performance", "persuasion"]
        for mod in mods:
            if mod in str_skills:
                stat = "strength"
            elif mod in dex_skills:
                stat = "dexterity"
            elif mod in int_skills:
                stat = "intelligence"
            elif mod in wis_skills:
                stat = "wisdom"
            elif mod in cha_skills:
                stat = "charisma"

            if "Jack of All Trades" in character.clas.feats:
                new_mod = getattr(character.statmods, stat) + (character.prof_mod * getattr(
                    character.skill_profs, mod)) + (character.prof_mod * (getattr(character.skill_profs, mod) == 0))//2
            elif "Remarkable Athlete" in character.clas.feats:
                new_mod = getattr(character.statmods, stat) + (character.prof_mod * getattr(character.skill_profs, mod)) + (character.prof_mod * (
                    getattr(character.skill_profs, mod) == 0) * (mod in ["athletics", "acrobatics", "sleight of hand", "stealth"]))//2
            else:
                new_mod = getattr(character.statmods, stat) + \
                    (character.prof_mod * getattr(character.skill_profs, mod))
            setattr(self, mod, new_mod)


class skill_profs:
    def __init__(self):
        self.acrobatics = 0
        self.animal_handling = 0
        self.arcana = 0
        self.athletics = 0
        self.deception = 0
        self.history = 0
        self.insight = 0
        self.intimidation = 0
        self.investigation = 0
        self.medicine = 0
        self.nature = 0
        self.perception = 0
        self.performance = 0
        self.persuasion = 0
        self.religion = 0
        self.sleight_of_hand = 0
        self.stealth = 0
        self.survival = 0

    def update(self, character):
        for skill in character.skill_prof:
            setattr(self, skill, 1)
        for skell in character.skill_expert:
            setattr(self, skell, 2)


class char_clas:
    def get_clas_base_info(self, character):
        info_lst = lst_from_file("class_base_info.txt")
        for i in range(len(info_lst)):
            info_str = remove_all(info_lst[i].split("\t"), "")
            if info_str[0].lower() == self.clas.lower():
                self.HD = int(info_str[1])
                self.armor_profs = check_none(info_str[2].split(","))
                self.weapon_profs = info_str[3].split(",")
                self.tool_profs = choose_from(info_str[4],
                                              unique_list(character.tool_prof,
                                                          ["artisan1", "artisan2", "artisan3",
                                                           "gaming1", "gaming2", "gaming3",
                                                           "instrument1", "instrument2", "instrument3"
                                                           ]))
                self.savingthrows = info_str[5].split(",")
                self.skills = choose_from(info_str[6], character.skill_prof)
                break

    def get_rand_subclas(self, character):
        clas_lst = lst_from_file("class_list.txt")
        subclasses = ""
        for i in range(len(clas_lst)):
            clas_str = clas_lst[i].split("\t")
            clas_str = remove_all(clas_str, "")
            if clas_str[0] in character.books and clas_str[1].lower() == self.clas.lower():
                if int(clas_str[2]) > character.level:
                    self.subclas = None
                    return
                else:
                    subclasses += clas_str[3] + ","
        sub_lst = subclasses[:-1].split(",")
        sub_choice = random.choice(sub_lst)
        self.subclas = sub_choice

    def get_rand_clas(self, character, clas=None):
        clas_lst = lst_from_file("class_list.txt")
        if clas == None:
            classes = []
            for i in range(len(clas_lst)):
                clas_str = clas_lst[i].split("\t")
                clas_str = remove_all(clas_str, "")
                if clas_str[0] in character.books and clas_str[1] not in classes:
                    classes.append(clas_str[1])
            self.clas = random.choice(classes)
        else:
            self.clas = clas
        self.get_rand_subclas(character)

    def __init__(self, character, clas=None, subclas=None):
        if clas == None or subclas == None:
            self.get_rand_clas(character, clas=clas)
        else:
            self.clas = clas
            self.subclas = subclas
        self.get_clas_base_info(character)
        self.core = {}
        self.feats = []
        self.prio = []

        # Add things
        character.skill_prof = merge(character.skill_prof, self.skills)
        character.armor_prof = merge(character.armor_prof, self.armor_profs)
        character.weapon_prof = merge(character.weapon_prof, self.weapon_profs)
        character.tool_prof = merge(character.tool_prof, self.tool_profs)


class char_background:
    def get_back_things(self):
        back_lst = lst_from_file("background_list.txt")
        for i in range(len(back_lst)):
            back_str = back_lst[i].split("\t")
            back_str = remove_all(back_str, "")
            if self.background.lower() in back_str[1].lower():
                self.feat = random.choice(back_str[2].split(","))
                self.skills = check_none(back_str[3].lower().split(","))
                self.languages = check_none(back_str[4].split(","))
                self.tools = check_none(back_str[5].split(","))
                break

    def get_personality(self):
        pers_lst = lst_from_file("background_info.txt")
        for i in range(len(pers_lst)):
            pers_str = pers_lst[i].split("\t")
            pers_str = remove_all(pers_str, "")
            if pers_str[0].lower() == self.background.lower():
                traits = pers_str[1].split(";")
                ideals = pers_str[2].split(";")
                bonds = pers_str[3].split(";")
                flaws = pers_str[4].split(";")
                align1 = pers_str[5].split(",")
                align2 = pers_str[6].split(",")
                extras = pers_str[7].split(";")
                break
        self.traits = random.sample(traits, 2)
        ideal_roll = random.randint(0, len(ideals)-1)
        self.ideal = ideals[ideal_roll]
        self.bond = random.choice(bonds)
        self.flaw = random.choice(flaws)
        self.align = align1[ideal_roll] + align2[ideal_roll]
        self.extra = random.choice(extras)

    def get_rand_back(self, character):
        back_lst = lst_from_file("background_list.txt")
        backs = []
        for i in range(len(back_lst)):
            back_str = back_lst[i].split("\t")
            back_str = remove_all(back_str, "")
            if back_str[0] in character.books:
                backs.append(back_str[1])
        back = random.choice(backs)
        if "," in back:
            back = random.choice(back.split(","))
        self.background = back

    def __init__(self, character, background=None):
        if background == None:
            self.get_rand_back(character)
        else:
            self.background = background
        self.get_back_things()
        self.get_personality()

        # Add skills to character list
        character.skill_prof = merge(character.skill_prof, self.skills)
        character.tool_prof = merge(character.tool_prof, self.tools)
        character.languages = merge(character.languages, self.languages)


class char_race:
    def add_race_feats(self, character):
        # Import race feats file to list
        race_feats_lst = lst_from_file("race_feats_list.txt")
        # Define the race of the character
        if self.subrace is not None:
            char_race = self.subrace + " " + self.race
        else:
            char_race = self.race
        # Find the right line of the race in the feats file
        for i in range(len(race_feats_lst)):
            if race_feats_lst[i].lower().startswith(char_race.lower()):
                race_feat_str = race_feats_lst[i]
        # Convert the feats string to a list
        race_feats = race_feat_str.split("\t")  # Separate by tabulations
        race_feats = remove_all(race_feats, "")  # Remove all empty indices
        # Extract data from feats list
        self.stat_bonus = [int(race_feats[j]) for j in [1, 2, 3, 4, 5, 6]]
        self.age_mod = float(race_feats[7])
        self.pref_alignment = race_feats[8]
        self.size = race_feats[9]
        self.height_dice = race_feats[10]
        self.weight_dice = race_feats[11]
        self.speed = int(race_feats[12])
        self.languages = race_feats[13].split(",")
        character.languages = merge(character.languages, self.languages)
        self.armor_prof = choose_from(race_feats[14], character.armor_prof)
        character.armor_prof = merge(character.armor_prof, self.armor_prof)
        self.weapon_prof = choose_from(race_feats[15], character.weapon_prof)
        character.weapon_prof = merge(character.weapon_prof, self.weapon_prof)
        self.tool_prof = choose_from(race_feats[16], character.tool_prof)
        character.tool_prof = merge(character.tool_prof, self.tool_prof)
        self.skill_prof = choose_from(race_feats[17], character.skill_prof)
        character.skill_prof = merge(character.skill_prof, self.skill_prof)
        self.feats = race_feats[18].split(",")

    def get_rand_race(self, character, race=None):
        race_lst = lst_from_file("race_list.txt")
        races = []
        subraces = []
        for i in range(len(race_lst)):
            race_str = race_lst[i].split("\t")
            if race_str[0] in character.books:
                if race_str[1] not in races:
                    races.append(race_str[1])
                    subraces.append(race_str[2])
                else:
                    subraces[where(races, race_str[1])] += "," + race_str[2]
        race_roll = random.randint(0, len(races)-1)
        if race == None:
            prim_race = races[race_roll]
        else:
            prim_race = race
        sec_races = subraces[where(races, prim_race)[0]].split(",")
        sub_roll = random.randint(0, len(sec_races)-1)
        sec_race = sec_races[sub_roll]
        if sec_race == "_":
            self.subrace = None
        else:
            self.subrace = sec_race
        self.race = prim_race

    def __init__(self, character, race=None, subrace=None):
        if race == None or subrace == None:
            self.get_rand_race(character, race=race)
        else:
            self.race = race
            self.subrace = subrace

        self.add_race_feats(character)

        # Add things
        character.languages = merge(character.languages, self.languages)
        character.armor_prof = merge(character.armor_prof, self.armor_prof)
        character.weapon_prof = merge(character.weapon_prof, self.weapon_prof)
        character.tool_prof = merge(character.tool_prof, self.tool_prof)
        character.skill_prof = merge(character.skill_prof, self.skill_prof)


class character:
    def calc_alignment(self):
        aligns1 = "LNC"
        aligns2 = "GNE"

        pref_align1 = self.race.pref_alignment[0]
        pref_align2 = self.race.pref_alignment[1]

        back_align1 = self.background.align[0]
        back_align2 = self.background.align[1]

        if back_align1 == "_":
            aligns1 += pref_align1
            align1 = random.choice(aligns1)
        else:
            align1 = back_align1

        if back_align2 == "_":
            aligns2 += pref_align2
            align2 = random.choice(aligns2)
        else:
            align2 = back_align2

        alignment = ""

        if align1 == "C":
            alignment += "Chaotic"
        elif align1 == "L":
            alignment += "Lawful"
        elif align1 == "N":
            alignment += "Neutral"
        if align2 == "G":
            alignment += " Good"
        elif align2 == "E":
            alignment += " Evil"
        elif align2 == "N" and align1 != "N":
            alignment += " Neutral"

        self.alignment = alignment

    def get_rand_name(self):
        name_lst = lst_from_file("names.txt")
        for i in range(len(name_lst)):
            name_str = remove_all(name_lst[i].split("\t"), "")
            if name_str[0] == self.race.race:
                if self.sex == "Male":
                    pos_names = name_str[1].split(",")
                elif self.sex == "Female":
                    pos_names = name_str[2].split(",")
                pos_surnames = check_none(name_str[3].split(","))
                pos_other = check_none(name_str[4].split(","))
                break

        name = ""
        first_name = random.choice(pos_names)
        name += first_name
        if pos_other != None:
            other_name = random.choice(pos_other)
            name += " '" + other_name + "'"
        if pos_surnames != None:
            surname = random.choice(pos_surnames)
            name += " " + surname

        self.name = name

    def stat_except(self):
        if "Human Ability Score" in self.race.feats:

            inc_ind = random.sample(list(range(6)), 2)
            for ind in inc_ind:
                self.race.stat_bonus[ind] += 1
        if "Half-elf Ability Score" in self.race.feats:
            inc_ind = random.sample(list(range(5)), 2)
            for ind in inc_ind:
                self.race.stat_bonus[ind] += 1

    def feat_except(self):
        if "Dwarven Toughness" in self.race.feats:
            self.extra_hp += char.level
        if "Cantrip" in self.race.feats:
            wiz_list = import_spell_lists("Wizard", self.books)
            chosen_cant = random.choice(wiz_list['0'])
            self.spells["0"] += [chosen_cant]
            self.race.feats.remove("Cantrip")
            self.race.feats += ["Cantrip: " + chosen_cant]
        if "Drow Magic" in self.race.feats:
            self.spells["0"] += ["dancing lights"]
        if "Human Feat" in self.race.feats:
            choose_feat(self)
        if "Natural Illusionist" in self.race.feats:
            self.spells["0"] += ["minor illusion"]
        if "Infernal Legacy" in self.race.feats:
            self.spells["0"] += ["thaumaturgy"]
        if "Innate Spellcasting:Yuan-ti" in self.race.feats:
            self.spells["0"] += ["poison spray"]

    def get_prof_mod(self):
        self.prof_mod = (self.level-1)//4 + 2

    def weight_height(self):
        h_split = self.race.height_dice.split("+")
        h_roll = roll_dice(h_split[1])
        height_inches = int(h_split[0]) + h_roll
        w_split = self.race.weight_dice.split("+")
        w_roll = roll_dice(w_split[1])
        weight_pounds = int(w_split[0]) + w_roll * h_roll

        self.height = inches_to_feet(height_inches)
        self.weight = weight_pounds
        self.height_cm = inches_to_cm(height_inches)
        self.weight_kg = lbs_to_kg(weight_pounds)

    def gen_age(self):
        age = random.normalvariate(
            30 * self.race.age_mod, 17 * self.race.age_mod)
        age_round = int(
            abs(round(age, 0) - 18*self.race.age_mod) + 18*self.race.age_mod)
        self.age = age_round

    def update_lists(self):
        self.tool_prof = check_any(self.tool_prof)
        self.languages = check_any(self.languages)
        self.skill_prof = check_any(self.skill_prof)

    def calc_hp(self, roll_hp=True):
        if roll_hp == True:
            hp_roll = self.clas.HD + \
                roll_dice(str(self.level-1) + "d" + str(self.clas.HD))
        else:
            hp_roll = self.clas.HD + (self.clas.HD/2 - 1) * (self.level-1)
        self.max_HP = hp_roll + \
            (self.statmods.constitution * self.level) + self.extra_hp

    def calc_speed(self):
        if "Unarmored Movement" in self.clas.core.keys():
            self.speed = self.race.speed + self.clas.core["Unarmored Movement"]
        elif "Fast Movement" in self.clas.feats:
            self.speed = self.race.speed + 10
        else:
            self.speed = self.race.speed

        if "Mobile" in char.feats:
            self.speed += 10

    def calc_ac(self):
        if self.ac_dex_cap == None:
            armor_ac = self.base_ac + self.statmods.dexterity
        elif self.ac_dex_cap == 0:
            armor_ac = self.base_ac
        else:
            if "Medium Armor Master" in char.feats:
                self.ac_dex_cap = 3
            armor_ac = self.base_ac + \
                min(self.ac_dex_cap, self.statmods.dexterity)

        if "Fighting Style" in char.clas.core.keys():
            if char.clas.core["Fighting Style"] == "Defense":
                armor_ac += 1

        pos_ac = [armor_ac]

        if "Unarmored Defense" in self.clas.core.keys():
            un_ac = 10 + sum([getattr(self.statmods, stat)
                             for stat in self.clas.core["Unarmored Defense"]])
            pos_ac += [un_ac]
        if "Draconic Resilience" in self.clas.core.keys():
            pos_ac += [self.clas.core["Draconic Resilience"]]

        if "Shield" in char.equipment:
            self.ac = max(pos_ac) + 2
        else:
            self.ac = max(pos_ac)

    def calc_initiative(self):
        if "Alert" in self.feats:
            self.initiative = self.statmods.dexterity + 5
        else:
            self.initiative = self.statmods.dexterity

    def update(self, roll_hp=True):
        self.update_lists()
        self.statmods.update(self)
        self.calc_hp(roll_hp=roll_hp)
        self.skill_profs.update(self)
        self.skills.update(self)
        self.savingthrows.update(self)
        self.calc_speed()
        self.calc_ac()
        self.calc_initiative()

    def __init__(self, name=None, level=1, books=["core"], clas=None, subclas=None,
                 race=None, subrace=None, background=None, sex=None,
                 rule8=False, rule70=True, droplowest=True, std_array=False):
        if sex == None:
            self.sex = random.choice(["Male", "Female"])
        else:
            self.sex = sex
        self.level = level
        self.books = books
        self.extra_hp = 0
        self.speed = 0
        self.base_ac = 10
        self.ac_dex_cap = None
        self.money = 0
        self.initiative = 0
        self.feats = []
        self.armor_prof = []
        self.weapon_prof = []
        self.languages = []
        self.tool_prof = []
        self.skill_prof = []
        self.skill_expert = []
        self.spells = {str(i): [] for i in range(10)}
        self.init_spells = {str(i): [] for i in range(2)}
        self.background = char_background(self, background=background)
        self.race = char_race(self, race=race, subrace=subrace)
        self.calc_alignment()
        if name == None:
            self.get_rand_name()
        else:
            self.name = name
        self.stat_except()
        self.weight_height()
        self.gen_age()
        self.clas = char_clas(self, clas=clas, subclas=subclas)
        self.get_prof_mod()
        self.skill_profs = skill_profs()
        self.skills = skills()
        self.stats = stats(self, rule8=rule8, rule70=rule70,
                           droplowest=droplowest, std_array=std_array)
        self.statlims = stats(self, stats=[20 for i in range(6)])
        self.statmods = statmods()
        self.savingthrows = savingthrows()
        self.feat_except()
        self.update_lists()
        self.equipment = []


if __name__ == "__main__":

    #ages = []
    for i in range(4):
        char = character(race="Dwarf", subrace="Mountain",
                         clas="Fighter", level=3, books=["core", "volom"])
        char.update()
        char = levelup(char)
        char = get_equipment(char)
        char.update()

    #    ages.append(char.age)
        print(char.name)
    # print(char.clas.clas)
    # print(char.race.subrace)
    # print(char.race.race)
    # print(char.background.background)
    # print(char.alignment)
    # print(char.spells)
    #print(char.clas.core["Eldritch Invocations"])
    # print(vars(char.stats))
    # print(vars(char.statmods))
    # print(vars(char.savingthrows))
    # print(char.race.stat_bonus)

        pc.print_char(char)

    # plt.close('all')
    # plt.figure()
    #plt.hist(ages, bins=list(range(1000)), edgecolor='black', align='left')
    #plt.xlim([min(ages)-0.5, max(ages)+0.5])
    # plt.xlabel("Age")
    # plt.show()
