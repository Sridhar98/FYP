import os
import xml.etree.ElementTree as ET 

read_dir = '/content/gdrive/My Drive/PascalVOC2012/VOCdevkit/VOC2012/Annotations/'
write_dir = '/content/gdrive/My Drive/PascalVOC2012/VOCdevkit/VOC2012/gt/'

for xmlfile in os.listdir(read_dir):
	print(read_dir+xmlfile)
	tree = ET.parse(read_dir+xmlfile)
	root = tree.getroot()
	txtfile = open(write_dir+xmlfile.split('.')[0]+"_gt.txt","w")
	print(root)
	for i,item in enumerate(root):
		if item.tag == 'object':
			for subitem in item:
				if subitem.tag == 'name':
					objname = subitem.text
				if subitem.tag == 'bndbox':
					k = 0
					for coords in subitem:
						txtfile.write(coords.text)
						k += 1
						if k != 4:
							txtfile.write('\t')
						else:
							txtfile.write('\t'+objname)
							txtfile.write('\n')
		if i == len(root)-1:
			txtfile.write('\n')				
	txtfile.close()
