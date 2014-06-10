from classes import Person, Metadata, SourceImage
from PIL import Image, ImageOps
import math


def load_images(training_set):
	"""
	In place method loads image property for each source image
	"""
	print 'Loading images into memory....'
	for source_image in training_set:
		source_image.image = Image.open(source_image.path)

def write_images(training_set):
	"""
	Writes images to local filesystem - used for testing
	"""
	print 'Writing files to filesystem'
	for i, source_image in enumerate(training_set):
		source_image.image.save('%s-%i-test.jpg' % (source_image.metadata.person.label, i))

def Distance(p1,p2):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	return math.sqrt(dx*dx+dy*dy)
  
def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
	if (scale is None) and (center is None):
		return image.rotate(angle=angle, resample=resample)
	nx,ny = x,y = center
	sx=sy=1.0
	if new_center:
		(nx,ny) = new_center
	if scale:
		(sx,sy) = (scale, scale)
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e
	return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def rotate_images(training_set):
	"""
	Rotates and aligns face images from SourceImages and Metadata
	"""

	for source_image in training_set:
		eye_right = [source_image.metadata.eyes['right']['x'], source_image.metadata.eyes['right']['y']]
		eye_left = [source_image.metadata.eyes['left']['x'], source_image.metadata.eyes['left']['y']]
		
  		eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  		
  		# calc rotation angle in radians
  		rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))

  		source_image.image = ScaleRotateTranslate(source_image.image, center=eye_left, angle=rotation)
  		
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

def crop_images(training_set, offset_pct=(0.2, 0.2), dest_sz=(70,70)):
	"""
	Crops rotated and aligned face images
	offset_pct -- the amount of proportional space above and do the sides of the eyes
	dest_sz -- the final image size after cropping
	"""
	for source_image in training_set:
		# calculate offsets in original image
		offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
		offset_v = math.floor(float(offset_pct[1])*dest_sz[1])

		eye_right = [source_image.metadata.eyes['right']['x'], source_image.metadata.eyes['right']['y']]
		eye_left = [source_image.metadata.eyes['left']['x'], source_image.metadata.eyes['left']['y']]
 		# distance between them
		dist = Distance(eye_left, eye_right)
		
		# calculate the reference eye-width
		reference = dest_sz[0] - 2.0*offset_h
		
		# scale factor
		scale = float(dist)/float(reference)
		crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  		crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
		image = source_image.image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
		# resize it
 		image = image.resize(dest_sz, Image.ANTIALIAS)
 		source_image.image = image

def normalize_images(training_set):
	"""
	Normalizes brightness of face images
	"""
	
	for source_image in training_set:
		source_image.image = ImageOps.grayscale(source_image.image)
		source_image.image = ImageOps.autocontrast(source_image.image)
		#source_image.image = ImageOps.equalize(source_image.image)
	
 
