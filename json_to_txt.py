import json
from bingo import get_obj_fast

obj = get_obj_fast("https://bingosync.karanum.xyz/room/_ehTIGtfQHK8zV6ybQqR5Q", "neo")

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
    for k in di.keys():
        atts = di[k]
        t_v = []
        for j in range(len(atts[1])):
            v = atts[1][j]
            #first we remove psynergy
            for item in have_items2.keys():
                for i in v:
                    frst = i.replace("_", " ").split()[0]
                    if frst.lower() in item.lower(): #TODO red cloth != red key, mars star != mars lit
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
    

def sphere(sphere_counter, dd):
    print ("===== sphere ", sphere_counter)
    global djinn
    global found_piers
    global found_reunion
    global have_djinn
    removal()

    dic_sp = available_checks(di)
    sphere_dic = {}
    for k,v in dic_sp.items():
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
            removal()
        #TODO maybe add trial road and gabomba here
        if v[0] == 'Briggs Fight':
            have_items[k] = "briggs_battle"
            have_items2["briggs_battle"] = 1
            removal()
        if v[0] == 'Serpent Defeated':
            have_items[k] = "susa"
            have_items2["susa"] = 1
            removal()
        if v[0] == 'Dwarven Cannon':
            have_items[k] = "cannon"
            have_items2["cannon"] = 1
            removal()
        if v[0] == 'Briggs Jailbreak':
            have_items[k] = "briggs_jailbreak"
            have_items2["briggs_jailbreak"] = 1
            removal()
        if v[0] == 'Jupiter Lighthouse Lit':
            have_items[k] = "jupiter lit"
            have_items2["jupiter lit"] = 1
            removal()
        if v[0] == 'Reunion' and not found_reunion:
            found_reunion = True
            have_items[k] = "reunion"
            have_items2["reunion"] = 1
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
            
    dic_sp = available_checks(di)
    
    exclusive = []

    for k in dic_sp.keys():
        if k not in dd.keys():
            exclusive.append(k)
            sphere_dic[k] = dic_sp[k]

    for k in sphere_dic.keys():
        
        try:
            have_items[k] = loc_items[k]
        except:
            if sphere_dic[k][0] in ["Piers", 'Briggs Fight', 'Serpent Defeated', 'Dwarven Cannon',\
                                    'Briggs Jailbreak','Jupiter Lighthouse Lit', 'Reunion']:
                continue
            if sphere_dic[k][0] in ["gabomba_statue", "trial_road"]:
                have_items[k] = sphere_dic[k][0]
                continue
            have_djinn[k] = loc_items[sphere_dic[k][0]]
            add_djinn(loc_items[sphere_dic[k][0]])

    for k in exclusive:
        try:
            ite = have_items[k]
            if "coin" not in ite:
                ite = ite.replace(" (empty)", "")
                ite = ite.replace(" (Mimic)", "")
                have_items2[ite] = have_items2.get(ite, 0) + 1
                print(ite)
        except:
            continue

    #for k,v in have_djinn.items():
        #print(k,v)
        
    return dic_sp

def check_obj(obj, have_items, sphere_counter):
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
                        obj[i][j] = sphere_counter
                elif obj[i][j][1][0] == "specific":
                    for d in obj[i][j][1][1]:
                        for dj in have_djinn.values():
                            if d.lower() == dj.lower():
                                obj[i][j] = sphere_counter
            elif obj[i][j][0] == "class":
                for option in obj[i][j][1]:
                    if option[0] in have_classes and djinn[option[2]] >= option[1]:
                        if len(option) < 4:
                            obj[i][j] = sphere_counter
                            break
                        else:
                            print(option)
            elif obj[i][j][0] == "plant":
                continue
            elif obj[i][j][0] == "count":
                continue
            else:
                for k in range(len(obj[i][j])):
                    #print(obj[i][j][k])
                    for l in obj[i][j][k]:
                        if "hasDjinn" in l:
                            if djinn["total"] >= int(l.split("|")[1]):
                                obj[i][j][k].remove(l)
                                continue
                        for item in have_items.keys():
                            if l.lower() in item.lower():
                                obj[i][j][k].remove(l)
                    if len(obj[i][j][k]) == 0:
                        obj[i][j] = sphere_counter
                        break
    return obj

def add_djinn(dji):
    global djinn
    
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
        t_v.append(v2)
    di[k][1] = t_v
di["0x000"] = ["gabomba_statue", [["lash", "pound", "scoop"]]]
di["0x001"] = ["trial_road", [["$hasDjinn|28", "shaman"]]]

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
    if '' in l:
        l.remove('')
    classes[l[0]] = c_ref[l.index(' X')]

have_classes = [classes["Felix"], classes["Jenna"], classes["Sheba"]]

loc_items = {}
loc_djinn = {}
for line in log_items.split('\n'):
    if "-->" not in line:
        continue
    addr = line.split()[0]
    item = line.split("--> ")[1]
    loc_items[addr]=item

mode = 0
m_c = 0
for line in log_djinn.split('\n'):
    if "reserve" in line.lower():
        mode = 1
    if "-->" not in line:
        continue
    if mode == 0:
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

print ("===== sphere ", sphere_counter)
sphere_counter +=1

print("== available items ==")
dic = available_checks(di)

have_items = {}
have_items2 = {}
have_djinn = {}

#idejima items
have_items["0x1"] = loc_items["0x1"]
have_items["0x2"] = loc_items["0x2"]
have_items["0x3"] = loc_items["0x3"]
have_items["0x4"] = loc_items["0x4"]



for k in dic.keys():
    try:
        have_items[k] = loc_items[k]
    except:
        have_djinn[k] = loc_items[dic[k][0]]
        add_djinn(loc_items[dic[k][0]])

for k,v in have_items.items():
    if "coin" not in v:
        ite = v.replace(" (empty)", "")
        ite = v.replace(" (mimic)", "")
        have_items2[ite] = have_items2.get(ite, 0) + 1
        print(v)


obj = check_obj(obj, have_items2, sphere_counter-1)           
print(obj)
for k,v in djinn.items():
    print(k,v)
    
ds = dic
same = False
while not same:
    ds1 = sphere(sphere_counter, ds)
    if ds1 == ds:
        same = True
    else:
        sphere_counter +=1
        ds = ds1
        obj = check_obj(obj, have_items2, sphere_counter-1)
        print(obj)
    for k,v in djinn.items():
        print(k,v)

print("=====DONE======")

for k,v in have_items2.items():
    print(k,v)  

print(have_classes)
