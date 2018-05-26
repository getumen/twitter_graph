import persistqueue
import schema
import settings
import tweepy
import time
import logging
from neomodel import install_labels


class Crawler:

    def __init__(self):
        self.q = persistqueue.UniqueQ(path='q')
        self.rate = 1.0
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
        self.sleep_time = 10.0

    def save_user(self, user: tweepy.User) -> schema.User:
        user_node = schema.User.nodes.get_or_none(screen_name=user.screen_name)

        if user_node is None:
            user_node = schema.User()

        user_node.user_id = user.id
        user_node.name = user.name
        user_node.screen_name = user.screen_name
        user_node.location = user.location
        user_node.description = user.description
        user_node.url = user.url
        user_node.protected = user.protected
        user_node.followers_count = user.followers_count
        user_node.friends_count = user.friends_count
        user_node.listed_count = user.listed_count
        user_node.created_at = user.created_at
        user_node.favourites_count = user.favourites_count
        user_node.utc_offset = user.utc_offset
        user_node.time_zone = user.time_zone
        user_node.geo_enabled = user.geo_enabled
        user_node.verified = user.verified
        user_node.statuses_count = user.statuses_count
        user_node.contributors_enabled = user.contributors_enabled
        user_node.is_translator = user.is_translator
        user_node.is_translation_enabled = user.is_translation_enabled
        user_node.profile_background_color = user.profile_background_color
        user_node.profile_background_image_url = user.profile_use_background_image
        user_node.profile_background_image_url_https = user.profile_background_image_url_https
        user_node.profile_background_tile = user.profile_background_tile
        user_node.profile_image_url = user.profile_image_url
        user_node.profile_image_url_https = user.profile_image_url_https
        user_node.profile_link_color = user.profile_link_color
        user_node.profile_sidebar_border_color = user.profile_sidebar_border_color
        user_node.profile_sidebar_fill_color = user.profile_sidebar_fill_color
        user_node.profile_text_color = user.profile_text_color
        user_node.profile_use_background_image = user.profile_use_background_image
        user_node.has_extended_profile = user.has_extended_profile
        user_node.default_profile = user.default_profile
        user_node.default_profile_image = user.default_profile_image
        user_node.notifications = user.notifications
        user_node.translator_type = user.translator_type

        user_node.save()

        return user_node

    def traverse(self, init_screen_name='letitbe_or_not', from_queue=False):

        install_labels(schema.User)

        if from_queue:
            screen_name = self.q.get()
        else:
            screen_name = init_screen_name

        while True:

            try:
                user = self.api.get_user(screen_name)
                user_node = self.save_user(user)

                for page in tweepy.Cursor(self.api.friends, id=user.id).pages():
                    for friend in page:
                        self.q.put(friend.screen_name)
                        friend_node = self.save_user(friend)
                        friend_node.is_followed_from.connect(user_node)
                    time.sleep(self.sleep_time)

                for page in tweepy.Cursor(self.api.followers, id=user.id).pages():
                    for follower in page:
                        self.q.put(follower.screen_name)
                        follower_node = self.save_user(follower)
                        user_node.is_followed_from.connect(follower_node)
                    time.sleep(self.sleep_time)

                screen_name = self.q.get()

            except tweepy.error.RateLimitError as e:
                logging.warning(e)
                time.sleep(15 * 60)
            except tweepy.error.TweepError as e:
                if e.message[0]['code'] >= 400:
                    logging.error(e)
                    self.sleep_time *= 2
