import scrapy
import urljoin
from qiushibaike.items import QiushibaikeItem


class QiushiSpider(scrapy.Spider):
    name = 'qiushibaike'
    # headers={
    #         'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36',
    #     }
    def start_requests(self):
        self.start_urls=[
            'https://www.qiushibaike.com/text/page/1'
        ]
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response,**kwargs):
        item = QiushibaikeItem()

        content = response.xpath('//*[@id="content"]/div/div[2]/div[contains(@class,"article")]')
        for cont in content:

            item['anthor'] = cont.xpath(".//div[@class='author clearfix']//a[2]//h2//text()").get()
            item["content"] = cont.xpath(".//div[@class='content']//span//text()").getall()
            item['_id'] = cont.attrib['id']
            yield item

        next_url = response.xpath("""//ul[@class="pagination"]/li[last()]/a/@href""")

        if next_url != []:
            next_url=response.urljoin(next_url.extract()[0])
            yield response.follow(next_url,callback=self.parse)

        # page=response.url.split('/')[-2]
        # filename='qiushi-page-%s.html'%page
        # # self.log(os.getcwd())
        # path=f'.\\qiushibaike\\qiushi_html\\{filename}'
        # if not os.path.exists(path):
        #     with open(path,'wb') as f:
        #         f.write(response.body)
        #     self.log('Saved file %s' % filename)
        #
        # content = response.xpath('//*[@id="content"]/div/div[2]/div[contains(@class,"article")]')
        # # author = content.xpath('./div[@class="author clearfix"]//a[2]//h2')

        # for cont in content:
        #     yield {
        #         "author": cont.xpath(".//div[@class='author clearfix']//a[2]//h2//text()").get(),
        #         "content":cont.xpath(".//div[@class='content']//span//text()").getall()
        #     }

