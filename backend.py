import json
import datetime as dt
import time

id_key = "userID"
name_key = "name"
surname_key = "surname"
status_key = "status"

def add_profile(userid:str ,name:str, surname:str):
    # to add new profile
    with open('./data/profile.json') as f:
        s = f.read()
        ss = json.loads(s)
    check = {
        id_key : userid,
        name_key : name,
        surname_key : surname,
        status_key : False
    }
    ss.append(check)
    json_ob = json.dumps(ss)
    output_file = open('./data/profile.json','w')
    output_file.write(json_ob)
    output_file.close

def count_write(count : int):
    output_file = open('./data/count.txt','w')
    output_file.write(str(count))
    output_file.close

#add_profile("123","what","everS")
# create list of userrID
id = []
na = []
sur = []
sta = []
with open('./data/profile.json') as f:
    s = f.read()
ss = json.loads(s)
for i in range(len(ss)):
    id.append(ss[i][id_key])
    na.append(ss[i][name_key])
    sur.append(ss[i][surname_key])
    sta.append(ss[i][status_key])
#print(id)

inp = "123"
count = 0
for i in range(len(id)):
    if(i == len(id)-1) and (id[i] != inp):
        #not a user
        #add new log
        x = dt.datetime.now()
        output_file = open('./data/enter.log','a')
        output_file.write(x.strftime("%c")+',')
        output_file.write(" id = "+ inp + ", NOT PASS\n")
        output_file.close
    elif id[i] == inp :
        if(sta[i] == False):
            sta[i] = True
            #add new log
            x = dt.datetime.now()
            output_file = open('./data/enter.log','a')
            output_file.write(x.strftime("%c")+',')
            output_file.write(" id = "+ id[i] + ", PASS IN\n")
            output_file.close
            count += 1
            re = 30-count
            remain_file = open('./data/remaining.txt','w')
            remain_file.write(str(re))
            remain_file.closed
            count_write(count)
        else : 
            sta[i] = False
            #add new log
            x = dt.datetime.now()
            output_file = open('./data/enter.log','a')
            output_file.write(x.strftime("%c")+',')
            output_file.write(" id = " + id[i] + ", PASS OUT\n")
            output_file.close
            count -= 1
            re = 30-count
            remain_file = open('./data/remaining.txt','w')
            remain_file.write(str(re))
            remain_file.closed
            count_write(count) 