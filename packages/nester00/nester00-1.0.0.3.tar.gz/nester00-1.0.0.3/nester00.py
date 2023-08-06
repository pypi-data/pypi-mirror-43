﻿"""这是“nester00.py”模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。"""
def print_lol(the_list,indent=False,level=0):
    """这个函数取一个位置参数，名为“the_list”,这可以是任何Python列表（也可以是包含嵌	套    列表）。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项占一行。
    第二个参数（名为“level”）用来在遇到嵌套列表时插入制表符。
    第三个参数（名为“indent”,默认False(不插入制表符)，当为True时参数level才起作用）"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_item)
