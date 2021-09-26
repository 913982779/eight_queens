#/*******************************************************************************
 #
 # \file    screen_design.py
 # \brief   八皇后问题GUI设计，包含页面布设、按键响应等
 # \author  1851738杨皓冬
 # \version 6.0
 # \date    2020-11-06
 #
 # -----------------------------------------------------------------------------
 #
 # -----------------------------------------------------------------------------
 # 文件修改历史：
 # <时间>       |  <版本>  | <作者>        |
 # 2020-10-31   |  v1.0    | 1851738杨皓冬 |
 # 2020-11-01   |  v2.0    | 1851738杨皓冬 |
 # 2020-11-03   |  v3.0    | 1851738杨皓冬 |
 # 2020-11-04   |  v4.0    | 1851738杨皓冬 |
 # 2020-11-05   |  v5.0    | 1851738杨皓冬 |
 # 2020-11-06   |  v6.0    | 1851738杨皓冬 |
 # -----------------------------------------------------------------------------
# ******************************************************************************/
import os
import pygame
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk
from mylib.queens_lib import Queens

# @name:画面设置类
# @breif:用于对画布和其中的框架Frame进行设计处理，并提供棋子移动的函数接口
class CMG:
    screen = None
    screen_rect = None

    #------------------------------------- 颜色属性 ---------------------------------------------#
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (240,163,24)
    YELLOW = (255, 255, 0)
    GREY = (128,128,128)
    #-------------------------------------------------------------------------------------------#

    #------------------------------------ 棋盘设计 ----------------------------------------------#
    block_number = 0                                        #每行/每列棋子数量
    blockSize_unit = 0                                      #单位格子大小
    blockSize_all = 400                                     #整个棋盘大小
    delta_x = 0                                             #为使棋盘居中的x偏移量
    delta_y = 0                                             #为使棋盘居中的y偏移量
    delta_two_blocks = 50                                   #过程棋盘和结果棋盘的间距
    #-------------------------------------------------------------------------------------------#

    def __init__(self,screen,number):                       #用屏幕和皇后数量初始化
        self.screen = screen
        self.block_number = number
        self.blockSize_unit = self.blockSize_all//number
        self.screen_rect = None
        surface = pygame.display.get_surface()
        width,height = surface.get_width(), surface.get_height()
        self.delta_x, self.delta_y = (width-2*self.blockSize_all-self.delta_two_blocks)/2, (height-self.blockSize_all)/2
    
    # @breif:绘制棋盘
    # @param[in]:None
    # @retval:None
    def draw_blocks_line(self):
        self.screen.fill(self.WHITE)    
        for x in range(0,self.block_number+1):
            end_pos = [(x*self.blockSize_unit+self.delta_x,self.delta_y),                                                  \
                       (x*self.blockSize_unit+self.delta_x,self.block_number*self.blockSize_unit+self.delta_y)]
            pygame.draw.lines(self.screen, CMG.RED,0 , end_pos, 2)
            end_pos = [(x*self.blockSize_unit+self.delta_x+450,self.delta_y),                                              \
                       (x*self.blockSize_unit+self.delta_x+450,self.block_number*self.blockSize_unit+self.delta_y)]
            pygame.draw.lines(self.screen, self.RED,0 , end_pos, 2)
        for y in range(0,self.block_number+1):
            end_pos = [(self.delta_x,y*self.blockSize_unit+self.delta_y),                                                  \
                       (self.block_number*self.blockSize_unit+self.delta_x,y*self.blockSize_unit+self.delta_y)]
            pygame.draw.lines(self.screen, self.RED,0 , end_pos, 2)
            end_pos = [(450+self.delta_x,y*self.blockSize_unit+self.delta_y),                                              \
                       (450+self.block_number*self.blockSize_unit+self.delta_x,y*self.blockSize_unit+self.delta_y)]
            pygame.draw.lines(self.screen, self.RED,0 , end_pos, 2)
    
    # @breif:绘制棋子，为动态演示八皇后求解过程提供接口
    # @param[in]:queen->Queens对象
    # @retval:None
    def printBlocks(self,queen):
        global param  
        if self.screen_rect == None:
            self.draw_blocks_line()
            self.screen_rect = self.screen.subsurface(0,0,1000,570).copy()
        else:
            self.screen.blit(self.screen_rect,(0,0))        
        for r in range(len(queen.row_axis)):
            x = r*self.blockSize_unit + self.delta_x
            y1 = (queen.row_axis[r]-1) *self.blockSize_unit+self.delta_y
            pygame.draw.rect(self.screen, self.GREY, ((x,y1), (self.blockSize_unit, self.blockSize_unit)), 0)
        if queen.h_value == 0:
            for r in range(len(queen.row_axis)):
                x = r*self.blockSize_unit + self.delta_x +450
                y2 = (queen.row_axis[r]-1) *self.blockSize_unit+self.delta_y
                pygame.draw.rect(self.screen, self.ORANGE, ((x,y2), (self.blockSize_unit, self.blockSize_unit)), 0)
                param.STATUS = param.STOP

