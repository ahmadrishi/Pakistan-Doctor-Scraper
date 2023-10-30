from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
import scrapy
from scrapy.selector import Selector
import json


class Marham(Spider):
    name = 'marham'
    allowed_domains = ['marham.pk']
    offset = 0
    cookies = {
            'laravel_session' : 'eyJpdiI6Ii8zQzFHVFBIRStGSVh5SkMrQ2VrZ0E9PSIsInZhbHVlIjoiNG5ZL0x3TkZxSnB1V05jOXZBQ1dtd0I4d0Jxd0xxN3VDNGhFak1oTXpVbE45WENrMGQ2dFUyM1dwalVLbmhEL1BVTm54bnZBb25BRHlESkFYbFpGdHBrdGdnM2piZW5KVFY2NWJva0lEOUtXVERLV1RUbEhUelg4UHVSVzM5R3kiLCJtYWMiOiJlN2U4ODBmZjE4ZmVjNTA2YTM0NTcwNzFmZmU2MGZmOGE4ZDE0MjUyMDc5NTAzMmQ2Nzk2YTUyNzBjYjNlNmMxIiwidGFnIjoiIn0%3D'
        }

    def start_requests(self):
        url = f'https://www.marham.pk/api/listing/load-more-doctors?listingType=1&availableToday=0&mostBooked=0&topReviewed=0&videoConsultation=0&discount=0&nearMe=0&lat=0&lng=0&sortBy=0&language=en&startTime=&endTime=&physicalDiscount=&offset={self.offset}'
        yield scrapy.Request(url=url, callback=self.parse_results, cookies=self.cookies)


    def parse_results(self, response):
        try:
            data = json.loads(response.body)
            if data['status']:
                selector = Selector(text=data['html'])
                links = selector.xpath("//div[contains(@id, 'doctor-counter')]/@data-url").getall()
                print(links)
                for link in links:
                    yield scrapy.Request(link, callback=self.parse_doctor)
                self.offset += 1
                url = f'https://www.marham.pk/api/listing/load-more-doctors?listingType=1&availableToday=0&mostBooked=0&topReviewed=0&videoConsultation=0&discount=0&nearMe=0&lat=0&lng=0&sortBy=0&language=en&startTime=&endTime=&physicalDiscount=&offset={self.offset}'
                yield scrapy.Request(url=url, callback=self.parse_results, cookies=self.cookies)
            else:
                return
        except Exception as e:
            print(e)
            return

    
    def parse_doctor(self, response):
        try:
            name = response.xpath("//p[@id='oc-doctor-name']/text()").get().strip()
        except:
            return
        
        try:
            typee = response.xpath("//p[@id='oc-doctor-name']/following-sibling::p/text()").get().strip()
        except:
            return
        
        try:
            yoe = response.xpath("//p[contains(text(), 'Experience')]/following-sibling::p/text()").get().strip()
        except:
            return
        
        try:
            about = response.xpath("//div[@id='other']/div[@class='row']/div/div/span/p[1]/text()").get().strip()
        except:
            return
        
        try:
            qualification = response.xpath("//div[@id='other']/div[@class='row']/div/div/span/p[2]/text()").get().strip()
        except:
            qualification = ''
        
        try:
            services = response.xpath("//div[@id='other']/div[@class='row']/div/div/span/p[5]/following-sibling::ul[1]/li/text()").get().strip()
        except:
            services = ''

        try:
            disease = response.xpath("//div[@id='other']/div[@class='row']/div/div/span/p[6]/following-sibling::ul[1]/li/text()").get().strip()
        except:
            disease = ''

        try:
            onlineName = response.xpath("//div[@id='booknow']//*[contains(text(), 'Consultation')]/text()").get().strip()
            onlineFees = response.xpath("//div[@id='booknow']//*[contains(text(), 'Consultation')]/../following-sibling::div/p/text()").get().strip()
            onlineDays = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'Consultation')]/../../following-sibling::div/div[@class='col-9']/div[1]/span/text()").extract()).strip()
            onlineTimes = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'Consultation')]/../../following-sibling::div/div[@class='col-9']/div[2]/span/text()").extract()).strip()
            onlineSchedule = onlineDays + "\n" + onlineTimes
        except:
            onlineName = ''
            onlineFees = ''
            onlineSchedule = ''

        try:
            hospitalName = response.xpath("//div[@id='booknow']//*[contains(text(), 'Hospital')]/text()").get().strip()
            hospitalFees = response.xpath("//div[@id='booknow']//*[contains(text(), 'Hospital')]/../following-sibling::div/p/text()").get().strip()
            hospitalDays = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'Hospital')]/../../following-sibling::div/div[@class='col-9']/div[1]/span/text()").extract()).strip()
            hospitalTimes = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'Hospital')]/../../following-sibling::div/div[@class='col-9']/div[2]/span/text()").extract()).strip()
            hospitalSchedule = hospitalDays + '\n' + hospitalTimes
            hospitalAddrs = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'Hospital')]/../../following-sibling::div/div[@class='col-9']/div[3]/span/text()").extract()).strip()

        except:
            hospitalName = ''
            hospitalFees = ''
            hospitalSchedule = ''
            hospitalAddrs = ''

        try:
            hospitalName2 = response.xpath("//div[@id='booknow']//*[contains(text(), 'hospital')]/text()").get().strip()
            hospitalFees2 = response.xpath("//div[@id='booknow']//*[contains(text(), 'hospital')]/../following-sibling::div/p/text()").get().strip()
            hospitalDays2 = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'hospital')]/../../following-sibling::div/div[@class='col-9']/div[1]/span/text()").extract()).strip()
            hospitalTimes2 = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'hospital')]/../../following-sibling::div/div[@class='col-9']/div[2]/span/text()").extract()).strip()
            hospitalSchedule2 = hospitalDays2 + '\n' + hospitalTimes2
            hospitalAddrs2 = " ".join(response.xpath("//div[@id='booknow']//*[contains(text(), 'hospital')]/../../following-sibling::div/div[@class='col-9']/div[3]/span/text()").extract()).strip()
        except:
            hospitalName2 = ''
            hospitalFees2 = ''
            hospitalAddrs2 = ''
            hospitalSchedule2 = ''
        

        yield {
            'Name': name,
            'Type' : typee,
            'Years of Experience': yoe,
            'About': about,
            'Services': services,
            'Qualification': qualification,
            'Disease': disease,
            'Online Consultation': onlineName,
            'Consultation Fees': onlineFees,
            'Consultation Schedule': onlineSchedule,
            'Hospital 1': hospitalName,
            'Address': hospitalAddrs,
            'Fees': hospitalFees,
            'Schedule': hospitalSchedule,
            'Hospital 2': hospitalName2,
            'Address 2': hospitalAddrs2,
            'Fees 2': hospitalFees2,
            'Schedule 2': hospitalSchedule2,
            'Page URL': response.url
        }


            
    
    
    