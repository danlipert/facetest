import os, sys, json
import warnings

from classes import Person, Metadata, SourceImage, TrainingError
from image import load_images, rotate_images, crop_images, normalize_images, write_images
from predict import create_predictive_model, test_model

DEFAULT_MODEL = 'PCA'
DEFAULT_THRESHOLD = 200

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
	if arg != 'PCA' and arg != 'LDA' and arg != 'LBH':
		show_usage()
		raise ValueError('Could not parse test type "%s"' % arg)
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
			if eachfile[-3:] == 'jpg' or eachfile[-4:] == 'jpeg' or eachfile[-3:] == 'JPG':
				file_prefix = eachfile.split('.')[0]
				person.image_count += 1
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
		if person.image_count == 0:
			warnings.warn("A person has been excluded from this analysis due to lack of source images in the person's directory.")

	print 'training set compiled... %s entries' % len(training_set)
	return training_set


def run_analysis(directory_path, model_type='PCA'):

	training_set = load_people(directory_path)

	if len(training_set) < 1:
		raise TrainingError("No source images were found in the specified directory.")

	load_images(training_set)

	rotate_images(training_set)

	normalize_images(training_set)
	crop_images(training_set)
	write_images(training_set)

	min_image_count = min([x.metadata.person.image_count for x in training_set])

	if model_type == 'LDA' and min_image_count < 2:
		warnings.warn("LDA requires at least two images per person. Defaulting to {0}.".format(DEFAULT_MODEL))
		model_type = DEFAULT_MODEL

	model = create_predictive_model(training_set, model_type=model_type)

	test_model(training_set, model, threshold=DEFAULT_THRESHOLD)


if __name__ == '__main__':

	try:
		directory_path = sys.argv[1]
	except Exception as e:
		show_usage()
		exit()

	test_type = parse_test_type(sys.argv[2])

	run_analysis(directory_path, model_type=test_type)