#=========================================== tkinker静态布局 ======================================================#
#=========================================== pygame动态刷新 =======================================================#
root = tk.Tk()
root.title("八皇后问题求解演示 作者：1851738杨皓冬")
root.resizable(0,0)

embed = tk.Frame(root,width = 1000, height = 570)
embed.grid(columnspan = 800, rowspan = 730)
embed.pack(side = BOTTOM)

top_win = tk.Frame(root, width = 1000, height = 200)
top_win.pack(side = TOP)

top_left_win = tk.Frame(top_win,width = 100, height = 200)
top_left_win.pack(side = LEFT)
top_right_win = tk.Frame(top_win,width = 600, height = 200)
top_right_win.pack(side = RIGHT)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())          #将pygame处理窗口附着在tkinter上
os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((1000,570))

img = Image.open('tongji_logo.png')
photo = ImageTk.PhotoImage(img)
imglabel = tk.Label(top_left_win, image=photo)
imglabel.grid(row=0, column=0, columnspan=1)

pygame.display.init()
pygame.mixer.init()
#===============================================================================================================#

# @name:事件响应类
# @breif:用于对画布中各个事件进行响应，执行与用户的实际交互；
#        同时通过内部定义状态STATUS与主函数接口匹配
class Fig_Response:
    #------------------------------ 宏定义------------------------------------#
    EXE_FLAG = 0                                #执行标志
    INIT = 1                                    #初始状态
    STOP = 2                                    #停止演示
    EXIT = 3                                    #退出演示
    EXE_CLIMB = 4                               #爬山法(贪婪)
    EXE_FSTCLIMB =5                             #首选爬山法
    EXE_RECLIMB = 6                             #随机重启爬山法
    EXE_LOCBEAM = 7                             #局部束搜索
    EXE_RANBEAM = 8                             #随机束搜索
    EXE_ANNEAL = 9                              #模拟退火算法
    ERROR_PARAM_FALSE = 10                      #参数错误警告
    ERROR_PARAM_NULL = 11                       #参数空警告
    EXE_GA = 12                                 #遗传算法
    #-------------------------------------------------------------------------#

    #--------------------------演示参数配置------------------------------------#
    V_MAX = 99                                  #演示速度上限
    V_MIN = 1                                   #演示速度下限
    NUMBER_MAX = 15                             #皇后数量上限
    NUMBER_MIN = 4                              #皇后数量下限
    #-------------------------------------------------------------------------#
    
    #-----------------------------其他配置------------------------------------#
    STATUS = 0
    TICK_NORMAL = 0
    TICK_STEP = 0
    cmg = None
    queens = None
    beam_flag = 1                              #局部束算法的初始状态标记，若flag=1
                                               #则说明还未初始化
    #-------------------------------------------------------------------------#

    def __init__(self):
        self.STATUS = self.INIT
        self.TICK_NORMAL = 5
        self.TICK_STEP = 5
        self.queens = Queens(8)
        self.cmg = CMG(screen,self.queens.queens)
        self.beam_flag = 0
    
    #-----------------------按钮控件响应回调函数组------------------------------#
    def get_input_data(self,inputcell,min,max):
        if inputcell.get().isdigit():
            num = int(inputcell.get())
            if min<=num and num<=max:
                return num
        return -1

    def exit_game(self):
        self.EXE_FLAG = 0
        self.STATUS = self.EXIT

    def stop_game(self):
        self.EXE_FLAG = 0
        self.STATUS = self.STOP

    def sel_game(self):
        #空参数检查
        if((cmb.get()=='')or(inputqs.get()=='')or(inputspd.get()=='')):
            self.EXE_FLAG = 0
            self.STATUS = self.ERROR_PARAM_NULL
            return
        queens_number = self.get_input_data(inputqs,self.NUMBER_MIN,self.NUMBER_MAX)
        speed = self.get_input_data(inputspd,self.V_MIN,self.V_MAX)

        #非法参数检查
        if ((queens_number<self.NUMBER_MIN)or(queens_number>self.NUMBER_MAX)or(speed<self.V_MIN)or(speed>self.V_MAX)):
            self.EXE_FLAG = 0
            self.STATUS = self.ERROR_PARAM_FALSE
            return
        else:
            self.queens = Queens(queens_number)
            self.cmg = CMG(screen,queens_number)
            self.TICK_STEP = speed
            if(cmb.get()=='爬山法'):
                self.STATUS = self.EXE_CLIMB
                self.EXE_FLAG = 1
            elif (cmb.get()=='首选爬山法'):
                self.STATUS = self.EXE_FSTCLIMB
                self.EXE_FLAG = 1
            elif(cmb.get()=='随机重启爬山法'):
                self.STATUS = self.EXE_RECLIMB
                self.EXE_FLAG = 1
            elif(cmb.get()=='局部束搜索'):
                self.beam_flag = 1
                self.STATUS = self.EXE_LOCBEAM
                self.EXE_FLAG = 1
            elif(cmb.get()=='随机束搜索'):
                self.beam_flag = 1
                self.STATUS = self.EXE_RANBEAM
                self.EXE_FLAG = 1
            elif(cmb.get()=='模拟退火'):
                self.STATUS = self.EXE_ANNEAL
                self.EXE_FLAG = 1
            elif(cmb.get()=='遗传算法'):
                self.beam_flag = 1
                self.STATUS = self.EXE_GA
                self.EXE_FLAG = 1
            else:
                self.STATUS =self.INIT
    #-------------------------------------------------------------------------#

