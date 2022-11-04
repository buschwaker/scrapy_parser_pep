import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        rows = response.css(
            'section#numerical-index table.pep-zero-table tr'
        )[1:]
        for row in rows:
            pep_link = row.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = int(response.css('h1.page-title::text').get().split(' ')[1])
        name = response.css('h1.page-title::text').get().strip(' ')
        status = response.css('dt:contains("Status") + dd::text').get()

        data = {
            'name': name,
            'number': number,
            'status': status
        }
        yield PepParseItem(data)
