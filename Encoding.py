import cv2
import numpy as np
import math
from zigzag import *

# defining the block size

#------------------

block_size = 8
block_counter = 0
quantization_factor = 16  # quantization value for dct

# defining standard JPEG quantization matrix

QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],
                             [12,12,14,19,26,58,60,55],
                             [14,13,16,24,40,57,69,56 ],
                             [14,17,22,29,51,87,80,62],
                             [18,22,37,56,68,109,103,77],
                             [24,35,55,64,81,104,113,92],
                             [49,64,78,87,103,121,120,101],
                             [72,92,95,98,112,100,103,99]])
                             
                             
image = cv2.imread('zebra.jpg')  #reading the image
gray_scale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)     # converting image to it's gray scale image
arr1 = []
arr = np.array(gray_scale)                               # storing in array
col = arr.shape[1]                        # saving column values
row = arr.shape[0]  
h = row
w = col                         # saving row values

# no. of block calculation

#------------------

row = np.float32(row) 
col = np.float32(col) 

nbh = math.ceil(row/block_size)
nbh = np.int32(nbh)

nbw = math.ceil(col/block_size)
nbw = np.int32(nbw)

# Pad the image, because sometime image size is not dividable to block size
# get the size of padded image by multiplying block size by number of blocks in height/width

# height of padded image
H =  block_size * nbh

# width of padded image
W =  block_size * nbw
dct = np.zeros((H,W))
dct[0:h,0:w] = arr[0:h,0:w]


print("Zig zag scanning & dct starting...")

#------------------

for i in range(0, nbh):           # traversing in row
    for j in range(0, nbw):       # traversing in col  

        block_val = dct[i:i+block_size, j:j+block_size]
        #val = np.float32(block_val) / 255.0  # float conversion/scale
        dcts = cv2.dct(block_val)  # the dct 
        #block_val = np.uint8(np.float32(dcts) * 255.0 ) # converting back
        block_val = np.divide(block_val,QUANTIZATION_MAT).astype(int)
        #if i == 0:
        #  print(block_val)
        
        #block_val = np.uint8(np.float32(dcts) * 255.0 ) # converting back
        # zigzag scanning
        exec(open("./zigzag.py").read())
        reordered = zigzag(block_val)
        myarray = np.asarray(reordered, dtype = object)
        reshaped= np.reshape(myarray, (block_size, block_size)) 
        dct[i:i+block_size, j:j+block_size] = reshaped
        #print(len(arr1))
        #print(len(result))
        #print(result)
        
        
        #print(len(arr1))
print("scanning & dct over!")


# RunLength Encoding

#------------------

i = 0
j = 0
skip = 0
stream = []  
bitstream = ""
dct = dct.astype(int)
for i in range(0, dct.shape[0]):
  for j in range(0, dct.shape[1]):
    if dct[i][j] != 0:            
      stream.append((dct[i][j],skip))
      bitstream = bitstream + str(dct[i][j])+ " " +str(skip)+ " "
      skip = 0
    else:
      skip = skip + 1
      #j = j + 1
      #return bitstream

      #i = i + 1
      
      #print(bitstream)
      

# Writing to image.txt

#------------------

print((bitstream))
bitstream = str(dct.shape[0]) + " " + str(dct.shape[1]) + " " + bitstream + ";"
file1 = open("image.txt","w")
file1.write(bitstream)
file1.close()

cv2.waitKey(0)
cv2.destroyAllWindows()

