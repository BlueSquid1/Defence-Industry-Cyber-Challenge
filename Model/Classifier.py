import tensorflow as tf
import numpy as np
import math

class Classifier:

    csvReader = None

    # input output placeholders
    x = None
    y = None

    # model define as a Tensor
    prediction = None

    outputNum = 0

    def __init__(self, csvReader):
        self.csvReader = csvReader

    def setupModel(self, numInputNodes, numNodesInHiddenLayers, numOutputNodes):
        print("setting up model")
        self.outputNum = numOutputNodes
        self.x = tf.placeholder(tf.float32, shape=[None, numInputNodes])
        self.y = tf.placeholder(tf.float32, shape=[None, numOutputNodes])
        self.prediction = self.defineModel(numInputNodes, numNodesInHiddenLayers, numOutputNodes)
        print("successfully created the model")

    def defineModel(self, inputNum, hiddenNodes, outputNum):
        # model input layer
        W = tf.Variable(tf.random_normal([inputNum, hiddenNodes[0]]))
        b = tf.Variable(tf.random_normal([hiddenNodes[0]]))
        output = tf.nn.relu(tf.add(tf.matmul(self.x, W), b))

        # model hidden layers
        # start at 1 because already done first hidden layer
        for i in range(1, len(hiddenNodes)):
            W = tf.Variable(tf.random_normal([hiddenNodes[i - 1], hiddenNodes[i]]))
            b = tf.Variable(tf.random_normal([hiddenNodes[i]]))
            output = tf.nn.relu(tf.add(tf.matmul(output, W), b))

        # model output layer
        lastIndex = len(hiddenNodes) - 1
        W = tf.Variable(tf.random_normal([hiddenNodes[lastIndex], outputNum]))
        b = tf.Variable(tf.random_normal([outputNum]))
        output = tf.add(tf.matmul(output, W), b)

        return output

    def trainModel(self, numOfEpoches, batchSize):
        # load the datasets from the csv files
        print("Loading dataset")
        trainingX, trainingY = self.csvReader.getTrainingCases()
        testingX, testingY = self.csvReader.getTestingCases()
        print("finished loading dataset")

        with tf.Session() as sess:
            saver = tf.train.Saver()
            print("preparing model for run time")
            # defining a bunch of tensors so extracting values from the model is easier later when running

            # cost tensor
            cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.prediction, labels=self.y))

            # confusion matrix tensor
            CM = tf.confusion_matrix(tf.argmax(self.y, 1), tf.argmax(self.prediction, 1))

            # optimizer tensor
            optimizer = tf.train.AdamOptimizer().minimize(cost)

            # accuracy tensor
            correct = tf.equal(tf.argmax(self.prediction, 1), tf.argmax(self.y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

            # confidence tensor
            confidenceCategories = tf.nn.softmax(self.prediction)
            # pick label with highest confidence
            confidence = tf.reduce_max(confidenceCategories, reduction_indices=[1])

            # inialize global variables
            sess.run(tf.global_variables_initializer())

            print("Starting Training")
            totalNumTrainingCases = len(trainingX)
            numOfTrainingBatches = math.ceil(totalNumTrainingCases / batchSize)

            totalNumTestingCases = len(testingX)
            numOfTestingBatches = math.ceil(totalNumTestingCases / batchSize)

            # for each epoch
            highestTestingEpoch = 0
            highestTestingAcc = 0.0
            for epoch in range(numOfEpoches):
                # train the neural network

                # for each batch
                epoch_loss = 0
                for i in range(numOfTrainingBatches):
                    print("Batch: " + str(i + 1) + " out of: " + str(numOfTrainingBatches))
                    batch_x = trainingX[i * batchSize: (i + 1) * batchSize]
                    batch_y = trainingY[i * batchSize:(i + 1) * batchSize]

                    _, c = sess.run([optimizer, cost], feed_dict={self.x: batch_x, self.y: batch_y})
                    epoch_loss += c

                print("Epoch " + str(epoch + 1) + " completed out of " + str(numOfEpoches) + " loss: " + str(epoch_loss))

                # collect statistics about the current state of the model (e.g. weights, accuracy, etc)
                # this is done in batches to prevent memory usage spikes
                trainAccTotal = 0
                for i in range(numOfTrainingBatches):
                    batch_x = trainingX[i * batchSize: (i + 1) * batchSize]
                    batch_y = trainingY[i * batchSize: (i + 1) * batchSize]
                    [accuracyTrain] = sess.run([accuracy], feed_dict={self.x: batch_x, self.y: batch_y})
                    trainAccTotal += accuracyTrain

                accuracyTrain = trainAccTotal / numOfTrainingBatches
                print('Train Accuracy: %.6f' % round(accuracyTrain, 6))

                # TESTING
                testingAccTotal = 0
                # for each batch
                for i in range(numOfTestingBatches):
                    batch_x = testingX[i * batchSize: (i + 1) * batchSize]
                    batch_y = testingY[i * batchSize: (i + 1) * batchSize]
                    [accuracyTesting] = sess.run([accuracy], feed_dict={self.x: batch_x, self.y: batch_y})
                    testingAccTotal += accuracyTesting

                accuracyTest = testingAccTotal / numOfTestingBatches
                print('Test Accuracy:', accuracyTest)

                if accuracyTest > highestTestingAcc:
                    print("new best model")
                    highestTestingEpoch = epoch
                    highestTestingAcc = accuracyTest
                    saver.save(sess, "results/best_model.ckpt")


        # post verification proccessing
        with tf.Session() as verSess:
            saver.restore(verSess, "results/best_model.ckpt")
            print("proccessing confidence in best verification model")

            # TESTING
            CMTestingSum = np.zeros([self.outputNum, self.outputNum]).tolist()
            for i in range(numOfTestingBatches):
                batch_x = testingX[i * batchSize: (i + 1) * batchSize]
                batch_y = testingY[i * batchSize: (i + 1) * batchSize]
                [CMbatch] = verSess.run([CM],
                                                              feed_dict={self.x: batch_x, self.y: batch_y})
                CMTestingSum += CMbatch

            self.outputModelResults(CMTestingSum)


    def outputModelResults(self, CM):
        with open('results/results.csv', 'w') as csvfile:
            # Confusion Matrix Test
            csvfile.write("Confusion Matrix Test\n")
            for i in range(2):
                for j in range(2):
                    csvfile.write("," + str(CM[i, j]))
                csvfile.write("\n")

            csvfile.write("\n\n")