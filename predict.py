from facerec.feature import Fisherfaces, SpatialHistogram, Identity, PCA, LDA
from facerec.distance import EuclideanDistance, ChiSquareDistance
from facerec.classifier import NearestNeighbor
from facerec.model import PredictableModel
from facerec.validation import KFoldCrossValidation, SimpleValidation
from facerec.util import minmax_normalize
from facerec.serialization import save_model, load_model
from facerec.lbp import LPQ, ExtendedLBP
import numpy as np
import random

def load_images_and_labels(training_set):
	"""
	returns an array of images and labels
	"""
	X = []
	y = []
	for source_image in training_set:
		X.append(np.array(source_image.image))
		y.append(source_image.metadata.person.label)	
	return (X, y)
	

def create_predictive_model(training_set):
	"""
	Create a predictive model for facial recognition
	training_set -- the images and data that will be used to create the model
	
	Returns a predictive model object
	"""
	feature = PCA()
	classifier = NearestNeighbor(dist_metric=EuclideanDistance(), k=1)
	# Define the model as the combination
	model = PredictableModel(feature=feature, classifier=classifier)
	X, y = load_images_and_labels(training_set)	
	
	print 'begin model computation'
	model.compute(X, y)
	print 'model computation complete'
	return model

def test_model(training_set, model):
	"""
	Test performance of a model against a training set
	Randomly Selects 10% of training set as the test set
	training_set -- the images and data used to create the model
	model -- the predictive model based on the training_set
	"""
	X, y = load_images_and_labels(training_set)	
	cross_validator = SimpleValidation(model)
	train_indices = range(0, len(y))
	random.seed(1)
	test_indices = random.sample(train_indices, int(len(train_indices)/10))
	train_indices = [index for index in train_indices if index not in test_indices]
	#print 'train indices: %s' % train_indices
	#print 'test indices: %s' % test_indices
	cross_validator.validate(X, y, train_indices, test_indices)
	cross_validator.print_results()
