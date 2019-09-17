import pymongo
import json
from pymongo import MongoClient
import time
import datetime
from datetime import timedelta
from datetime import datetime
from pprint import pprint
from dateutil import parser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	client = MongoClient("mongodb+srv://extra_user:dobies12345@seniorproject-u3ows.mongodb.net/test?retryWrites=true")
	db = client["DonaldTrumpRyan"]
	retweets = db["1069324231333289991"]

	# TODO - Retrieve the entire database (without duplicates) 
	firstTweet = retweets[0]

	cursor = retweets.find()
	print(retweets.count())
	tweetIDS = []
	tweets = []
	for document in cursor:
		tweetID = document["id"]
		if tweetID not in tweetIDS:
			tweetIDS.append(tweetID)
			tweets.append(document)

	timeData = []
	for i in tweets:

		timeStr = i["created_at"]
		datetime_object = parser.parse(timeStr)
		timeData.append(datetime_object)

	timeData.sort()
	print(len(timeData))
	print(timeData[len(timeData)-1] - timeData[0])

	#Grabbing differences
	time1 = timeData[0]
	timeDifferences = []
	for i in timeData:
		date1 = i - time1
		timeDifferences.append(date1)

	split = 100

	timeData.pop(0)

	lengthOfTimeData = len(timeData)


	counter = (int)(lengthOfTimeData/split)

	finalTimeDifferences = []
	valFrom = 0;
	valTo = 0;
	for i in range(0,counter):
		valFrom = i*split
		valTo = valFrom + split
		timeDifference = timeDifferences[valTo] - timeDifferences[valFrom]
		finalTimeDifferences.append(timeDifference)
		print(timeDifference)

	finalSeconds =[]
	for i in finalTimeDifferences:
		finalSeconds.append(i.total_seconds())

	finalSeconds = np.array(finalSeconds)

	# firstHalf = 0
	# for i in range(0,70):
	# 	firstHalf = finalSeconds[i] + firstHalf

	# secondHalf = 0
	# for i in range(70,95):
	# 	secondHalf = finalSeconds[i] + secondHalf

	# print(firstHalf)
	# print(secondHalf)

	plt.plot(finalSeconds)


	plt.show()

	# print(len(tweetIDS))
	# print(len(tweets))
	# print(len(timeData))

	# for document in tweets:
	# 	print(document["id"])
		
		# pprint(document)
