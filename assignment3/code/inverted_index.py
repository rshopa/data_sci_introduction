import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line 

def mapper(record):
    doc_id = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        mr.emit_intermediate(w,doc_id)  # emit each word

def reducer(key,list_of_values):
    doc_ids = []
    for l in list_of_values:            # create a list
        if l not in doc_ids:            # of documents
                doc_ids.append(l)
    mr.emit([key,doc_ids])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer) 
