# author: Adrian Rosebrock
# website: http://www.pyimagesearch.com

# USAGE
# python search_external.py --dataset images --index index.cpickle --query queries/rivendell-query.png

# import the necessary packages
from pyimagesearch.rgbhistogram import RGBHistogram
from pyimagesearch.searcher import Searcher
import numpy as np
import argparse
import os
import pickle
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where we stored our index")

master_results = {}

for place in ['alley', 'garage', 'grundle', 'rocks', 'rslofts', 'southwick', 'stairs', 'tower', 'tunnel', 'turf']:
	args = vars(ap.parse_args())
	
	# load the query image and show it
	queryImage = cv2.imread("queries/" + place + "-001.png")
	cv2.imshow("Query", queryImage)
	print("query: {}".format("queries/" + place + "-001.png"))
	
	# describe the query in the same way that we did in
	# index.py -- a 3D RGB histogram with 8 bins per
	# channel
	desc = RGBHistogram([8, 8, 8])
	queryFeatures = desc.describe(queryImage)
	
	# load the index perform the search
	index = pickle.loads(open(args["index"], "rb").read())
	searcher = Searcher(index)
	results = searcher.search(queryFeatures)

	totalScore = 0
	numRight = 0
	numConsidered = 10

	for j in range(0, 10):
		# grab the result (we are using row-major order) and
		# load the result image
		(score, imageName) = results[j]
		path = os.path.join(args["dataset"], imageName)
		result = cv2.imread(path)

		correct = place in imageName

		mult = 1 if correct else -1
		numRight += 1 if correct else 0

		print("\t{}. {} : {:.3f}".format(j + 1, imageName, 1 / score * mult))

		totalScore += 1/score*mult
		
	master_results[place] = {
		"score": totalScore,
		"correct_num": numRight
	}


print (master_results)
