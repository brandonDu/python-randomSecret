#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import operator
import json

'''
该算法的思路为，通过一个样本，进行训练和学习，对模型进行训练
最后将该训练后的模型作为通道，将样本数据中最终的几个作为输入
从而进行预测，并判断。
最终的预测结果需要和下面的数据进行对比分析：
9	10	20	21	22	33	9
'''
# 根据csv列表，读取信息并写入数组中。

def main():
	

	s_data = getCsv()
	i_data = [[int(y) for y in x] for x in s_data]
	r_data = [x[0:6] for x in i_data]
	#定义训练和测试的集合
	interNum = 3
	
	# 定义训练输入和训练输出
	inPut,outPut = getInOutList(r_data,interNum)
	trainIn = inPut[0:len(inPut)-1]
	trainOut = outPut[:]
	# 定义预测输入和预测输出
	preIn = inPut[-1]
	actOut = [9,10,20,21,22,33]
	# print(trainOut[1])
	trainset(trainIn,trainOut)




def getCsv():
    data_all_ls = []
# 打开csv文件，定义打开编码格式，定义分隔符
# 将每条记录拆分成数组并写入二维数组
    with open('ssq.csv' ,encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = '	')
        for row in readCSV:
            data_all_ls.append(row)
    return data_all_ls

#获取训练集合，采用二维数组的格式。
#返回
def getInOutList(data,interval):
	n = len(data)	#数组长度 ex:4
	# print(n)
	m = interval	#每隔一定数量进行划分大组 ex:3
	k = n-m+1 		# 4-3+1 = 2
	# if n = 4, m  = 3, then numSet = 2
	# in = a[0:3], a[1:4] 
	# out = a[3], a[4]
	InNum = [data[i:i+m] for i in range(0,k)]
	OutNum = [data[i+m] for i in range(0,k-1)]
	return InNum,OutNum
#判断两个list中相同的数据数量。
def reSameNumLen(pre,fact):
	SameSet = [i for i in pre if i in fact]
	return len(SameSet)
#对输入的样本和输出的样本进行训练
def trainset(ins,outs):
	modelData = initModel(len(ins[0]))
	for i in range(0,len(ins)):
		tr_i = ins[i] #单一训练集合
		tr_o = outs[i]#单一结果集合
		#print(tr_i,tr_o)
		#针对一对训练输入和输出进行学习。
		modelData = trainls(tr_i,tr_o,modelData)


#初始化模型集合。
#定义M行N列的矩阵
def initModel(n):
	initList = []
	m = 6
	for i in range(0,m):
		vrow = []
		for j in range(0,n):
			vrow.append(1)
		initList.append(vrow)
	return initList
#训练模型
def trainls(il,ol,mll):
	predata = []
	for i in range(0,6):
		coldata = [x[i] for x in il]
		cald = [x*y for x in coldata for y in mll[i]]
		predata.append(sum(cald))
	accurate = compare(ol,predata)
	return accurate

#判断准确度
def compare(fact,pre):
	allNum = len(fact)
	samNum = len([x for x in fact if x in pre])
	return samNum/10




if __name__ == '__main__':
	main()