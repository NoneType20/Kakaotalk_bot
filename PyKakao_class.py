import win32con , win32api , pyautogui , pyperclip , win32gui
from def__ import save_c , make_text_g , SepTEXT , load_diction



# 카카오톡 객체 생성
class make_kakao() : 


    # 기본 객체 생성 , 창 찾기 
    def __init__(self , name , con_id) : 
        self.FindWindow = win32gui.FindWindow
        self.FindWindowEx = win32gui.FindWindowEx
        self.GetDlgItem = win32gui.GetDlgItem
        self.PostMessage = win32gui.PostMessage
        self.SendMessage = win32api.SendMessage

        self.hwnd = self.FindWindow(None, name) # window 찾기 
        self.edit_txb = self.GetDlgItem(self.hwnd, int(con_id))
        self.edit_vtx = self.FindWindowEx(self.hwnd , None , "EVA_VH_ListControl_Dblclk" , None) # 카톡 리스트창 ( 문자 창 )
        self.edit_msb = self.FindWindowEx(self.hwnd , None , "RICHEDIT50W" , None) #  메시지 인풋박스


    # 문자 보내기
    def send_ms(self , char) : 
        if type(char) == str : # 들어온 텍스트가 문자면 그냥 전송
            for i in char : 
                self.SendMessage(self.edit_txb, win32con.WM_CHAR, ord(i), 0)
                win32api.Sleep(5)
        elif type(char) == list : # 들어온 텍스트가 리스트면 줄바꿈 해가면서 전송
            for i in char : 
                i = str(i)
                if not i == "": 
                    for z in i: 
                        self.SendMessage(self.edit_txb, win32con.WM_CHAR, ord(z), 0)
                        win32api.Sleep(5) 
                    pyautogui.keyDown('ctrl')
                    self.PostMessage(self.edit_msb ,win32con.WM_KEYDOWN, win32con.VK_RETURN , 0 )
                    pyautogui.keyUp('ctrl')
        self.PostMessage(self.edit_msb ,win32con.WM_KEYDOWN, win32con.VK_RETURN , 0 )
        win32api.Sleep(100)


    # 문자 얻어오기     
    def get_texts(self) :  
        pyautogui.keyDown('ctrl')
        self.PostMessage(self.edit_vtx , win32con.WM_KEYDOWN , 0x41 , 0)  
        self.PostMessage(self.edit_vtx , win32con.WM_KEYDOWN , 0x43 , 0)  
        pyautogui.keyUp('ctrl')
        self.clipbd = pyperclip.paste()











class opentalk_bot() : 
    # 카톡룸 객체 생성
    def __init__(self , name_room , conn_id=0x3EE) :
        self.name_room = name_room
        self.check_AA = []
        self.opentalk = make_kakao(self.name_room , conn_id)
        self.diction = load_diction()
         




    # 텍스트 불러오기 , 텍스트 그룹 형성
    def processing_text(self):    
        self.opentalk.get_texts() 
        self.text = self.opentalk.clipbd
        self.text  = SepTEXT(self.text) 
        self.text = make_text_g(self.text)  



    # 중복 텍스트 삭제 , 새로운 텍스트만 찾기
    def del_sameTEXT(self) :
        if self.text == self.check_AA : # 체크그룹(이전 그룹)과 현재 그룹이 같으면 continue
            return "continue"             
        self.New_text = [] # 체크 그룹(이전그룹) 에 없는것만 골라내기
        for i in self.text : 
            if not i in self.check_AA :  
                self.New_text.append(i)
        self.check_AA = self.text # 체크 그룹을 현재 그룹으로 지정 
        # 체크그룹에 없는것만 골라낸것중 새로 추가된 텍스트만 골라내기 
        # 한 그룹 묶음일떄는 마지막 텍스트만 . 2 묶음일때는 마지막 2개 텍스트만  , 3묶음 일때는 마지막 3개 텍스트만 ...
        self.command_text = []
        if len(self.New_text) <= 8 and len(self.New_text) >= 1  :  
            self.command_text.append(self.New_text[-1][-(len(self.New_text)) :]) # command_text에 저장 
        else : 
            return "continue" 
        



    # [이름 , 시간 , 텍스트] 분류 
    def MS_text(self) :
        self.name = []
        self.time = []
        self.ms = []
        for i in self.command_text : 
            if type(i) == list :
                for z in i : 
                    if type(z) == list :
                        self.name.append(z[0])
                        self.time.append(z[1])
                        self.ms.append(z[2])
                    



    # 처리된 텍스트에서 명령어가 있는지 , 명령실행
    def check_command(self) :
        # 명령추가 
        for m in self.ms :
            self.m = str(m)
            if "[+" in self.m : 
                self.add_cm = self.m.replace("[+" , "").split('_')
                if len(self.add_cm) == 2 :
                    # if not self.add_cm[0] in list(diction.keys()) : 
                    #     if not self.add_cm[1] in list(diction.keys()) : 
                        self.diction[self.add_cm[0]] = self.add_cm[1]
                        self.opentalk.send_ms("명령추가완료")
                    #     else : 
                    #         opentalk.send_ms("이미 있는 명령")
                    # else :
                    #     opentalk.send_ms("이미 있는 명령")
                else : 
                    self.opentalk.send_ms("명령추가 오류")
        #일반 명령어         
        self.command = self.diction.keys()
        for i in self.command : 
            if i in self.ms  :
                self.value = self.diction[i]                
                if "break.break" in self.value : 
                    self.opentalk.send_ms("-종료-")
                    save_c(self.diction)
                    self.opentalk.send_ms("사용자 커맨드 저장 완료")
                    return "break"
                elif "diction.list" in self.value : 
                    self.opentalk.send_ms(list(self.diction.keys()))
                else : 
                    self.opentalk.send_ms(self.value)

    
            
    # 실행함수 
    def run_bot(self) : 

        while True :
            self.processing_text()
            
            self.check = self.del_sameTEXT() # continue 리턴 
            if self.check == "continue" : 
                continue
            
            self.MS_text()
                    
            self.check_break = self.check_command()   # break 리턴     
            if self.check_break == "break" :
                break   

            for i in range(len(self.ms)) : 
                print(self.name_room , self.name[i] , self.time[i] , self.ms[i] , sep=' ')





            
