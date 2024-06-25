import json
from bingo import get_obj_fast
from bingo import get_obj
import math
import copy

modes = ["pre-run", "post-run"]
mode = modes[0]
bingo_possible = False

isolate_spoiler = False

if mode == modes[0]:
    foundGrind = False
elif mode == modes[1]:
    foundGrind = True

if not isolate_spoiler:
    url = "https://bingosync.karanum.xyz/room/CBfwmhv9QwG1meY5R671wQ"
    passw = "khan"
    obj = get_obj_fast(url, passw)
    if mode == modes[1]:
        print(obj) 
    orig_obj = obj[0]
    obj = obj[1]
    obj_time = copy.deepcopy(obj)


f = open('locations.json', 'r')
data = json.load(f)
f.close()

f = open('spoilers.log', 'r')
spoiler_log = f.read()
f.close()

sphere_counter = 0
di = {}

in_exceptions = {}
in_exceptions["sand"] = ["Ninja Sandals"]
in_exceptions["briggs_jailbreak"] = ["briggs_battle"]
in_exceptions["red_cloth"] = ["Red Key"]
in_exceptions["red_key"] = ["Red Cloth"]
in_exceptions["Mars Star"] = ["mars_lit"]
in_exceptions["mars_lit"] = ["Mars Star"]
found_piers = False
found_reunion = False
def clean_access(lst):
    lst2 = []
    for item in lst:
        if not "sett_show_captures" in item and not "skips" in item and not "_hide_" in item:
            lst2.append(item)
    return lst2

def recurse(dic, access):
    if "children" not in dic:
        return
    if "access_rules" in dic:
        if not access:
            access = dic["access_rules"]
        else:
            lstn = []
            for a1 in access:
                for a2 in dic["access_rules"]:
                    strn = a1+","+a2
                    lstn.append(strn)
            access = lstn
    kids = dic["children"]
    if "sections" in dic:
        counter = 0
        for sect in dic["sections"]:
            skip = False
            if "visibility_rules" in sect:
                vis = sect["visibility_rules"]
                for rule in vis:
                    if "sett_mode_2" in rule:
                        skip = True
                        counter += 1
            if not skip:
                access2 = []
                if "access_rules" in sect:
                    if not access:
                        access2 = sect["access_rules"]
                    else:
                        for ru in access:
                            ru = clean_access([ru])
                            if len(ru) == 0:
                                continue
                            ru = ru[0]
                            for se in sect["access_rules"]:
                                se = clean_access([se])
                                if len(se) == 0 or se[0] in access:
                                    continue
                                se = se[0]
                                a2 = ru +","+ se
                                access2.append(a2)
                if len(access2) == 0:
                    if "access_rules" in sect:
                        access2 = sect["access_rules"]
                    else:
                        access2 = access
                        
                addrs = dic["children"][counter]
                addr = addrs["name"]
                name = sect["name"]
                caddr = clean_access(access2)

                for ad in addr.split(","):
                    di[ad.lower()] = [name, caddr]
                counter +=1

    for child in kids:
        recurse(child, clean_access(access))

def get_djinn(dic):
    global have_djinn
    global have_items2
    poop = []
    for k in dic.keys():
        if int(k, 16) < 48 or int(k, 16) >= 128 or k in have_djinn.keys():
            continue
        v = dic[k]
        if len(v[1]) == 0:
            have_djinn[k] = loc_items[v[0]]
            add_djinn(loc_items[v[0]])
            poop.append(k)
        for req in v[1]:
            if len(req) == 0:
                have_djinn[k] = loc_items[v[0]]
                add_djinn(loc_items[v[0]])
                poop.append(k)
                break
    for pp in poop:
        di.pop(pp)
                

def available_checks(dic):
    checks = {}
    for k in dic.keys():
        v = dic[k]
        if len(v[1]) == 0:
            checks[k] = v
        for req in v[1]:
            if len(req) == 0:
               checks[k] = v
    return checks

def removal():
    global have_items2
    for k in di.keys():
        atts = di[k]
        t_v = []
        for j in range(len(atts[1])):
            v = atts[1][j]
            #first we remove psynergy
            for item in have_items2.keys():
                for i in v:
                    frst = i.replace("_", " ").split()[0]
                    if frst.lower() in item.lower():
                        if i not in in_exceptions or item not in in_exceptions[i]:
                            c = v.count(i)
                            for j in range(c):
                                v.remove(i)
            #then we remove other requirements
            for i in v:
                if ("hasDjinn" in i):
                    num = int(i.split("|")[1])
                    if num <= djinn["total"]:
                        v.remove(i)
            t_v.append(v)
        di[k][1] = t_v
    
