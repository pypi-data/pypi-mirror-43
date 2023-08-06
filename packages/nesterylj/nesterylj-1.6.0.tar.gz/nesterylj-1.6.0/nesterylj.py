import sys
"""这是nester.py模块，提供了一个名为print_lol()的函数用来打印列表，其中包含或不包含嵌套列表"""
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
	"""这个函数取一个位置参数，名为the_list，这可以是任何Python列表（也可以是包含嵌套列表的列表）。
	所指定的列表中的每个数据项会（递归地）输出到屏幕上，个数据项各占一行。fh参数默认在屏幕输出，也可以指定其他输出"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fh)
		else:
			if indent:
				# for tab_stop in range(level):
				# 	print("\t",end='')
				print("\t"*level,end='',file=fh)
			print(each_item,file=fh)
