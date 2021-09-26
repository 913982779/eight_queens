# 2020.11.06 八皇后问题演示软件说明文档

## 1 工程说明

##### 1.1 项目简介

@项目名称：八皇后问题演示软件
@项目作者：1851738 杨皓冬	

##### 1.2 项目文件目录结构

└── 八皇后问题演示软件_1851738杨皓冬
 │    ├──01 Eight_Queens.py  	   	   // 八皇后问题软件展示交互界面
 │    ├──02 mylib
 │    │   ├── 01 __init__.py     			  		// 链接到mylib底层库文件
 │    │   ├── 02 queens_lib.py	  		// 此为八皇后问题算法库，包括爬山法、束搜索等底层实现 
 │    │   ├── 03 screen_design.py		// 八皇后问题GUI设计，包含页面布设、按键响应等
 │
 │   ├──03 README.md	 				  //即本文档，包含环境配置、操作手册等	
 │		
 │   ├──04 优化搜索实验报告.pdf



## 2 环境配置

Python 3.7.3、VSCode2019
Package:  time、operator、mylib、tkinter、pygame1.9.6
OS: Windows10

其中mylib是本人制作的底层库，需手动导入至工程文件夹根目录下



## 3 操作手册

(1) 环境配置完成后，打开Eight_Queens.py并运行。运行成功则显示演示交互界面，如Fig 3.1所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201106163030897.png#pic_center)

<center>Fig 3.1</center>

(2) 选择算法，并配置皇后数量、运行速度等基本参数。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201106163138121.png#pic_center)

<center>Fig 3.2</center>

若不按要求配置参数，将无法运行程序，如图Fig3.3

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020110616332622.png#pic_center)

<center>Fig 3.3</center>

(3) 以模拟退火算法为例，点击执行：局部最优画面将显示求解过程，找到解后显示在全局最优画面中。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201106163355621.png#pic_center)

<center>Fig 3.4</center>


(4) 点击“退出”即可退出软件



