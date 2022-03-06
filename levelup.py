# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 23:33:13 2021

@author: Jesper
"""

import random

def capwords(s):
    return " ".join(w.capitalize() for w in s.split())

# Read lines of .txt file into a list
def lst_from_file(file_name):
    # Load in .txt file in read only
    file = open(file_name, "r", encoding="utf-8")
    # Convert to list, split at new lines
    lst = file.read().split("\n")
    # Return the list
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

def import_spell_lists(clas, books):
    lst = lst_from_file("spell_list.txt")
    for string in lst:
        cl_lst = string.split("\t")
        if cl_lst[1].lower() == clas.lower() and cl_lst[0] in books:
            sp_lst = cl_lst[2].split(";")
            dct = {str(i):[] for i in range(10)}
            for i in range(len(sp_lst)):
                dct[sp_lst[i][0]] += sp_lst[i][2:].split(",")
    return dct

def rand_spells(clas, level, num, char):
    spell_list = import_spell_lists(clas,char.books)
    print(spell_list)
    print(level)
    pos_spells = unique_list(spell_list[str(level)], char.spells[str(level)])
    print(pos_spells)
    chosen_spells = random.sample(pos_spells,num)
    return chosen_spells

def choose_cantrips(dct, char, num=None):
    if num == None:
        char.spells["0"] += random.sample(unique_list(dct["0"],char.spells["0"]), char.clas.core["Cantrips known"])
    else:
        char.spells["0"] += random.sample(unique_list(dct["0"],char.spells["0"]), num)

def choose_spells(dct, max_lvl, char, num=None):
    if num == None:
        quan = char.clas.core["Spells known"]
    else:
        quan = num
    chosen = 0
    while chosen < quan:
        lvl_roll = random.randint(1,max_lvl)
        pos_lst = unique_list(dct[str(lvl_roll)], char.spells[str(lvl_roll)])
        if len(pos_lst) > 0:
            char.spells[str(lvl_roll)] += [random.choice(pos_lst)]
            chosen += 1
        
def choose_invocations(char):
    invos = ["Armor of Shadows",
             "Beast Speech",
             "Beguiling Influence",
             "Devil's Sight",
             "Eldritch Sight",
             "Eyes of the Rune Keeper",
             "Fiendish Vigor",
             "Gaze of the Two Minds",
             "Mask of Many Faces",
             "Misty Visions",
             "Thief of Five Fates" ]
    if "eldritch blast" in char.spells["0"]:
        invos += ["Agonizing Blast", "Eldritch Spear", "Repelling Blast"]
    if char.level >= 3:
        if char.clas.core["Pact Boon"] == "Pact of the Tome":
            invos += ["Book of Ancient Secrets"]
        if char.clas.core["Pact Boon"] == "Pact of the Chain":
            invos += ["Voice of the Chain Master"]
    if char.level >= 5:
        invos += ["Mire the Mind", "One with the Shadows", "Sign of Ill Omen"]
        if char.clas.core["Pact Boon"] == "Pact of the Blade":
            invos += ["Thirsting Blade"]
    if char.level >= 7:
        invos += ["Bewitching Whispers", "Dreadful Word", "Sculptor of Flesh"]
    if char.level >= 9:
        invos += ["Ascendant Step", "Minions of Chaos", "Oterworldly Leap", "Whispers of the Grave"]
    if char.level >= 12:
        if char.clas.core["Pact Boon"] == "Pact of the Blade":
            invos += ["Lifedrinker"]
    if char.level >= 15:
        invos += ["Master of Myriad Forms", "Visions of Distant Realms", "Witch Sight"]
        if char.clas.core["Pact Boon"] == "Pact of the Chain":
            invos += ["Chains of Carceri"]
            
    char.clas.core["Eldritch Invocations"] += random.sample(invos, char.clas.core["Invocations known"])
    
def choose_feat(char):
    feats = ["Alert",
             "Athlete",
             "Actor",
             "Charger",
             "Dual Wielder",
             "Dungeon Delver",
             "Durable",
             "Healer",
             "Keen Mind",
             "Linguist",
             "Lucky",
             "Mage Slayer",
             "Magic Initiate",
             "Martial Adept",
             "Mobile",
             "Mounted Combat",
             "Observant",
             "Savage Attacker",
             "Sentinel",
             "Sharpshooter",
             "Skilled",
             "Tavern Brawler",
             "Tough",
             ]
    if char.stats.dexterity >= 13:
        feats += ["Defensive Duelist", "Skulker"]
    if char.stats.strength >= 13:
        feats += ["Grappler"]
    if char.stats.charisma >= 13:
        feats += ["Inspiring Leader"]
    if char.stats.intelligence >= 13:
        feats += ["Ritual Caster"]
    if "Spellcasting" in char.clas.core.keys() or "Pact Magic" in char.clas.core.keys() or "Magic Initiate" in char.feats:
        feats += ["Elemental Adept", "Spell Sniper", "War Caster"]
    if "Martial" in char.weapon_prof and char.stats.strength > char.stats.dexterity:
        feats += ["Polearm Master"]
        if "Fighting Style" in char.clas.core.keys():
            if char.clas.core["Fighting Style"] not in ["Two-Weapon Fighting", "Duelist", "Archery"]:
                feats += ["Great Weapon Master"]
        else:
            feats += ["Great Weapon Master"]
    if "Martial" in char.weapon_prof or "Simple" in char.weapon_prof or "Light Crossbow" in char.weapon_prof:
        feats += ["Crossbow Expert"]
    if "Light" not in char.armor_prof:
        feats += ["Lightly Armored"]
    if "Light" in char.armor_prof and "Medium" not in char.armor_prof and char.statmods.dexterity <= 2:
        feats += ["Moderately Armored"]
    if "Medium" in char.armor_prof and "Heavy" not in char.armor_prof:
        if char.statmods.dexterity <= 0:
            feats += ["Heavily Armored"]
        elif char.statmods.dexterity <= 2:
            feats += ["Medium Armor Master"]
    if "Heavy" in char.armor_prof:
        feats += ["Heavy Armor Master"]
    if "Shield" in char.armor_prof:
        feats += ["Shield Master"]
    if "Martial" not in char.weapon_prof:
        feats += ["Weapon Master"]
    if len(unique_list(list(vars(char.stats).keys()),char.clas.savingthrows)) > 0:
        feats += ["Resilient"]
        
    pos_feats = unique_list(feats, char.feats)
    feat = capwords(random.choice(pos_feats))

    
    char.feats += [capwords(feat)]
    
    if feat in ["Athlete", "Lightly Armored", "Moderately Armored", "Weapon Master"]:
        str_prio = char.clas.prio[0]
        dex_prio = char.clas.prio[1]
        if str_prio > dex_prio and char.stats.strength < char.statlims.strength:
            char.stats.strength += 1
        elif char.stats.dexterity < char.statlims.dexterity:
            char.stats.dexterity += 1
        elif char.stats.strength < char.statlims.strength:
            char.stats.strength += 1
    if feat in ["Tavern Brawler"]:
        str_prio = char.clas.prio[0]
        con_prio = char.clas.prio[2]
        if str_prio > con_prio and char.stats.strength < char.statlims.strength:
            char.stats.strength += 1
        elif char.stats.constitution < char.statlims.constitution:
            char.stats.constitution += 1
        elif char.stats.strength < char.statlims.strength:
            char.stats.strength += 1
    if feat in ["Observant"]:
        int_prio = char.clas.prio[3]
        wis_prio = char.clas.prio[4]
        if int_prio > wis_prio and char.stats.intelligence < char.statlims.intelligence:
            char.stats.intelligence += 1
        elif char.stats.wisdom < char.statlims.wisdom:
            char.stats.wisdom += 1
        elif char.stats.intelligence < char.statlims.intelligence:
            char.stats.intelligence += 1
    if feat in ["Keen Mind", "Linguist"]:
        if char.stats.intelligence < char.statlims.intelligence:
            char.stats.intelligence += 1
    if feat in ["Actor"]:
        if char.stats.charisma < char.statlims.charisma:
            char.stats.charisma += 1
    if feat in ["Durable"]:
        if char.stats.constitution < char.statlims.constitution:
            char.stats.constitution += 1
    if feat in ["Heavy Armor Master", "Heavily Armored"]:
        if char.stats.strength <= char.statlims.strength:
            char.stats.strength += 1
    if feat == "Heavily Armored":
        char.armor_prof += ["Heavy"]
    elif feat == "Moderately Armored":
        char.armor_prof += ["Medium"]
    elif feat == "Lightly Armored":
        char.armor_prof += ["Light"]
    elif feat == "Linguist":
        pos_languages = unique_list(lst_from_file("language_list.txt"), char.languages)
        char.languages += random.sample(pos_languages,3)
    elif feat == "Magic Initiate":
        clases = ["Bard", "Cleric", "Druid", "Sorcerer", "Warlock","Wizard"]
        clas_roll = random.choice(clases)
        print(clas_roll)
        if clas_roll in ["Bard", "Sorcerer", "Warlock"]:
            char.init_spells["mod"] = "charisma"
        elif clas_roll in ["Cleric", "Druid"]:
            char.init_spells["mod"] = "wisdom"
        else:
            char.init_spells["mod"] = "intelligence"
        char.init_spells["0"] = rand_spells(clas_roll, 0, 2, char)
        char.init_spells["1"] = rand_spells(clas_roll, 1, 1, char)
    elif feat == "Martial Adept":
        pass
    elif feat == "Mobile":
        char.speed += 10
    elif feat == "Resilient":
        pos_stats = unique_list(list(vars(char.stats).keys()),char.clas.savingthrows)
        stat = random.choice(pos_stats)
        if getattr(char.stats, stat) < getattr(char.statlims, stat):
            setattr(char.stats, stat, getattr(char.stats, stat)+1)
        char.clas.savingthrows.append(stat)
    elif feat == "Ritual Caster":
        pass
    elif feat == "Skilled":
        all_skills = list(vars(char.skills).keys())
        pos_skills = unique_list(all_skills, char.skill_prof)
        new_skills = random.sample(pos_skills,3)
        char.skill_prof += new_skills
        char.update()
    elif feat == "Spell Sniper":
        pass
    elif feat == "Tough":
        char.extra_hp += char.level * 2
    elif feat == "Weapon Master":
        pass
    
    
def ability_score_improvement(char):
    assigned = 0
    while assigned < 2:
        stat = random.choice(list(vars(char.stats).keys()))
        if getattr(char.stats, stat) < getattr(char.statlims,stat):
            setattr(char.stats, stat, getattr(char.stats, stat)+1)
            assigned += 1
            
def level4(char):
    roll = random.random()
    if roll < 0.5:
        ability_score_improvement(char)
    elif roll >= 0.5:
        choose_feat(char)
            

def levelup(char):
    # BARBARIAN
    if char.clas.clas == "Barbarian":
        ragedmg=[2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4]
        rages = [2,2,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6,"Unlimited"]
        char.clas.core["Rages"] = rages[char.level-1]
        char.clas.core["Rage Damage"] = ragedmg[char.level-1]
        char.clas.core["Unarmored Defense"] = ["dexterity", "constitution"]
        char.update()
        if char.level > 1:
            char.clas.feats += ["Reckless Attack", "Danger Sense"]
        if char.level > 2:
            if char.clas.subclas == "Berserker":
                char.clas.feats += ["Frenzy"]
            elif char.clas.subclas == "Totem Warrior":
                totem_spirit = random.choice(["Bear","Eagle","Wolf"])
                char.clas.feats += ["Spirit Seeker", "Totem Spirit: " + totem_spirit]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Extra Attack","Fast Movement"]
        if char.level > 5:
            if char.clas.subclas == "Berserker":
                char.clas.feats += ["Mindless Rage"]
            elif char.clas.subclas == "Totem Warrior":
                totem_spirit = random.choice(["Bear","Eagle","Wolf"])
                char.clas.feats += ["Aspect of the Beast: " + totem_spirit]
        if char.level > 6:
            char.clas.feats += ["Feral Instinct"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            char.clas.feats += ["Brutal Critical (1 die)"]
        if char.level > 9:
            if char.clas.subclas == "Berserker":
                char.clas.feats += ["Intimidating Presence"]
            elif char.clas.subclas == "Totem Warrior":
                char.clas.feats += ["Spirit Walker"]
        if char.level > 10:
            char.clas.feats += ["Relentless Rage"]
        if char.level > 11:
            level4(char)
        if char.level > 12:
            char.clas.feats.remove("Brutal Critical (1 die)")
            char.clas.feats += ["Brutal Critical (2 dice)"]
        if char.level > 13:
            if char.clas.subclas == "Berserker":
                char.clas.feats += ["Retaliation"]
            elif char.clas.subclas == "Totem Warrior":
                totem_spirit = random.choice(["Bear", "Eagle", "Wolf"])
                char.clas.feats += ["Totemic Attunement: " + totem_spirit]
        if char.level > 14:
            char.clas.feats += ["Persistent Rage"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.feats.remove("Brutal Critical (2 dice)")
            char.clas.feats += ["Brutal Critical (3 dice)"]
        if char.level > 17:
            char.clas.feats += ["Indomitable Might"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Primal Champion"]
            char.stats.strength += 4
            char.stats.constitution += 4
            char.statlims.strength += 4
            char.statlims.constitution += 4
       
         
    # BARD
    elif char.clas.clas == "Bard":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4]
        spells= [4,5,6,7,8,9,10,11,12,14,15,15,16,18,19,19,20,22,22,22]
        char.clas.core["Spellcasting"] = "charisma"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = spells[char.level-1]
        char.clas.feats += ["Bardic Inspiration (d6)"]
        if char.level > 1:
            char.clas.feats += ["Jack of All Trades", "Song of Rest (d6)"]
        if char.level > 2:
            char.skill_expert += random.sample(char.skill_prof, 2)
            char.update()
            if char.clas.subclas == "Lore":
                char.skill_prof += ["Choice3"]
                char.update()
                char.clas.feats += ["Cutting Words"]
            elif char.clas.subclas == "Valor":
                char.armor_prof += ["Medium", "Shield"]
                char.weapon_prof += ["Martial"]
                char.clas.feats += ["Combat Inspiration"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats.remove("Bardic Inspiration (d6)")
            char.clas.feats += ["Bardic Inspiration (d8)", "Font of Inspiration"]
        if char.level > 5:
            char.clas.feats += ["Countercharm"]
            if char.clas.subclas == "Lore":
                for i in range(2):
                    sp_cl = random.choice(["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"])
                    if sp_cl not in ["Paladin", "Ranger"]:
                        sp_lv = random.randint(0,3)
                    else:
                        sp_lv = random.randint(1,3)
                    char.spells[str(sp_lv)] += rand_spells(sp_cl,sp_lv,1,char)
            elif char.clas.subclas == "Valor":
                char.clas.feats += ["Extra Attack"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            char.clas.feats.remove("Song of Rest (d6)")
            char.clas.feats += ["Song of Rest (d8)"]
        if char.level > 9:
            char.clas.feats.remove("Bardic Inspiration (d8)")
            char.clas.feats += ["Bardic Inspiration (d10)"]
            char.skill_expert += random.sample(unique_list(char.skill_prof, char.skill_expert), 2)
            char.update()
            for i in range(2):
                sp_cl = random.choice(["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"])
                if sp_cl not in ["Paladin", "Ranger"]:
                    sp_lv = random.randint(0,5)
                else:
                    sp_lv = random.randint(1,5)
                char.spells[str(sp_lv)] += rand_spells(sp_cl,sp_lv,1,char)
        if char.level > 11:
            level4(char)
        if char.level > 12:
            char.clas.feats.remove("Song of Rest (d8)")
            char.clas.feats += ["Song of Rest (d10)"]
        if char.level > 13:
            for i in range(2):
                sp_cl = random.choice(["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"])
                if sp_cl not in ["Paladin", "Ranger"]:
                    sp_lv = random.randint(0,7)
                else:
                    sp_lv = random.randint(1,7)
                char.spells[str(sp_lv)] += rand_spells(sp_cl,sp_lv,1,char)
            if char.clas.subclas == "Lore":
                char.clas.feats += ["Peerless Skill"]
            elif char.clas.subclas == "Valor":
                char.clas.feats += ["Battle Magic"]
        if char.level > 14:
            char.clas.feats.remove("Bardic Inspiration (d10)")
            char.clas.feats += ["Bardic Inspiration (d12)"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.feats.remove("Song of Rest (d10)")
            char.clas.feats += ["Song of Rest (d12)"]
        if char.level > 17:
            for i in range(2):
                sp_cl = random.choice(["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"])
                if sp_cl not in ["Paladin", "Ranger"]:
                    sp_lv = random.randint(0,9)
                else:
                    sp_lv = random.randint(1,9)
                char.spells[str(sp_lv)] += rand_spells(sp_cl,sp_lv,1,char)
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Superior Inspiration"]
        choose_cantrips(spell_list, char)
        choose_spells(spell_list, int(min([9,(char.level+1)//2])), char)
            
        
    # CLERIC
    elif char.clas.clas == "Cleric":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5]
        char.clas.core["Spellcasting"] = "wisdom"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = max([char.level + char.statmods.wisdom, 1])
        if char.clas.subclas == "Knowledge":
            spell_list["1"] += ["command", "identify"]
            char.languages += ["Any2"]
            char.skill_prof += choose_from("2:arcana,history,nature,religion", char.skill_prof)
            char.skill_expert += random.sample([cskill for cskill in ["arcana","history","nature","religion"] if cskill in char.skill_prof],2)
            char.update()
        elif char.clas.subclas == "Life":
            char.spells["1"] += ["bless", "cure wounds"]
            char.armor_prof += ["Heavy"]
            char.clas.feats += ["Disciple of Life"]
        elif char.clas.subclas == "Light":
            char.spells["1"] += ["burning hands", "faerie fire"]
            char.spells["0"] += unique_list(["light"], char.spells["0"])
            char.clas.feats += ["Warding Flare"]
        elif char.clas.subclas == "Nature":
            char.spells["1"] += ["animal friendship", "speak with animals"]
            char.spells["0"] += random.sample(unique_list(import_spell_lists("Druid",char.books)["0"],char.spells["0"]),1)
            char.skill_prof += choose_from("1:animal handling,nature,survival",char.skill_prof)
            char.armor_prof += ["Heavy"]
            char.update()
        elif char.clas.subclas == "Tempest":
            char.spells["1"] += ["fog cloud", "thunderwave"]
            char.armor_prof += ["Heavy"]
            char.weapon_prof += ["Martial"]
            char.clas.feats += ["Wrath of the Storm"]
        elif char.clas.subclas == "Trickery":
            char.spells["1"] += ["charm person", "disguise self"]
            char.clas.feats += ["Blessing of the Trickster"]
        elif char.clas.subclas == "War":
            char.spells["1"] += ["divine favor", "shield of faith"]
            char.armor_prof += ["Heavy"]
            char.weapon_prof += ["Martial"]
            char.clas.feats += ["War Priest"]
        if char.level > 1:
            char.clas.feats += ["Channel Divinity (1/rest)", "Channel Divinity: Turn Undead"]
            if char.clas.subclas == "Knowledge":
                char.clas.feats += ["Channel Divinity: Knowledge of the Ages"]
            elif char.clas.subclas == "Life":
                char.clas.feats += ["Channel Divinity: Preserve Life"]
            elif char.clas.subclas == "Light":
                char.clas.feats += ["Channel Divinity: Radiance of the Dawn"]
            elif char.clas.subclas == "Nature":
                char.clas.feats += ["Channel Divinity: Charm Animals and Plants"]
            elif char.clas.subclas == "Tempest":
                char.clas.feats += ["Channel Divinity: Destructive Wrath"]
            elif char.clas.subclas == "Trickery":
                char.clas.feats += ["Channel Divinity: Invoke Duplicity"]
            elif char.clas.subclas == "War":
                char.clas.feats += ["Channel Divinity: Guided Strike"]
        if char.level > 2:
            if char.clas.subclas == "Knowledge":
                char.spells["2"] += ["augury", "suggestion"]
            elif char.clas.subclas == "Life":
                char.spells["2"] += ["lesser restoration", "spiritual weapon"]
            elif char.clas.subclas == "Light":
                char.spells["2"] += ["flaming sphere", "scorching ray"]
            elif char.clas.subclas == "Nature":
                char.spells["2"] += ["barkskin", "spike growth"]
            elif char.clas.subclas == "Tempest":
                char.spells["2"] += ["gust of wind", "shatter"]
            elif char.clas.subclas == "Trickery":
                char.spells["2"] += ["mirror image", "pass without trace"]
            elif char.clas.subclas == "War":
                char.spells["2"] += ["magic weapon", "spiritual weapon"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Destroy Undead (CR 1/2)"]
            if char.clas.subclas == "Knowledge":
                char.spells["3"] += ["nondetection", "speak with dead"]
            elif char.clas.subclas == "Life":
                char.spells["3"] += ["beacon of hope", "revivify"]
            elif char.clas.subclas == "Light":
                char.spells["3"] += ["daylight", "fireball"]
            elif char.clas.subclas == "Nature":
                char.spells["3"] += ["plant growth", "wind wall"]
            elif char.clas.subclas == "Tempest":
                char.spells["3"] += ["call lightning", "sleet storm"]
            elif char.clas.subclas == "Trickery":
                char.spells["3"] += ["blink", "dispel magic"]
            elif char.clas.subclas == "War":
                char.spells["3"] += ["crusader's mantle", "spirit guardians"]
        if char.level > 5:
            char.clas.feats.remove("Channel Divinity (1/rest)")
            char.clas.feats += ["Channel Divinity (2/rest)"]
            if char.clas.subclas == "Knowledge":
                char.clas.feats += ["Channel Divinity: Read Thoughts"]
            elif char.clas.subclas == "Life":
                char.clas.feats += ["Blessed Healer"]
            elif char.clas.subclas == "Light":
                char.clas.feats += ["Improved Flare"]
            elif char.clas.subclas == "Nature":
                char.clas.feats += ["Dampen Elements"]
            elif char.clas.subclas == "Tempest":
                char.clas.feats += ["Thunderbolt Strike"]
            elif char.clas.subclas == "Trickery":
                char.clas.feats += ["Channel Divinity: Cloak of Shadows"]
            elif char.clas.subclas == "War":
                char.clas.feats += ["Channel Divinity: War God's Blessing"]
        if char.level > 6:
            if char.clas.subclas == "Knowledge":
                char.spells["4"] += ["arcane eye", "confusion"]
            elif char.clas.subclas == "Life":
                char.spells["4"] += ["death ward", "guardian of faith"]
            elif char.clas.subclas == "Light":
                char.spells["4"] += ["guardian of faith", "wall of fire"]
            elif char.clas.subclas == "Nature":
                char.spells["4"] += ["dominate beast", "grasping vine"]
            elif char.clas.subclas == "Tempest":
                char.spells["4"] += ["control water", "ice storm"]
            elif char.clas.subclas == "Trickery":
                char.spells["4"] += ["dimension door", "polymorph"]
            elif char.clas.subclas == "War":
                char.spells["4"] += ["freedom of movement", "stoneskin"]
        if char.level > 7:
            level4(char)
            char.clas.feats.remove("Destroy Undead (CR 1/2)")
            char.clas.feats += ["Destroy Undead (CR 1)"]
            if char.clas.subclas == "Knowledge":
                char.clas.feats += ["Potent Spellcasting"]
            elif char.clas.subclas == "Life":
                char.clas.feats += ["Divine Strike (Radiant)"]
            elif char.clas.subclas == "Light":
                char.clas.feats += ["Potent Spellcasting"]
            elif char.clas.subclas == "Nature":
                char.clas.feats += ["Divine Strike (Cold/Fire/Ligtning)"]
            elif char.clas.subclas == "Tempest":
                char.clas.feats += ["Divine Strike (Thunder)"]
            elif char.clas.subclas == "Trickery":
                char.clas.feats += ["Divine Strike (Poison)"]
            elif char.clas.subclas == "War":
                char.clas.feats += ["Divine Strike (Weapon)"]
        if char.level > 8:
            if char.clas.subclas == "Knowledge":
                char.spells["5"] += ["legend lore", "scrying"]
            elif char.clas.subclas == "Life":
                char.spells["5"] += ["mass cure wounds", "raise dead"]
            elif char.clas.subclas == "Light":
                char.spells["5"] += ["flame strike", "scrying"]
            elif char.clas.subclas == "Nature":
                char.spells["5"] += ["insect plague", "tree stride"]
            elif char.clas.subclas == "Tempest":
                char.spells["5"] += ["destructive wave", "insect plague"]
            elif char.clas.subclas == "Trickery":
                char.spells["5"] += ["dominate person", "modify memory"]
            elif char.clas.subclas == "War":
                char.spells["5"] += ["flame strike", "hold monster"]
        if char.level > 9:
            char.clas.feats += ["Divine Intervention"]
        if char.level > 10:
            char.clas.feats.remove("Destroy Undead (CR 1)")
            char.clas.feats += ["Destroy Undead (CR 2)"]
        if char.level > 11:
            level4(char)
        if char.level > 13:
            char.clas.feats.remove("Destroy Undead (CR 2)")
            char.clas.feats += ["Destroy Undead (CR 3)"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.feats.remove("Destroy Undead (CR 3)")
            char.clas.feats += ["Destroy Undead (CR 4)"]
            if char.clas.subclas == "Knowledge":
                char.clas.feats += ["Visions of the Past"]
            elif char.clas.subclas == "Life":
                char.clas.feats += ["Supreme Healing"]
            elif char.clas.subclas == "Light":
                char.clas.feats += ["Corona of Light"]
            elif char.clas.subclas == "Nature":
                char.clas.feats += ["Master of Nature"]
            elif char.clas.subclas == "Tempest":
                char.clas.feats += ["Stormborn"]
            elif char.clas.subclas == "Trickery":
                char.clas.feats += ["Improved Duplicity"]
            elif char.clas.subclas == "War":
                char.clas.feats += ["Avatar of Battle"]
        if char.level > 17:
            char.clas.feats.remove("Channel Divinity (2/rest)")
            char.clas.feats += ["Channel Divinity (3/rest)"]
        if char.level > 18:
            level4(char)
        choose_cantrips(spell_list,char)
        choose_spells(spell_list, int(min([9,(char.level+1)//2])), char)
            
        
    # DRUID
    elif char.clas.clas == "Druid":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4]
        char.clas.core["Spellcasting"] = "wisdom"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = max([char.level + char.statmods.wisdom, 1])
        char.languages += ["Druidic"]
        if char.level > 1:
            char.clas.core["Wild Shape"] = "1/4 CR, no flying or swimming"
            if char.clas.subclas == "Land":
                char.spells["0"] += [random.choice(unique_list(spell_list["0"], char.spells["0"]))]
                char.clas.feats += ["Natural Recovery"]
            elif char.clas.subclas == "Moon":
                char.clas.core["Wild Shape"] = "1 CR, no flying or swimming"
                char.clas.feats += ["Combat Wild Shape"]
        if char.level > 2:
            if char.clas.subclas == "Land":
                land = random.choice(["Arctic","Coast","Desert","Forest","Grassland","Mountain","Swamp","Underdark"])
                char.clas.core["Land"] = land
                add_spells = {"Arctic":["hold person","spike growth"],
                              "Coast":["mirror image","misty step"],
                              "Desert":["blur","silence"],
                              "Forest":["barkskin","climb"],
                              "Grassland":["invisibility","pass without trace"],
                              "Mountain":["spider climb","spike growth"],
                              "Swamp":["darkness","melf's acid arrow"],
                              "Underdark":["spider climb","web"] }
                char.spells["2"] += unique_list(add_spells[land],char.spells["2"])
        if char.level > 3:
            char.clas.core["Wild Shape"] = "1/2 CR, no flying"
            level4(char)
        if char.level > 4:
            if char.clas.subclas == "Land":
                add_spells = {"Arctic":["sleet storm", "slow"],
                              "Coast":["water breathing", "water walk"],
                              "Desert":["create food and water","protection from energy"],
                              "Forest":["call lightning", "plant growth"],
                              "Grassland":["daylight", "haste"],
                              "Mountain":["lightning bolt", "meld into stone"],
                              "Swamp":["water walk", "stinking cloud"],
                              "Underdark":["gaseous form","stinking cloud"] }
                char.spells["3"] += unique_list(add_spells[land],char.spells["3"])
        if char.level > 5:
            if char.clas.subclas == "Land":
                char.clas.feats += ["Land's Stride"]
            elif char.clas.subclas == "Moon":
                char.clas.core["Wild Shape"] = "CR " + str(char.level//3) + ", no flying"
                char.clas.feats += ["Primal Strike"]
        if char.level > 6:
            if char.clas.subclas == "Land":
                add_spells = {"Arctic":["freedom of movement","ice storm"],
                              "Coast":["control water","freedom of movement"],
                              "Desert":["blight","hallucinatory terrain"],
                              "Forest":["divination","freedom of movement"],
                              "Grassland":["divination","freedom of movement"],
                              "Mountain":["stone shape","stoneskin"],
                              "Swamp":["freedom of movement","locate creature"],
                              "Underdark":["greater invisibility","stone shape"] }
                char.spells["4"] += unique_list(add_spells[land],char.spells["4"])
        if char.level > 7:
            level4(char)
            if char.clas.subclas == "Moon":
                char.clas.core["Wild Shape"] = "CR " + str(char.level//3)
            else:
                char.clas.core["Wild Shape"] = "CR 1"
        if char.level > 8:
            if char.clas.subclas == "Land":
                add_spells = {"Arctic":["commune with nature","cone of cold"],
                              "Coast":["conjure elemental","scrying"],
                              "Desert":["insect plague","wall of stone"],
                              "Forest":["commune with nature","tree stride"],
                              "Grassland":["dream","insect plague"],
                              "Mountain":["passwall","wall of stone"],
                              "Swamp":["insect plague","scrying"],
                              "Underdark":["cloudkill","insect plague"] }
                char.spells["5"] += unique_list(add_spells[land],char.spells["5"])
        if char.level > 9:
            if char.clas.subclas == "Land":
                char.clas.feats += ["Nature's Ward"]
            elif char.clas.subclas == "Moon":
                char.clas.feats += ["Elemental Wild Shape"]
        if char.level > 11:
            level4(char)
        if char.level > 13:
            if char.clas.subclas == "Land":
                char.clas.feats += ["Nature's Sanctuary"]
            elif char.clas.subclas == "Moon":
                char.clas.feats += ["Thousand Forms"]
        if char.level > 15:
            level4(char)
        if char.level > 17:
            char.clas.feats += ["Timeless Body", "Beast Spells"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Archdruid"]
        choose_cantrips(spell_list,char)
        choose_spells(spell_list, int(min([9,(char.level+1)//2])), char)
                
        
    # FIGHTER
    elif char.clas.clas == "Fighter":
        if char.stats.strength > char.stats.dexterity:
            char.clas.core["Fighting Style"] = random.choice(["Defense","Dueling","Great Weapon Fighting","Protection"])
        elif char.stats.dexterity > char.stats.strength:
            char.clas.core["Fighting Style"] = random.choice(["Archery","Defense","Dueling","Protection","Two-Weapon Fighting"])
        else:
            char.clas.core["Fighting Style"] = random.choice(["Archery","Defense","Dueling","Great Weapon Fighting","Protection","Two-Weapon Fighting"])
        char.clas.feats += ["Second Wind"]
        if char.level > 1:
            char.clas.feats += ["Action Surge (1 use)"]
        if char.level > 2:
            if char.clas.subclas == "Champion":
                char.clas.feats += ["Improved Critical"]
            elif char.clas.subclas == "Battle Master":
                if char.stats.strength >= char.stats.dexterity:
                    maneuvers = ["Commander's Strike","Disarming Attack","Distracting Strike","Evasive Footwork","Feinting Attack","Goading Attack","Lunging Attack","Maneuvering Attack","Menacing Attack","Parry","Precision Attack","Pushing Attack","Rally","Riposte","Sweeping Attack","Trip Attack"]
                else:
                    maneuvers = ["Commander's Strike","Disarming Attack","Distracting Strike","Evasive Footwork","Feinting Attack","Goading Attack","Maneuvering Attack","Menacing Attack","Parry","Precision Attack","Pushing Attack","Rally","Trip Attack"]
                char.clas.core["Maneuvers"] = random.sample(maneuvers,3)
                char.clas.core["Superiority Dice"] = "4d8"
                char.clas.core["Maneuver DC"] = 8 + char.prof_mod + max([char.statmods.strength, char.statmods.dexterity])
                char.tool_prof += ["Artisan1"]
                char.update()
            elif char.clas.subclas == "Eldritch Knight":
                spell_list = import_spell_lists("Wizard", char.books)
                cants = [0,0,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3]
                spells = [0,0,3,4,4,4,5,6,6,7,8,8,9,10,10,11,11,11,12,13]
                max_slot = [0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4]
                char.clas.core["Spellcasting"] = "intelligence"
                char.clas.core["Cantrips known"] = cants[char.level-1]
                char.clas.core["Spells known"] = spells[char.level-1]
                char.clas.feats += ["Weapon Bond"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Extra Attack"]
        if char.level > 5:
            level4(char)
        if char.level > 6:
            if char.clas.subclas == "Champion":
                char.clas.feats += ["Remarkable Athlete"]
            elif char.clas.subclas == "Battle Master":
                char.clas.core["Maneuvers"] = random.sample(unique_list(maneuvers, char.clas.core["Maneuvers"]),2)
                char.clas.core["Superiority Dice"] = "5d8"
                char.clas.feats += ["Know Your Enemy"]
            elif char.clas.subclas == "Eldritch Knight":
                char.clas.feats += ["War Magic"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            char.clas.feats += ["Indomitable (1 use)"]
        if char.level > 9:
            if char.clas.subclas == "Champion":
                if char.stats.strength > char.stats.dexterity:
                    char.clas.core["Fighting Style 2"] = random.choice(unique_list(["Defense","Dueling","Great Weapon Fighting","Protection"], [char.clas.core["Fighting Style"]]))
                elif char.stats.dexterity > char.stats.strength:
                    char.clas.core["Fighting Style 2"] = random.choice(unique_list(["Archery","Defense","Dueling","Protection","Two-Weapon Fighting"], [char.clas.core["Fighting Style"]]))
                else:
                    char.clas.core["Fighting Style 2"] = random.choice(unique_list(["Archery","Defense","Dueling","Great Weapon Fighting","Protection","Two-Weapon Fighting"],[char.clas.core["Fighting Style"]]))
            elif char.clas.subclas == "Battle Master":
                char.clas.core["Superiority Dice"] = "5d10"
                char.clas.core["Maneuvers"] = random.sample(unique_list(maneuvers, char.clas.core["Maneuvers"]),2)
            elif char.clas.subclas == "Eldritch Knight":
                char.clas.feats += ["Eldritch Strike"]
        if char.level > 10:
            char.clas.feats.remove("Extra Attack")
            char.clas.feats += ["Extra Attack (2)"]
        if char.level > 11:
            level4(char)
        if char.level > 12:
            char.clas.feats.remove("Indomitable (1 use)")
            char.clas.feats += ["Indomitable (2 uses)"]
        if char.level > 13:
            level4(char)
        if char.level > 14:
            if char.clas.subclas == "Champion":
                char.clas.feats.remove("Improved Critical")
                char.clas.feats += ["Superior Critical"]
            elif char.clas.subclas == "Battle Master":
                char.clas.feats += ["Relentless"]
                char.clas.core["Superiority Dice"] = "6d10"
                char.clas.core["Maneuvers"] = random.sample(unique_list(maneuvers, char.clas.core["Maneuvers"]),2)
            elif char.clas.subclas == "Eldritch Knight":
                char.clas.feats += ["Arcane Charge"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.feats.remove("Action Surge (1 use)")
            char.clas.feats.remove("Indomitable (2 uses)")
            char.clas.feats += ["Action Surge (2 uses)", "Indomitable (3 uses)"]
        if char.level > 17:
            if char.clas.subclas == "Champion":
                char.clas.feats += ["Survivor"]
            elif char.clas.subclas == "Battle Master":
                char.clas.core["Superiority Dice"] = "6d12"
            elif char.clas.subclas == "Eldritch Knight":
                char.clas.feats += ["Improved War Magic"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats.remove("Extra Attack (2)")
            char.clas.feats += ["Extra Attack (3)"]
        if char.clas.subclas == "Eldritch Knight":
            choose_cantrips(spell_list,char)
            choose_spells(spell_list, max_slot[char.level-1],char)
                
    # MONK
    elif char.clas.clas == "Monk":
        mart_dice = [4,4,4,4,6,6,6,6,6,6,8,8,8,8,8,8,10,10,10,10]
        char.clas.core["Martial Arts Die"] = "1d" + str(mart_dice[char.level-1])
        char.clas.core["Unarmored Defense"] = ["dexterity", "wisdom"]
        char.update()
        char.clas.feats += ["Martial Arts"]
        if char.level > 1:
            char.clas.core["Ki"] = char.level
            una_mov = [0,10,10,10,10,15,15,15,15,20,20,20,20,25,25,25,25,30,30,30]
            char.clas.core["Unarmored Movement"] = una_mov[char.level-1]
            char.update()
        if char.level > 2:
            char.clas.feats += ["Deflect Missiles"]
            if char.clas.subclas == "Open Hand":
                char.clas.feats += ["Open Hand Technique"]
            elif char.clas.subclas == "Shadow":
                char.spells["0"] += ["minor illusion"]
                char.clas.feats += ["Shadow Arts"]
            elif char.clas.subclas == "Four Elements":
                disciplines = ["fangs of the fire snake","fist of four thunders","fist of unbroken air","rush of the gale spirits","shape the flowing river","sweeping cinder strike","water whip"]
                char.clas.core["Elemental Disciplines"] = ["elemental attunement"]
                disc_num = 1
        if char.level > 3:
            level4(char)
            char.clas.feats += ["Slow Fall"]
        if char.level > 4:
            char.clas.feats += ["Extra Attack", "Stunning Strike"]
        if char.level > 5:
            char.clas.feats += ["Ki-Empowered Strikes"]
            if char.clas.subclas == "Open Hand":
                char.clas.feats += ["Wholeness of Body"]
            elif char.clas.subclas == "Shadow":
                char.clas.feats += ["Shadow Step"]
            elif char.clas.subclas == "Four Elements":
                disc_num += 1
        if char.level > 6:
            char.clas.feats += ["Evasion", "Stillness of Mind"]
        if char.level > 7:
            level4(char)
        if char.level > 9:
            char.clas.feats += ["Purity of Body"]
        if char.level > 10:
            if char.clas.subclas == "Open Hand":
                char.clas.feats += ["Tranquility"]
            elif char.clas.subclas == "Shadow":
                char.clas.feats += ["Cloak of Shadows"]
            elif char.clas.subclas == "Four Elements":
                disc_num += 1
        if char.level > 11:
            level4(char)
        if char.level > 12:
            char.clas.feats += ["Tongue of the Sun and Moon"]
        if char.level > 13:
            char.clas.feats += ["Diamond Soul"]
            char.clas.savingthrows = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        if char.level > 14:
            char.clas.feats += ["Timeless Body"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            if char.clas.subclas == "Open Hand":
                char.clas.feats += ["Quivering Palm"]
            elif char.clas.subclas == "Shadow":
                char.clas.feats += ["Opportunist"]
            elif char.clas.subclas == "Four Elements":
                disc_num += 1
        if char.level > 17:
            char.clas.feats += ["Empty Body"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Perfect Self"]
        if char.clas.subclas == "Four Elements":
            char.clas.core["Elemental Disciplines"] += random.sample(disciplines,disc_num)
            
    # PALADIN
    elif char.clas.clas == "Paladin":
        char.clas.core["Lay on Hands"] = 5 * char.level
        char.clas.feats += ["Divine Sense"]
        if char.level > 1:
            char.clas.core["Fighting Style"] = random.choice(["Defense","Dueling","Great Weapon Fighting","Protection"])
            char.clas.feats += ["Divine Smite"]
            spell_list = import_spell_lists(char.clas.clas, char.books)
            char.clas.core["Spellcasting"] = "charisma"
            char.clas.core["Spells known"] = max([char.statmods.charisma + char.level//2, 1])
        if char.level > 2:
            char.clas.feats += ["Divine Health"]
            if char.clas.subclas == "Devotion":
                char.spells["1"] += ["protection from evil and good","sanctuary"]
                char.clas.feats += ["Channel Divinity: Sacred Weapon","Channel Divinity: Turn the Unholy"]
            elif char.clas.subclas == "Ancients":
                char.spells["1"] += ["ensnaring strike","speak with animals"]
                char.clas.feats += ["Channel Divinity: Nature's Wrath","Channel Divinity: Turn the Faithless"]
            elif char.clas.subclas == "Vengeance":
                char.spells["1"] += ["bane","hunter's mark"]
                char.clas.feats += ["Channel Divinity: Abjure Enemy","Channel Divinity: Vow of Enmity"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Extra Attack"]
            if char.clas.subclas == "Devotion":
                char.spells["2"] += ["lesser restoration", "zone of truth"]
            elif char.clas.subclas == "Ancients":
                char.spells["2"] += ["moonbeam", "misty step"]
            elif char.clas.subclas == "Vengeance":
                char.spells["2"] += ["hold person", "misty step"]
        if char.level > 5:
            char.clas.core["Aura of Protection"] = "10 feet"
        if char.level > 6:
            if char.clas.subclas == "Devotion":
                char.clas.core["Aura of Devotion"] = "10 feet"
            elif char.clas.subclas == "Ancients":
                char.clas.core["Aura of Warding"] = "10 feet"
            elif char.clas.subclas == "Vengeance":
                char.clas.feats += ["Relentless Avenger"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            if char.clas.subclas == "Devotion":
                char.spells["3"] += ["beacon of hope", "dispel magic"]
            elif char.clas.subclas == "Ancients":
                char.spells["3"] += ["plant growth", "protection from energy"]
            elif char.clas.subclas == "Vengeance":
                char.spells["3"] += ["haste", "protection from energy"]
        if char.level > 9:
            char.clas.core["Aura of Courage"] = "10 feet"
        if char.level > 10:
            char.clas.feats += ["Improved Divine Smite"]
        if char.level > 11:
            level4(char)
        if char.level > 12:
            if char.clas.subclas == "Devotion":
                char.spells["4"] += ["freedom of movement", "guardian of faith"]
            elif char.clas.subclas == "Ancients":
                char.spells["4"] += ["ice storm", "stoneskin"]
            elif char.clas.subclas == "Vengeance":
                char.spells["4"] += ["banishment", "dimension door"]
        if char.level > 13:
            char.clas.feats += ["Cleansing Touch"]
        if char.level > 14:
            if char.clas.subclas == "Devotion":
                char.clas.feats += ["Purity of Spirit"]
            elif char.clas.subclas == "Ancients":
                char.clas.feats += ["Undying Sentinel"]
            elif char.clas.subclas == "Vengeance":
                char.clas.feats += ["Soul of Vengeance"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            if char.clas.subclas == "Devotion":
                char.spells["5"] += ["commune", "flame strike"]
            elif char.clas.subclas == "Ancients":
                char.spells["5"] += ["commune with nature", "tree stride"]
            elif char.clas.subclas == "Vengeance":
                char.spells["5"] += ["hold monster", "scrying"]
        if char.level > 17:
            char.clas.core["Aura of Protection"] = "30 feet"
            char.clas.core["Aura of Courage"] = "30 feet"
            if char.clas.subclas == "Devotion":
                char.clas.core["Aura of Devotion"] = "30 feet"
            elif char.clas.subclas == "Ancients":
                char.clas.core["Aura of Warding"] = "30 feet"
        if char.level > 18:
            level4(char)
        if char.level > 19:
            if char.clas.subclas == "Devotion":
                char.clas.feats += ["Holy Nimbus"]
            elif char.clas.subclas == "Ancients":
                char.clas.feats += ["Elder Champion"]
            elif char.clas.subclas == "Vengeance":
                char.clas.feats += ["Avenging Angel"]
        if char.level > 1:
            choose_spells(spell_list, (char.level-1)//4 + 1, char)
        
    # RANGER
    elif char.clas.clas == "Ranger":
        enemies = ["aberrations","beasts","celestials","constructs","dragons","elementals","fey","fiends","giants","monstrosities","oozes","plants","undead","humanoids"]
        humanoids = ["humans","elves","dwarfs","gnomes","halflings","orcs","tieflings","goblins","kobolds","hobgoblins","bugbears","dragonborn","gnolls","aarakocra","genasi","gith","lizardfolk","werewolves","wererats","werebears"]
        languages = {"aberrations":["Deep Speech"],
                     "celestials":["Celestial"],
                     "dragons":["Draconic"],
                     "elementals":["Primordial"],
                     "fey":["Sylvan"],
                     "fiends":["Infernal","Abyssal"],
                     "giants":["Giant"],
                     "elves":["Elvish"],
                     "dwarfs":["Dwarvish"],
                     "gnomes":["Gnomish"],
                     "halflings":["Halfling"],
                     "orcs":["Orc"],
                     "tieflings":["Infernal"],
                     "goblins":["Goblin"],
                     "hobgoblins":["Goblin"],
                     "bugbears":["Goblin"],
                     "kobolds":["Draconic"],
                     "gnolls":["Gnoll"],
                     "aarakocra":["Aarakocra","Primordial"],
                     "genasi":["Primordial"],
                     "dragonborn":["Draconic"],
                     "lizardfolk":["Draconic"],
                     "gith":["Gith"],
                     "undead":[],
                     "monstrosities":[],
                     "plants":[],
                     "constructs":[],
                     "oozes":[],
                     "beasts":[]
                     }
        terrain = ["arctic","coast","desert","forest","grassland","mountain","swamp","underdark"]
        favor_roll = random.choice(enemies)
        if favor_roll == "humanoids":
            human_roll = random.sample(humanoids,2)
            char.clas.core["Favored Enemy"] = human_roll
            for r in human_roll:
                pos_lang = []
                if r in languages.keys():
                    pos_lang += unique_list(languages, char.languages)
        else:
            char.clas.core["Favored Enemy"] = [favor_roll]
            pos_lang = unique_list(languages[favor_roll],char.languages)
        if len(pos_lang) > 0:
            char.languages += random.sample(pos_lang,1)
        char.clas.core["Natural Explorer"] = [random.choice(terrain)]
        if char.level > 1:
            spell_list = import_spell_lists(char.clas.clas, char.books)
            spells = [0,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]
            char.clas.core["Spellcasting"] = "wisdom"
            char.clas.core["Spells known"] = spells[char.level-1]
            if char.stats.strength > char.stats.dexterity:
                char.clas.core["Fighting Style"] = random.choice(["Defense","Dueling"])
            else:
                char.clas.core["Fighting Style"] = random.choice(["Archery","Defense","Dueling","Two-Weapon Fighting"])
        if char.level > 2:
            char.clas.feats += ["Primeval Awareness"]
            if char.clas.subclas == "Hunter":
                prey = random.choice(["Colossus Slayer", "Giant Killer", "Horde Breaker"])
                char.clas.feats += ["Hunter's Prey: " + prey]
            elif char.clas.subclas == "Beast Master":
                pet = random.choice(["Boar","Constrictor Snake","Mastiff","Mule","Panther","Poisonous Snake","Wolf","Axe Beak","Blood Hawk","Camel","Flying Snake","Giant Badger","Giant Bat","Giant Centipede","Giant Crab","Giant Frog","Giant Lizard","Giant Owl","Giant Poisonous Snake","Giant Rat","Giant Weasel","Giant Wolf Spider"])
                char.clas.core["Ranger's Companion"] = pet
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Extra Attack"]
        if char.level > 5:
            favor_roll = random.choice(unique_list(enemies, char.clas.core["Favored Enemy"]))
            if favor_roll == "humanoids":
                human_roll = random.sample(unique_list(humanoids,char.clas.core["Favored Enemy"]),2)
                char.clas.core["Favored Enemy"] += human_roll
                for r in human_roll:
                    pos_lang = []
                    if r in languages.keys():
                        pos_lang += unique_list(languages, char.languages)
            else:
                char.clas.core["Favored Enemy"] += [favor_roll]
                pos_lang = unique_list(languages,char.languages)
            if len(pos_lang) > 0:
                char.languages += random.sample(pos_lang,1)
            char.clas.core["Natural Explorer"] += [random.choice(unique_list(terrain,char.clas.core["Natural Explorer"]))]
        if char.level > 6:
            if char.clas.subclas == "Hunter":
                tactic = random.choice(["Escape the Horde", "Multiattack Defense", "Steel Will"])
                char.clas.feats += ["Defensive Tactics: " + tactic]
            elif char.clas.subclas == "Beast Master":
                char.clas.feats += ["Exceptional Training"]
        if char.level > 7:
            level4(char)
            char.clas.feats += ["Land's Stride"]
        if char.level > 9:
            char.clas.core["Natural Explorer"] += [random.choice(unique_list(terrain,char.clas.core["Natural Explorer"]))]
            char.clas.feats += ["Hide in Plain Sight"]
        if char.level > 10:
            if char.clas.subclas == "Hunter":
                if char.stats.strength > char.stats.dexterity:
                    attack = "Whirlwind Attack"
                elif char.stats.dexterity > char.stats.strength:
                    attack = "Volley"
                else:
                    attack = random.choice(["Volley", "Whirlwind Attack"])
                char.clas.feats += ["Multiattack: " + attack]
            elif char.clas.subclas == "Beast Master":
                char.clas.feats += ["Bestial Fury"]
        if char.level > 11:
            level4(char)
        if char.level > 13:
            char.clas.feats += ["Vanish"]
            favor_roll = random.choice(unique_list(enemies, char.clas.core["Favored Enemy"]))
            if favor_roll == "humanoids":
                human_roll = random.sample(unique_list(humanoids,char.clas.core["Favored Enemy"]),2)
                char.clas.core["Favored Enemy"] += human_roll
                for r in human_roll:
                    pos_lang = []
                    if r in languages.keys():
                        pos_lang += unique_list(languages, char.languages)
            else:
                char.clas.core["Favored Enemy"] += [favor_roll]
                pos_lang = unique_list(languages,char.languages)
            if len(pos_lang) > 0:
                char.languages += random.sample(pos_lang,1)
        if char.level > 14:
            if char.clas.subclas == "Hunter":
                defense = random.choice(["Evasion", "Stand Against the Tide", "Uncanny Dodge"])
                char.clas.feats += ["Superior Hunter's Defense: " + defense]
            elif char.clas.subclas == "Beast Master":
                char.clas.feats += ["Share Spells"]
        if char.level > 15:
            level4(char)
        if char.level > 17:
            char.clas.feats += ["Feral Senses"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Foe Slayer"]
        if char.level > 1:
            choose_spells(spell_list, (char.level-1)//4 + 1,char)
    
    # ROGUE    
    elif char.clas.clas == "Rogue":
        char.clas.core["Sneak Attack"] = str((char.level+1)//2) + "d6"
        char.skill_expert += random.sample(char.skill_prof, 2)
        char.update()
        char.languages += ["Thieves' Cant"]
        if char.level > 1:
            char.clas.feats += ["Cunning Action"]
        if char.level > 2:
            if char.clas.subclas == "Thief":
                char.clas.feats += ["Fast Hands","Second-Story Work"]
            elif char.clas.subclas == "Assassin":
                char.tool_prof += unique_list(["disguise kit","poisoner's kit"],char.tool_prof)
                char.clas.feats += ["Assassinate"]
            elif char.clas.subclas == "Arcane Trickster":
                spell_list = import_spell_lists(char.clas.clas, char.books)
                wiz_list = import_spell_lists("wizard", char.books)
                cants = [0,0,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4]
                spells = [0,0,3,4,4,4,5,6,6,7,8,8,9,10,10,11,11,11,12,13]
                wiz_spells = 1
                max_slot = [0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4]
                char.clas.core["Spellcasting"] = "intelligence"
                char.clas.core["Cantrips known"] = cants[char.level-1] - 1
                char.clas.core["Spells known"] = spells[char.level-1]
                char.spells["0"] += ["mage hand"]
                char.clas.feats += ["Mage Hand Legerdemain"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            char.clas.feats += ["Uncanny Dodge"]
        if char.level > 5:
            char.skill_expert += random.sample(unique_list(char.skill_prof, char.skill_expert), 2)
        if char.level > 6:
            char.clas.feats += ["Evasion"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            if char.clas.subclas == "Thief":
                char.clas.feats += ["Supreme Sneak"]
            elif char.clas.subclas == "Assassin":
                char.clas.feats += ["Infilitration Expertise"]
            elif char.clas.subclas == "Arcane Trickster":
                char.clas.feats += ["Magical Ambush"]
        if char.level > 9:
            level4(char)
        if char.level > 10:
            char.clas.feats += ["Reliable Talent"]
        if char.level > 11:
            level4(char)
        if char.level > 12:
            if char.clas.subclas == "Thief":
                char.clas.feats += ["Use Magic Device"]
            elif char.clas.subclas == "Assassin":
                char.clas.feats += ["Impostor"]
            elif char.clas.subclas == "Arcane Trickster":
                char.clas.feats += ["Versatile Trickster"]
        if char.level > 13:
            char.clas.feats += ["Blindsense"]
        if char.level > 14:
            char.clas.feats += ["Slippery Mind"]
            if "wisdom" not in char.clas.savingthrows:
                char.clas.savingthrows += ["wisdom"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            if char.clas.subclas == "Thief":
                char.clas.feats += ["Thief's Reflexes"]
            elif char.clas.subclas == "Assassin":
                char.clas.feats += ["Death Strike"]
            elif char.clas.subclas == "Arcane Trickster":
                char.clas.feats += ["Spell Thief"]
        if char.level > 17:
            char.clas.feats += ["Elusive"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Stroke of Luck"]
        if char.clas.subclas == "Arcane Trickster":
            choose_cantrips(wiz_list,char)
            choose_spells(spell_list, max_slot[char.level-1], char,num=char.clas.core["Spells known"]-wiz_spells)
            choose_spells(wiz_list, max_slot[char.level-1], char, num=wiz_spells)
        
    # SORCERER
    elif char.clas.clas == "Sorcerer":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6]
        spells = [2,3,4,5,6,7,8,9,10,11,12,12,13,13,14,14,15,15,15,15]
        char.clas.core["Spellcasting"] = "charisma"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = spells[char.level-1]
        if char.clas.subclas == "Draconic":
            colors = ["Black","Blue","Brass","Bronze","Copper","Gold","Green","Red","Silver","White"]
            types = ["Acid","Lightning","Fire","Lightning","Acid","Fire","Poison","Fire","Cold","Cold"]
            color_roll = random.randint(0,len(colors)-1)
            color = colors[color_roll]
            typ = types[color_roll]
            char.languages += unique_list(["Draconic"], char.languages)
            char.clas.core["Draconic Ancestor"] = color
            char.extra_hp += char.level
            char.clas.core["Draconic Resilience"] = 13 + char.statmods.dexterity
        elif char.clas.subclas == "Wild Magic":
            char.clas.feats += ["Wild Magic Surge", "Tides of Chaos"]
        if char.level > 1:
            char.clas.core["Sorcery Points"] = char.level
        if char.level > 2:
            metamagics = ["Careful Spell", "Distant Spell", "Empowered Spell", "Extended Spell", "Heightened Spell", "Quickened Spell", "Subtle Spell", "Twinned Spell"]
            char.clas.core["Metamagic"] = random.sample(metamagics,2)
        if char.level > 3:
            level4(char)
        if char.level > 5:
            if char.clas.subclas == "Draconic":
                char.clas.core["Elemental Affinity"] = typ
            elif char.clas.subclas == "Wild Magic":
                char.clas.feats += ["Bend Luck"]
        if char.level > 7:
            level4(char)
        if char.level > 9:
            char.clas.core["Metamagic"] += random.sample(unique_list(metamagics,char.clas.core["Metamagic"]),1)
        if char.level > 11:
            level4(char)
        if char.level > 13:
            if char.clas.subclas == "Draconic":
                char.clas.feats += ["Dragon Wings"]
            elif char.clas.subclas == "Wild Magic":
                char.clas.feats += ["Controlled Chaos"]
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.core["Metamagic"] += random.sample(unique_list(metamagics,char.clas.core["Metamagic"]),1)
        if char.level > 17:
            if char.clas.subclas == "Draconic":
                char.clas.feats += ["Draconic Presence"]
            elif char.clas.subclas == "Wild Magic":
                char.clas.feats += ["Spell Bombardment"]
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Sorcerous Restoration"]
        choose_cantrips(spell_list, char)
        choose_spells(spell_list, int(min([9,(char.level+1)//2])), char)

    # WARLOCK
    elif char.clas.clas == "Warlock":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4]
        spells = [2,3,4,5,6,7,8,9,10,10,11,11,12,12,13,13,14,14,15,15]
        char.clas.core["Pact Magic"] = "charisma"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = spells[char.level-1]
        char.clas.core["Slot Level"] = int(min([5,(char.level+1)//2]))
        if char.clas.subclas == "Archfey":
            spell_list["1"] += ["faerie fire","sleep"]
            char.clas.feats += ["Fey Presence"]
        elif char.clas.subclas == "Fiend":
            spell_list["1"] += ["burning hands","command"]
            char.clas.feats += ["Dark One's Blessing"]
        elif char.clas.subclas == "Great Old One":
            spell_list["1"] += ["dissonant whispers","tasha's hideous laughter"]
            char.clas.feats += ["Awakened Mind"]
        if char.level > 1:
            invos = [0,2,2,2,3,3,4,4,5,5,5,6,6,6,7,7,7,8,8,8]
            char.clas.core["Invocations known"] = invos[char.level-1]
            char.clas.core["Eldritch Invocations"] = []
        if char.level > 2:
            pact = random.choice(["Pact of the Chain", "Pact of the Blade", "Pact of the Tome"])
            char.clas.core["Pact Boon"] = pact
            if pact == "Pact of the Chain":
                char.spells["1"] += ["find familiar"]
            if char.clas.subclas == "Archfey":
                spell_list["2"] += ["calm emotions", "phantasmal force"]
            elif char.clas.subclas == "Fiend":
                spell_list["2"] += ["blindness/deafness", "scorching ray"]
            elif char.clas.subclas == "Great Old One":
                spell_list["2"] += ["detect thoughts", "phantasmal force"]
        if char.level > 3:
            level4(char)
        if char.level > 4:
            if char.clas.subclas == "Archfey":
                spell_list["3"] += ["blink", "plant growth"]
            elif char.clas.subclas == "Fiend":
                spell_list["3"] += ["fireball", "stinking cloud"]
            elif char.clas.subclas == "Great Old One":
                spell_list["3"] += ["clairvoyance", "sending"]
        if char.level > 5:
            if char.clas.subclas == "Archfey":
                char.clas.feats += ["Misty Escape"]
            elif char.clas.subclas == "Fiend":
                char.clas.feats += ["Dark One's Own Luck"]
            elif char.clas.subclas == "Great Old One":
                char.clas.feats += ["Entropic Ward"]
        if char.level > 6:
            if char.clas.subclas == "Archfey":
                spell_list["4"] += ["dominate beast", "greater invisibility"]
            elif char.clas.subclas == "Fiend":
                spell_list["4"] += ["fire shield", "wall of fire"]
            elif char.clas.subclas == "Great Old One":
                spell_list["4"] += ["dominate beast", "evard's black tentacles"]
        if char.level > 7:
            level4(char)
        if char.level > 8:
            if char.clas.subclas == "Archfey":
                spell_list["5"] += ["dominate person", "seeming"]
            elif char.clas.subclas == "Fiend":
                spell_list["5"] += ["flame strike", "hallow"]
            elif char.clas.subclas == "Great Old One":
                spell_list["5"] += ["dominate person", "telekinesis"]
        if char.level > 9:
            if char.clas.subclas == "Archfey":
                char.clas.feats += ["Beguiling Defenses"]
            elif char.clas.subclas == "Fiend":
                char.clas.feats += ["Fiendish Resilience"]
            elif char.clas.subclas == "Great Old One":
                char.clas.feats += ["Thought Shield"]
        if char.level > 10:
            char.clas.core["Mystic Arcanum (6th level)"] = random.choice(spell_list["6"])
        if char.level > 11:
            level4(char)
        if char.level > 12:
            char.clas.core["Mystic Arcanum (7th level)"] = random.choice(spell_list["7"])
        if char.level > 13:
            if char.clas.subclas == "Archfey":
                char.clas.feats += ["Dark Delirium"]
            elif char.clas.subclas == "Fiend":
                char.clas.feats += ["Hurl Through Hell"]
            elif char.clas.subclas == "Great Old One":
                char.clas.feats += ["Create Thrall"]
        if char.level > 14:
            char.clas.core["Mystic Arcanum (8th level)"] = random.choice(spell_list["8"])
        if char.level > 15:
            level4(char)
        if char.level > 16:
            char.clas.core["Mystic Arcanum (9th level)"] = random.choice(spell_list["9"])
        if char.level > 18:
            level4(char)
        if char.level > 19:
            char.clas.feats += ["Eldritch Master"]
        choose_cantrips(spell_list, char)
        choose_spells(spell_list, char.clas.core["Slot Level"], char)
        if char.level > 2 and pact == "Pact of the Tome":
            cant_clas = random.choice(["bard", "cleric", "druid", "sorcerer", "wizard"])
            choose_cantrips(import_spell_lists(cant_clas, char.books),char,num=3)
        choose_invocations(char)
        
    # WIZARD
    elif char.clas.clas == "Wizard":
        spell_list = import_spell_lists(char.clas.clas, char.books)
        cants = [3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5]
        char.clas.core["Spellcasting"] = "intelligence"
        char.clas.core["Cantrips known"] = cants[char.level-1]
        char.clas.core["Spells known"] = 6 + ((char.level-1)*2)
        char.clas.core["Spells prepared"] = max([1,char.level + char.statmods.intelligence])
        char.clas.core["Arcane Recovery"] = int((char.level+1)//2)
        if char.level > 1:
            char.clas.feats += [char.clas.subclas + " Savant"]
            if char.clas.subclas == "Abjuration":
                char.clas.feats += ["Arcane Ward"]
            elif char.clas.subclas == "Conjuration":
                char.clas.feats += ["Minor Conjuration"]
            elif char.clas.subclas == "Divination":
                char.clas.feats += ["Portent"]
            elif char.clas.subclas == "Enchantment":
                char.clas.feats += ["Hypnotic Gaze"]
            elif char.clas.subclas == "Evocation":
                char.clas.feats += ["Sculpt Spells"]
            elif char.clas.subclas == "Illusion":
                char.clas.feats += ["Improved Minor Illusion"]
                if "minor illusion" not in char.spells["0"]:
                    char.spells["0"] += ["minor illusion"]
                else:
                    char.spells["0"] += [random.choice(unique_list(spell_list["0"], char.spells["0"]))]
            elif char.clas.subclas == "Necromancy":
                char.clas.feats += ["Grim Harvest"]
            elif char.clas.subclas == "Transmutation":
                char.clas.feats += ["Minor Alchemy"]
        if char.level > 3:
            level4(char)
        if char.level > 5:
            if char.clas.subclas == "Abjuration":
                char.clas.feats += ["Projected Ward"]
            elif char.clas.subclas == "Conjuration":
                char.clas.feats += ["Benign Transposition"]
            elif char.clas.subclas == "Divination":
                char.clas.feats += ["Expert Divination"]
            elif char.clas.subclas == "Enchantment":
                char.clas.feats += ["Instinctive Charm"]
            elif char.clas.subclas == "Evocation":
                char.clas.feats += ["Potent Cantrip"]
            elif char.clas.subclas == "Illusion":
                char.clas.feats += ["Malleable Illusions"]
            elif char.clas.subclas == "Necromancy":
                char.clas.feats += ["Undead Thralls"]
            elif char.clas.subclas == "Transmutation":
                char.clas.feats += ["Transmuter's Stone"]
        if char.level > 7:
            level4(char)
        if char.level > 9:
            if char.clas.subclas == "Abjuration":
                char.clas.feats += ["Improved Abjuration"]
            elif char.clas.subclas == "Conjuration":
                char.clas.feats += ["Focused Conjuration"]
            elif char.clas.subclas == "Divination":
                char.clas.feats += ["The Third Eye"]
            elif char.clas.subclas == "Enchantment":
                char.clas.feats += ["Split Enchantment"]
            elif char.clas.subclas == "Evocation":
                char.clas.feats += ["Empowered Evocation"]
            elif char.clas.subclas == "Illusion":
                char.clas.feats += ["Illusory Self"]
            elif char.clas.subclas == "Necromancy":
                char.clas.feats += ["Inured to Undeath"]
            elif char.clas.subclas == "Transmutation":
                char.clas.feats += ["Shapechanger"]
        if char.level > 11:
            level4(char)
        if char.level > 13:
            char.clas.feats += [char.clas.subclas + " Savant"]
            if char.clas.subclas == "Abjuration":
                char.clas.feats += ["Spell Resistance"]
            elif char.clas.subclas == "Conjuration":
                char.clas.feats += ["Durable Summons"]
            elif char.clas.subclas == "Divination":
                char.clas.feats += ["Greater Portent"]
            elif char.clas.subclas == "Enchantment":
                char.clas.feats += ["Alter Memories"]
            elif char.clas.subclas == "Evocation":
                char.clas.feats += ["Overchannel"]
            elif char.clas.subclas == "Illusion":
                char.clas.feats += ["Illusory Reality"]
            elif char.clas.subclas == "Necromancy":
                char.clas.feats += ["Command Undead"]
            elif char.clas.subclas == "Transmutation":
                char.clas.feats += ["Master Transmuter"]
        if char.level > 15:
            level4(char)
        if char.level > 18:
            level4(char)
        choose_cantrips(spell_list,char)
        choose_spells(spell_list, int(min([9,(char.level+1)//2])),char)
        if char.level > 17:
            char.clas.core["Spell Mastery"] = [random.choice(char.spells["1"]),random.choice(char.spells["2"])]
        if char.level > 19:
            char.clas.core["Signature Spell"] = random.sample(char.spells["3"],2)
            
            
    return char