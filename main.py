import csv
import operator

# 根据csv列表，读取信息并写入数组中。
# [4, 18, 20, 22, 25, 33]
# {'learnrate': 0.094, 'posibility': {'16': -0.259, '2': -0.734, '1': -0.682, '33': 0.849, '15': 0.308, '26': -0.504, '23': 0.416, '32': -0.504, '14': -0.569, '25': 0.762, '21': -0.432, '31': -0.362, '12': 0.357, '29': -0.395, '13': -0.85, '4': 0.73, '7': -0.468, '24': 0.442, '3': 0.096, '11': 0.126, '17': -0.214, '27': -0.194, '10': 0.614, '8': -0.428, '5': 0.192, '18': 0.713, '22': 0.878, '19': -0.391, '20': 0.638, '9': 0.05, '28': 0.126, '6': -0.325, '30': 0.13}, 'threshole': 0.879}
# [Finished in 16200.3s]

def main():
	s_data = getCsv()
	i_data = [[int(y) for y in x] for x in s_data]
	study={}#学习参数字典
	#最终预测参数字典
	prePara = {}
	rightNum =0;
	
	#study['threshole']=0.618 #define 0.1~100  #range(0.1,100,0.1)
	#study['learnrate']=0.3 #define 0.01~1     #range(0.01,0.1,0.01)
	thresholeArr = [round(i,4) for i in list(drange(0.1,1,0.01))]
	learnrateArr = [round(i,4) for i in list(drange(0.01,0.1,0.01))]

	for i in thresholeArr:
		study['threshole']=i
		for j in learnrateArr:
			study['learnrate']=j
			study['posibility'] = initNumPossibility()
			predict = model(i_data[0:len(i_data)-2],study)
			factArr = i_data[len(i_data)-1][0:6]
			sameCount = comparePreAndFac(predict,factArr)
			if sameCount>rightNum:
				prePara['threshole'] = predict['threshole'] 
				prePara['learnrate'] = predict['learnrate']
				rightNum = sameCount
	###
	prePara['posibility'] = initNumPossibility()
	outpre = model(i_data,prePara)
	preNums = selFromStudy(outpre)
	print(preNums)
	print(outpre)
	#1	3	8	11	29	31	13


def getCsv():
    data_all_ls = []
# 打开csv文件，定义打开编码格式，定义分隔符
# 将每条记录拆分成数组并写入二维数组
    with open('ssq.csv' ,encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = '	')
        for row in readCSV:
            data_all_ls.append(row)
    return data_all_ls

def model(data,game):
	#traindata= data[0:len(data)-2]	
	for odata in data:
		#读取数组中的元素，并进行分析判断，如果当前数值，则在范围内增加概率
		#读取概率，如果概率值超过了阈值，则进行取反，同时周边范围也进行取反操作
		vstudy = anaTrain(odata,game)
	return vstudy

def anaTrain(data,train):
	allData = list(range(1,34))
	vdata = data[0:6]
	outdata = [i for i in allData if i not in vdata]
	# red_data_2=[x-2 for x in red if x>2]+[x+2 for x in red if x<32]

	oposibility = train['posibility']
	
	m = train['threshole']  #阈值
	n = train['learnrate']  #学习速率
	for x in vdata:
		v = oposibility[str(x)]+n
		if v>=m:
			v = v%m
			oposibility[str(x)] = -1*v
		elif v<=-1*m:
			v = -1*(v%m)
			oposibility[str(x)] = -1*v
		else:
			oposibility[str(x)] = v
		oposibility[str(x)] = round(oposibility[str(x)],4)
	##
	for y in outdata:
		v = oposibility[str(y)]-n
		if v>=m:
			v = v%m
			oposibility[str(y)] = -1*v
		elif v<=-1*m:
			v = -1*(v%m)
			oposibility[str(y)] = -1*v
		else:
			oposibility[str(y)] = v
		oposibility[str(y)] = round(oposibility[str(y)],4)

	return train

###初始化字典中的每个数字的概率。
def initNumPossibility():
	obj={}#每个数字的灵魂，即概率字典
	vm=list(range(1,34))
	for i in vm:
		obj[str(i)] = 0
	return obj
###根据计算出的每个数字的概率字典。
###通过比较概率最大的几个数字和实际数字的相同数量，判断概率字典的准确度。
def comparePreAndFac(predic,fact):
	preDict = predic['posibility'] #the predict set for every num.
	preSelSix = dict(sorted(preDict.items(), key=operator.itemgetter(1), reverse=True)[:6])#获取概率最大的六个数字
	# pB = dict(sorted(predictBlue.items(), key=operator.itemgetter(1), reverse=True)[:1])	
	# pre = sorted([int(i) for i in list(pR.keys())])+[int(i) for i in list(pB.keys())]
	pre = sorted([int(i) for i in list(preSelSix.keys())])
	sameNum = [x for x in fact if x in pre]
	print(fact,pre,len(sameNum))
	return len(sameNum)
#define range for float.
def drange(start,stop,step):
	r=start
	while r<stop:
		yield r
		r+=step

def selFromStudy(ov):
	ovp = ov['posibility'] #the predict set for every num.
	ovpsix = dict(sorted(ovp.items(), key=operator.itemgetter(1), reverse=True)[:6])#获取概率最大的六个数字
	# pB = dict(sorted(predictBlue.items(), key=operator.itemgetter(1), reverse=True)[:1])	
	# pre = sorted([int(i) for i in list(pR.keys())])+[int(i) for i in list(pB.keys())]
	ovlast = sorted([int(i) for i in list(ovpsix.keys())])
	return ovlast

if __name__ == '__main__':
	main()