import cv2 as cv
import random

def plot_boxes_cv2(img, boxes, savename=None, class_names=None, color=None):
    
    import cv2
    
    
    for box in boxes:
        
        r = int(random.uniform(0,255))
        g = int(random.uniform(0,255))
        b = int(random.uniform(0,255))
        img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (r,g,b), 1)

    if savename:
        
        print("save plot results to %s" % savename)
        cv2.imwrite(savename, img)
        		
	
	
	


def draw_bounding_box(img,path,minModel):
	
	dict = {"YOLOv3":"_yolo3.txt","SSD":"_ssd.txt","ERROR_OFFSET_YOLOv3":"_erroryolo.txt","MAX":"1","MIN":"2","AVG":"3","AVG(MAX,MIN)":"4","MEDIAN":"5","YOLOv4":"_erroryolo.txt"}
	val = dict[minModel]
	
	if len(val) > 1:
		
		coordinate_file_path = path.split('.')[0]+val
		coord_file = open(coordinate_file_path, "r")
		object_diag_list = []
		object_coord_list = []
		
		for line in coord_file:
			
			l = [int(s) for s in line.split('\t')]
			
			for coord in l:
				
				object_coord_list.append(coord)
			
			object_diag_list.append(object_coord_list)
			object_coord_list = []
			
		plot_boxes_cv2(img,object_diag_list,savename=path.split('.')[0]+"_output.jpg")


	else:
		
		coordinate_file_path = path.split('.')[0]+"_Output.txt"
		coord_file = open(coordinate_file_path, "r")
		coord_file_list = []
		object_diag_list = []
		
		for line in coord_file:
			
			coord_file_list.append(line)
		
		object_diag_list = coord_file_list[int(val)-1]
		c = 0
		object_coord_list = []
		object_list = []
		
		for s in object_diag_list.split(','):
			
			if s[0] == "[":
				
				object_list.append(int(float(s[1:])))
			
			elif s[-1] == "\n":
				
				object_list.append(int(float(s[:-2])))
			
			else:
				
				object_list.append(int(float(s)))
				
		obj_list = []		
		
		for coord in object_list:
			
			object_coord_list.append(coord)
			c += 1
			
			if c == 4:
				
				obj_list.append(object_coord_list)
				object_coord_list = []
				c = 0
		
		plot_boxes_cv2(img,obj_list,savename="output.jpg")
