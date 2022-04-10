import json
import datetime as dt
import time

id_key = "userID"
name_key = "name"
surname_key = "surname"
status_key = "status"

from practicum import find_mcu_boards, McuBoard, PeriBoard
devices = find_mcu_boards()
mcu = McuBoard(devices[0])
peri = PeriBoard(mcu)

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

#update count file
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

timeout = 100      
start_time = 0

while True:
    try :
        tmp = mcu.usb_read(request=0, length=1)
        inp = tmp[0]
        print(inp)
        #inp = "123"
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

                    #write to servo
                    print("open")
                    mcu.usb_write(request=1,value=1)
                    time.sleep(2) #open for 2 sec
                    print("close")
                    mcu.usb_write(request-1,value=0)

                    #add new log
                    x = dt.datetime.now()
                    output_file = open('./data/enter.log','a')
                    output_file.write(x.strftime("%c")+',')
                    output_file.write(" id = "+ id[i] + ", PASS IN\n")
                    output_file.close

                    #update count and remaining
                    count += 1
                    re = 30-count
                    remain_file = open('./data/remaining.txt','w')
                    remain_file.write(str(re))
                    remain_file.closed
                    count_write(count)

                else : 
                    sta[i] = False

                    #write to servo
                    print("open")
                    mcu.usb_write(request=1,value=1)
                    time.sleep(2) #open for sec
                    print("close")
                    mcu.usb_write(request-1,value=0)
                    
                    #add new log
                    x = dt.datetime.now()
                    output_file = open('./data/enter.log','a')
                    output_file.write(x.strftime("%c")+',')
                    output_file.write(" id = " + id[i] + ", PASS OUT\n")
                    output_file.close

                    #update count and remaining
                    count -= 1
                    re = 30-count
                    remain_file = open('./data/remaining.txt','w')
                    remain_file.write(str(re))
                    remain_file.closed
                    count_write(count) 

    except Exception as err:
        print(err)
        print("ERROR")
        devices = find_mcu_boards()
        mcu = McuBoard(devices[0])
        peri = PeriBoard(mcu)