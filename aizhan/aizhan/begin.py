from scrapy import cmdline

cmdline.execute("scrapy crawl aizhanSitesInfo -s DOWNLOAD_TIMEOUT=15".split())