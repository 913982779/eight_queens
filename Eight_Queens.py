#/*******************************************************************************
 #
 # \file    Eight_Queens.py
 # \brief   八皇后问题软件展示交互界面
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
import pygame
import sys
from mylib import queens_lib
from mylib.queens_lib import Queens
from mylib.screen_design import *

#--------------------------------------------------------------------------------
#主函数，使用pygame框架，无限循环对各种事件然后相应处理
#--------------------------------------------------------------------------------
if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if  param.STATUS == param.INIT:
            param.cmg.draw_blocks_line()
        elif param.STATUS == param.EXIT:
            if tk.messagebox.askokcancel('提示', '要退出画面吗'):
                break
            param.STATUS = param.INIT
        elif param.STATUS == param.STOP:
            pass
        elif param.STATUS == param.ERROR_PARAM_FALSE:
            tk.messagebox.showwarning('提示', '请输入合法的参数！')
            param.STATUS = param.INIT
        elif param.STATUS ==param.ERROR_PARAM_NULL:
            tk.messagebox.showwarning('提示', '请配置参数与算法！')
            param.STATUS = param.INIT
        #------------------------------- 算法调用区 -----------------------------------#
        elif param.EXE_FLAG == 1:
            param.cmg.printBlocks(param.queens)
            if param.STATUS == param.EXE_CLIMB:
                param.queens.hill_climbing()
            elif param.STATUS == param.EXE_RECLIMB:
                param.queens.random_rehill_climbing()
            elif param.STATUS == param.EXE_FSTCLIMB:
                param.queens.first_hill_climbing()
            elif param.STATUS == param.EXE_ANNEAL:
                param.queens.simu_anneal()
            elif param.STATUS == param.EXE_LOCBEAM:
                if(param.beam_flag):
                    temp_dic = param.queens.lb_init_dict
                    param.beam_flag = 0
                temp_dic = param.queens.local_beam(temp_dic)
            elif param.STATUS == param.EXE_RANBEAM:
                if(param.beam_flag):
                    temp_dic = param.queens.lb_init_dict
                    param.beam_flag = 0
                temp_dic = param.queens.random_beam(temp_dic)
            elif param.STATUS == param.EXE_GA:
                if(param.beam_flag):
                    temp_dic = param.queens.ga_init_dict
                    param.beam_flag = 0         
                temp_dic = param.queens.genetic_algorithm(temp_dic)
        #-----------------------------------------------------------------------------#
            h_label = tk.Label(embed,text='启发式函数值h:'+str(param.queens.h_value)+' ',font=('黑体',15),bg='white')
            h_label.place(x=426,y=35)
            
        #显示游戏画面
        pygame.display.flip()	
        #设置帧率：长期画面不操作，设置成最闲
        if param.EXE_FLAG == 1:
            clock.tick(param.TICK_STEP)
        else:
            clock.tick(param.TICK_NORMAL)            
        root.update()