'''
說明:
    每隔一段時間會於senseHat的最左側生成敵人，形狀為視力檢查的C，若敵人移動至senseHat的最右側，則玩家將受到一點傷害
    ，當玩家三點生命耗盡，遊戲結束，玩家須依對應的方向按下JOYSTICK，才能將其消除，而敵人每前進一格的時間間隔會逐漸
    變短。
'''

import random
from time import sleep
import threading
from sense_hat import SenseHat

class Target():
    def __init__(self, pattern):
        #bitmap representation
        pattern_dict={"right":[0, 0, 1, 0, 0, 1, 0, 2, 1, 2],
                              "down":[0, 0, 0, 1, 1, 0, 2, 0, 2, 1],
                              "left":[0, 0, 1, 0, 0, 2, 1, 1, 1, 2],
                              "up":[0, 0, 0, 1, 1, 1, 2, 1, 2, 0]}
        self.is_hit=False
        
        #pattern name
        self.pattern=pattern
        
        #get pattern representation
        self.patternToUse=pattern_dict[pattern]
        
        #y_pos represent the y-axis of the top-left corner of the pattern
        if pattern=="right"or pattern=="left":
            self.y_pos=random.randint(0,4)
        else:
            self.y_pos=random.randint(0,5)
            
        #determine the y_position of the pattern
        for y in range(1,10,2):
            self.patternToUse[y]+=self.y_pos
    
    def render(self):
        for pos in range(0,9,2):
            sense.set_pixel(self.patternToUse[pos],self.patternToUse[pos+1],255,0,0)
    
    def move(self):
            for x in range(0,9,2):
                try:
                    sense.set_pixel(self.patternToUse[x],self.patternToUse[x+1],0,0,0)#disable the target first, then move 1 pixel
                    self.patternToUse[x]+=1
                except:
                    pass
            for x in range(0,9,2):#if target reach the right side line, delete the target and give damage to player
                if self.patternToUse[x]==8:
                    self.is_hit=True
                    self.__del__()
                    pass
                try:
                    sense.set_pixel(self.patternToUse[x],self.patternToUse[x+1],255,0,0)
                except :
                    pass
    
    def __del__(self):
        for del_pos in range(0,9,2):
             if self.patternToUse[del_pos]==8:
                    pass
             try:
                    sense.set_pixel(self.patternToUse[del_pos],self.patternToUse[del_pos+1],0,0,0)
             except :
                    pass


        



        
   
if __name__=="__main__":
    sense=SenseHat()
    score=0
    Sleeptime=1.0
    target_list=[]
    life=3
    global end_thread
    end_thread=True

    sense.clear()
   
#detect which way the player push the joystick,and if it match the first target's pattern, give the player 1 point
    def push(direction):
        global score
        if len(target_list) > 0:
              if target_list[0].pattern = direction:
                    del target_list[0]
                    score += 1
                    
    def push_up():
        push("up")
    def push_down():
        push("down")
    def push_right():
        push("right")
    def push_left():
        push("left")
                
    def stick():
            sense.stick.direction_up = push_up
            sense.stick.direction_down = push_down
            sense.stick.direction_left = push_left
            sense.stick.direction_right = push_right
            
    t_stick=threading.Thread(target=stick)
    t_stick.start()

    def all_move():#move all target on senseHat
        global Sleeptime
        while end_thread==False:
            print('movespeed'+str(Sleeptime))
            sleep(Sleeptime)
            print(len(target_list))
            for t in target_list:
                t.move()
                if Sleeptime<=0.2:
                    Sleeptime-=0.0005
                else:
                    Sleeptime-=0.01
            
            

    
    while True:
        r_pattern=random.randint(1,4)
        if r_pattern==1:
            r_pattern="right"
        elif r_pattern==2:
            r_pattern="down"
        elif r_pattern==3:
            r_pattern="left"
        else:
            r_pattern="up"
            
        if r_pattern=="right" or r_pattern=="left":
            sleep(Sleeptime*3-0.01*3)
            target=Target(r_pattern)
            target.render()
         
        else:
            sleep(Sleeptime*4-0.01*6)
            target=Target(r_pattern)
            target.render()
            
        target_list.append(target)
        
       
        if Sleeptime>=1.0:
            end_thread=False
            t_move=threading.Thread(target=all_move)
            t_move.start()
            
        if target_list[0].is_hit==True:
            life-=1
            
        if life==0:
            break
        
    end_thread=True            
    sense.show_message("GAME OVER")
    sense.show_message("Your score : {}".format(str(score)))


            

