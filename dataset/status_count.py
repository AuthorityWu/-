import sys
from operator import add
import json
#from jieba import posseg
from pyspark.sql import SparkSession

input_path = "output_chessdata.json"
output_path = "status_count.json"
'''
with open(input_path, "r") as f:
    input_data = json.load(f)
'''
output_data = []



if __name__=="__main__":
   # if len(sys.argv)!=2:
   #     print("Usage: wordcount <file>",file=sys.stderr)
   #     sys.exit(-1)

    spark=SparkSession.builder.appName("StatusCount").getOrCreate()
    set=spark.read.text(input_path).map(lambda r:json.load(r))
    elements=set.flatMap(
        lambda _set:[elem for elem in _set]
    ).map(lambda elem:([elem['init'],elem['move'],elem['color']],[elem['result'],1])).reduceByKey(lambda a,b:[a[0]+b[0],a[1]+b[1]])
    elements=elements.sortBy(lambda key_value:key_value[0][0],ascending=False)
    output=elements.collect()
    for(data,count)in output:
        data['result']=count[0]
        data['count']=count[1]
        output_data.append(data)

    spark.stop()
    with open(output_path, "w") as f:
        json.dump(output_data, f)