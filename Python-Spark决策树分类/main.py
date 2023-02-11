import findspark

findspark.init()
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vector, Vectors
from pyspark.ml.classification import DecisionTreeClassificationModel
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import Row
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()


def f(x):
    rel = {}
    rel['features'] = Vectors.dense(float(x[0]), float(x[2]), float(x[4]), float(x[8]), float(x[9]), float(x[10]),
                                    float(x[11]), float(x[12]), )
    rel['label'] = str(x[14])
    return rel


data = spark.sparkContext.textFile('adult3.txt').map(lambda line: line.split(',')).map(lambda p: Row(**f(p)))
traindata = spark.createDataFrame(data)
testData = spark.sparkContext.textFile('adult1.txt').map(lambda line: line.split(',')).map(lambda p: Row(**f(p)))
Testdata = spark.createDataFrame(testData)

labelIndexer = StringIndexer().setInputCol('label').setOutputCol('indexedLabel').fit(traindata)
featureIndexer = VectorIndexer().setInputCol('features').setOutputCol('indexedFeatures').setMaxCategories(14).fit(
    traindata)
labelConverter = IndexToString().setInputCol('prediction').setOutputCol('predictedLabel').setLabels(labelIndexer.labels)

dtClassifier = DecisionTreeClassifier().setLabelCol('indexedLabel').setFeaturesCol('indexedFeatures')

dtPipeline = Pipeline().setStages([labelIndexer, featureIndexer, dtClassifier, labelConverter])
dtPipelineModel = dtPipeline.fit(traindata)
dtPredictions = dtPipelineModel.transform(Testdata)
dtPredictions.select('predictedLabel', 'label', 'features').show(50)
evaluator = MulticlassClassificationEvaluator().setLabelCol('indexedLabel').setPredictionCol('prediction')
dtAccuracy = evaluator.evaluate(dtPredictions)
print(dtAccuracy)  # 打印准确率
