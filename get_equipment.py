# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:33:04 2021

@author: Jesper
"""

import random

# Read lines of .txt file into a list
def lst_from_file(file_name):
    # Load in .txt file in read only
    file = open(file_name, "r", encoding="utf-8")
    # Convert to list, split at new lines
    lst = file.read().split("\n")
    # Return the list
    return lst

def remove_heavy(lst):
    heavy_lst = ["Glaive","Greataxe","Greatsword","Halberd","Maul","Pike","Heavy Crossbow","Longbow"]
    for obj in heavy_lst:
        try:
            lst.remove(obj)
        except ValueError:
            pass
    return lst

def prof_instruments(char):
    instruments = lst_from_file("instrument_list.txt")
    new_lst = []
    for instrument in instruments:
        if instrument.lower() in char.tool_prof:
            new_lst.append(instrument)
    return new_lst

def prof_tools(char):
    instruments = lst_from_file("artisan_tool_list.txt")
    new_lst = []
    for instrument in instruments:
        if instrument.lower() in char.tool_prof:
            new_lst.append(instrument)
    return new_lst

def prof_games(char):
    instruments = lst_from_file("gaming_list.txt")
    new_lst = []
    for instrument in instruments:
        if instrument.lower() in char.tool_prof:
            new_lst.append(instrument)
    return new_lst
    

def get_equipment(char):
    simple_melee_weapons = ["Club","Dagger","Greatclub","Handaxe","Javelin","Light hammer","Mace","Quarterstaff","Sickle","Spear"]
    simple_ranged_weapons = ["Light Crossbow","Dart","Shortbow","Sling"]
    martial_melee_weapons = ["Battleaxe","Flail","Glaive","Greataxe","Greatsword","Halberd","Lance","Longsword","Maul","Morningstar","Pike","Rapier","Scimitar","Shortsword","Trident","War Pick","Warhammer","Whip"]
    martial_ranged_weapons = ["Blowgun","Hand Crossbow","Heavy Crossbow","Longbow","Net"]
    
    if char.race.size == "Small":
        simple_melee_weapons = remove_heavy(simple_melee_weapons)
        simple_ranged_weapons = remove_heavy(simple_ranged_weapons)
        martial_melee_weapons = remove_heavy(martial_melee_weapons)
        martial_ranged_weapons = remove_heavy(martial_ranged_weapons)
    
    # CLASSES
    
    # Barbarian
    if char.clas.clas == "Barbarian":
        pack = "Exporer's Pack"
        char.equipment += ["Javelin" for i in range(4)]
        char.equipment += random.choice([["Handaxe","Handaxe"],[random.choice(simple_melee_weapons+simple_ranged_weapons)]])
        char.equipment += [random.choice(["Greataxe",random.choice(martial_melee_weapons)])]
        
    # Bard
    elif char.clas.clas == "Bard":
        pack = random.choice(["Diplomat's Pack", "Entertainer's Pack"])
        instruments = prof_instruments(char)
        char.equipment += [random.choice([random.choice(instruments), "Lute"])]
        if char.stats.dexterity > char.stats.strength:
            char.equipment += ["Rapier"]
        elif char.stats.strength > char.stats.dexterity:
            char.equipment += ["Longsword"]
        else:
            char.equipment += [random.choice(["Rapier","Longsword",random.choice(simple_melee_weapons+simple_ranged_weapons)])]
        char.equipment += ["Leather Armor", "Dagger"]
        
    # Cleric
    elif char.clas.clas == "Cleric":
        pack = random.choice(["Priest's Pack","Explorer's Pack"])
        if "Warhammer" in char.weapon_prof or "Martial" in char.weapon_prof:
            char.equipment += ["Warhammer"]
        else:
            char.equipment += ["Mace"]
        if "Heavy" in char.armor_prof:
            char.equipment += ["Chain Mail"]
        elif char.statmods.dexterity > 2:
            char.equipment += ["Leather Armor"]
        else:
            char.equipment += ["Scale Mail"]
        char.equipment += [random.choice(["Light Crossbow",random.choice(simple_melee_weapons+simple_ranged_weapons)])]
        char.equipment += ["Shield", "Holy Symbol"]
    
    # Druid    
    elif char.clas.clas == "Druid":
        pack = "Explorer's Pack"
        char.equipment += [random.choice(["Shield",random.choice(simple_melee_weapons+simple_ranged_weapons)])]
        char.equipment += [random.choice(["Scimitar",random.choice(simple_melee_weapons)])]
        char.equipment += ["Leather Armor", "Druidic Focus"]
        
    # Fighter
    elif char.clas.clas == "Fighter":
        pack = random.choice(["Dungeoneer's Pack", "Explorer's Pack"])
        if char.stats.strength > char.stats.dexterity:
            char.equipment += ["Chain Mail"]
        elif char.stats.dexterity > char.stats.strength:
            char.equipment += ["Leather Armor", "Longbow"]
        else:
            char.equipment += random.choice([["Chain Mail"],["Longbow", "Leather Armor"]])
        if char.clas.core["Fighting Style"] == "Archery":
            good_weaps = ["Rapier","Scimitar","Shortsword","Whip","Blowgun","Hand Crossbow","Heavy Crossbow","Longbow","Net"]
        elif char.clas.core["Fighting Style"] == "Defense":
            if char.stats.strength > char.stats.dexterity:
                good_weaps = ["Battleaxe","Flail","Glaive","Greataxe","Greatsword","Halberd","Lance","Longsword","Maul","Morningstar","Pike","Trident","War Pick","Warhammer"]
            elif char.stats.dexterity > char.stats.strength:
                good_weaps = ["Rapier","Scimitar","Shortsword","Whip","Blowgun","Hand Crossbow","Heavy Crossbow","Longbow","Net"]
            else:
                good_weaps = martial_melee_weapons+martial_ranged_weapons
        elif char.clas.core["Fighting Style"] == "Dueling" or char.clas.core["Fighting Style"] == "Protection":
            if char.stats.strength > char.stats.dexterity:
                good_weaps = ["Battleaxe","Flail","Lance","Longsword","Morningstar","Trident","War Pick","Warhammer"]
            elif char.stats.dexterity > char.stats.strength:
                good_weaps = ["Rapier","Scimitar","Shortsword","Whip"]
            else:
                good_weaps = ["Flail","Lance","Longsword","Morningstar","Trident","War Pick","Warhammer", "Rapier","Scimitar","Shortsword","Whip"]
        elif char.clas.core["Fighting Style"] == "Great Weapon Fighting":
            good_weaps = ["Battleaxe","Glaive","Greataxe","Greatsword","Halberd","Longsword","Maul","Pike","Trident","Warhammer"]
        elif char.clas.core["Fighting Style"] == "Two-Weapon Fighting":
            good_weaps = ["Scimitar","Shortsword"]
        if char.race.size == "Small":
            good_weaps = remove_heavy(good_weaps)
        if char.clas.core["Fighting Style"] == "Protection":
            char.equipment += ["Shield", random.choice(good_weaps)]
        else:
            char.equipment += random.choice([["Shield", random.choice(good_weaps)],[random.choice(good_weaps) for i in range(2)]])
        char.equipment += random.choice([["Light Crossbow"],["Handaxe" for i in range(2)]])
        
    # Monk
    elif char.clas.clas == "Monk":
        pack = random.choice(["Dungeoneer's Pack", "Explorer's Pack"])
        char.equipment += ["Dart" for i in range(10)]
        char.equipment += [random.choice(["Shortsword",random.choice(simple_melee_weapons+simple_ranged_weapons)])]
    
    # Paladin
    elif char.clas.clas == "Paladin":
        pack = random.choice(["Priest's Pack", "Explorer's Pack"])
        char.equipment += ["Chain Mail", "Holy Symbol"]
        if "Fighting Style" in char.clas.core.keys():
            if char.clas.core["Fighting Style"] == "Defense":
                good_weaps = ["Battleaxe","Flail","Glaive","Greataxe","Greatsword","Halberd","Lance","Longsword","Maul","Morningstar","Pike","Trident","War Pick","Warhammer"]
            elif char.clas.core["Fighting Style"] == "Dueling" or char.clas.core["Fighting Style"] == "Protection":
                good_weaps = ["Battleaxe","Flail","Lance","Longsword","Morningstar","Trident","War Pick","Warhammer"]
            elif char.clas.core["Fighting Style"] == "Great Weapon Fighting":
                good_weaps = ["Battleaxe","Glaive","Greataxe","Greatsword","Halberd","Longsword","Maul","Pike","Trident","Warhammer"]
        else:
            good_weaps = martial_melee_weapons
        if char.race.size == "Small":
            good_weaps = remove_heavy(good_weaps)
        if "Fighting Style" in char.clas.core.keys():
            if char.clas.core["Fighting Style"] == "Protection":
                char.equipment += ["Shield",random.choice(good_weaps)]
            else:
                char.equipment += random.choice([["Shield",random.choice(good_weaps)],[random.choice(good_weaps) for i in range(2)]])
        else:
            char.equipment += random.choice([["Shield",random.choice(good_weaps)],[random.choice(good_weaps) for i in range(2)]])
        char.equipment += random.choice([["Javelin" for i in range(5)],[random.choice(simple_melee_weapons+simple_ranged_weapons)]])
    
    # Ranger
    elif char.clas.clas == "Ranger":
        pack = random.choice(["Dungeoneer's Pack", "Explorer's Pack"])
        char.equipment += ["Longbow"]
        if char.statmods.dexterity > 2:
            char.equipment += ["Leather Armor"]
        else:
            char.equipment += ["Scale Mail"]
        if "Fighting Style" in char.clas.core.keys():
            if char.clas.core["Fighting Style"] == "Archery" or char.clas.core["Fighting Style"] == "Defense":
                if char.stats.strength > char.stats.dexterity:
                    good_weaps = simple_melee_weapons
                else:
                    good_weaps = ["Dagger"]
            elif char.clas.core["Fighting Style"] == "Dueling":
                if char.stats.strength > char.stats.dexterity:
                    good_weaps = ["Javelin", "Mace","Quarterstaff","Spear"]
                else:
                    good_weaps = ["Dagger"]
            elif char.clas.core["Fighting Style"] == "Two-Weapon Fighting":
                if char.stats.strength > char.stats.dexterity:
                    good_weaps = ["Club", "Handaxe", "Light Hammer", "Sickle"]
                else:
                    good_weaps = ["Dagger"]
        else:
            good_weaps = simple_melee_weapons
        if char.race.size == "Small":
            good_weaps = remove_heavy(good_weaps)
        char.equipment += random.choice([["Shortsword" for i in range(2)],[random.choice(good_weaps) for i in range(2)]])
        
    # Rogue
    elif char.clas.clas == "Rogue":
        pack = random.choice(["Burglar's Pack", "Dungeoneer's Pack", "Explorer's Pack"])
        char.equipment += ["Leather Armor", "Dagger", "Dagger", "Thieves' Tools"]
        char.equipment += [random.choice(["Shortsword", "Rapier"])]
        char.equipment += [random.choice(["Shortsword", "Shortbow"])]
        
    # Sorcerer
    elif char.clas.clas == "Sorcerer":
        pack = random.choice(["Dungeoneer's Pack", "Explorer's Pack"])
        char.equipment += ["Dagger" for i in range(2)]
        char.equipment += [random.choice(["Component Pouch", "Arcane Focus"])]
        char.equipment += [random.choice(["Light Crossbow", random.choice(simple_melee_weapons+simple_ranged_weapons)])]
        
    # Warlock
    elif char.clas.clas == "Warlock":
        pack = random.choice(["Scholar's Pack", "Dungeoneer's Pack"])
        char.equipment += ["Leather Armor", random.choice(simple_melee_weapons+simple_ranged_weapons), "Dagger", "Dagger"]
        char.equipment += [random.choice(["Light Crossbow", random.choice(simple_melee_weapons+simple_ranged_weapons)])]
        char.equipment += [random.choice(["Component Pouch", "Arcane Focus"])]
        
    # Wizard
    elif char.clas.clas == "Wizard":
        pack = random.choice(["Scholar's Pack", "Explorer's Pack"])
        char.equipment += ["Spellbook"]
        char.equipment += [random.choice(["Quarterstaff", "Dagger"])]
        char.equipment += [random.choice(["Component Pouch", "Arcane Focus"])]
        
    # Set AC
    if "Leather Armor" in char.equipment:
        char.base_ac = 11
    if "Scale Mail" in char.equipment:
        char.base_ac = 14
        char.ac_dex_cap = 2
    if "Chain Mail" in char.equipment:
        char.base_ac = 16
        char.ac_dex_cap = 0
        
    # BACKGROUNDS
    
    # Acolyte
    if char.background.background == "Acolyte":
        char.equipment += ["Holy symbol", "Prayer book", "5 Sticks of Incense", "Vestments", "Common Clothes", "Belt Pouch"]
        char.money += 1500
    elif char.background.background == "Charlatan":
        char.equipment += ["Fine Clothes", "Disguise Kit", "Con Tools", "Belt Pouch"]
        char.money += 1500
    elif char.background.background == "Criminal":
        char.equipment += ["Crowbar", "Common Clothes", "Belt Pouch"]
        char.money += 1500
    elif char.background.background in ["Entertainer", "Gladiator"]:
        char.equipment += ["Admirer's Favor", "Costume", "Belt Pouch"]
        char.money += 1500
        if char.background.background == "Entertainer":
            char.equipment.append(random.choice(prof_instruments(char)).capitalize())
        elif char.background.background == "Gladiator":
            char.equipment.append(random.choice(["Trident", "Net", "Blowgun"]))
    elif char.background.background == "Folk Hero":
        char.equipment += [random.choice(prof_tools(char)), "Shovel", "Iron Pot", "Common Clothes", "Belt Pouch"]
        char.money += 1000
    elif char.background.background == "Guild Artisan":
        char.equipment += [random.choice(prof_tools(char)), "Letter of Introduction", "Traveler's Clothes", "Belt Pouch"]
        char.money += 1500
    elif char.background.background == "Hermit":
        char.equipment += ["Case of Notes", "Winter Blanket", "Common Clothes", "Herbalism Kit"]
        char.money += 500
    elif char.background.background in ["Noble", "Knight"]:
        char.equipment += ["Fine Clothes", "Signet Ring", "Scroll of Pedigree", "Purse"]
        char.money += 2500
    elif char.background.background == "Outlander":
        char.equipment += ["Staff", "Hunting Trap", "Hunting Trophy", "Traveler's Clothes", "Belt Pouch"]
        char.money += 1000
    elif char.background.background == "Sage":
        char.equipment += ["Bottle of Black Ink", "Quill", "Small Knife", "Letter from Colleague", "Common Clothes", "Belt Pouch"]
        char.money += 1000
    elif char.background.background in ["Sailor", "Pirate"]:
        char.equipment += ["Belaying Pin", "50 feet of Silk Rope", "Lucky Charm", "Common Clothes", "Belt Pouch"]
        char.money += 1000
    elif char.background.background == "Soldier":
        char.equipment += ["Insignia of Rank", "Trophy from Fallen Enemy", random.choice(prof_games(char)), "Common Clothes", "Belt Pouch"]
        char.money += 1000
    elif char.background.background == "Urchin":
        char.equipment += ["Small Knife", "City Map", "Pet Mouse", "Token of Parents", "Common Clothes", "Belt Pouch"]
        char.money += 1000
            
    return char