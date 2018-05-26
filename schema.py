import settings

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      Relationship, BooleanProperty, DateTimeProperty)

config.DATABASE_URL = settings.NEO4J_URL


class User(StructuredNode):
    user_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty()
    screen_name = StringProperty(unique_index=True, required=True)
    location = StringProperty()
    description = StringProperty()
    url = StringProperty()
    protected = BooleanProperty
    followers_count = IntegerProperty(required=True)
    friends_count = IntegerProperty(required=True)
    listed_count = IntegerProperty(required=True)
    created_at = DateTimeProperty()
    favourites_count = IntegerProperty()
    utc_offset = IntegerProperty()
    time_zone = StringProperty()
    geo_enabled = BooleanProperty()
    verified = BooleanProperty()
    statuses_count = IntegerProperty()
    contributors_enabled = BooleanProperty()
    is_translator = BooleanProperty()
    is_translation_enabled = BooleanProperty()
    profile_background_color = StringProperty()
    profile_background_image_url = StringProperty()
    profile_background_image_url_https = StringProperty()
    profile_background_tile = StringProperty()
    profile_image_url = StringProperty()
    profile_image_url_https = StringProperty()
    profile_link_color = StringProperty()
    profile_sidebar_border_color = StringProperty()
    profile_sidebar_fill_color = StringProperty()
    profile_text_color = StringProperty()
    profile_use_background_image = BooleanProperty()
    has_extended_profile = BooleanProperty()
    default_profile = BooleanProperty()
    default_profile_image = BooleanProperty()
    notifications = BooleanProperty()
    translator_type = StringProperty()

    is_followed_from = Relationship('User', 'FOLLOW')


config.AUTO_INSTALL_LABELS = True
