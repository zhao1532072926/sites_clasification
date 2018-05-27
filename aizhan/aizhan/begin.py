from scrapy import cmdline

cmdline.execute("scrapy crawl aizhan_sites_detailed -s DOWNLOAD_DELAY=1.5".split())