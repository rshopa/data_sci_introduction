import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line 

dim_A = [5,5]   # assuming that we know dimensions
dim_B = [5,5]

def mapper(record):

    matrix = record[0]      # assign each element of input string
    i = record[1]           # to the corresponding variable
    j = record[2]
    value = record[3]

    if matrix == 'a':
        for k in range(0,dim_B[1]):
            mr.emit_intermediate((i,k),[matrix,j,value])

    else:
        for k in range(0,dim_A[0]):
            mr.emit_intermediate((k,j),[matrix,i,value])
                        #----------------------^--------
                        # only one index is needed


def reducer(key,list_of_values):

    Sum = 0         # total sum of multiplications
    A = {}          # empty dict of elements
    B = {} 

    for elem in list_of_values:
        if elem[0] == 'a':
            A[elem[1]] = elem[2]    # two separate dictionaries
        else:                       # of elements from each matrix
            B[elem[1]] = elem[2]

    for a in A.keys():
        for b in B.keys():
            if a == b:
                Sum += A[a]*B[b]    # multiply by indices

    if Sum != 0:
        mr.emit([key[0],key[1],Sum])    # only non-zero ones
    

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
