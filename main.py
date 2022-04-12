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
count = 0

while True:
    try :
        time.sleep(0.2)
        tmp = mcu.usb_read(request=0,length=1)
        #print(tmp)
        inp = str(tmp[0])
        print(inp)
        re = 30-count

        #update count and remaining
        remain_file = open('/var/www/html/remaining.txt','w')
        remain_file.write(str(re))
        remain_file.closed
        output_file = open('/var/www/html/count.txt','w')
        output_file.write(str(count))
        output_file.close

        if (inp == "0"):
            continue
        else:
            for i in range(len(id)):
                if(i == len(id)-1) and (id[i] != inp):
                    #not a user
                    print("not a user")
                    #add new log
                    x = dt.datetime.now()
                    output_file = open('/var/www/html/enter.txt','a')
                    output_file.write(x.strftime("%c")+',')
                    output_file.write(" id = "+ inp + ", NOT PASS\n")
                    output_file.close

                elif id[i] == inp :
                    if(sta[i] == False):
                        sta[i] = True
                        print("in")
                        #add new log
                        x = dt.datetime.now()
                        output_file = open('/var/www/html/enter.txt','a')
                        output_file.write(x.strftime("%c")+',')
                        output_file.write(" id = "+ id[i] + ", PASS IN\n")
                        output_file.close

                        #person in count +1
                        count += 1

                        #write to servo
                        print("open")
                        mcu.usb_write(request=1,value=1)
                        time.sleep(5) #open for 5 sec
                        print("close")
                        mcu.usb_write(request=1,value=0)
                        break

                    else : 
                        sta[i] = False
                        print("out")
                        #add new log
                        x = dt.datetime.now()
                        output_file = open('/var/www/html/enter.txt','a')
                        output_file.write(x.strftime("%c")+',')
                        output_file.write(" id = " + id[i] + ", PASS OUT\n")
                        output_file.close

                        #person out count -1
                        count -= 1

                        #write to servo
                        print("open")
                        mcu.usb_write(request=1,value=1)
                        time.sleep(5) #open for 5 sec
                        print("close")
                        mcu.usb_write(request=1,value=0)
                        break

    except Exception as err:
        print(err)
        print("ERROR")
        devices = find_mcu_boards()
        mcu = McuBoard(devices[0])
        peri = PeriBoard(mcu)