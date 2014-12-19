__author__ = 'j'
import scrapy
import re

class ProxySpider(scrapy.Spider):
    name = "proxycrawl"
    start_urls = ["http://www.proxynova.com/proxy-server-list/elite-proxies/"]
    allowed_domains = ["proxynova.com"]
    length = 36
    fileLocation = "proxy-dump.txt"
    def parse(self, response):
        f = open(self.fileLocation,'w')
        for x in range(self.length):
            if x == 13:     #13 is empty -> ignore
                pass
            else:
                ipxpath = '//*[@id="tbl_proxy_list"]/tbody[1]/tr[%s]/td[1]/span/text()' % x
                hrefPortxpath  = '//*[@id="tbl_proxy_list"]/tbody[1]/tr[%s]/td[2]/a/text()' % x
                nonHrefPortxpath = '//*[@id="tbl_proxy_list"]/tbody[1]/tr[%s]/td[2]/text()' % x

                ip = response.xpath(ipxpath).extract()
                nonHrefPort = response.xpath(nonHrefPortxpath).extract()
                hrefPort = response.xpath(hrefPortxpath).extract()

                ip = self.getIp(str(ip))
                port = self.getPort(nonHrefPort, hrefPort)
                if(ip != None):
                    proxy = str(ip+":"+port)
                    f.write(proxy + "\n")
        f.close()



    def getIp(self, ip):
        pattern = r"(((\d?)+\.)+(\d?)+)"
        m = re.search(pattern, ip)
        if(m):
            return m.groups()[0]
    def getPort(self, nonHrefPort, hrefPort):
        pattern = r"(\d+)"
        m = re.search(pattern, str(nonHrefPort + hrefPort))
        if(m):
            return m.groups()[0]

