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

predictionFile = os.getcwd() + "/pred.txt"
pred = open(predictionFile, "a")

def writeFile(item,file) :
	file.write(str(item) + "\t")

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
	return matrix

def printGroundTruth(mstMatrix,gt) :
	dict = ["YOLOv3","SSD","YOLOv4","MAX","MIN","AVG","AVG(MAX,MIN)","MEDIAN"]
	sum=[]
	for i in range(0,len(mstMatrix)) :
		element = MST(gt, mstMatrix[i])
		sum.append(element)
	for i in range(0, len(sum)) :
		print("The RMSE for the model", dict[i]," is = ", sum[i])
		writeFile(sum[i],pred)
	for i in sum :
		print("The minimum amongst all is ",min(sum),"\n")
		if(sum.index(min(sum)) < len(dict)) :
			print("The model accuractely detecting is ", dict[sum.index(min(sum))])
			break
		else :
			print("Error: Wrong method")
	return dict[sum.index(min(sum))], sum.index(min(sum))
	
def MST(gt, model) :
	sumMst=0
	if len(gt) == 1:
		print("Error : Check the ground labels")
	for i in range(0,len(gt)-3) :
		sumMst += ((math.sqrt((float(gt[i]) - float(model[i]))**2 + (float(gt[i+1]) - float(model[i+1]))**2) + math.sqrt((float(gt[i+2]) - float(model[i+2]))**2 + (float(gt[i+3]) - float(model[i+3]))**2))/2)**2
		i = i+4
	if len(gt)!=0 :
		sumMst = math.sqrt(sumMst/(len(gt)/4))	
	else :
		print("Not valid input")
	return sumMst

def convert2d(array) :
	minArray = []
	k=-1
	for i in range(0, len(array)) :
		if i%4 == 0 :
			minArray.append([])
			k=k+1
			minArray[k].append(array[i])
		else :
			minArray[k].append(array[i])
	return minArray

def drawBounding(bestMST, modelMST, img, gtContent, indexImage) :
	#Drawing bounding box co-ordinates
	best = convert2d(bestMST)
	gt = convert2d(gtContent)
	model = convert2d(modelMST)
	for i in range(0, len(best)) :
		#cv follows (b,g,r)
		img = cv.rectangle(img,(int(best[i][0]), int(best[i][1])), (int(best[i][2]), int(best[i][3])), (97,30,30), 3)
		img = cv.rectangle(img,(int(gt[i][0]), int(gt[i][1])), (int(gt[i][2]), int(gt[i][3])), (0,0,0), 3)
		if indexImage == 0:
			img = cv.rectangle(img,(int(model[i][0]), int(model[i][1])), (int(model[i][2]), int(model[i][3])), (255,0,0), 3)
		if indexImage == 1:
			img = cv.rectangle(img,(int(model[i][0]), int(model[i][1])), (int(model[i][2]), int(model[i][3])), (0,255,0), 3)
		if indexImage == 2:
			img = cv.rectangle(img,(int(model[i][0]), int(model[i][1])), (int(model[i][2]), int(model[i][3])), (0,0,255), 3)
		cv.imwrite(str(os.getcwd() + output_path + "output_min_" + (arg.path.split("_")[1]).split(".")[0]+"_"+str(indexImage)+".jpg") ,img)

def main() :
	img = cv.imread(os.getcwd() + input_path + arg.path)
	print(img)
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
	pred.write("\t" + minimumModel)
	pred.write("\n")
	for i in range(0,3) :
		img = cv.imread(os.getcwd() + input_path + arg.path)
		if os.path.exists(str(os.getcwd()) + output_path) :
			drawBounding(mstMatrix[minIndex],mstMatrix[i], img, gtContent,i)
		else :
			try :
				os.mkdir(str(os.getcwd()) + output_path)
				drawBounding(mstMatrix[minIndex],mstMatrix[i], img, gtContent,i)
			except :
				print("Creation of outputs folder cannot be done. Manually create a directory 'outputs'")
				break	

if __name__ == "__main__":
    main()
