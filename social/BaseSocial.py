from core import helpers
from config import constants
import random
import json
import os


class BaseSocial:
    def post(self):
        pass

    def select_posting_images(self, parsing_date):
        images = helpers.get_images_in_specific_date(parsing_date)
        if len(images) == 0:
            return False

        if len(images) > 3:
            random_numbers = self.generate_random_numbers(len(images))
            post_images = []
            for i in random_numbers:
                post_images.append(images[i])
            return post_images
        else:
            return images

    @staticmethod
    def generate_random_numbers(count):
        return random.sample(range(1, count), 3)

    @staticmethod
    def get_random_caption(caption_date):
        captions = json.load(open(os.path.join(constants.ROOT_DIR, 'social/templates.json')))
        caption = captions[random.randint(0, len(captions))];

        return caption.replace('[DATE]', caption_date)