param = Fig_Response()  #全局响应变量，用于前后端交互

#======================================= 控件设计与定义 ====================================================#
cmb_select = tk.Label(top_right_win, text='请选择算法：',font=('黑体',15))
cmb_select.place(x=190,y=10)
cmb = ttk.Combobox(top_right_win)
cmb['value'] = ('爬山法','首选爬山法','随机重启爬山法','局部束搜索','随机束搜索','模拟退火','遗传算法')
cmb.place(x=310,y=10)

label_loc_opt = tk.Label(embed, text='局部最优解',font=('黑体',15),bg='white')
label_loc_opt.place(x=220,y=500)

label_opt = tk.Label(embed, text='全局最优解',font=('黑体',15),bg='white')
label_opt.place(x=670,y=500)

btnwin_qs_l = tk.Label(top_right_win, text='请输入皇后数(4-15)：',font=('黑体',15))
btnwin_qs_l.place(x=190,y=50)
inputqs = StringVar()
btnwin_qs_e = tk.Entry(top_right_win, show=None,width=5,textvariable = inputqs)
btnwin_qs_e.place(x=390,y=50)

btnwin_spd_l = tk.Label(top_right_win, text='演示速度(1-99)：',font=('黑体',15))
btnwin_spd_l.place(x=190,y=90)
inputspd = StringVar()
btnwin_spd_e = tk.Entry(top_right_win, show=None,width=5,textvariable = inputspd)
btnwin_spd_e.place(x=390,y=90)

button_sel_b = Button(top_right_win,text = '执行', font=('黑体',15), width=7, command=param.sel_game)
button_sel_b.place(x=200,y=150)

button_stop_b = Button(top_right_win,text = '本次演示结束', font=('黑体',15), width=13, command=param.stop_game)
button_stop_b.place(x=310,y=150)

button_exit_b = Button(top_right_win,text = '退出画面', font=('黑体',15), width=10, command=param.exit_game)
button_exit_b.place(x=480,y=150)
#===============================================================================================================#
