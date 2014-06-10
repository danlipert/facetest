from classes import Person, Metadata, SourceImage
from PIL import Image


def load_images(training_set):
	"""
	In place method loads image property for each source image
	"""
	for source_image in training_set:
		source_image.image = Image.open(source_image.path)
	

def rotate_images(training_set):
	"""
	Rotates and aligns face images from SourceImages and Metadata
	"""

	for source_image in training_set:
		eye_right = [source_image.metadata['right']['x'], source_image.metadata['right']['y']]
		eye_left = [source_image.metadata['left']['x'], source_image.metadata['left']['y']]
		
  		eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  		
  		# calc rotation angle in radians
  		rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  		
  		source_image.image = source_image.image.rotate(rotation)
  		
  		"""
  		# distance between them
  		dist = Distance(eye_left, eye_right)
  		# calculate the reference eye-width
  		reference = dest_sz[0] - 2.0*offset_h
  		# scale factor
  		scale = float(dist)/float(reference)
  		# rotate original around the left eye
  		image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  		# crop the rotated image
  		crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  		crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  		image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  		# resize it
  		image = image.resize(dest_sz, Image.ANTIALIAS)
  		return image
  		"""

def crop_images():
	"""
	Crops rotated and aligned face images
	"""
	
def normalize_images():
	"""
	Normalizes brightness of face images
	"""
	
 
