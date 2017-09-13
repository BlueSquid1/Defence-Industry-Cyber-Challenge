# this script is used to create and train the deep neural network


from Model.Classifier import Classifier
from Model.CSVReader import CSVReader

numInputNodes = 21
numNodesInHiddenLayers = [100, 100]
numOutputNodes = 2

numOfEpoches = 100

# Ran this script on a computer with only 4Gb of RAM so I will only train with 10,000 entries at a time.
# If you have more memory then consider increasing this number
batchSize = 10000

pathToTestCsvFile = "testing.csv"
pathToTrainCsvFile = "training.csv"

csvReader = CSVReader(pathToTrainCsvFile, pathToTestCsvFile)

model = Classifier( csvReader)

model.setupModel(
    numInputNodes,
    numNodesInHiddenLayers,
    numOutputNodes
    )

model.trainModel(numOfEpoches, batchSize)
