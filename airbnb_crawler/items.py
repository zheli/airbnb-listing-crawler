# -*- coding: utf-8 -*-
import scrapy

class AirbnbItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    photos = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    bed_type = scrapy.Field()
    url = scrapy.Field()
    amenities = scrapy.Field()
    host_id = scrapy.Field()
    hosting_id = scrapy.Field()
    person_capacity = scrapy.Field()

    rev_count = scrapy.Field()
    cancel_policy = scrapy.Field()
    rating_communication = scrapy.Field()
    rating_cleanliness = scrapy.Field()
    rating_checkin = scrapy.Field()
    satisfaction_guest = scrapy.Field()
    response_time = scrapy.Field()
    response_rate  = scrapy.Field()
    nightly_price = scrapy.Field()
