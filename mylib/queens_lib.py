#/*******************************************************************************
 #
 # \file    queens_lib.py
 # \brief   八皇后问题算法库
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
from collections import Counter
import random
import math

#----------------------------------------------------------------------------------------------------------#
class Queens:
    queens = 0
    col_axis = []
    row_axis = []
    h_value = 0                 #启发式函数值
    loc_opt_flag = 0            #局部最优标签，当flag=1且h_value>0时即认为陷入局部最优
    K = 0                       #局部束算法的K值
    G = 0                       #遗传算法的种群数量
    lb_init_dict = None         #局部束算法的初始K状态
    ga_init_dict = None         #遗传算法的初始G状态
    mutation_rate = 0.1         #遗传变异概率

    #-------------------------模拟退火算法参数--------------------------#
    T_n = 0                     #模拟退火温度
    T_MAX = 10000               #控温上限
    T_lamda = 0.85              #温度转移迭代因子
    #------------------------------------------------------------------#

    # @breif:构造函数
    # @param[in]:queens->皇后问题的皇后数量
    # @retval:None
    def __init__(self,queens):
        self.queens = queens
        self.col_axis = [i for i in range(1,queens+1)]
        self.row_axis = [random.randint(1,queens) for _ in range(queens)]
        self.h_value = self.__h_x(self.row_axis,self.col_axis)
        self.T_n = self.T_MAX    #模拟退火初始温度
        self.K = 8               #预设局部束K值，可更改
        self.G = 14               #预设遗传算法G值，可更改，但必须为偶数
        self.lb_init_dict = self.__random_explor_k(self.row_axis,self.col_axis,self.K)
        self.ga_init_dict = self.__random_explor_k(self.row_axis,self.col_axis,self.G)

    #---------------------封装于内部的私有处理函数-----------------------#
    
    # @breif:合并字典
    # @param[in]:dic1,dic2
    # @retval:dic_new->合并后的字典
    # @attention:dic2会覆盖dic1中相同key的元素，这不影响本问题的求解
    def __dic_sum(self,dic1,dic2):
        return {**dic1,**dic2}

    # @breif:字典正向切片，总共切end-start个
    # @param[in]:dic,start,end
    # @retval:dic_new->切片后的字典
    def __dic_cut(self,dict, start, end):
        temp = list(dict.keys())[start:end]
        dic_new = {}
        for i in range(len(temp)):
            dic_new[temp[i]] = dict.get(temp[i])
        return dic_new

    # @breif:计算组合数
    # @param[in]:m,n->组合因子
    # @retval:组合数
    def __C(self,m,n):
        if((m>n)|(m<0)|(n<0)):
            return 0
        else: 
            return (self.__factorial(n)/(self.__factorial(m)*self.__factorial(n-m)))

    # @breif:计算阶乘
    # @param[in]:number->数值
    # @retval:number的阶乘
    def __factorial(self,number):
        if number <= 1:
            return 1
        else:
            return number*self.__factorial(number-1)

    # @breif:根据笛卡尔坐标计算倾斜坐标系
    # @param[in]:row_list->纵坐标族，col_list->横坐标族
    # @retval:lt2rb_list->从左上到右下的倾斜坐标族，rt2lb_list->从右上到左下的倾斜坐标族
    def __cal_inclined_coordinate(self,row_list,col_list):
        lt2rb_list = []
        rt2lb_list = []
        for i in range(len(row_list)):
            lt2rb_list = lt2rb_list+[col_list[i]+row_list[i]-1]
            rt2lb_list = rt2lb_list+[len(row_list)+row_list[i]-col_list[i]]
        return lt2rb_list,rt2lb_list

    # @breif:根据当前局面随机探索一个不劣于当前的节点
    # @param[in]:row_list->纵坐标族，col_list->横坐标族
    # @retval:new_row_list->新纵坐标族，new_h_value->新的启发函数值
    def __random_explor_opt(self,row_list,col_list):
        h_value = self.__h_x(row_list,col_list)
        new_row_list = row_list.copy()
        while(1):
            i = random.randint(0,len(row_list)-1)
            j = new_row_list[i]
            new_row_list[i] = random.randint(1,len(row_list))
            new_h_value = self.__h_x(new_row_list,col_list)
            if(new_h_value<=h_value):
                break
            else:
                new_row_list[i] = j              #恢复状态
        return new_row_list,new_h_value

    # @breif:根据当前局面随机探索K个邻域节点，并将这些节点及对应的启发函数值组合成字典返回
    # @param[in]:row_list->纵坐标族，col_list->横坐标族,k->要探索的节点数
    # @retval:k_node_dic
    def __random_explor_k(self,row_list,col_list,k):
        k_node_dic = {}
        while(1):
            i = random.randint(0,self.queens-1)
            j = row_list[i]
            row_list[i] = random.randint(1,self.queens)
            k_node_dic[tuple(row_list)] = self.__h_x(row_list,self.col_axis)
            if(len(k_node_dic)==k):
                break
            row_list[i] = j
        return k_node_dic

    # @breif:根据横纵坐标数计算启发式函数值
    # @param[in]:row_list->纵坐标族，col_list->横坐标族
    # @retval:h_value->当前坐标族下的启发函数值
    def __h_x(self,row_list,col_list):
        temp_value = 0
        lt2rb_list,rt2lb_list = self.__cal_inclined_coordinate(row_list,col_list)
        count_dic_row = dict(Counter(row_list))
        count_dic_lt2rb,count_dic_rt2lb = dict(Counter(lt2rb_list)),dict(Counter(rt2lb_list))
        for value in count_dic_row.values():
            temp_value = temp_value+self.__C(2,value)
        for value in count_dic_lt2rb.values():
            temp_value = temp_value+self.__C(2,value)
        for value in count_dic_rt2lb.values():
            temp_value = temp_value+self.__C(2,value)
        return int(temp_value)

    # @breif:随机束算法的概率转移函数
    # @param[in]:h_value
    # @retval:bool->返回1则接受向新方向转移，否则不接受
    def __random_beam_trans(self,h_value):
        trans_p = 2**(-h_value)
        p = random.random()
        if(p<=trans_p):
            return 1
        else:
            return 0 

    # @breif:模拟退火概率转移函数
    # @param[in]:T_current->当前温度
    #            old_h_value->转移前能量,new_h_value->转移后能量
    # @retval:bool->返回1则接受向新方向转移，否则不接受
    def __simu_anneal_trans(self,T_current,old_h_value,new_h_value):
        if(new_h_value<=old_h_value):
            return 1
        else:
            delta = new_h_value - old_h_value
            p_trans = math.exp(-delta/T_current)    #退火概率转移函数
            p = random.random()
            if(p<=p_trans):
                return 1
            else:
                return 0

    # @breif:遗传算法自然选择函数
    # @param[in]:population->种群
    # @retval:selected_population->经过自然选择后的种群
    def __ga_selection(self,population):
        select_rate = list(population.values())
        for i in range(len(select_rate)):
            select_rate[i] = 2**(-select_rate[i])      
        selected_population = {}
        while(1):
            j = random.randint(0,len(select_rate)-1)
            p = random.random()
            if(p <= select_rate[j]):
                selected_population[list(population.keys())[j]] = list(population.values())[j]
            if(len(selected_population) == self.G):
                break
        return selected_population

    # @breif:遗传算法杂交函数
    # @param[in]:selected_population->经过自然选择的种群
    # @retval:crossover_population->杂交后的种群
    def __ga_crossover(self,selected_population):
        crossover_population = {}
        while(1):
            #----------------- 随机确定亲代 ----------------------#
            i = random.randint(1,len(selected_population)-1)
            father = list(list(selected_population.keys())[i])
            mother = list(list(selected_population.keys())[i-1])
            #----------------------------------------------------#

            #----------------- 开始随机杂交 ----------------------#
            j = random.randint(0,self.queens-1)
            son_1 = mother[0:j+1] + father[j+1:self.queens]
            son_2 = father[0:j+1] + mother[j+1:self.queens]
            h_son_1 = self.__h_x(son_1,self.col_axis)
            h_son_2 = self.__h_x(son_2,self.col_axis)
            #----------------- 随机杂交结束 ----------------------#
            crossover_population[tuple(son_1)] = h_son_1
            if(len(crossover_population) == self.G):
                break
            crossover_population[tuple(son_2)] = h_son_2
            if(len(crossover_population) == self.G):
                break
        return crossover_population

    # @breif:遗传算法变异函数
    # @param[in]:crossover_population->杂交的种群
    # @retval:mutation_population->随机变异后的种群
    def __ga_mutation(self,crossover_population):
        mutation_population = {}
        while(1):
            for i in range(len(crossover_population)):
                p = random.random()
                #发生变异
                if(p<=self.mutation_rate):
                    j = random.randint(0,self.queens-1)
                    temp_row_list = list(list(crossover_population.keys())[i])
                    temp_row_list[j] = random.randint(1,self.queens)
                    mutation_population[tuple(temp_row_list)] = self.__h_x(temp_row_list,self.col_axis)
                else:
                    mutation_population[list(crossover_population.keys())[i]] = list(crossover_population.values())[i]
                if(len(mutation_population)==self.G):
                    break
            else:
                continue
            break
        return mutation_population
    #------------------------------------------------------------------#

    #--------------------公有化的算法层函数-----------------------------#

    # @breif:贪婪爬山算法
    # @attention:每次选取全局邻域内最优的点拓展
    # @param[in]:None
    # @retval:None
    def hill_climbing(self):
        best_row_list = self.row_axis.copy()
        for i in range(self.queens):
            temp_row_list = self.row_axis.copy()
            for j in range(self.queens):
                temp_row_list[i] = self.col_axis[j]
                temp_h_value = self.__h_x(temp_row_list,self.col_axis)           
                if(temp_h_value<self.h_value):
                    self.h_value = temp_h_value
                    best_row_list = temp_row_list.copy()
        self.row_axis = best_row_list

    # @breif:首选爬山算法
    # @attetion:随机探索邻域，若探索点优于当前则拓展，直至最优
    # @param[in]:None
    # @retval:None
    def first_hill_climbing(self):
        best_row_list = self.row_axis.copy()
        self.row_axis,self.h_value = self.__random_explor_opt(best_row_list,self.col_axis)

    # @breif:随机重启爬山算法
    # @attetion:当贪婪爬山算法陷入局部最优时，立即随机重启
    # @param[in]:None
    # @retval:None
    def random_rehill_climbing(self):
        self.loc_opt_flag = 1
        best_row_list = self.row_axis.copy()
        for i in range(self.queens):
            temp_row_list = self.row_axis.copy()
            for j in range(self.queens):
                temp_row_list[i] = self.col_axis[j]
                temp_h_value = self.__h_x(temp_row_list,self.col_axis)           
                if(temp_h_value<self.h_value):
                    self.h_value = temp_h_value
                    best_row_list = temp_row_list.copy()
                    self.loc_opt_flag = 0                       #只要有一点改进就不处于局部最优
        if((self.loc_opt_flag==1)&(self.h_value>0)):            #随机重启
            self.row_axis = [random.randint(1,self.queens) for _ in range(self.queens)]
            self.h_value = self.__h_x(self.row_axis,self.col_axis)
        else:
            self.row_axis = best_row_list

    # @breif:局部束算法
    # @param[in]:last_K_dic->前一次K个状态组成的字典
    # @retval:new_K_dic->新一次K个状态组成的字典
    def local_beam(self,last_K_dic):
        new_K_dic = {}
        for key in last_K_dic:
            temp_dic = self.__random_explor_k(list(key),self.col_axis,self.K)
            new_K_dic = self.__dic_sum(new_K_dic,temp_dic)
        new_K_dic = dict(sorted(new_K_dic.items(),key=lambda kv: kv[1]))
        new_K_dic = self.__dic_cut(new_K_dic,0,self.K)
        self.row_axis = list(list(new_K_dic.keys())[0])
        self.h_value = list(new_K_dic.values())[0]
        return new_K_dic 

    # @breif:随机束算法
    # @param[in]:last_K_dic->前一次K个状态组成的字典
    # @retval:new_K_dic->新一次K个状态组成的字典
    def random_beam(self,last_K_dic):
        temp_K_dic,new_K_dic = {},{}
        for key in last_K_dic:
            temp_dic = self.__random_explor_k(list(key),self.col_axis,self.K)
            temp_K_dic = self.__dic_sum(temp_K_dic,temp_dic)
        while(1):
            random_index = random.randint(0,len(temp_K_dic)-1)
            temp_flag = self.__random_beam_trans(list(temp_K_dic.values())[random_index])
            if(temp_flag):
                new_K_dic[list(temp_K_dic.keys())[random_index]] = list(temp_K_dic.values())[random_index]  
            else:
                continue
            if(len(new_K_dic)==self.K):
                break
        new_K_dic = dict(sorted(new_K_dic.items(),key=lambda kv: kv[1]))
        self.row_axis = list(list(new_K_dic.keys())[0])
        self.h_value = list(new_K_dic.values())[0]
        return new_K_dic

    # @breif:模拟退火算法
    # @attetion:以一定概率接受劣于当前节点的值，以求避免陷入局部最优
    # @param[in]:None
    # @retval:None
    def simu_anneal(self):
        temp_row_list = self.row_axis.copy()
        i = random.randint(0,self.queens-1)
        temp_row_list[i] = random.randint(1,self.queens)
        temp_h_value = self.__h_x(temp_row_list,self.col_axis)
        flag = self.__simu_anneal_trans(self.T_n,self.h_value,temp_h_value)
        self.T_n = self.T_n*self.T_lamda
        if(flag):
            self.row_axis = temp_row_list
            self.h_value = temp_h_value
        else:
            return
    
    # @breif:遗传算法
    # @param[in]:last_G_dic->前一代种群组成的字典
    # @retval:new_G_dic->新一代种群组成的字典
    def genetic_algorithm(self,last_G_dic):
        selected_population = self.__ga_selection(last_G_dic)
        crossover_population = self.__ga_crossover(selected_population)
        new_G_dic = self.__ga_mutation(crossover_population)
        new_G_dic = dict(sorted(new_G_dic.items(),key=lambda kv: kv[1]))
        self.row_axis = list(list(new_G_dic.keys())[0])
        self.h_value = list(new_G_dic.values())[0]
        return new_G_dic
    #------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------#