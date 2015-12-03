import MapReduce
import sys

# =============================
# Do not modify above this line

mr = MapReduce.MapReduce()


def mapper(record):
    nucleos = record[1][:-10]       # drop last 10 chars
    mr.emit_intermediate(nucleos,1)

def reducer(key,list_of_values):
    mr.emit(key)                    # this one's simplest
    
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
