from .BaseSocial import BaseSocial
from facepy import GraphAPI
from config import constants


class Facebook(BaseSocial):
    graph = None

    def __init__(self):
        self.graph = GraphAPI(constants.FACEBOOK_ACCESS_TOKEN)
        # self.graph = GraphAPI().for_application(constants.FACEBOOK_APP_ID, constants.FACEBOOK_APP_SECRET)

    def post(self, parsing_date):
        posting_images = self.select_posting_images(parsing_date)

        if posting_images:
            images_ids = [self.graph.post(
                path='/me/photos',
                source=open(i, 'rb'),
                retry=0,
                published=False
            ) for i in posting_images]

            attachments = {}
            for image in images_ids:
                attachments[
                    "attached_media[" + str(images_ids.index(image)) + "]"] = "{'media_fbid': '" + image['id'] + "'}"

            self.graph.post(
                path='/me/feed',
                retry=2,
                message=self.get_random_caption(parsing_date),
                published=True,
                **attachments
            )
