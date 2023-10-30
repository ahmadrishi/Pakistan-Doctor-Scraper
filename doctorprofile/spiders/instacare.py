from scrapy.spiders import Spider
import scrapy
import requests
import json
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



class Instacare(Spider):
    name = 'instacare'
    allowed_domains = ['instacare.pk']
    start_urls = ['https://instacare.pk/doctors/gynecologist']
    hasmore = True
    offset = 1

    def parse(self, response):
        rvc = response.xpath("//input[@name =  '__RequestVerificationToken']/@value").get()
        #print(rvc)
        cookies = response.headers.getlist('Set-Cookie')
        cookies_dict = {}
        for cookie in cookies:
            key_value = cookie.decode('ascii').split(';')[0]
            key, value = key_value.split('=')
            cookies_dict[key] = value
            
        while self.hasmore:
            res = scrapy.FormRequest('https://instacare.pk/LatestDoctor/GetDoctorList', formdata={
                'NextFetch': str(100),
                'Offset': str(self.offset),
                'Telemedicince': 'false',
                'Today': 'false',
                '__RequestVerificationToken': rvc
            }, cookies=cookies_dict, callback=self.parse_results)
            try:         
                yield res
                self.offset += 1
                if self.hasmore > 1:
                    self.hasmore = False
                    break
            except Exception as e:
                self.hasmore = False
                print(e)
                break

    def parse_results(self, response):
        try:
            data = json.loads(response.body)
            if 'totalCount' in data:
                print("True")
            selector = Selector(text=data['html'])
            links = selector.xpath("//div[@class='doctor-card']//a[@class='btn btn-default btn-block']/@href").getall()
            for link in links:
                yield scrapy.Request("https://instacare.pk" + link, callback=self.parse_doctor)
            self.hasmore = True
        except Exception as e:
            print(e)
            self.hasmore = False
    
    def parse_doctor(self, response):
        print(response.url)
        name_special = response.xpath("//span[@id='name']/text()").extract_first().split('-')
        name = name_special[0].strip()
        typee = name_special[1].strip()

        try:
            pmc = response.xpath("//span[contains(text(), 'PMC Verified')]/text()").get()
            if pmc is None:
                pmc = 'No'
            else:
                pmc = 'Yes'
        except:
            pass
        
        yoe = response.xpath("//*[@id='doctor-profile-summarycard']/div[3]/div/div[3]/b/text()").get().strip()


        services = list(dict.fromkeys(response.xpath("//div[@id='services']//label//text()").getall()))
        services = "\n".join(services).strip()

        try:
            exp = list(dict.fromkeys(response.xpath("//b[contains(text(), 'Experience:')][1]/../following-sibling::ul[1]/li/text()").getall()))
            exp = "\n".join(exp)
        except:
            exp = ''
        
        try:
            education = list(dict.fromkeys(response.xpath("//b[contains(text(), 'Qualification:')][1]/../following-sibling::ul[1]/li/text()").getall()))
            education = "\n".join(education).strip()
        except:
            education = ''
        
        try:
            about = list(dict.fromkeys(response.xpath("//div[@id='about']/div[@id='ss']/div/*[last()]//text()").extract()))
            about = " ".join(about).strip()
        except:
            about = ''
            
        

        #Clinic
        try:
            clinicName = response.xpath("//div[@class='book-appointment-widget']/div[@class='row']/div/h3/text()").extract_first().strip()
            clinicCharge = response.xpath("//div[@class='book-appointment-widget']/div[@class='row mb-1 border-bottom']/div[@class='mt-1 ']/strong/text()").extract_first().strip()
            clinicAddrs = response.xpath("//div[@class='book-appointment-widget']/div[@class='row mb-1 border-bottom']/div[@class=' mt-1 mb-1']/a/text()").extract_first().strip()
            clinicSchedule = "\n".join(response.xpath("//ul[@class='timeslots']/li/span/text()").extract()).strip()
        except:
            clinicName = ''
            clinicAddrs = ''
            clinicCharge = ''
            clinicSchedule = ''



        #Online
        try:
            onlineName = response.xpath("//div[@class='box_general_3']/div[@class='mb-2 border-bottom']/h2[contains(text(), 'Online')]/text()").extract_first().strip()
            onlineCharge = response.xpath("//div[@class='mb-2 border-bottom']/h2[contains(text(), 'Online')]/../following-sibling::div[@class='book-appointment-widget']/div[@class='row']/div[@class='mt-1']/strong/text()").extract_first().strip()
            onlineDays = list(dict.fromkeys(response.xpath("//div[@class='mb-2 border-bottom']/h2[contains(text(), 'Online')]/../following-sibling::div[@class='book-appointment-widget']/div[@class='row']/div[@class='mt-2 w-100']/div[@class='mt-1 w-100']/ul[@class='timeslots']/li/span/text()").extract()))
            #onlineDays = "\n".join(onlineDays).strip()
            onlineTime = list(dict.fromkeys(response.xpath("//div[@class='mb-2 border-bottom']/h2[contains(text(), 'Online')]/../following-sibling::div[@class='book-appointment-widget']/div[@class='row']/div[@class='mt-2 w-100']/div[@class='mt-1 w-100']/ul[@class='timeslots']/li/ul/li/text()").extract()))
            onlineSchedule = []
            for i in range(len(onlineTime)):
                onlineSchedule[i] = onlineDays[i] + onlineTime[i]
            onlineSchedule = "\n".join(onlineSchedule).strip()
        except:
            onlineName = ''
            onlineCharge = ''
            onlineSchedule = ''


        yield{
            'Doctor Name': name,
            'Years of Experience': yoe,
            'PMC Verified': pmc,
            'Type' : typee,
            'About' : about,
            'Services': services,
            'Education and Certification' : education,
            'Experience': exp,
            'Clinic Name': clinicName,
            'Clinic Address': clinicAddrs,
            'Clinic Fees': clinicCharge,
            'Clinic Schedule': clinicSchedule,
            'Consultation' : onlineName,
            'Consultation Fees': onlineCharge,
            'Consultation Schedule': onlineSchedule,
            'Page Url': response.url
        }



def run():
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(Instacare)
    process.start()

if __name__ == '__main__':
    run()
