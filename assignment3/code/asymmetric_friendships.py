import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line 

def mapper(record):
    person = record[0]
    friend = record[1]
    mr.emit_intermediate((person,friend),1) # emit both people
    mr.emit_intermediate((friend,person),1)

def reducer(key,list_of_values):
    total = 0
    for v in list_of_values:
        total += v
    if total == 1:                  # emit only these who
        mr.emit([key[0],key[1]])    # appears only once

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
