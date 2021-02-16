

 # 명령어 저장 함수 
def save_c(diction) : 
    key = []
    value = []

    for i , v in zip(list(diction.keys())  , list(diction.values())): 
        key.append(i)
        value.append(v)


    with open('command.txt' , 'w' , encoding="utf-8") as f : 
        for i in range(len(key)) : 
            f.write(key[i] + "_+_+" + value[i]  + "##_=+#\n")




# 명령어 불러오는 함수 
def load_diction() :

    with open('command.txt' , 'r' , encoding="utf-8" ) as f :
        text = f.read().replace('\n' , "").split('##_=+#')
        text_dic = [x.split('_+_+') for x in text]
        diction = {}
        for i in text_dic : 
            if len(i) == 2 :
                diction[i[0]] = i[1]
    return diction



# 리스트 입력을 받으면  3개씩 그룹으로 묶어주는 함수 , a = [1,2,3,4,5] - > 123 234 345 
def make_text_g(a) : 
    
    text_group = []
    for i in range(len(a)) : 
        if i+7 == len(a) : 
            break
        x = a[i]
        y = a[i + 1]
        z = a[i + 2]
        y = a[i + 3]
        u = a[i + 4]
        p = a[i + 5]
        q = a[i + 6]
        k = a[i + 7]
        text_group.append([x,y,z,y,u,p,q,k])
        
    return text_group



# 카톡에서 받아온 문자열을 문장 기준으로 나누고 문장별로 [이름 , 시간 , 메시지]로 만든후 리스트에 저장하는 함수
def SepTEXT(clipbd) : 
    text = clipbd.split('\n')
    text = [i[:-1] for i in text]
    check_list = []
    for i in text : 
        if '] [' in i : 
            
            num = i.find('] [') + 1
            name = i[:num]
            time_msg = i[num + 1:]
            time = time_msg[:time_msg.find(']') + 1]
            msg = time_msg[time_msg.find(']') + 2 :]
            
            check_list.append([name , time , msg])
    return check_list 

