# -*- coding: utf-8 -*-
import json
import logging
import scrapy
from urlparse import urlparse
from airbnb_crawler.items import AirbnbItem


KEY = "ck_066207cacfd44f8762ca24dc5c6cb8a03dc73dfe"
SECRET = "cs_e3feecd8e87581c74bce441ff0f6700327a973cd"
# QUERY = 'Los-Angeles--CA--United-States'
# QUERY = 'Stockholm--Sweden'
# QUERY = 'Lucca--Italy'
# QUERY = 'Los-Angeles--CA--United-States?description_languages%5B%5D=128&s_tag=X6agZTS_'
QUERY = ('Rowland-Heights--CA--United-States?room_types%5B%5D=Entire+home%2Fapt&'
         'description_languages%5B%5D=128&ss_id=kj7h5rfa&s_tag=zhUnUAPv')
fetched_listings = []


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com"]
    start_urls = (
        'https://www.airbnb.com/s/'+QUERY,
    )

    def parse(self, response):
        last_page_number = self.last_pagenumer_in_search(response)
        if last_page_number:
            for pageNumber in range(1, last_page_number + 1):
                page_url = response.url + "&page=%d" % pageNumber
                yield scrapy.Request(page_url, callback=self.parse_listing_results_page)

    def parse_listing_results_page(self, response):
        for href in response.xpath('//a[@class="media-photo media-cover"]/@href').extract():
            url = response.urljoin(href)
            path = urlparse(url).path
            if path not in fetched_listings:
                fetched_listings.append(path)
                logging.debug('Requesting new item (url=%s)' % href)
                yield scrapy.Request(url, callback=self.parse_listing_contents)

    def parse_listing_contents(self, response):
        item = AirbnbItem()

        detail = _get_meta_json_by_id(response, '_bootstrap-listing')
        options = _get_meta_json_by_id(response, '_bootstrap-room_options')
        item['latitude'] = _get_meta_by_property(response, 'airbedandbreakfast:location:latitude')
        item['longitude'] = _get_meta_by_property(response, 'airbedandbreakfast:location:longitude')

        if detail:
            listing = detail['listing']
            item['name'] = listing['name']
            item['description'] = listing['description']
            item['address'] = detail['full_address']
            item['photos'] = _get_photos(listing)

        if options:
            item['host_id'] = options['hostId']
            item['nightly_price'] = options['nightly_price']

            event_data = options['airEventData']
            item['rev_count'] = event_data['visible_review_count']
            item['amenities'] = event_data['amenities']
            item['hosting_id'] = event_data['hosting_id']
            item['room_type'] = event_data['room_type']
            item['price'] = event_data['price']
            item['bed_type'] = event_data['bed_type']
            item['person_capacity'] = event_data['person_capacity']
            item['cancel_policy'] = event_data['cancel_policy']
            item['rating_communication'] = event_data['communication_rating']
            item['rating_cleanliness'] = event_data['cleanliness_rating']
            item['rating_checkin'] = event_data['checkin_rating']
            item['satisfaction_guest'] = event_data['guest_satisfaction_overall']
            item['response_time'] = event_data['response_time_shown']
            item['response_rate'] = event_data['reponse_rate_shown']

        item['url'] = response.url
        yield item

    def last_pagenumer_in_search(self, response):
        try:  # to get the last page number
            last_page_number = int(response
                                   .xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
                                   .extract()[0]
                                   .split('page=')[1]
                                   )
            logging.debug('Found last_page_numer %d' % last_page_number)
            return last_page_number

        except IndexError:  # if there is no page number
            # get the reason from the page
            reason = response.xpath('//p[@class="text-lead"]/text()').extract()
            # and if it contains the key words set last page equal to 0
            if reason and ('find any results that matched your criteria' in reason[0]):
                logging.log(logging.DEBUG, 'No results on page' + response.url)
                return None
            else:
                # otherwise we can conclude that the page
                # has results but that there is only one page.
                return 1


def _get_photos(listing):
    return [{'caption': photo['caption'], 'url': photo['xx_large']} for photo in listing['photos']]


def _get_meta_json_by_id(response, id):
    json_array = response.xpath('//meta[@id="%s"]/@content' % id).extract()
    if json_array:
        return json.loads(json_array[0])


def _get_meta_by_property(response, property):
    return response.xpath('//meta[@property="%s"]/@content' % property).extract()[0]
