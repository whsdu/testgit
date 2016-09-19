from pyspark import SparkContext
from pyspark import SparkConf
logFile = "/ukl/wuhao/spark-1.6.1-bin-hadoop2.6/README.md"
conf = SparkConf().setAppName("Simple App")

sc = SparkContext(conf=conf)
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print ("Lines with a : %i, lines with b: %i" % (numAs,numBs))
