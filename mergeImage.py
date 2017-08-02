import os
import shutil
from PIL import Image
import numpy
from enum import Enum

def duplicateFile(filename,fileformat,time):
	file_name = filename
	file_format = fileformat
	old_full_name = file_name + '.' + file_format

	if (os.path.isfile(old_full_name)):
		for x in range(time):
			new_full_name = file_name + '_' + str(x) + '.' + file_format
			shutil.copy(old_full_name,new_full_name)
	print 'duplicate ' + old_full_name + ' ' + str(time) + ' times'
	print 'new file name is like ' + file_name + '_0.' + file_format

def getPNGmatrix(filename):
	file_name = filename
	image = Image.open(file_name)
	fullmatrix = numpy.atleast_2d(image)
	return fullmatrix

def printFullPNGMatrix(filename):
	matrix = getPNGmatrix(filename)
	shape = matrix.shape
	dimensions = len(shape)
	creatVar = globals()
	for x in range(dimensions):
		creatVar['shape_' + str(x)] = shape[x]

	for y in range(shape_0):
		print matrix[y][:]

def getEdgePx(direction,PNGfilename,imageformat = 'png'):
	file_name = PNGfilename + '.' + imageformat
	matrix_full = getPNGmatrix(file_name)
	
	shape = matrix_full.shape
	dimensions = len(shape)
	creatVar = globals()
	for x in range(dimensions):
		creatVar['shape_' + str(direction) + '_' + str(x)] = shape[x]

	matrix_edge = globals()['matrix_' + str(direction)] = [([0] * 50)]

	if direction == 'up':
		#matrix_up = matrix_full[0:1,:]# slice line1 in 1d, all in line1-2d
		matrix_edge = atrix_full[0][:]
	elif direction == 'down':
		matrix_edge = matrix_full[shape_down_0 - 1][:]
	elif direction == 'left':
		matrix_edge = matrix_full[:][0]
	elif direction == 'right':
		matrix_edge = matrix_full[:][shape_right_1 - 1]
	print 'get ' + str(direction) + ' edge done!'
	return matrix_edge

def findSameEdgeByPx(name1 = 'wallEdgeUp',name2 = 'wallEdgeDown'):
	#same_for_each = dict() -> change all the direction_for_matrix1/2
	same_array = []

	filename1 = name1
	filename2 = name2
	matrix1 = [[0] for i in range(4)]
	matrix2 = [[0] for i in range(4)]

	Direction = Enum('up','left','down','right')
	for i,element in enumerate(Direction):
		matrix1[i] = getEdgePx(element,filename1)
		matrix2[i] = getEdgePx(element,filename2)

	for j,element1 in enumerate(Direction):
		for k,element2 in enumerate(Direction):
			if ((j + k) % 2) == 0 and (j != k):
				if matrix1[j] == matrix2[k]:
					same_for_each = dict()
					same_for_each['direction_for_matrix1'] = str(element1)
					same_for_each['direction_for_matrix2'] = str(element2)
					same_array.append(same_for_each)
					print 'the ' + str(element1) + ' of matrix for ' + filename1 + ' and the ' + str(element2) + ' of matrix for '+ filename2 + ' is the same!'
	return same_array

def mergeTwoImage(image1,image2,byedge):
	image1_name = image1 + '.png'
	image2_name = image2 + '.png'

	img1 = Image.open(image1_name)
	sz = img1.size
	matrix1 = numpy.atleast_2d(img1)

	img2 = Image.open(image2_name)
	img2 = img2.resize(sz,Image.ANTIALIAS)
	matrix2 = numpy.atleast_2d(img2)

	if byedge == 'up':
		final_matrix = numpy.append(matrix2,matrix1,axis = 0)
		final_name = 'merged_' + image1 + '_' + image2 + '_vertical_21.png'
	elif byedge == 'down':
		final_matrix = numpy.append(matrix1,matrix2,axis = 0)
		final_name = 'merged_' + image1 + '_' + image2 + '_vertical_12.png'
	elif byedge == 'left':
		final_matrix = numpy.append(matrix2,matrix1,axis = 1)
		final_name = 'merged_' + image1 + '_' + image2 + '_level_21.png'
	elif byedge == 'right':
		final_matrix = numpy.append(matrix1,matrix2,axis = 1)
		final_name = 'merged_' + image1 + '_' + image2 + '_level_12.png'
	else:
		print "Sigh. Wrong parameter."
		return

	final_img = Image.fromarray(final_matrix)
	final_img.save(final_name)
	print 'saved ' + final_name

def findImage1SameEdge(same_edge_array):
	same_firection_for_matrix1 = [0 for x in range(len(same_edge_array))]
	for i in range(len(same_edge_array)):
		same_firection_for_matrix1[i] = same_edge_array[i]['direction_for_matrix1']
	return same_firection_for_matrix1

def mergeByName():
	prefix = input('input prefex:')
	#find all
	files = glob.glob(prefix + '_*')
	num = len(files)

	filename_lens = [len(file) for file in files]
	min_len = min(filename_lens)
	max_len = max(filename_lens)

	#_00,_01
	if min_len == max_len:
		files = sorted(files)
	#_0,_1
	else:
		index = [0 for x in range(num)]#[0,0,0...]
		for i in range(num):
			filename = files[i]
			start = filename.rfind('_')+1
			end = filename.rfind('.')
			file_no = int(filename[start:end])
			index[i] = file_no
		index = sorted(index)
		files = [prefix + '_' + str(x) + '.png' for x in index]

	baseimg = Image.open(files[0])
	sz = baseimg.size
	basematrix = numpy.atleast_2d(baseimg)
	for i in range(1,num):
		file = files[i]
		im = Image.open(file)
		im = im.resize(sz,Image.ANTIALIAS)
		matrix = numpy.atleast_2d(im)
		basematrix = numpy.append(basematrix,matrix,axis = 1)#0 is vertical
	final_img = Image.fromarray(basematrix)
	final_img.save('merged.png')
	
def main():
	samearray = findSameEdgeByPx()
	same_direction_1 = findImage1SameEdge(samearray)
	#TODO: 0 should be set
	mergeTwoImage('wallEdgeUp','wallEdgeDown',same_direction_1[0])

if __name__ == '__main__':
	main()