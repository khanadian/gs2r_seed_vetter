import json

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
                    if num <= djinncounter:
                        v.remove(i)
            t_v.append(v)
        di[k][1] = t_v
    

def sphere(sphere_counter, dd):
    print ("===== sphere ", sphere_counter)
    global djinncounter
    
    removal()

    dic_sp = available_checks(di)
    sphere_dic = {}
    for k,v in dic_sp.items():
        if v[0] == "Piers":
            #piers items
            have_items["0x105"] = loc_items["0x105"]
            have_items["0x106"] = loc_items["0x106"]
            have_items2[loc_items["0x105"]] = have_items2.get(loc_items["0x105"], 0) + 1
            have_items2[loc_items["0x106"]] = have_items2.get(loc_items["0x106"], 0) + 1
            removal()
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
        if v[0] == 'Reunion':
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
            have_djinn[k] = loc_items[sphere_dic[k][0]]
            djinncounter += 1

    for k,v in have_items.items():
        have_items2[v] = have_items2.get(v, 0) + 1
        
    for k in exclusive:
        try:
            print(have_items[k])
        except:
            continue

    #for k,v in have_djinn.items():
        #print(k,v)
        
   # print(djinncounter)
    return dic_sp



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


log1 = spoiler_log.split('========== Djinn ==========')[1]
log2 = log1.split('========== Character Stats ==========')
log_djinn = log2[0]
log_items = log2[1].split('========== All Items ==========')[1]

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

djinncounter = 0
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
        djinncounter += 1

for k,v in have_items.items():
    print(v)
    have_items2[v] = have_items2.get(v, 0) + 1


ds = dic
same = False
while not same:
    ds1 = sphere(sphere_counter, ds)
    if ds1 == ds:
        same = True
    else:
        sphere_counter +=1
        ds = ds1

    





