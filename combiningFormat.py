import sys
import cv2 as cv
import random

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
	if(array[len(array)-1] == []) :
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


def printTwo(arrayOne, arrayTwo) :
	print("\n" , arrayOne , "\n" , arrayTwo)

def sort(array) :
	if len(array) > 1 :
		array = sorted(array, key=lambda x:x[0])
	return array

def main() :
	img = cv.imread("input2.jpeg")
	ssdFile = "ssd.txt"
	yolo3File = "yolo3.txt"
	ssd = open(ssdFile, "r")
	yolo3 = open(yolo3File,"r")
	yolo3Content = readFile(yolo3)
	ssdContent = readFile(ssd)
	trailingZeros(yolo3Content)
	trailingZeros(ssdContent)
	yolo3Content = sort(yolo3Content)
	ssdContent = sort(ssdContent)
	printTwo(yolo3Content,ssdContent)
	minLen = min(len(yolo3Content),len(ssdContent))
	if(minLen == len(ssdContent)) :
		for x in range(0,len(ssdContent)) :
			if(len(yolo3Content) == len(ssdContent)) :
				break
			index = compare(yolo3Content,ssdContent,x)
			if index == -1 :
				break;
			elif x!=index :
				for i in range(x,index) :
					yolo3Content.pop(i)
	if(len(yolo3Content)!=len(ssdContent)) :
		while(len(yolo3Content)!=len(ssdContent)) :
			yolo3Content.pop(len(yolo3Content)-1)
	elif(minLen == len(yolo3Content)) :
		for x in range(0,len(yolo3Content)) :
			if(len(yolo3Content) == len(ssdContent)) :
				break
			index = compare(ssdContent,yolo3Content,x)
			if index == -1 :
				break;
			elif x!=index :
				for i in range(x,index) :
					ssdContent.pop(i)
	if(len(yolo3Content)!=len(ssdContent)) :
		while(len(yolo3Content)!=len(ssdContent)) :
			ssdContent.pop(len(ssdContent)-1)
	print(len(yolo3Content))
	print(len(ssdContent))
	f = open("drawbb.txt","w")
	f.write(str(yolo3Content))
	f.write(str('input2.jpeg'))
	for i in range(0, len(yolo3Content)) :
		r = int(random.uniform(0,255))
		g = int(random.uniform(0,255))
		b = int(random.uniform(0,255))
		img = cv.rectangle(img,(int(yolo3Content[i][0]), int(yolo3Content[i][1])), (int(yolo3Content[i][2]), int(yolo3Content[i][3])), (r,g,b), 3)
		cv.imwrite("output.jpg",img)
	img = cv.imread("input2.jpeg")
	for i in range(0, len(ssdContent)) :
		r = int(random.uniform(0,255))
		g = int(random.uniform(0,255))
		b = int(random.uniform(0,255))
		img = cv.rectangle(img,(int(ssdContent[i][0]), int(ssdContent[i][1])), (int(ssdContent[i][2]), int(ssdContent[i][3])), (r,g,b), 3)
		cv.imwrite("output1.jpg",img)

if __name__ == "__main__":
    main()