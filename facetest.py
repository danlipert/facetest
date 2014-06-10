import os, sys, json

from classes import Person, Metadata, SourceImage
from image import load_images, rotate_images, crop_images, normalize_images

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
	print 'Usage:'
	print 'python facetest.py ./faceimages/'
	
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
	
	print 'Found %s labels and %s files' % (len(file_dictionaries.keys()), len(file_dictionaries.values()))
	
	for key, value in file_dictionaries.iteritems():
		person = Person(label = key)
		files_for_person = file_dictionaries[key]
		#find matching .meta and .jpg
		for eachfile in files_for_person:
			if eachfile[-4:] == 'meta':
				continue
			file_prefix = eachfile.split('.')[0]
			for eachotherfile in files_for_person:
				if file_prefix == eachotherfile.split('.')[0] and eachotherfile.split('.')[1] != 'jpg':
					#match found
					metadatafile = eachotherfile
					eyes_data = json.load(open(eachotherfile))
					eyes={}
					eyes['left'] = {}
					eyes['right'] = {}
					eyes['left']['x'] = eyes_data['left_eye_x']
					eyes['left']['y'] = eyes_data['left_eye_y']
					eyes['right']['x'] = eyes_data['right_eye_x']
					eyes['right']['y'] = eyes_data['right_eye_y']
					metadata = Metadata(eyes=eyes, person=Person)
					source_image = SourceImage(metadata=metadata, path=os.path.join(key, value))
					training_set.append(source_image)
		
	return training_set

try:
	directory_path = sys.argv[1]
except Exception as e:
	show_usage()
	exit()
	
training_set = load_people(directory_path)

#test images quickly
for source_image in training_set:
	print source_image.path
	print source_image.image

load_images(training_set)

#test images quickly
for source_image in training_set:
	print source_image.path
	print source_image.image
	
#rotate_images(people)
#normalize_images(people)
#crop_images(people)

#model = create_predictive_model(people)

#results = test_model(model)

#render_output(results)
