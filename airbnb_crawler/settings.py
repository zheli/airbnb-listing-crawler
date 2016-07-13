# -*- coding: utf-8 -*-

BOT_NAME = 'airbnb_crawler'
SPIDER_MODULES = ['airbnb_crawler.spiders']
NEWSPIDER_MODULE = 'airbnb_crawler.spiders'
USER_AGENT = 'airbnb_crawler (http://meixiaozhu.com)'
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 16
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_DEBUG = False
