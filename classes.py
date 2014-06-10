class Metadata:
	"""
	An object representing the occurance of one face in a Source Image
	
	eyes -- dictionary representing the location of the person's eyes in the image (default None)
		eyes['left' or 'right']['x' or 'y']
		ex: 
		> eyes['left']['x']
		100
	person -- Person object identifying who the metadata represents (default None)
	
	"""
	
	def __init__(self, eyes=None, person=None):
		self.eyes = eyes
		self.person = person

class SourceImage:
	"""
	One source image containing a photo of one or more faces
	
	path -- local file path of image (default None)
	metadatas -- a metadata object representing feature information about a face within the image (default None)
	image -- PIL image (default None)
	"""
	
	def __init__(self, path=None, metadata=None, image=None):
		self.path = path
		self.metadata = metadata

class Person:
	"""
	One human individual represented by a collection of source images and a label
	
	label -- string representing the person's name (default None)
	"""
	
	def __init__(self, label=None):
		self.label = label

