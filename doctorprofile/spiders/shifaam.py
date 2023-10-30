from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup 

class Shifaam(CrawlSpider):
    allowed_domain = ['shifaam.com']
    start_urls = ['https://www.shifaam.com/doctors/pakistan/']

    le_doctors = LinkExtractor(restrict_xpaths="//div[@class = 'doc-name']//a")
    doctors_rule = Rule(le_doctors, callback='parse_item', follow=True)

    le_pagination = LinkExtractor(restrict_xpaths="//ul[@class = 'pagination justify-content-center']/li[last()]/a")
    pagination_rule = Rule(le_pagination, follow=True)

    rules = [doctors_rule, pagination_rule]
    name = 'shifaam'

    def parse_item(self, response):
        id = response.url.split('-')[-1]
        name = response.xpath("//div[@class = 'doc-name']/h4/text()").get()
        xp = response.xpath("//p[@class='xp-level']/text()").get()[12:]
        xp = "".join(xp).strip()
        try:
            pmc = response.xpath("//span[@class='pmc-verified']/span/text()").get()
            if pmc is not None:
                pmc = 'Yes'
            else:
                pmc = 'No'
        except:
            pass

        try:
            img = response.url + response.xpath("//div[@class='doctor-card-large']//div[@class = 'img-cont']/img/@src").get()
        except:
            img = ''

        try:
            typee = response.xpath("//p[@class='doc-desc']/text()").get().strip()
        except:
            typee = ''

        try:
            about = response.xpath("//div[@class='shifaam-card']/div[@class='card-body']/p/text()").get().strip()
        except:
            about = ''

        try:
            services = response.xpath("//div[@class='services-tags']//a/text()").getall()
            services = "\n".join(services)
        except:
            pass

        try:
            education = response.xpath("//div[@class='education']/ul/following-sibling::h6[contains(text(), 'Specializations')]/preceding-sibling::ul//text()").getall()
            education = "\n".join(education)
        except:
            education = ''
        
        try:
            specialization = response.xpath("//div[@class='education']/h6[contains(text(), 'Specializations')]/following-sibling::ul[1]//text()").getall()
            specialization = "\n".join(specialization)
        except:
            specialization = ''
        
        try:
            langs = response.xpath("//div[@class='education']/h6[contains(text(), 'Languages')]/following-sibling::ul[1]//text()").getall()
            langs = "\n".join(langs)
        except:
            langs = ''
        
        try:
            exp = response.xpath("//div[@class='education']/h6[contains(text(), 'Experience')]/following-sibling::ul[1]//text()").getall()
            exp = "\n".join(exp)
        except:
            exp = ''

        #Clinic
        try:
            clinicName = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Clinic')]/text()").get().strip()
            clinicAddress = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Clinic')]/../../following-sibling::div/div/span[@class='pd-18-38']/text()").get().strip()
            clinicCharge = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Clinic')]/../../following-sibling::div/div/span[@class='dark ml-auto']/text()").extract_first().strip()
            clinicSchedule = "\n".join(response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Clinic')]/../../following-sibling::div//div[@class='doc-info available-today doc-details-hide']/div/span//text()").extract()).strip()
        except:
            clinicName = ''
            clinicAddress = ''
            clinicCharge = ''
            clinicSchedule = ''

        #Online Consultation
        try:
            onlineName = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Online')]/text()").get().strip()
            onlineFees = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Online')]/../../following-sibling::div/div/span[@class='dark ml-auto']/text()").extract_first().strip()
            onlineSchedule = "\n".join(response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Online')]/../../following-sibling::div//div[@class='doc-info available-today doc-details-hide']/div/span//text()").extract()).strip()
        except:
            onlineName = ''
            onlineFees = ''
            onlineSchedule = ''

        #Medical Center
        try:
            medicalName = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Medical')]/text()").get().strip()
            medicalAddrs = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Medical')]/../../following-sibling::div/div/span[@class='pd-18-38']/text()").get().strip()
            medicalCharge = response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Medical')]/../../following-sibling::div/div/span[@class='dark ml-auto']/text()").extract_first().strip()
            medicalSchedule = "\n".join(response.xpath("//div[@class='shifaam-card']//h2[contains(text(), 'Medical')]/../../following-sibling::div//div[@class='doc-info available-today doc-details-hide']/div/span//text()").extract()).strip()
        except:
            medicalName = ''
            medicalAddrs = ''
            medicalCharge = ''
            medicalSchedule = ''

        yield{
            'Doctor ID': id,
            'Doctor Name': name,
            'Years of Experience': xp,
            'PMC Verified': pmc,
            'Doctor Image': img,
            'Type' : typee,
            'About' : about,
            'Services': services,
            'Education and Certification' : education,
            'Specialization': specialization,
            'Languages': langs,
            'Experience': exp,
            'Clinic Name': clinicName,
            'Clinic Address': clinicAddress,
            'Clinic Fees': clinicCharge,
            'Clinic Schedule': clinicSchedule,
            'Consultation' : onlineName,
            'Consultation Fees': onlineFees,
            'Consultation Schedule': onlineSchedule,
            'Medical Center': medicalName,
            'Center Address': medicalAddrs,
            'Center Fees': medicalCharge,
            'Center Schedule': medicalSchedule,
            'Page Url': response.url
        }





        

