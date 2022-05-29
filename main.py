from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen, Request
import pandas as pd
import lxml
from pandas import DataFrame
import openpyxl
from time import sleep
import gspread
import datetime
from gspread_dataframe import set_with_dataframe

gc = gspread.service_account(filename='indeed-jobs-351617-065b73e533d1.json')
sh = gc.open_by_key('1aN42ySnnX8tnzhTsw_6Wg5KTUA_74xS4lthGL-d8OC8')
worksheet = sh.get_worksheet(0)
main_sheet = []
excel_sheet = []


#Function To Scrape Page
def scrape_page(url, hdr):
    req = Request(url, headers=hdr)
    gfg = BeautifulSoup(urlopen(req).read(), features='lxml')
    jobs = gfg.find_all('div',
                        {'class': 'slider_container css-11g4k3a eu4oa1w0'})
    print(len(jobs))

    for job in jobs:
        jobtitle = job.find('div', {
            'class': 'job_seen_beacon'
        }).find('table', {
            'class': 'jobCard_mainContent big6_visualChanges'
        }).find('div', {
            'class':
            'heading4 color-text-primary singleLineTitle tapItem-gutter'
        }).text.replace('new', '')
        job_url = 'www.indeed.com' + job.find('div', {
            'class': 'job_seen_beacon'
        }).find('table', {
            'class': 'jobCard_mainContent big6_visualChanges'
        }).find('div', {
            'class':
            'heading4 color-text-primary singleLineTitle tapItem-gutter'
        }).find('a', {'class': 'jcs-JobTitle'})['href']

        company = job.find('div', {
            'class': 'job_seen_beacon'
        }).find('table', {
            'class': 'jobCard_mainContent big6_visualChanges'
        }).find('div', {
            'class': 'heading6 company_location tapItem-gutter companyInfo'
        }).find('span', {
            'class': 'companyName'
        }).text
        try:
            company_url = 'https://www.indeed.com' + job.find(
                'div', {
                    'class': 'job_seen_beacon'
                }).find('table', {
                    'class': 'jobCard_mainContent big6_visualChanges'
                }).find('div', {
                    'class':
                    'heading6 company_location tapItem-gutter companyInfo'
                }).find('span', {
                    'class': 'companyName'
                }).find('a')['href']
        except:
            company_url = ''
        try:
            rating = job.find('div', {
                'class': 'job_seen_beacon'
            }).find('table', {
                'class': 'jobCard_mainContent big6_visualChanges'
            }).find('div', {
                'class':
                'heading6 company_location tapItem-gutter companyInfo'
            }).find('span', {
                'class': 'ratingNumber'
            }).text
        except:
            rating = ''
        try:
            company_location = job.find('div', {
                'class': 'job_seen_beacon'
            }).find('table', {
                'class': 'jobCard_mainContent big6_visualChanges'
            }).find('div', {
                'class':
                'heading6 company_location tapItem-gutter companyInfo'
            }).find('div', {
                'class': 'companyLocation'
            }).text
        except:
            company_location = ''
        try:
            Salary = job.find('div', {
                'class': 'job_seen_beacon'
            }).find('table', {
                'class': 'jobCard_mainContent big6_visualChanges'
            }).find(
                'div', {
                    'class':
                    'heading6 tapItem-gutter metadataContainer noJEMChips salaryOnly'
                }).text.strip()
        except:
            Salary = ''
        try:
            short_des = job.find('div', {
                'class': 'job_seen_beacon'
            }).find('table', {
                'class': 'jobCardShelfContainer big6_visualChangesr'
            }).find('div', {
                'class': 'heading6 tapItem-gutter result-footer'
            }).find('div', {
                'class': 'job-snippet'
            }).text.strip().find(
                'ul', {
                    'class':
                    'list-style-type:circle;margin-top: 0px;margin-bottom: 0px;padding-left:20px;'
                }).replace('\n', '')
        except:
            short_des = ''
        posted = job.find('div', {
            'class': 'job_seen_beacon'
        }).find('table', {
            'class': 'jobCardShelfContainer big6_visualChanges'
        }).find('div', {
            'class': 'heading6 tapItem-gutter result-footer'
        }).find('span', {
            'class': 'date'
        }).text
        excel_item = {
            'Job Title': jobtitle,
            'Job URL': job_url,
            'Company': company,
            'Rating': rating,
            'Company Url': company_url,
            'Location': company_location,
            'Salary': Salary,
            'Posted': posted,
        }
        excel_sheet.append(excel_item)
        main_sheet.append(excel_item)


hdr = {'User-Agent': 'Mozilla/5.0'}
#Url Input
input_url = 'https://www.indeed.com/jobs?q=food%20industry&l=Kansas&radius=100&limit=50&start='
#It's the input of page num
pages = 20
#Filename Input
filename = "Kansas Jobs"
#Waiting for 3 sec for the new page, just for the security

for page in range(0, pages):
    url = input_url + str(page * 10)
    print(url)
    scrape_page(url, hdr)
    print(len(main_sheet))

df = DataFrame(main_sheet)
final_df = df.drop_duplicates()

worksheet.append_rows(values=final_df.values.tolist(),
                      value_input_option='USER_ENTERED',
                      insert_data_option='INSERT_ROWS',
                      table_range='A1:H1')
