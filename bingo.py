from selenium import webdriver
from tkinter import simpledialog
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import copy

def replace_obj(obj):
    static_obj = {}
    static_obj["Unequip a cursed item"] = [[]]
    static_obj["Talk to a hint NPC"] = [["whirlwind"], ["reveal"], ["pound", "lash", "scoop"], ["grind"]]
    static_obj["Drain the underground lake in Mikasalla"] = [["scoop", "parch"]]
    static_obj["Use the Ruin Key"] = [["reveal", "ruin key"]]
    static_obj["Mind Read the cow in Lemuria"] = [["grind", "mind read", "growth"], ["trident", "mind read", "growth", "$hasDjinn|24"]]
    static_obj["Use the cannon in Loho"] = [["magma ball", "grind"]]
    static_obj["Fix a rusted weapon"] = [["rusty"]] #plz work
    static_obj["Forge with a Tear Stone"] = [["tear stone"]]
    static_obj["Forge with Dragon Skin"] = [["dragon skin"]]
    static_obj["Forge with a Salamander Tail"] = [["salamander tail"]]
    static_obj["Forge with a Sylph Feather"] = [["sylph feather"]]
    static_obj["Forge with Orihalcon"] = [["orihalcon"]]
    static_obj["Forge with a Golem Core"] = [["golem core"]]
    static_obj["Forge with Mythril Silver"] = [["mythril silver"]]
    static_obj["Forge with Dark Matter"] = [["dark matter"]]
    static_obj["Obtain a Potion"] = [["potion"]] #might cause issues with mist potion
    static_obj["Obtain a Water of Life"] = [[]]
    static_obj["Obtain the Black Crystal"] = [["black crystal"]]
    static_obj["Obtain the Mysterious Card"] = [["mysterious card"]]
    static_obj["Obtain the Trainer's Whip"] = [["trainer's whip"]]
    static_obj["Obtain the Tomegathericon"] = [["tomegathericon"]]
    static_obj["Obtain the Trident"] = [["trident"]]
    static_obj["Obtain the Corn"] = [["corn"]] #unicorn ring issues?
    static_obj["Obtain the Laughing or Healing Fungus"] = [["fungus"]] #plz work
    static_obj["Obtain the Mars Star"] = [["mars star"]]
    static_obj["Defeat Briggs"] = [["hasDjinn|6"]]
    static_obj["Defeat the Chest Beaters"] = [["whirlwind"]]
    static_obj["Defeat King Scorpion"] = [["pound"]]
    static_obj["Defeat Aqua Hydra"] = [["frost", "hasDjinn|10"]]
    static_obj["Defeat Serpent"] = [["dancing idol", "cyclone", "growth", "hasDjinn|24"], \
                                    ["dancing idol", "cyclone", "growth", "whirlwind", "hasDjinn|16"]]
    static_obj["Defeat Avimander"] = [["pound", "lash", "burst", "hasDjinn|20"]]
    static_obj["Defeat Poseidon"] = [["grind", "hasDjinn|24"]]
    static_obj["Defeat the Flame Dragons"] = [["teleport", "blaze", "magma ball", "pound", "burst", "grind","hasDjinn|48"]]
    static_obj["Defeat Moapa and co."] = [["grind", "whirlwind", "shaman", "hasDjinn|28"]]
    static_obj["Collect the Tremor Bit chest"] = [["reveal"]]
    static_obj["Collect the Lemuria fountain item"] = [["grind"]]
    static_obj["Collect the item on the Dancing Idol pedestal"] = [["whirlwind", "reveal"]]
    static_obj["Collect the chest in Gondowan Settlement"] = [["grind", "cyclone"]]
    static_obj["Collect the chest in Hesperia Settlement"] = [["grind", "growth"]]
    static_obj["Collect the chest in SW Atteka Islet"] = [["grind"]]
    static_obj["Collect the item in both Indra and Osenia Cavern"] = [["scoop", "lash"]]
    static_obj["Collect the Izumo summon tablet"] = [["parch", "pound", "sand", "reveal", "frost"]]
    static_obj["Collect the Teleport Lapis chest"] = [["pound","burst","blaze"], ["pound","burst","teleport"]]
    static_obj["Collect the Angara Cavern summon tablet"] = [["grind", "carry"]]
    static_obj["Enter the boss room in Yampi Desert Cave"] = [["sand", "burst", "pound", "teleport"]]
    static_obj["Enter the boss room in Treasure Isle"] = [["grind", "lift"]]
    static_obj["Enter the boss room in Islet Cave"] = [["mind read", "li'l", "teleport"]]
    static_obj["Learn Sand"] = [["sand"]]
    static_obj["Learn Mind Read + Reveal"] = [["mind read", "reveal"]]
    static_obj["Learn Frost + Douse"] = [["frost", "douse"]]
    static_obj["Learn Growth + Whirlwind"] = [["growth", "whirlwind"]]
    static_obj["Learn Burst + Parch"] = [["burst", "parch"]]
    static_obj["Learn Cyclone + Hover"] = [["cyclone", "hover"]]
    static_obj["Learn Tremor + Catch"] = [["tremor", "catch"]]
    static_obj["Learn Teleport"] = [["teleport"]]
    static_obj["Learn Blaze"] = [["blaze"]]
    static_obj["Learn Force"] = [["force"]]
    static_obj["Learn both Lift and Carry"] = [["lift", "carry"]]
    static_obj["Befriend the Djinni in Taopo Swamp"] = [["whirlwind"]]
    static_obj["Befriend the Djinni in Aqua Rock"] = [["douse", "parch"]]
    static_obj["Befriend the Djinni in Apojii Islands"] = [["sand", "whirlwind"]]
    static_obj["Defeat all overworld Djinn (6)"] = [["grind"]]
    static_obj["Befriend the Djinni in SW Atteka Islet"] = [["lift"]]
    static_obj["Befriend the Djinni in Gabomba Catacombs"] = [["pound", "lash", "scoop", "cyclone"]]
    static_obj["Befriend the Djinni in Lemuria"] = [["grind", "tremor", "cyclone"]]
    static_obj["Befriend both Djinn in Contigo"] = [["grind", "scoop", "force"]]
    static_obj["Befriend the Djinni in Trial Road"] = [["grind", "shaman", "whirlwind", "hover", "lift"]]
    static_obj["Befriend the Djinni in Yampi Desert Cave"] = [["scoop", "burst", "teleport", "sand"]]
    static_obj["Enter Air Rock's tablet room"] = [["whirlwind"]]
    static_obj["Collect the Air's Rock summon tablet"] = [["whirlwind"]]
    static_obj["Collect the Fujin Shield chest"] = [["whirlwind"]]
    static_obj["Learn Zagan or Haures"] = [["zagan"], ["haures"]]
    static_obj["Learn Megaera or Flora"] = [["megaera"], ["flora"]]
    static_obj["Learn Moloch or Ulysses"] = [["moloch"], ["ulysses"]]
    static_obj["Learn Eclipse or Coatlicue"] = [["eclipse"], ["coatlicue"]]
    static_obj["Learn the Daedalus summon"] = [["daedalus"]]
    static_obj["Learn the Catastrophe summon"] = [["catastrophe"]]
    static_obj["Learn the Azul summon"] = [["azul"]]
    static_obj["Obtain Fire Brand or Sol Blade"] = [["fire brand"], ["sol blade"]]
    static_obj["Obtain Meditation Rod or Thanatos Mace"] = [["meditation rod"], ["thanatos mace"]]
    static_obj["Obtain Masamune or Phaeton's Blade"] = [["masamune"], ["phaeton"]]
    static_obj["Obtain the Erinyes' Tunic"] = [["erinyes"]]
    static_obj["Obtain the Iris Robe"] = [["iris robe"]]
    static_obj["Obtain the Alastor's Hood"] = [["alastor"]]
    static_obj["Obtain the Fujin Shield"] = [["fujin"]]
    static_obj["Obtain the Jester's Armlet"] = [["jester"]]
    static_obj["Obtain the Valkyrie Mail"] = [["valkyrie"]]
    static_obj["Defeat each Doomsayer-type enemy (2)"] = [["lash", "scoop", "grind"]]
    static_obj["Defeat each Assassin-type enemy (2)"] = [["grind"]]
    static_obj["Defeat each Merman-type enemy (3)"] = [["grind", "lift"]]
    static_obj["Defeat a Phoenix-type enemy"] = [["grind"], ["li'l", "mind read", "teleport"]] 
    static_obj["Defeat each Roc-type enemy (2)"] = [["grind", "magma ball"]]
    static_obj["Defeat a Blue Dragon-type enemy"] = [["li'l", "mind read", "teleport"], \
                                                     ["grind", "cyclone", "hover", "red key"], \
                                                     ["grind", "cyclone", "hover", "blue key", "reveal"]]
    static_obj["Defeat an Aka Manah-type enemy"] = [["li'l", "mind read", "teleport"], \
                                                    ["teleport", "reveal", "blaze", "burst", "pound", "magma ball", "grind"]]
    static_obj["Defeat each Sea Dragon-type enemy (3)"] = [["douse", "grind", "lift"]]
    static_obj["Reach the top of Tundaria Tower"] = [["parch", "pound", "reveal"]]
    static_obj["Reach the top of Shrine of the Sea God"] = [["tear", "frost", "lash"]]
    static_obj["Reach the top of Ankohl Ruins"] = [["whirlwind", "sand", "reveal"]]
    static_obj["Enter Aqua Rock's tablet room"] = [["douse", "frost", "aquarius"], ["douse", "parch", "aquarius"]]
    static_obj["Clear Gabomba Statue"] = [["lash", "pound", "scoop"]]
    static_obj["Enter the innermost room of Taopo Swamp"] = [["tremor", "douse", "frost", "whirlwind", "growth"]]
    static_obj["Enter Magma Rock's tablet room"] = [["whirlwind", "growth", "burst", "lift", "grind"]]
    static_obj["Clear Jupiter Lighthouse"] = [["blue key", "red key", "reveal", "pound", "hover", "cyclone", "grind"]]
    static_obj["Own 2 boots"] = [[]] #alhafra + garoh shops. code below just in case
    #[["turtle boots"], ["golden boots"], ["ninja sandals"], ["knight's greave"],\
                                  #["silver greave"], ["reveal"]]


    djinn_obj = {}

    djinn_obj["Befriend 20 Djinn"] = ["count", 20, "total"]
    djinn_obj["Befriend 5 Venus Djinn"] = ["count", 5, "venus"]
    djinn_obj["Befriend 5 Mars Djinn"] = ["count", 5, "mars"]
    djinn_obj["Befriend 5 Jupiter Djinn"] = ["count", 5, "jupiter"]
    djinn_obj["Befriend 5 Mercury Djinn"] = ["count", 5, "mercury"]
    djinn_obj["Befriend 7 Venus Djinn"] = ["count", 7, "venus"]
    djinn_obj["Befriend 7 Mars Djinn"] = ["count", 7, "mars"]
    djinn_obj["Befriend 7 Jupiter Djinn"] = ["count", 7, "jupiter"]
    djinn_obj["Befriend 7 Mercury Djinn"] = ["count", 7, "mercury"]
    djinn_obj["Befriend Spritz, Flower or Crystal"] = ["specific", ["spritz", "flower", "crystal"]]
    djinn_obj["Befriend Granite, Flash or Shade"] = ["specific", ["granite", "flash", "shade"]]
    djinn_obj["Befriend Aroma, Ether or Ember"] = ["specific", ["aroma", "ether", "ember"]]
    djinn_obj["Befriend Zephyr, Coal or Vine"] = ["specific", ["zephyr", "coal", "vine"]]
    djinn_obj["Befriend Ground or Petra"] = ["specific", ["ground", "petra"]]
    djinn_obj["Befriend Lull or Kite"] = ["specific", ["lull", "kite"]]
    djinn_obj["Befriend Dew or Balm"] = ["specific", ["dew", "balm"]]
    djinn_obj["Befriend Corona or Kindle"] = ["specific", ["corona", "kindle"]]

    class_obj = {}
    class_obj["Have someone be an Ascetic"] = [["jupiter_c", 4, "mars"], ["mercury_c", 4, "mars"],\
                                               ["mars_c", 6, "jupiter"], ["mars_c", 6, "mercury"]]
    class_obj["Have someone be a Shaman"] = [["jupiter_c", 4, "venus"], ["mercury_c", 4, "venus"],\
                                               ["venus_c", 6, "jupiter"], ["venus_c", 6, "mercury"]]
    class_obj["Have someone be a Cavalier"] = [["venus_c", 4, "mercury"], ["mars_c", 4, "mercury"],\
                                               ["mercury_c", 6, "venus"], ["mercury_c", 6, "mars"]]
    class_obj["Have someone be an Enchanter"] = [["venus_c", 4, "jupiter"], ["mars_c", 4, "jupiter"],\
                                               ["jupiter_c", 6, "venus"], ["jupiter_c", 6, "mars"]]
    class_obj["Have someone be a Ninja"] = [["venus_c", 3, "jupiter", 3, "mars"], \
                                              ["mars_c", 3, "jupiter", 3, "venus"]]
    class_obj["Have someone be a Medium"] = [["mercury_c", 3, "jupiter", 3, "venus"], \
                                              ["jupiter_c", 3, "venus", 3, "mercury"]]
    class_obj["Have someone be a Ranger"] = [["mercury_c", 3, "jupiter", 3, "mars"], \
                                              ["jupiter_c", 3, "mars", 3, "mercury"]]
    class_obj["Have someone be a Dragoon"] = [["venus_c", 3, "mercury", 3, "mars"], \
                                              ["mars_c", 3, "mercury", 3, "venus"]]

    count_obj = {}
    count_obj["Defeat 3 Mad Plants"] = [3, "Mad Plant"]
    count_obj["Own 3 Lucky Medals"] = [3, "Lucky Medal"]
    count_obj["Own 3 Vials"] =  [3, "Vial"]
    count_obj["Own 2 shirts"] = [2, "shirt"] 
    count_obj["Own 2 rings"] = [2, "ring"]
    count_obj["Own 8 stat-boosting items"] = [8, "stats"]
    count_obj["Obtain 2 prongs"] = [2, "prong"]
    count_obj["Obtain 2 trading sequence items"] = [2, "trade"]
    count_obj["Obtain 2 keys"] = [2, "key"]
    count_obj["Own 2 Mist Potions"] = [2, "Mist Potion"]

    for i  in range(len(obj)):
        for j  in range(len(obj[i])):
            if obj[i][j] in static_obj.keys():
                obj[i][j] = static_obj[obj[i][j]]
            elif obj[i][j] in djinn_obj.keys():
                obj[i][j] = ["djinn", djinn_obj[obj[i][j]]]
            elif obj[i][j] in class_obj.keys():
                obj[i][j] = ["class", class_obj[obj[i][j]]]
            elif obj[i][j] in count_obj.keys():
                obj[i][j] = ["count", count_obj[obj[i][j]]]
    return obj

