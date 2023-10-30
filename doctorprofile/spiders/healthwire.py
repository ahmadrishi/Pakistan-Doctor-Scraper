from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

links = [(lambda x: f"https://healthwire.pk/doctors?page={x}")(x) for x in range(1, 101)]

class HealthWire(CrawlSpider):
    name = 'healthwire'
    start_urls = links
    allowed_domains = ['healthwire.pk']
    le_doctors = LinkExtractor(restrict_xpaths="//div[@class='doctor-treat-detail']/div[@class='detail']/h3/a")
    doctors_rule = Rule(le_doctors, callback='parse_item', follow=True)

    rules = [doctors_rule]

    def parse_item(self, response):
        try:
            name = response.xpath("//div[@class='detail']/h1/text()").get().strip()
        except:
            print("Name")
            return


        try:
            typee = response.xpath("//div[@class='detail']/p/text()").extract_first().strip()
        except:
            print("Type")
            return

        try:
            yoe = response.xpath("//div[@class='detail']/p[@class='experiance-doctor']/text()").get().strip()
        except:
            print("Years of Exp")
            return

        try:
            about = response.xpath("//div[@class='comment more']/p/text()").getall()
            about = "".join(about).strip()
        except:
            print("About")
            return

        try:
            education = "\n".join(response.xpath("//div[@class='address-detail-inner']/ul/li/text()").extract()).strip()
        except:
            education = ''

        try:
            services = "\n".join(response.xpath("//div[@class='services-box']/ul/li/span/text()").extract()).strip()
        except:
            print("Sevices")
            return

        try:
            disease = "\n".join(response.xpath("//div[@class='diseases-box']/ul/li/a/span/text()").extract()).strip()
        except:
            print("Disease")
            return

        try:
            minimumFee = response.xpath("//div[@class='attribute-list']/div[1]/span/text()").get().strip()
        except:
            minimumFee = ''

        try:
            SatisfactionRate = response.xpath("//div[@class='attribute-list']/div[2]/span/text()").get().strip()
        except:
            SatisfactionRate = ''
        
        try:
            hospitalName = "\n".join(response.xpath("//div[@class='locate-detail']/ul/li/a/text()").extract()).strip()
            docSchedule = "\n".join(response.xpath("//div[@class='locate-detail']/ul/li/span/text()").extract()).strip()
        except:
            print("Hospital")
            return
        
        try:
            langs = response.xpath("//div[@class='accordion-item-body-content']/p[contains(text(), 'English') or contains(text(), 'Urdu')]/text()").get().split('in')[1]
            langs = langs.strip()
        except:
            langs = ''
        
        yield{
            'Name': name,
            'Type': typee,
            'Years of Expereience': yoe,
            'About': about,
            'Education': education,
            'Services': services,
            'Diseases': disease,
            'Hospital Name': hospitalName,
            'Doctor Schedule': docSchedule,
            'Minimum Fees': minimumFee,
            'Languages': langs,
            'Page URL' : response.url
        }
        

            

