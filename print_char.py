# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:43:57 2021

@author: Jesper
"""

def write_separator(file,symbol,width):
    string = ""
    for i in range(width):
        string += symbol
    string += "\n"
    file.write(string)
    
def text_separator(file,text,symbol,width):
    string = ""
    left = (width-len(text))//2
    right= int(round((width-len(text))/2,0))
    for i in range(left):
        string += symbol
    string += text
    for j in range(right):
        string += symbol
    string += "\n"
    file.write(string)
    
def fill_spaces(file,string,space):
    rem_space = space-len(string)
    if rem_space < 0:
        rem_space = 0
    space_string = ""
    for i in range(rem_space):
        space_string += " "
    file.write(space_string)
    
def write_string(file,string,space):
    file.write(string)
    fill_spaces(file,string,space)
    
def where(string, ch):
    ind = []
    for i in range(len(string)):
        if string[i] == ch:
            ind.append(i)
    return ind

def remove_greater(lst, val):
    return [n for n in lst if n <= val]
    
def text_wrap(string, width):
    wraps = [-1]
    lst = []
    running = True
    i = 0
    ind = where(string, " ")
    while running:
        prelen = sum([len(s) for s in lst])
        if len(string) - prelen < width:
            lst.append(string[wraps[i]+1:])
            running = False
        else:
            wrap_ind = max(remove_greater(ind, prelen + width))
            wraps.append(wrap_ind)
            lst.append(string[wraps[i]+1:wraps[i+1]])
            i += 1
    return lst

def capwords(s):
    return " ".join(w.capitalize() for w in s.split())
        

def print_char(char):
    width = 101
    
    file_name = char.name.replace(" ", "_")
    f = open("characters/" + file_name + ".txt", "w")
    
    
    write_separator(f,"/",width)
    
    # GENERAL INFO line 1
    write_string(f,"|| " + char.name,33)
    if char.race.subrace != None:
        write_string(f,"| " + char.sex + " " + char.race.subrace + " " + char.race.race,33)
    else:
        write_string(f,"| " + char.sex + " " + char.race.race,33)
    if char.clas.subclas != None:
        write_string(f,char.clas.subclas + " " + char.clas.clas + " " + str(char.level), 33)
    else:
        write_string(f,char.clas.clas, 33)
    f.write("||\n")
    
    # GENERAL INFO line 2
    write_string(f,"||",33)
    write_string(f,"| " + char.background.background,33)
    write_string(f,char.alignment,33)
    f.write("||\n")
    
    text_separator(f,"ATTRIBUTES","\\", width)
    
    # ATTRIBUTES
    write_string(f,"|| STR: " + str(char.stats.strength) + " (" + str(char.statmods.strength) + ")",19)
    write_string(f,"DEX: " + str(char.stats.dexterity) + " (" + str(char.statmods.dexterity) + ")",16)
    write_string(f,"CON: " + str(char.stats.constitution) + " (" + str(char.statmods.constitution) + ")",16)
    write_string(f,"INT: " + str(char.stats.intelligence) + " (" + str(char.statmods.intelligence) + ")",16)
    write_string(f,"WIS: " + str(char.stats.wisdom) + " (" + str(char.statmods.wisdom) + ")",16)
    write_string(f,"CHA: " + str(char.stats.charisma) + " (" + str(char.statmods.charisma) + ")",16)
    f.write("||\n")
    
    # OTHER THINGS
    write_string(f, "|| Proficiency: " + str(char.prof_mod),20)
    write_string(f, "AC: " + str(char.ac), 20)
    write_string(f, "HP: " + str(char.max_HP), 20)
    write_string(f, "Speed: " + str(char.speed), 20)
    write_string(f, "Initiative: " + str(char.initiative),19)
    f.write("||\n")
    
    text_separator(f,"SAVING THROWS","/", width)
    
    # SAVING THROWS
    write_string(f,"|| STR: " + str(char.savingthrows.strength),19)
    write_string(f,"DEX: " + str(char.savingthrows.dexterity),16)
    write_string(f,"CON: " + str(char.savingthrows.constitution),16)
    write_string(f,"INT: " + str(char.savingthrows.intelligence),16)
    write_string(f,"WIS: " + str(char.savingthrows.wisdom),16)
    write_string(f,"CHA: " + str(char.savingthrows.charisma),16)
    f.write("||\n")
    
    text_separator(f,"SKILLS","\\",width)
    
    # SKILLS
    skill_keys = list(vars(char.skills).keys())
    skill_vals = list(vars(char.skills).values())
    for i in range(len(skill_keys)):
        if i%3 == 0:
            f.write("|| ")
        write_string(f,capwords(skill_keys[i].replace("_", " ")) + ": " + str(skill_vals[i]),32)
        if (i+1)%3 == 0:
            f.write("||\n")
            
    text_separator(f,"FEATURES","/",width)

    # FEATS
    # Feats
    if len(char.feats) > 0:
        write_string(f, "|| Feats:", 99)
        f.write("||\n")
        for feat in char.feats:
            write_string(f, "||  " + feat,99)
            f.write("||\n")
    # Background
    write_string(f,"|| Background feat: ", 99)
    f.write("||\n")
    write_string(f,"||  " + char.background.feat, 99)
    f.write("||\n")
    # Race
    write_string(f,"|| Race feats: ", 99)
    f.write("||\n")
    for feat in char.race.feats:
        write_string(f,"||  " + capwords(feat), 99)
        f.write("||\n")
    # Class
    write_string(f,"|| Class feats: ", 99)
    f.write("||\n")
    for feat in list(char.clas.core.keys()):
        if feat not in ["Cantrips known", "Spells known"]:
            if type(char.clas.core[feat]) == list:
                write_string(f, "||  " + feat + ": " + ", ".join(char.clas.core[feat]),99)
            else:
                write_string(f, "||  " + feat + ": " + str(char.clas.core[feat]), 99)
            f.write("||\n")
    for feat in char.clas.feats:
        write_string(f,"||  " + feat, 99)
        f.write("||\n")
        
    text_separator(f, "EQUIPMENT", "\\", width)
    
    # EQUIPMENT
    for string in char.equipment:
        write_string(f, "|| " + string,99)
        f.write("||\n")
    
    text_separator(f,"PROFICIENCIES","/",width)
    
    # PROFICIENCIES
    write_string(f, "|| Languages:", 99)
    f.write("||\n")
    for language in char.languages:
        write_string(f, "||  " + language,99)
        f.write("||\n")
    write_string(f, "|| Weapons:",99)
    f.write("||\n")
    for weapon in char.weapon_prof:
        write_string(f,"||  " + weapon, 99)
        f.write("||\n")
    if len(char.armor_prof) > 0:
        write_string(f,"|| Armor:",99)
        f.write("||\n")
        for armor in char.armor_prof:
            write_string(f,"||  " + armor, 99)
            f.write("||\n")
    if len(char.tool_prof) > 0:
        write_string(f,"|| Tools:",99)
        f.write("||\n")
        for tool in char.tool_prof:
            write_string(f,"||  " + tool, 99)
            f.write("||\n")
    
    text_separator(f,"PERSONALITY","/",width)
    
    # BACKGROUND
    write_string(f,"|| Traits:",99)
    f.write("||\n")
    for trait in char.background.traits:
        t_lst = text_wrap(trait, 94)
        for substring in t_lst:
            write_string(f,"||  " + substring, 99)
            f.write("||\n")
    write_string(f,"|| Ideal:",99)
    f.write("||\n")
    i_lst = text_wrap(char.background.ideal,94)
    for i in i_lst:
        write_string(f,"||  " + i,99)
        f.write("||\n")
    write_string(f,"|| Bond:",99)
    f.write("||\n")
    b_lst = text_wrap(char.background.bond,94)
    for b in b_lst:
        write_string(f,"||  " + b,99)
        f.write("||\n")
    write_string(f,"|| Flaw:",99)
    f.write("||\n")
    f_lst = text_wrap(char.background.flaw,94)
    for flaw in f_lst:
        write_string(f,"||  " + flaw,99)
        f.write("||\n")
    
    # SPELLS
    if "Spellcasting" in char.clas.core.keys() or "Pact Magic" in char.clas.core.keys():
        
        text_separator(f,"SPELL INFO","=",width)
        
        if "Spellcasting" in char.clas.core.keys():
            spell_mod = getattr(char.statmods, char.clas.core["Spellcasting"])
        if "Pact Magic" in char.clas.core.keys():
            spell_mod = getattr(char.statmods, char.clas.core["Pact Magic"])
        spell_atk = spell_mod + char.prof_mod
        spell_dc = 8 + spell_atk
        
        write_string(f,"|| Spell Attack Modifier: " + str(spell_atk), 50)
        write_string(f,"| Spell DC: " + str(spell_dc),49)
        f.write("||\n")
        
        text_separator(f, "SPELLS", "-", width)
        
        for i in range(10):
            if len(char.spells[str(i)]) > 0:
                if i == 0:
                    write_string(f, "|| Cantrips: ", 99)
                else:
                    write_string(f, "|| Level " + str(i) + " spells:", 99)
                f.write("||\n")
                for j in range(len(char.spells[str(i)])):
                    write_string(f, "||  " + capwords(char.spells[str(i)][j]),99)
                    f.write("||\n")
        
    # MAGIC INITIATE            
    if "Magic Initiate" in char.feats:
        
        text_separator(f,"MAGIC INITIATE", "=", width)
        spell_mod = getattr(char.statmods, char.init_spells["mod"])
        spell_atk = spell_mod + char.prof_mod
        spell_dc = 8 + spell_atk
        
        write_string(f,"|| Spell Attack Modifier: " + str(spell_atk), 50)
        write_string(f,"| Spell DC: " + str(spell_dc),49)
        f.write("||\n")
        
        text_separator(f, "SPELLS", "-", width)
        
        for i in range(2):
            if len(char.init_spells[str(i)]) > 0:
                if i == 0:
                    write_string(f, "|| Cantrips: ", 99)
                else:
                    write_string(f, "|| Level " + str(i) + " spells:", 99)
                f.write("||\n")
                for j in range(len(char.init_spells[str(i)])):
                    write_string(f, "||  " + capwords(char.init_spells[str(i)][j]),99)
                    f.write("||\n")
    
    write_separator(f,"/",width)
    
    f.close()