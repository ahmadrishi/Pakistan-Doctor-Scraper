# Pakistan Doctor Scraper

This Python script employs Scrapy to extract data from the following healthcare websites:

- [Healthwire](https://healthwire.pk)
- [InstaCare](https://instacare.pk)
- [Marham](https://www.marham.pk)
- [Shifaam](https://www.shifaam.com)

## Data Points Extracted

The script is designed to scrape the following information from these websites:

1. **Doctor Information**:
    - Doctor ID
    - Doctor Name
    - Years of Experience
    - PMC Verified
    - Doctor Image
    - About Section

2. **Services Provided**:
    - List of services offered

3. **Education and Certification**:
    - Doctor's educational background
    - Certification details

4. **Specialization**:
    - Areas of medical specialization

5. **Languages Spoken**:
    - Languages in which the doctor is proficient

6. **Clinic Details**:
    - Clinic Name
    - Clinic Address
    - Clinic Fees
    - Clinic Schedule
    - Consultation Fees

## Usage

Ensure you have Scrapy installed. You can run the script with the following command:

```shell
scrapy runspider doctor_scraper.py
