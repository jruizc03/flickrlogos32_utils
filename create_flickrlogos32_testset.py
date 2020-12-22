# -*- coding: utf-8 -*-
"""
Script that converts all the multiple annotation files of the flickrlogos32 dataset
to a single .txt file with the format: "imgfilename classname subset x1 y1 x2 y2" that
is the format that the method DeepLogo uses.

@author: Julio César Ruiz Calle
"""

import glob

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_coord(x:int, y:int, width:int, height:int):
    x1 = x
    y1 = y
    x2 = x+width
    y2 = y+height
    
    if(x1<1):
        x1 = 1
    if(y1<1):
        y1 = 1
    if(x2<1):
        x2 = 1
    if(y2<1):
        y2 = 1
    return round(x1),round(y1),round(x2),round(y2)

imagefilenames = []
imageclassnames = []
imagex1 = []
imagey1 = []
imagex2 = []
imagey2 = []
testset_images = []
testset_annots = []
with open('testset-logosonly.relpaths.txt', 'r') as infile:
    for line in infile:
        clean_line = line.replace('\n', '')
        testset_images.append('/home/julio/wdir/datasets/flickrlogos32/FlickrLogos-v2/'+clean_line)

#Store the location of the image files
for imagefile in testset_images:
    temp = imagefile.replace('jpg', 'masks', 1)
    temp = temp + '.bboxes.txt'
    testset_annots.append(temp)

print('Testset number of annotations = ' + str(len(testset_annots)))
#Retrieve the x1 y1 x2 y2 for each of the annotation files
for i in range(len(testset_annots)):
    with open(testset_annots[i], 'r') as infile:
        for line in infile:
            if hasNumbers(line):
                numbers = line.split(' ')
                x1, y1, x2, y2 = get_coord(int(numbers[0]), int(numbers[1]), int(numbers[2]), int(numbers[3]))
                imagex1.append(str(x1))
                imagey1.append(str(y1))
                imagex2.append(str(x2))
                imagey2.append(str(y2))
                subdirectories = testset_annots[i].split('/')
                imageclassnames.append(subdirectories[-2].capitalize())
                imagefilename = subdirectories[-1].rstrip('.bboxes.txt')
                imagefilenames.append(imagefilename)

#Write the lines in the text file
for i in range(len(imagefilenames)):
    with open('flickr_logos_32_dataset_test_set_annotation.txt', 'a') as infile:
        infile.write(imagefilenames[i]+' '+imageclassnames[i]+' '+'1'+' '+imagex1[i]+' '+imagey1[i]+' '+imagex2[i]+' '+imagey2[i]+'\n')
