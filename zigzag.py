#print(dct.shape)
#print(arr.shape)
%%writefile zigzag.py
def zigzag(input):
  vmax = input.shape[0]
  hmax = input.shape[1] 
  result = [[] for k in range(vmax*hmax)]
  for k in range(block_size):                
    for l in range(block_size):
      sum_val = k + l
      if (sum_val % 2 == 0):
        result[sum_val].insert(0, block_val[k][l])          # adding at beginning

      else:
      # adding at end of the list
        result[sum_val].append(block_val[k][l])
  return result
