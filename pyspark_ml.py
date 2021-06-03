from pyspark.ml import Pipeline
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import re
import sys
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

amino_hydropathy_index = {
    "A": 1.8, "C": 2.5, "D": -3.5, "E": -3.5, "F": 2.8, "G": -0.4, "H": -3.2, "I": 4.5, "K": -3.9, "L": 3.8,
    "M": 1.9, "N": -3.5, "P": -1.6, "Q": -3.5, "R": -4.5, "S": -0.8, "T": -0.7, "V": 4.2,"W": -0.9,"Y": -1.3
}

def main():
    sc, spark = create_session('local')
    data, labels, sequences = retrieve_data('train_set.fasta', sc)
    vectors = get_vectors(sequences)
    df = create_dataframe(labels, vectors, spark)
    fit_model(df)

def create_session(context):
    sc = SparkContext(context)
    spark = SparkSession(sc)

    return sc, spark

def retrieve_data(path, sc):
    data = sc.textFile(path)
    labels = data.filter(lambda x: x.startswith(">")).map(lambda x: re.match(r'^>.+?\|.+?\|(?P<label>.+?)\|\d*$',x).group('label')).collect()
    sequences = data.filter(lambda x: not x.startswith(">") and x.startswith('M') and not x.startswith('MMM')).collect()

    return data, labels, sequences

def get_vectors(sequences):
    vectors = []

    for sequence in sequences:
        vector = []
        for amino_acid in sequence:
            vector = vector + [amino_hydropathy_index[amino_acid]]
        vectors.append(Vectors.dense(vector))

    return vectors

def create_dataframe(labels, vectors, spark):
    columns = ["label", "features"]
    length = len(vectors[0])
    rows = [(labels[i], vectors[i]) for i in range(len(labels)) if i < len(vectors) and len(vectors[i]) == length]
    df = spark.createDataFrame(rows, columns)

    return df

def fit_model(df):
    stringIndexer = StringIndexer(inputCol="label", outputCol="indexed")
    si_model = stringIndexer.fit(df)
    td = si_model.transform(df)
    rf = RandomForestClassifier(numTrees=3, maxDepth=2, labelCol="indexed", seed=42, leafCol="leafId")
    rf.getMinWeightFractionPerNode()
    model = rf.fit(td)
    predictions = model.transform(td)
    evaluator = MulticlassClassificationEvaluator(
    labelCol="indexed", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    
    # show results
    predictions.select("rawPrediction", "prediction", "label", "features").show(5)
    print(F"Test Accuracy = {accuracy*100}%")
    print(f"Test Error = {(1.0 - accuracy)*100}%")

# call with 'python pyspark_ml.py main'
if __name__ == '__main__':
    globals()[sys.argv[1]]()
    