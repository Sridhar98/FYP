from statistics import median
import math
import cv2 as cv
import argparse
import os

parser = argparse.ArgumentParser(description='Taking image file')
parser.add_argument('--path', type=str,help='PATH')
arg = parser.parse_args()
input_path = "/inputs/"
output_path = "/outputs/"

def readFile(model) :
		content = ""
		cont = []
		for line in model :
			if len(line.strip()) != 0 :
				for i in line :
					if i != '\t' and i!= '\n' :
						content+=i
					elif i == '\t' or i== '\n' :
						content = "".join(content.split())
						if content != "" :
							cont.append(float(content))
							content = ""
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
	dict = ["YOLOv3","SSD","YOLOv4","MAX","MIN","AVG","AVG(MAX,MIN)","MEDIAN"]
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
	return dict[sum.index(min(sum))], sum.index(min(sum))
	
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
	img = cv.imread(os.getcwd() + input_path + arg.path)
	ssdFile = os.getcwd() + str('/'+arg.path.split('.')[0]+"_ssd.txt")
	yolo3File = os.getcwd() + str('/'+arg.path.split('.')[0]+"_yolo3.txt")
	yolo4File = os.getcwd() + str('/'+arg.path.split('.')[0]+"_yolo4.txt")
	gtFile = os.getcwd() + str('/'+arg.path.split('.')[0]+"_gt.txt")
	ssd = open(ssdFile, "r")
	yolo3 = open(yolo3File,"r")
	yolo4 = open(yolo4File,"r")
	gt = open(gtFile,"r")
	yolo3Content = []
	ssdContent = []
	yolo4Content = []
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
	yolo4Content = readFile(yolo4)
	gtContent = readFile(gt)
	print (len(yolo3Content))
	print (len(yolo4Content))
	print (len(ssdContent))
	print (len(gtContent))
	for i in range(0,len(yolo3Content)) :
			enMax.append(float(max(yolo3Content[i],ssdContent[i],yolo4Content[i])))
	print("The prediction of the MAX model : ")
	matrix = printMatrix(enMax)
	print(matrix,"\n")
	for i in range(0,len(yolo3Content)) :
			enMin.append(float(min(yolo3Content[i],ssdContent[i],yolo4Content[i])))
	print("The prediction of the MIN model : ")
	matrix = printMatrix(enMin)
	print(matrix,"\n")
	for i in range(0,len(yolo3Content)) :
			enAvg.append(( float(yolo3Content[i])+ float(ssdContent[i]) + float(yolo4Content[i]))/3 )
	print("The prediction of the AVG model : ")
	matrix = printMatrix(enAvg)
	print(matrix,"\n")
	for i in range(0,len(enMax)) :
			enAvg1.append( (float(enMax[i])+ float(enMin[i]))/2)
	print("The prediction of the AVG(MAX,MIN) model : ")
	matrix = printMatrix(enAvg1)
	print(matrix,"\n")
	for i in range(0,len(enMax)) :
			t = [yolo3Content[i],ssdContent[i],yolo4Content[i]]	
			enMed.append(float(median(t)))
	print("The prediction of the MEDIAN model : ")
	matrix = printMatrix(enMed)
	print(matrix,"\n")
	mstMatrix = [yolo3Content, ssdContent, yolo4Content, enMax, enMin, enAvg, enAvg1, enMed]
	minimumModel, minIndex = printGroundTruth(mstMatrix,gtContent)
	print("The Optimized model is", minimumModel)
	minArray = []
	k=-1
	for i in range(0, len(mstMatrix[minIndex])) :
		if i%4 == 0 :
			minArray.append([])
			k=k+1
			minArray[k].append(mstMatrix[minIndex][i])
		else :
			minArray[k].append(mstMatrix[minIndex][i])

	#Drawing bounding box co-ordinates
	for i in range(0, len(minArray)) :
		#cv follows (b,g,r)
		img = cv.rectangle(img,(int(minArray[i][0]), int(minArray[i][1])), (int(minArray[i][2]), int(minArray[i][3])), (0,0,0), 3)
		cv.imwrite(str(os.getcwd() + output_path + "output_min_" + (arg.path.split("_")[1]).split(".")[0] +".jpg") ,img)

if __name__ == "__main__":
    main()