def special(v, k):
    global found_piers # probably redundant now
    global found_reunion #TODO remove
    global have_items
    global have_items2

    exclusive = []
    if v[0] == "Piers" and not found_piers:
        found_piers = True
        #piers items
        have_items["0x105"] = loc_items["0x105"]
        have_items["0x106"] = loc_items["0x106"]
        have_items2[loc_items["0x105"]] = have_items2.get(loc_items["0x105"], 0) + 1
        have_items2[loc_items["0x106"]] = have_items2.get(loc_items["0x106"], 0) + 1 

        have_classes.append(classes["Piers"])
        have_djinn["000"] = loc_items["Shade"]
        have_djinn["001"] = loc_items["Spring"]
        add_djinn(loc_items["Shade"])
        add_djinn(loc_items["Spring"])
        if k in di.keys():
            exclusive.append("0x105")
            exclusive.append("0x106")
            exclusive.append(k)
            di.pop(k)
        removal()
    #TODO maybe add trial road and gabomba here
    if v[0] == 'Briggs Fight':
        have_items[k] = "briggs_battle"
        have_items2["briggs_battle"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == 'Serpent Defeated':
        have_items[k] = "susa"
        have_items2["susa"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == 'Dwarven Cannon':
        have_items[k] = "cannon"
        have_items2["cannon"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == 'Briggs Jailbreak':
        have_items[k] = "briggs_jailbreak"
        have_items2["briggs_jailbreak"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == 'Jupiter Lighthouse Lit':
        have_items[k] = "jupiter_lit"
        have_items2["jupiter_lit"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == "Lighthouse Heated":
        have_items[k] = "mars_lit"
        have_items2["mars_lit"] = 1
        if k in di.keys():
            exclusive.append(k)
            di.pop(k)
        removal()
    if v[0] == 'Jupiter Lighthouse Lit' and not found_reunion:
        found_reunion = True
        if k in di.keys():
            exclusive.append("0x101")
            exclusive.append("0x102")
            exclusive.append("0x103")
            exclusive.append("0x104")
            exclusive.append(k)
            di.pop(k)
        #reunion items
        have_items["0x101"] = loc_items["0x101"]
        have_items["0x102"] = loc_items["0x102"]
        have_items["0x103"] = loc_items["0x103"]
        have_items["0x104"] = loc_items["0x104"]
        have_items2[loc_items["0x101"]] = have_items2.get(loc_items["0x101"], 0) + 1
        have_items2[loc_items["0x102"]] = have_items2.get(loc_items["0x102"], 0) + 1
        have_items2[loc_items["0x103"]] = have_items2.get(loc_items["0x103"], 0) + 1
        have_items2[loc_items["0x104"]] = have_items2.get(loc_items["0x104"], 0) + 1

        have_classes.append(classes["Isaac"])
        have_classes.append(classes["Garet"])
        have_classes.append(classes["Mia"])
        have_classes.append(classes["Ivan"])
        
        have_djinn["002"] = loc_items["Flint"]
        have_djinn["003"] = loc_items["Granite"]
        have_djinn["004"] = loc_items["Quartz"]
        have_djinn["005"] = loc_items["Vine"]
        have_djinn["006"] = loc_items["Sap"]
        have_djinn["007"] = loc_items["Ground"]
        add_djinn(loc_items["Flint"])
        add_djinn(loc_items["Granite"])
        add_djinn(loc_items["Quartz"])
        add_djinn(loc_items["Vine"])
        add_djinn(loc_items["Sap"])
        add_djinn(loc_items["Ground"])
        
        have_djinn["008"] = loc_items["Fizz"]
        have_djinn["009"] = loc_items["Sleet"]
        have_djinn["010"] = loc_items["Mist"]
        have_djinn["011"] = loc_items["Spritz"]
        have_djinn["012"] = loc_items["Hail"]
        have_djinn["013"] = loc_items["Tonic"]
        add_djinn(loc_items["Fizz"])
        add_djinn(loc_items["Sleet"])
        add_djinn(loc_items["Mist"])
        add_djinn(loc_items["Spritz"])
        add_djinn(loc_items["Hail"])
        add_djinn(loc_items["Tonic"])

        have_djinn["014"] = loc_items["Forge"]
        have_djinn["015"] = loc_items["Fever"]
        have_djinn["016"] = loc_items["Corona"]
        have_djinn["017"] = loc_items["Scorch"]
        have_djinn["018"] = loc_items["Ember"]
        have_djinn["019"] = loc_items["Flash"]
        add_djinn(loc_items["Forge"])
        add_djinn(loc_items["Fever"])
        add_djinn(loc_items["Corona"])
        add_djinn(loc_items["Scorch"])
        add_djinn(loc_items["Ember"])
        add_djinn(loc_items["Flash"])
        #skipping 20-21 cuz im lazy

        have_djinn["022"] = loc_items["Gust"]
        have_djinn["023"] = loc_items["Breeze"]
        have_djinn["024"] = loc_items["Zephyr"]
        have_djinn["025"] = loc_items["Smog"]
        have_djinn["026"] = loc_items["Kite"]
        have_djinn["027"] = loc_items["Squall"]
        add_djinn(loc_items["Gust"])
        add_djinn(loc_items["Breeze"])
        add_djinn(loc_items["Zephyr"])
        add_djinn(loc_items["Smog"])
        add_djinn(loc_items["Kite"])
        add_djinn(loc_items["Squall"])
        
        removal()
    return exclusive


def sphere(sphere_counter, dd):
    if mode == modes[1]:
        print ("===== sphere ", sphere_counter)
    global djinn
    global found_piers
    global found_reunion
    global have_djinn
    global have_items
    global have_items2
    global statics
    removal()
    get_djinn(di)
    removal()
    dic_sp = available_checks(di)
    sphere_dic = {}
    exclusive = []
    temp = -1
    while temp != len(have_items): #TODO change to a repeat flag
        temp = len(have_items)
        for k,v in dic_sp.items():
            exclusive += special(v, k)
        dic_sp = available_checks(di)

    if len(exclusive) > 0:
        get_djinn(di)
        removal()
    dic_sp = available_checks(di)

    #idejima items
    if sphere_counter == 0:
        have_items["0x1"] = loc_items["0x1"]
        have_items["0x2"] = loc_items["0x2"]
        have_items["0x3"] = loc_items["0x3"]
        have_items["0x4"] = loc_items["0x4"]
        exclusive.append("0x1")
        exclusive.append("0x2")
        exclusive.append("0x3")
        exclusive.append("0x4")
        
    for k in dic_sp.keys():
        if k not in dd.keys() and (int(k, 16) < 48 or int(k, 16) >= 128):
            exclusive.append(k)
            sphere_dic[k] = dic_sp[k]

    for k in sphere_dic.keys():
        try:
            have_items[k] = loc_items[k]
        except:
            if sphere_dic[k][0] in ["Piers", 'Briggs Fight', 'Serpent Defeated', 'Dwarven Cannon',\
                                    'Briggs Jailbreak','Jupiter Lighthouse Lit', 'Reunion', 'Lighthouse Heated']:
                continue
            if sphere_dic[k][0] in statics:
                have_items[k] = sphere_dic[k][0]
                exclusive.append(k)
                continue

    for k in exclusive:
        try:
            ite = have_items[k]
            if "coin" not in ite:
                ite = ite.replace(" (empty)", "")
                ite = ite.replace(" (Mimic)", "")
                have_items2[ite] = have_items2.get(ite, 0) + 1
                if mode == modes[1]:
                    print(ite, k)
            di.pop(k)
        except:
            continue

    #for k,v in have_djinn.items():
        #print(k,v)
        
    return dic_sp

def check_obj(obj, have_items, sphere_counter):
    global orig_obj
    global bingo_possible
    for i in range(len(obj)):
        for j in range(len(obj[i])):
            #print(obj[i][j])
            if type(obj[i][j]) == int:
                continue
            if len(obj[i][j]) == 0:
                obj[i][j] = sphere_counter
            elif obj[i][j][0] == "djinn":
                if obj[i][j][1][0] == "count":
                    if djinn[obj[i][j][1][2]] >= obj[i][j][1][1]:
                        if mode == modes[1]:
                            print(orig_obj[i][j])
                        obj[i][j] = sphere_counter
                elif obj[i][j][1][0] == "specific":
                    for d in obj[i][j][1][1]:
                        for dj in have_djinn.values():
                            if d.lower() == dj.lower():
                                if mode == modes[1]:
                                    print(orig_obj[i][j])
                                obj[i][j] = sphere_counter
            elif obj[i][j][0] == "class":
                if djinn["total"] < 10:
                    continue
                for option in obj[i][j][1]:
                    if option[0] in have_classes and djinn[option[2]] >= option[1]:
                        if len(option) < 4:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                            break
                        elif djinn[option[4]] >= option[3]:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                            break
            elif obj[i][j][0] == "count":
                if obj[i][j][1][1] in have_items2.keys():
                    if obj[i][j][1][0] <= have_items2[obj[i][j][1][1]]:
                        if mode == modes[1]:
                            print(orig_obj[i][j])
                        obj[i][j] = sphere_counter
                else:
                    count = 0
                    if obj[i][j][1][1] == "shirt":
                        for item in have_items2.keys():
                            if "shirt" in item.lower() or item == "Divine Camisole":
                                count += 1
                        if count >= 2:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                    elif obj[i][j][1][1] == "ring":
                        for item in have_items2.keys():
                            if "ring" in item.lower():
                                count += 1
                        if count >= 2:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                    elif obj[i][j][1][1] == "stats":
                        count = have_items2.get("Apple", 0) + have_items2.get("Cookie", 0) +\
                                have_items2.get("Hard Nut", 0) + have_items2.get("Lucky Pepper", 0) +\
                                have_items2.get("Mint", 0) + have_items2.get("Power Bread", 0)
                        if count >= 5: #5 cuz -3 from statics off the bat
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                    elif obj[i][j][1][1] == "prong":
                        for item in have_items2.keys():
                            if "prong" in item.lower():
                                count += 1
                        if count >= 2:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                    elif obj[i][j][1][1] == "trade":
                        trad = ["Lil Turtle", "Pretty Stone", "Red Cloth", "Milk"]
                        count = sum(t in trad for t in have_items2.keys())
                        if count >= 2:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter
                    elif obj[i][j][1][1] == "key":
                        for item in have_items2.keys():
                            if "key" in item.lower():
                                count += 1
                        if count >= 2:
                            if mode == modes[1]:
                                print(orig_obj[i][j])
                            obj[i][j] = sphere_counter

                        
            else:
                for k in range(len(obj[i][j])):
                    toRemove = []
                    #print(obj[i][j][k])
                    for l in obj[i][j][k]:
                        if "hasDjinn" in l:
                            if djinn["total"] >= int(l.split("|")[1]):
                                obj[i][j][k].remove(l)
                                if len(obj[i][j][k]) == 0:
                                    break
                        for item in have_items.keys():
                            if l.lower() in item.lower():
                                if l not in in_exceptions or item not in in_exceptions[l]:
                                    toRemove.append(l)
                    for item in toRemove:
                        if len(obj[i][j][k]) == 0 or item not in obj[i][j][k]:
                            break
                        obj[i][j][k].remove(item)
                        
                    if len(obj[i][j][k]) == 0:
                        if mode == modes[1]:
                            print(orig_obj[i][j])
                        obj[i][j] = sphere_counter
                        break
                    
    if not bingo_possible:
        #rows
        for row in range(len(obj)):
            for col in range(len(obj[row])):
                if not isinstance(obj[row][col], int):
                    break
                if col == 4:
                    bingo_possible = True

        #columns
        for col in range(len(obj)):
            for row in range(len(obj[row])):
                if not isinstance(obj[row][col], int):
                    break
                if row == 4:
                    bingo_possible = True

        for diag1 in range(len(obj)):
            if not isinstance(obj[diag1][diag1], int):
                    break
            if diag1 == 4:
                bingo_possible = True

        for diag2 in range(len(obj)):
            if not isinstance(obj[diag2][4-diag2], int):
                    break
            if diag2 == 4:
                bingo_possible = True

    return obj

def add_djinn(dji, k=None):
    global djinn
    global have_djinn2
    have_djinn2[dji] = 1
    djinn["total"] += 1
    if dji in d_venus:
        djinn["venus"] += 1
    elif dji in d_mars:
        djinn["mars"] += 1
    elif dji in d_mercury:
        djinn["mercury"] += 1
    elif dji in d_jupiter:
        djinn["jupiter"] += 1
    else:
        print("WWWWWW ",dji)
    


recurse(data[0], [])

# splitting up the strings by comma, adding ship to sphere 0
for k in di.keys():
    t_v = []
    atts = di[k]
    for v in atts[1]:
        v2 = v.split(',')
        v2 = [i for i in v2 if i != "lemurian_ship"]
        v2 = [i for i in v2 if i != "$canAccessYampiBackside"]
        if "gabomba_statue" in v2:
            v2.append("lash")
            v2.append("pound")
            v2.append("scoop")
            v2.remove("gabomba_statue")
        if "$canAccessUpperMars" in v2: #mars star?
            v2.append("burst")
            v2.append("pound")
            v2.append("blaze")
            v2.append("reveal")
            v2.append("teleport")
            v2.remove("$canAccessUpperMars")
        if "$canAccessShip" in v2: #also add hover
            v2.append("grind")
            v2.remove("$canAccessShip")
        t_v.append(v2)
    di[k][1] = t_v
di["0x001"] = ["trial_road", [["$hasDjinn|28", "shaman", "grind"], ["$hasDjinn|28", "shaman", "hover"]]]
di["0x002"] = ["Mad Plant", [["cyclone", "lash", "pound", "scoop", "frost", "reveal"]]]
di["0x003"] = ["Mad Plant", [["cyclone", "whirlwind"]]]
di["0x004"] = ["Mad Plant", [["cyclone", "dancing idol"]]]
di["0x005"] = ["Mad Plant", [["cyclone", "grind"], ["cyclone", "hover"]]]
di["0x006"] = ["Mad Plant", [["cyclone", "shaman", "hover", "lift"]]]
di["0x007"] = ["Apple", [["grind", "catch"], ["hover", "catch"]]] 
di["0x008"] = ["Cookie", [["grind", "magma ball"], ["hover", "magma ball"]]]
di["0x009"] = ["Hard Nut", [["grind", "growth", "cyclone"],["trident", "growth", "cyclone"]]]
di["0x00A"] = ["Lucky Pepper", [["cyclone", "shaman", "hover", "lift"]]]
di["0x00B"] = ["Lucky Pepper", [["$hasDjinn|28", "shaman", "grind"], ["$hasDjinn|28", "shaman", "hover"]]]
di["0x00C"] = ["Mint", [["lash", "pound", "scoop", "cyclone"]]]
di["0x00D"] = ["Mint", [["cyclone"]]]
di["0x00E"] = ["Mint", [["cyclone", "grind"],["cyclone", "hover"]]]#2 in jupiter
di["0x00F"] = ["Mint", [["cyclone", "grind"],["cyclone", "hover"]]]
di["0x010"] = ["Power Bread", [["pound", "lash", "burst"]]]
di["0x011"] = ["Power Bread", [["grind"], ["hover"]]]
di["0x012"] = ["Lucky Medal", [[]]]
di["0x013"] = ["Golem Core", [["grind", "scoop", "lift", "magma ball"],["hover", "scoop", "lift", "magma ball"]]]
di["0x014"] = ["Vial", [["$hasDjinn|6"]]] #on briggs
di["0x015"] = ["Lucky Medal", [["$hasDjinn|6"]]] #after briggs
di["0x016"] = ["Vial", [["scoop"]]] #on king scorp
di["0x017"] = ["Lucky Medal", [["grind", "scoop"]]]
di["0x018"] = ["Lucky Medal", [["grind"]]]
di["0x019"] = ["Lucky Medal", [[]]] #champa
di["0x01A"] = ["Mist Potion", [["grind", "magma ball"],["hover", "magma ball"]]] #prox shop
di["0x01B"] = ["Mythril Silver", [["grind", "scoop", "magma ball"],["hover", "scoop", "magma ball"]]]
#care, 0x03 will be considered djinn
statics = ["gabomba_statue", "trial_road", "Mad Plant", "Apple", "Cookie",\
            "Hard Nut", "Lucky Pepper", "Mint", "Power Bread", "Lucky Medal",\
           "Golem Core", "Vial", "Mist Potion", "Mythril Silver"]
di["0x9f9"] = ["Magma Ball", [["grind","lift","burst","growth","lash","whirlwind","blaze"],\
                              ["hover","lift","burst","growth","lash","whirlwind","blaze"]]]
di.pop('0x8de') #lemurian ship

boss_dic = {}
boss_dic['0x94d'] = di.pop('0x94d') #moapa
boss_dic['0x9ba'] = di.pop('0x9ba') #serpent
boss_dic['0x978'] = di.pop('0x978') #avimander
boss_dic['0xa3a'] = di.pop('0xa3a') #flame dragons
boss_dic['0xa4b'] = di.pop('0xa4b') #mars lit
boss_dic['0xf93'] = di.pop('0xf93') #tomegathericon
boss_dic['0x19'] = di.pop('0x19') #star magician
boss_dic['0x18'] = di.pop('0x18') #valukar
boss_dic['0x1a'] = di.pop('0x1a') #sentinel
boss_dic['0x918'] = di.pop('0x918') #mayor's gift
boss_dic['0xf65'] = di.pop('0xf65') #deep taopo
boss_dic['0xf75'] = di.pop('0xf75') #gaia whirlwind check

di2 = copy.deepcopy(di)

log1 = spoiler_log.split('========== Djinn ==========')[1]
log2 = log1.split('========== Character Stats ==========')
log_djinn = log2[0]
log3 = log1.split('========== Character Elements ==========')
log_class = log3[1].split('========== Class Stats ==========')[0]
log_items = log2[1].split('========== All Items ==========')[1]

classes = {}
c_ref = ["a", "venus_c", "mercury_c", "mars_c", "jupiter_c"]
for line in log_class.split('\n'):
    if not line:
        continue
    if line[0].isspace():
        continue
    l = line.split("  ")
    for i in range(len(l)):
        l[i]= l[i].strip()
    if '' in l:
        l.remove('')
    classes[l[0]] = c_ref[l.index('X')]

have_classes = [classes["Felix"], classes["Jenna"], classes["Sheba"]]

loc_items = {}
loc_djinn = {}
for line in log_items.split('\n'):
    if "-->" not in line:
        continue
    addr = line.split()[0]
    item = line.split("--> ")[1]
    loc_items[addr]=item

moder = 0
m_c = 0
for line in log_djinn.split('\n'):
    if "reserve" in line.lower():
        moder = 1
    if "-->" not in line:
        continue
    if moder == 0:
        was = line.split(" --> ")[0].strip()
    else:
        if m_c == 0:
            was = 'Reserve Djinni (Venus)'
        elif m_c == 1:
            was = 'Reserve Djinni (Mercury)'
        elif m_c == 2:
            was = 'Reserve Djinni (Mars)'
        elif m_c == 3:
            was = 'Reserve Djinni (Jupiter)'
        m_c += 1
    iss = line.split(" --> ")[1]
    loc_items[was]=iss

djinn = {}
djinn["total"] = 0
djinn["mars"] = 0
djinn["venus"] = 0
djinn["mercury"] = 0
djinn["jupiter"] = 0
#god forgive me for my sins
d_venus = "FlintGraniteQuartzVineSapGroundBaneEchoIronSteelMudFlowerMeldPetraSaltGeodeMoldCrystal"
d_mars = "ForgeFeverCoronaScorchEmberFlashTorchCannonSparkKindleCharCoalRefluxCoreTinderShineFuryFugue"
d_mercury = "FizzSleetMistSpritzHailTonicDewFogSourSpringShadeChillSteamRimeGelEddyBalmSerac"
d_jupiter = "GustBreezeZephyrSmogKiteSquallLuffBreathBlitzEtherWaftHazeWheezeAromaWhorlGaspLullGale"

have_djinn = {}
have_djinn2 = {}
have_items = {}
have_items2 = {}

have_items["0x01C"] = "reunion"
have_items2["reunion"] = 1

ds = {}
same = False
djinn_old = list(have_djinn.values())
bingo_p2 = True
while not same:
    ds1 = sphere(sphere_counter, ds)
    if ds1 == ds:
        same = True
    else:
        sphere_counter +=1 #what if I move this down and remove the -1?
        ds = ds1
        if mode == modes[1]:
            print("\n=objectives completed=")
        if not isolate_spoiler:
            obj = check_obj(obj, have_items2, sphere_counter-1)
        if mode == modes[1]:
            print("\n=djinn obtained=")
        for dj in have_djinn.values():
            if dj not in djinn_old:
                if mode == modes[1]:
                    print(dj)
        djinn_old = list(have_djinn.values())
        if mode == modes[1]:
            print(djinn["total"])
        if not foundGrind and ("Grindstone" in have_items2.keys() \
           or "Hover Jade" in have_items2.keys()):
            foundGrind = True
            grindSphere = sphere_counter

    if bingo_possible and bingo_p2:
        bingo_p2 = False
        for k in boss_dic.keys():
            di[k] = boss_dic[k]

print("=====DONE======")
#if mode == modes[1]:
    #print(di)

if not isolate_spoiler:
    if mode == modes[1]:
        for row in obj:
            print(row)
            
    sols = []
    sols.append([max(obj[0]), "row 1"])
    sols.append([max(obj[1]), "row 2"])
    sols.append([max(obj[2]), "row 3"])
    sols.append([max(obj[3]), "row 4"])
    sols.append([max(obj[4]), "row 5"])

    sols.append([max([i[0] for i in obj]), "column 1"])
    sols.append([max([i[1] for i in obj]), "column 2"])
    sols.append([max([i[2] for i in obj]), "column 3"])
    sols.append([max([i[3] for i in obj]), "column 4"])
    sols.append([max([i[4] for i in obj]), "column 5"])


    temp = []
    for i in range(len(obj)):
        temp.append(obj[i][i])
    sols.append([max(temp), "top-left diagonal"])

    temp = []
    for i in range(len(obj)):
        temp.append(obj[i][4-i])
    sols.append([max(temp), "top-right diagonal"])

    sols = sorted(sols, key=lambda x: x[0])

    minn = sols[0][0]
    minc = 0
    for soll in sols:
        if soll[0] == minn:
            minc += 1
        elif soll[0] == minn+1:
            minc += 0.5
        else:
            break

    if mode == modes[1]:
        print("")
        for sol in sols:
            print(sol)
        print("\n fastest bingo is " + sols[0][1] + " with sphere " + str(sols[0][0]))

    if mode == modes[0]:
        #print(grindSphere, sphere_counter, minc, minn)
        
        aab1 = abs(0.5 - (grindSphere/sphere_counter))+1 #smaller better 1 to 1.5
        aab2 = 1 + (minn/sphere_counter) #smaller better, 1 to 2
        mincc = 0
        if minc > 4: #too many bingos in lowest sphere is detrimental
            mincc = minc-4
        aab3 = minc - mincc
        #change aab2 to 1 to allow longer runs
        #print(aab1, aab2, math.sqrt(minc))
        final_score = round(((4-(aab1*aab2))*2*math.sqrt(aab3))-1, 1)
        #print("I give this a rating of ",final_score," out of 10")
        if aab3 > 3:
            print("good enough bro")
        else:
            print("not good enough homeslice")

#time estimates
##for row in range(len(obj_time)):
##    for col in range(len(obj_time[row])):
##        ob = obj_time[row][col]
##        if ob[0] in ["count", "djinn", "class"]:
##            continue
##        for method in range(len(ob)):
##            for req in range(len(ob[method])):
##                indiv = ob[method][req]
##                if indiv == "0x":
##                    continue
##                for k, v in have_items.items():
##                    if indiv.lower() in v.lower():
##                        if indiv.lower() not in in_exceptions or v not in in_exceptions[indiv]:
##                            obj_time[row][col][method][req] = k
##                            break     
###obj_time
##
##first_bingo = sols[0][0]
##req_items = []
##req_addrs = []
##
##for sol in sols:
##    if sol[0] != first_bingo:
##        break
##    if sol[1][0] == "r":
##        line = obj_time[int(sol[1].split(" ")[1])-1]
##    elif sol[1][0] == 'c':
##        num = int(sol[1].split(" ")[1])-1
##        line = [i[num] for i in obj_time]
##    elif sol[1][4] == 'l':
##        line = []
##        for i in range(len(obj_time)):
##            line.append(obj_time[i][i])
##    elif sol[1][4] == 'r':
##        line = []
##        for i in range(len(obj_time)):
##            line.append(obj_time[i][4-i])
##    print(line, "\n")
##
##    for obj in line:
##        if obj[0] in ["count", "djinn", "class"]:
##            continue
##        #TODO should i find time for all paths, or fastest?
        
        





