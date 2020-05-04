import sys
import cv2 as cv
import random
import argparse
import os

parser = argparse.ArgumentParser(description='Taking image file')
parser.add_argument('--path', type=str,help='PATH')
arg = parser.parse_args()

def readFile(model) :
		content = ""
		cont = []
		k=-1;
		for line in model :
			if len(line.strip()) != 0 :
				k = k+1
				cont.append([])
				for i in line :
					if i != '\t' and i!= '\n' :
						content+=i
					elif i == '\t' or i== '\n' :
						content = "".join(content.split())
						if content != "" :
							cont[k].append(float(content))
							content = ""
		return cont

def trailingZeros(array) :
	if array[len(array)-1] == [] :
		array.pop(len(array)-1)
	return array

def compare(array,best,point) :
	index = point
	if(point > len(best)) :
		return -1
	minimum = abs(array[index][0] - best[point][0]) + abs(array[index][1] - best[point][1]) + abs(array[index][2] - best[point][2]) + abs(array[index][3] - best[point][3])
	for index in range(point+1,len(array)) :
		x = abs(array[index][0] - best[point][0]) + abs(array[index][1] - best[point][1]) + abs(array[index][2] - best[point][2]) + abs(array[index][3] - best[point][3])
		if(minimum < x) :
			return index-1
		else :
			minimum = min(minimum,x)
	return point


def printTwo(arrayOne, arrayTwo, arrayThree) :
	print("\n" , arrayOne , "\n" , arrayTwo , "\n" , arrayThree)

def sort(array) :
	if len(array) > 1 :
		array = sorted(array, key=lambda x:x[0])
	return array

def removeLines(minLen,array,best) :
	for x in range(0,len(best)) :
		if(len(array) == len(best)) :
			break
		index = compare(array,best,x)
		if index == -1 :
			break;
		elif x!=index :
			for i in range(x,index) :
				array.pop(i)
	if(len(array)!=len(best)) :
		while(len(array)!=len(best)) :
			array.pop(len(array)-1)
	return array

def format(array,height,width) :
	
	for i in range(0, len(array)) :
		array[i][0] = array[i][0] * width
		array[i][1] = array[i][1] * height
		array[i][2] = array[i][2] * height
		array[i][3] = array[i][3] * width
		array[i][1], array[i][2] = array[i][2], array[i][1]
	return array

def writeFile(array,file) :
	for i in range(0,len(array)) :
		file.write("\n")
		for j in range(0,4) :
			file.write(str(array[i][j]))
			if j<=2 :
				file.write("\t")
	file.write("\n")

input_path = "/inputs/"
output_path = "/outputs/"

def main() :
	#reading image
	print(os.getcwd() + input_path + arg.path)
	img = cv.imread(os.getcwd() + input_path + arg.path)
	#reading from text files
	ssdFile = os.getcwd() + str('/'+arg.path.split('.')[0]+"_ssd.txt")
	yolo3File = os.getcwd() + str('/'+arg.path.split('.')[0]+"_yolo3.txt")
	yolo4File = os.getcwd() + str('/'+arg.path.split('.')[0]+"_yolo4.txt")
	gtFile = os.getcwd() + str('/'+arg.path.split('.')[0]+"_gt.txt")
	ssd = open(ssdFile, "r")
	yolo3 = open(yolo3File,"r")
	yolo4 = open(yolo4File, "r")
	gt = open(gtFile, "r")
	yolo3Content = readFile(yolo3)
	ssdContent = readFile(ssd)
	yolo4Content = readFile(yolo4)
	gtContent = readFile(gt)
	#removing empty array elements like [[],[]]
	print(yolo3Content)
	yolo3Content = trailingZeros(yolo3Content)
	ssdContent = trailingZeros(ssdContent)
	yolo4C = trailingZeros(yolo4Content)
	gtContent = trailingZeros(gtContent)
	# sorting the output
	yolo3Content = sort(yolo3Content)
	ssdContent = sort(ssdContent)
	yolo4Content = sort(yolo4Content)
	gtContent = sort(gtContent)
	printTwo(yolo3Content,ssdContent,yolo4Content)
	minLen = min(min(len(yolo3Content),len(ssdContent)),len(yolo4Content))
	
	#Removing the unnecessary lines

	if minLen == len(ssdContent) :
		yolo3Content = removeLines(minLen, yolo3Content, ssdContent)
		yolo4Content = removeLines(minLen, yolo4Content, ssdContent)
	elif minLen == len(yolo4Content) :
		ssdContent = removeLines(minLen, ssdContent, yolo4Content)
		yolo3Content = removeLines(minLen, yolo3Content, yolo4Content)
	else :
		yolo4Content = removeLines(minLen, yolo4Content, yolo3Content)
		ssdContent = removeLines(minLen, ssdContent, yolo3Content)
	
	print("\n", gtContent, "\n")
	#change to (x,y) and (x1,y1) - diagonal co-ordinates
	
	#gtContent = format(gtContent,height,width)
	gtContent = removeLines(minLen, gtContent, ssdContent)
	for i in range(0, len(yolo3Content)) :
		#cv follows (b,g,r)
		img = cv.rectangle(img,(int(yolo3Content[i][0]), int(yolo3Content[i][1])), (int(yolo3Content[i][2]), int(yolo3Content[i][3])), (255,255,255), 3)
		img = cv.rectangle(img,(int(ssdContent[i][0]), int(ssdContent[i][1])), (int(ssdContent[i][2]), int(ssdContent[i][3])), (255,0,0), 3)
		img = cv.rectangle(img,(int(yolo4Content[i][0]), int(yolo4Content[i][1])), (int(yolo4Content[i][2]), int(yolo4Content[i][3])), (0,255,0), 3)
		img = cv.rectangle(img,(int(gtContent[i][0]), int(gtContent[i][1])), (int(gtContent[i][2]), int(gtContent[i][3])), (0,0,255), 3)
		cv.imwrite(str(os.getcwd() + output_path + "output_" + (arg.path.split("_")[1]).split(".")[0] +".jpg") ,img)
	#Writing co-ordinates in the file
	open(ssdFile, "w").close()
	ssd = open(ssdFile, "w")
	yolo3 = open(yolo3File,"w")
	yolo4 = open(yolo4File, "w")
	gt = open(gtFile, "w")
	writeFile(ssdContent, ssd)
	writeFile(yolo4Content, yolo4)
	writeFile(yolo3Content, yolo3)
	writeFile(gtContent, gt)

if __name__ == "__main__":
    main()