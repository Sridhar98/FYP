import cv2 as cv
import random
import argparse

input_path = 'inputs/'

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image-path', type=str, help='The path to the image file')
FLAGS = parser.parse_args()

def plot_boxes_cv2(img_in_path,boxes, savename=None, class_names=None, color=None):
    
    import cv2
    img = cv2.imread(img_in_path)
    
    for box in boxes:
        
        r = int(random.uniform(0,255))
        g = int(random.uniform(0,255))
        b = int(random.uniform(0,255))
        img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (r,g,b), 1)

    if savename:
        
        print("save plot results to %s" % savename)
        cv2.imwrite(savename, img)
        		
	
def draw_bounding_box():
		bbfile = open(input_path+str(FLAGS.image_path),"r")
		c = 0
		for line in bbfile:
			print('line: ',len(line))
			if c == 0:
				coord_string = line
				line = ""
			elif c == 1:
				image_in_path = line.split('[')[0]
				line = ""
			c += 1
			if c == 2:
				break
				
		
		coord_string = coord_string.split('[')[-1]
		coord_string = coord_string.split(']')[0]
		
		object_list = []
		object_coord_list = []
		
		c = 0
		for coord in coord_string.split(','):
			object_coord_list.append(int(float(coord)))
			c += 1
			if c % 4 == 0:
				object_list.append(object_coord_list)
				object_coord_list = []
				
				
		image_name_ext = image_in_path.split('/')[-1]
		image_name = image_name_ext.split('.')[0]
		image_format = image_name_ext.split('.')[1]
				
		plot_boxes_cv2(image_in_path,object_list,savename="outputs/"+image_name+"_out."+image_format)
		
		
if __name__ == "__main__":
	draw_bounding_box()
