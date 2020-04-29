from statistics import median
import math

def readFile(model) :
		content = ""
		cont = []
		for line in model :
			for i in line :
				if i != '\t' and i!= '\n' :
					content+=i
				if i == '\t' or i== '\n' :
					cont.append(float(content))
					content = ""
		print("The prediction of the model is : ", cont, "\n")
		return cont

def printMatrix(enMax) :
	k=-1
	matrix = []
	for i in range(0,len(enMax)) :
		if i%4 != 0:
			matrix[k].append(enMax[i])
		elif i%4 == 0:
			matrix.append([])
			k=k+1
			matrix[k].append(enMax[i])
	return matrix;

def printGroundTruth(mstMatrix,gt) :
	dict = ["YOLOv3","SSD","ERROR_OFFSET_YOLOv3","MAX","MIN","AVG","AVG(MAX,MIN)","MEDIAN"]
	sum=[]
	for i in range(0,len(mstMatrix)) :
		element = MST(gt, mstMatrix[i])
		sum.append(element)
	for i in range(0, len(sum)) :
		print("The MST for the model", dict[i]," is = ", sum[i])
	for i in sum :
		print("The minimum amongst all is ",min(sum),"\n")
		if(sum.index(min(sum)) < len(dict)) :
			print("The model accuractely detecting is ", dict[sum.index(min(sum))])
			break
		else :
			print("Error: Wrong method")
	return dict[sum.index(min(sum))]
	
def MST(gt, model) :
	sum=0
	if len(gt) == 1:
		print("Error : Check the ground labels")
	for i in range(0,len(gt)-3) :
		sum = ((math.sqrt((float(gt[i]) - float(model[i]))**2 + (float(gt[i+1]) - float(model[i+1]))**2) + math.sqrt((float(gt[i+2]) - float(model[i+2]))**2 + (float(gt[i+3]) - float(model[i+3]))**2))/2)**2
	if len(gt)!=0 :
		sum = math.sqrt(sum/(len(gt)/4))	
	else :
		print("Not valid input")
	return sum

def main() :
	ssdFile = "ssd.txt"
	yolo3File = "yolo3.txt"
	erroryoloFile = "erroryolo.txt"
	gtFile = "gt.txt"
	ssd = open(ssdFile, "r")
	yolo3 = open(yolo3File,"r")
	erroryolo = open(erroryoloFile,"r")
	gt = open(gtFile,"r")
	yolo3Content = []
	ssdContent = []
	erroryoloContent = []
	gtContent = []
	t = []
	matrix = []
	enMed = []
	enMax = []
	enMin = []
	enAvg = []
	enAvg1 = []
	yolo3Content = readFile(yolo3)
	ssdContent = readFile(ssd)
	erroryoloContent = readFile(erroryolo)
	gtContent = readFile(gt)
	for i in range(0,len(yolo3Content)) :
			enMax.append(float(max(yolo3Content[i],ssdContent[i],erroryoloContent[i])))
	print("The prediction of the MAX model : ")
	matrix = printMatrix(enMax)
	print(matrix,"\n")
	for i in range(0,len(yolo3Content)) :
			enMin.append(float(min(yolo3Content[i],ssdContent[i],erroryoloContent[i])))
	print("The prediction of the MIN model : ")
	matrix = printMatrix(enMin)
	print(matrix,"\n")
	for i in range(0,len(yolo3Content)) :
			enAvg.append(( float(yolo3Content[i])+ float(ssdContent[i]) + float(erroryoloContent[i]))/3 )
	print("The prediction of the AVG model : ")
	matrix = printMatrix(enAvg)
	print(matrix,"\n")
	for i in range(0,len(enMax)) :
			enAvg1.append( (float(enMax[i])+ float(enMin[i]))/2)
	print("The prediction of the AVG(MAX,MIN) model : ")
	matrix = printMatrix(enAvg1)
	print(matrix,"\n")
	for i in range(0,len(enMax)) :
			t = [yolo3Content[i],ssdContent[i],erroryoloContent[i]]	
			enMed.append(float(median(t)))
	print("The prediction of the MEDIAN model : ")
	matrix = printMatrix(enMed)
	print(matrix,"\n")
	mstMatrix = [yolo3Content, ssdContent, erroryoloContent, enMax, enMin, enAvg, enAvg1, enMed]
	minimumModel = printGroundTruth(mstMatrix,gtContent)
	print("The Optimized model is", minimumModel)

if __name__ == "__main__":
    main()