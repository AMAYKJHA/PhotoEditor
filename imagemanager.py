import cv2 as cv
import numpy as np
from PIL import Image, ImageEnhance

class ImageManager():
    def __init__(self):
        self.original_image = None
        self.edited_image = None
        self.display_image = None
        
    def load_image(self, path):
        self.original_image = cv.imread(path)
        self.edited_image = self.original_image.copy()
        
    def get_image(self, value=1):
        if self.edited_image is None:
            return None
        img = self.edited_image if value == 1 else self.original_image.copy()
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)        
        return Image.fromarray(rgb_img)

    def reset_edits(self):
        if self.original_image is not None:
            self.edited_image = self.original_image.copy()

    def set_brightness(self, value):
        # value: -100 to 100, 0 is original
        pil_img = self.get_image()
        enhancer = ImageEnhance.Brightness(pil_img)
        factor = 1 + (value / 100.0)
        bright_img = enhancer.enhance(factor)
        self.edited_image = cv.cvtColor(np.array(bright_img), cv.COLOR_RGB2BGR)

    def set_contrast(self, value):
        pil_img = self.get_image()
        enhancer = ImageEnhance.Contrast(pil_img)
        factor = 1 + (value / 100.0)
        contrast_img = enhancer.enhance(factor)
        self.edited_image = cv.cvtColor(np.array(contrast_img), cv.COLOR_RGB2BGR)

    def set_sharpness(self, value):
        pil_img = self.get_image()
        enhancer = ImageEnhance.Sharpness(pil_img)
        factor = 1 + (value / 100.0)
        sharp_img = enhancer.enhance(factor)
        self.edited_image = cv.cvtColor(np.array(sharp_img), cv.COLOR_RGB2BGR)

    def set_saturation(self, value):
        pil_img = self.get_image()
        enhancer = ImageEnhance.Color(pil_img)
        factor = 1 + (value / 100.0)
        sat_img = enhancer.enhance(factor)
        self.edited_image = cv.cvtColor(np.array(sat_img), cv.COLOR_RGB2BGR)