def credential(driver, url, password):
    #driver.set_window_position(2000, 100)
    #driver.maximize_window()

    #logging in
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.XPATH, "//input[@type='text']")))
    textfields = driver.find_elements(By.XPATH,"//input[@type='text']")
    passfield = driver.find_element(By.XPATH,"//input[@type='password']")
    specbox = driver.find_element(By.XPATH,"//input[@type='checkbox']")
    join_button = driver.find_element(By.XPATH,"//input[@type='submit']")
    for field in textfields:
        if not field.get_attribute("readonly"):
            field.send_keys("script")
    passfield.send_keys(password)
    specbox.click()
    join_button.click()

    # grabbing the objectives
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.CSS_SELECTOR, ".vertical-center.text-container")))
    objs = driver.find_elements(By.CSS_SELECTOR, ".vertical-center.text-container")
    objectives = [[]]
    index1 = 0
    counter = 0
    for obj in objs:
        if counter == 5:
            counter = 0
            objectives.append([])
            index1 += 1
        objectives[index1].append(obj.text)
        counter += 1
    return objectives
    
        
def get_obj():

    url = simpledialog.askstring("Bingo", "url")
    password = simpledialog.askstring("Bingo", "password")
    driver = webdriver.Chrome(ChromeDriverManager().install())

    obj = credential(driver, url, password)
    obj2 = copy.deepcopy(obj)
    obj2 = replace_obj(obj2)

    driver.close()
    driver.quit()
    
    return [obj, obj2]

def get_obj_fast(url, password):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    obj = credential(driver, url, password)
    obj2 = copy.deepcopy(obj)
    obj2 = replace_obj(obj2)

    driver.close()
    driver.quit()
    
    return [obj, obj2]

