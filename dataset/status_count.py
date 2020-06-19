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

    spark=SparkSession.builder.appName("StatusCount").getOrCreate()
    sets=spark.read.json(input_path).rdd.map(lambda x:x.asDict())
    
    elements=sets.map(
	lambda elem:(
		str({'init':elem['init'],'color':elem['color'],'move':elem['move']}),
                (elem['result'],1)
    )).reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))
    elements=elements.sortBy(lambda key_value:key_value[0],ascending=False)
    output=elements.collect()

    for(data,count)in output:
 
        data=eval(data)

        data['result']=count[0]
        data['count']=count[1]
        output_data.append(data)
 	
    spark.stop()
    with open(output_path, "w") as f:
        json.dump(output_data, f)
