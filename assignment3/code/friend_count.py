import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    key = record[0]
    mr.emit_intermediate(key,1) # we need only 1st names

def reducer(key,list_of_values):
    total = 0
    for v in list_of_values:
        total += v
    mr.emit([key,total])    # same as in 'wordcount'

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
