'''
此为spark代码文件，由于数据量过大。不得不先分切文件文件，再进行逐个跑代码与合并文件的操作。（使用另外的py文件来分割合并文件）
代码中的地址为当时文件的临时地址
'''

import json
from pyspark.sql import SparkSession

#input_path = "output_chessdata.json"
#output_path = "status_count.json"

if __name__=="__main__":
    spark=SparkSession.builder.appName("StatusCount").getOrCreate()
    for i in range(1,2):
        output_data = []
        sets=spark.read.json('data/data19g'+str(i)+'p.json').rdd.map(lambda x:x.asDict())
            
        elements=sets.map(
            lambda elem:(
                str({'init':elem['init'],'color':elem['color'],'move':elem['move']}),
                (elem['result'],elem['count'])
            )).reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))
        elements=elements.sortBy(lambda key_value:key_value[0],ascending=False)
        output=elements.collect()

        for(data,count)in output:
         
            data=eval(data)

            data['result']=count[0]
            data['count']=count[1]
            output_data.append(data)
        #print(len(output_data))

        with open('data/data20g'+str(i)+'p.json', "w") as f:
            json.dump(output_data, f)
    spark.stop()
