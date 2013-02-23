from PIL import Image, ExifTags 
from random import shuffle
import os

class WeddingPhotoAlbumGenerator:

    def __init__(self):
        self.options = {}
        self.options = self.get_default_options()

    def set_option(self, key, value):
        self.options[key] = value

    def get_option(self, key):
        return self.options.get(key)

    def get_default_options(self):
        defaults = {
            'max_height': 300,
            'max_width': 300,
            'input_directory': 'static/photo-album',
            'output_directory': 'static/photo-album',
            'allowed_file_types': ['jpg', 'jpeg', 'png', 'gif'],
            'exif_orientation_key': self._get_exif_orientation_key()
        }
        return defaults

    def _get_exif_orientation_key(self):
        for key in ExifTags.TAGS.keys(): 
            if ExifTags.TAGS[key]=='Orientation':
                return key

    def create(self):
        images = self._get_images()
        for image in images:
            self._create_thumbnail(image)

    def _get_images(self):
        file_paths = []
        input_directory = self.options['input_directory']
        allowed_file_types = self.options['allowed_file_types']
        for file in os.listdir(input_directory):
            file_path = os.path.join(os.getcwd(), input_directory, file)
            if 'thumbnail' in file:
                continue
            extension = os.path.splitext(file)[1][1:]
            if extension.lower() in allowed_file_types:
                file_paths.append(file_path)
        return file_paths

    def _create_thumbnail(self, input_file):
        max_size = self._get_max_size()
        output_file = self._get_output_thumbnail_filename(input_file)
        try:
            im = Image.open(input_file)
            im = self._fix_image_orientation(im)
            im.thumbnail(max_size, Image.ANTIALIAS)
            im.save(output_file, 'JPEG', quality=100)
        except IOError, e:
            print("Can not create a thumbnail for '{0}'".format(input_file))
            print(e)

    def _fix_image_orientation(self, image_resource):
        ''' See: http://stackoverflow.com/a/6218425/657661 '''
        exif_orientation_key = self.options['exif_orientation_key']
        exif = dict(image_resource._getexif().items())
        if exif and exif_orientation_key:
            if exif[exif_orientation_key] == 3: 
                image_resource = image_resource.rotate(180, expand=True)
            elif exif[exif_orientation_key] == 6: 
                image_resource = image_resource.rotate(270, expand=True)
            elif exif[exif_orientation_key] == 8: 
                image_resource = image_resource.rotate(90, expand=True)
        return image_resource

    def _get_max_size(self):
        max_width = self.options['max_width']
        max_height = self.options['max_height']
        max_size = (max_width, max_height)
        return max_size

    def _get_output_thumbnail_filename(self, input_file):
        path, ext = os.path.splitext(input_file)
        output_filename = path + '.thumbnail' + ext.lower()
        return output_filename

class WeddingPhotoAlbumImages:

    def __init__(self):
        self.directory = self._set_default_directory()

    def _set_default_directory(self):
        album_generator = WeddingPhotoAlbumGenerator()
        directory = album_generator.get_option('output_directory')
        return directory

    def set_dir(self, directory):
        self.directory = directory

    def get_images_shuffled(self, image_path = ""):
        images = self.get_images(image_path)
        shuffle(images)
        return images

    def get_images(self, image_path = ""):
        images = []
        this_dir = os.path.dirname(__file__)
        base_dir = os.path.join(this_dir, '..')
        path = os.path.join(base_dir, self.directory)
        for file in os.listdir(path):
            if '.thumbnail' in file:
                image = self._generate_image_info(file)
                images.append(image)
        return images

    def _generate_image_info(self, thumbnail):
        fullsize = thumbnail.replace('.thumbnail', '')
        dir = '/' + self.directory
        link = os.path.join(dir, fullsize)
        image = os.path.join(dir, thumbnail)
        image_info = (image, link)
        return image_info
