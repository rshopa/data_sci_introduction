import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    table_name = [record[0]]
    order_id = record[1]
    value = record[2:]
    int_val = table_name + value            # emit hash with table name
    mr.emit_intermediate(order_id,int_val)  # and its value

def reducer(key,list_of_values):

            # create two separate lists - for orders and items

    order = [s for s in list_of_values if s[0] == 'order']
    line_item = [s for s in list_of_values if s[0] == 'line_item']

            # now join them by merging elements of lists

    for x in order:
        for y in line_item:
            mr.emit(str([x[0]]+[key]+x[1:]+[y[0]]+[key]+y[1:]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
