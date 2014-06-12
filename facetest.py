import os, sys, json

from classes import Person, Metadata, SourceImage
from image import load_images, rotate_images, crop_images, normalize_images, write_images
from predict import create_predictive_model, test_model

def show_usage():
	print 'Please enter the path of the directory containing the source images and metadata'
	print 'This directory should contain a series of directories, each containing source images and metadata for one person'
	print 'Source images should be in JPEG format, and the metadata for each image should have the same file prefix as the source image'
	print 'EX:'
	print '/faceimages/'
	print '   ->/batman/'
	print '        ->batman.jpg'
	print '        ->batman.meta'
	print '        ->batman2.jpg'
	print '        ->batman2.meta'
	print ''
	print 'Please enter the test type as the 2nd argument'
	print 'Supported test types: PCA LDA'
	print 'Usage:'
	print 'python facetest.py ./faceimages/ PCA'

def parse_test_type(arg):
	"""
	Option to allow different test types
	Currently supported: PCA LDA
	"""
	if arg != 'PCA' and arg != 'LDA':
		show_usage()
		raise Exception('ERROR: Could not parse test type "%s"' % arg)
		exit()
	else:
		return arg
	

def load_people(directory_path):
	"""
	Loads images and metadata from a directory into Person, SourceImage, and Metadata objects
	"""
	
	#array of person objects
	training_set = []
	
	#dictionary to hold all filenames
	file_dictionaries = {}

	print 'Compiling file list...'
	
	for eachdirectory, subdirectories, files in os.walk(directory_path):
		for eachfile in files:
			if eachdirectory not in file_dictionaries:
				file_dictionaries[eachdirectory] = []
			file_dictionaries[eachdirectory].append(eachfile)
	
	values_count = 0
	#compile value list
	for key, value in file_dictionaries.iteritems():
		values = file_dictionaries[key]
		values_count += len(values)
			
	print 'Found %s labels and %s files' % (len(file_dictionaries.keys()), values_count)
	
	for key, value in file_dictionaries.iteritems():
		person = Person(label = key)
		files_for_person = file_dictionaries[key]
		#find matching .meta and .jpg
		for eachfile in files_for_person:
			if eachfile[-3:] == 'jpg' or eachfile[-4:] == 'jpeg':
				file_prefix = eachfile.split('.')[0]
				for eachotherfile in files_for_person:
					if file_prefix == eachotherfile.split('.')[0] and eachotherfile.split('.')[1] == 'meta':
						#match found
						metadatafile = os.path.join(key, eachotherfile)
						eyes_data = json.load(open(metadatafile))
						eyes={}
						eyes['left'] = {}
						eyes['right'] = {}
						eyes['left']['x'] = eyes_data['left_eye_x']
						eyes['left']['y'] = eyes_data['left_eye_y']
						eyes['right']['x'] = eyes_data['right_eye_x']
						eyes['right']['y'] = eyes_data['right_eye_y']
						metadata = Metadata(eyes=eyes, person=person)
						source_image = SourceImage(metadata=metadata, path=os.path.join(key, eachfile))
						training_set.append(source_image)
					
	print 'training set compiled... %s entries' % len(training_set)
	return training_set

def run_pca():
	
	training_set = load_people(directory_path)

	load_images(training_set)

	rotate_images(training_set)

	normalize_images(training_set)
	crop_images(training_set)
	write_images(training_set)

	model = create_predictive_model(training_set, model_type='PCA')

	test_model(training_set, model)

def run_lda():
	training_set = load_people(directory_path)

	load_images(training_set)

	rotate_images(training_set)

	normalize_images(training_set)
	crop_images(training_set)
	write_images(training_set)

	model = create_predictive_model(training_set, model_type='LDA')

	test_model(training_set, model)
	
try:
	directory_path = sys.argv[1]
except Exception as e:
	show_usage()
	exit()

test_type = parse_test_type(sys.argv[2])

if test_type == 'PCA':
	run_pca()
elif test_type == 'LDA':
	run_lda()
	


