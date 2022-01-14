import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import requests
from bs4 import BeautifulSoup


def darbs():
    df = pd.read_csv('MSC/jobs.csv')

    job_title = []
    company_name = []
    location = []
    date = []
    job_link = []
    job_link_gb = []

    for m in ['data', 'analyst']:
        url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=105719246&keywords='+m+'&location=Oslo%2C%20Norway&locationId='
        wd = webdriver.Chrome(ChromeDriverManager().install())
        wd.get(url)
        no_of_jobs = int(wd.find_element_by_css_selector('h1>span').get_attribute('innerText'))
        i = 2
        while i <= int(no_of_jobs/25)+1: 
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1
            try:
                wd.find_element_by_xpath('/html/body/main/div/section/button').click()
                time.sleep(5)
            except:
                pass
                time.sleep(5)

        job_lists = wd.find_element_by_class_name('jobs-search__results-list')
        jobs = job_lists.find_elements_by_tag_name('li') # return a list
        #print('list of jobs: ',len(jobs))
    
        for job in jobs:
            job_title0 = job.find_element_by_css_selector('h3').get_attribute('innerText')
            job_title.append(job_title0)

            company_name0 = job.find_element_by_css_selector('h4').get_attribute('innerText')
            company_name.append(company_name0)

            location0 = job.find_element_by_css_selector('[class="job-search-card__location"]').get_attribute('innerText')
            location.append(location0)

            date0 = job.find_element_by_css_selector('div>div>time').get_attribute('datetime')
            date.append(date0)

            job_link0 = job.find_element_by_css_selector('a').get_attribute('href')
            job_link.append(job_link0)
            job_link_gb.append(str('https://')+job_link0[11:re.search('refId=',job_link0).start()-2])

        wd.quit()

    job_data = pd.DataFrame({
    'Date': date,
    'Company': company_name,
    'Title': job_title,
    'Location': location,
    #'Link': job_link,
    'link_full': job_link,
    'Link' : job_link_gb
    })

    print(job_data.shape)
    have = list(df.Link)

    for i in range(0,len(job_data)):
        if job_data.iloc[i]['Link'] not in have and job_data.iloc[i]['Link'] not in list(df.Link):
            atbilde = []
            
            for m in ['Date', 'Company', 'Title', 'Link', 'link_full']:
                atbilde.append(job_data.iloc[i][m])

            r = requests.get(str('https://')+job_data.iloc[i]['link_full'][11:])
            data = r.text
            soup = BeautifulSoup(data, features="lxml")
            atbilde.append([soup])

            if len(soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria")) == 4:
                for link in soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria"):
                    atbilde.append(link.text.strip())  
            else:
                for link in soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria"):
                    atbilde.append(link.text.strip())
                for i in range(4-len(soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria"))):
                    atbilde.append("")
                
            description = []
            for link in soup.find_all(class_="show-more-less-html__markup"):
                for linkk in link.find_all('p'):
                    if len([tag.name for tag in linkk.find_all(['strong','em'])]) ==1:
                        description.append([tag.name for tag in linkk.find_all(['strong','em'])])
                    else:pass
                    description.append(linkk.text.strip())

            for link in soup.find_all(class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5"):

                if len([tag.name for tag in link.find_all(['strong','em'])]) ==1:
                        description.append([tag.name for tag in link.find_all(['strong','em'])])
                else:pass
                description.append(link.text.strip())

            atbilde.append(description)

            if soup.find_all(class_="num-applicants__caption") == []:
                atbilde.append("")
            else:
                for link in soup.find_all(class_="num-applicants__caption"):
                    atbilde.append(link.text.strip())

            df.loc[len(df)] = atbilde
    print('Total Linkedin jobs: ', df.shape)

    df.to_csv('MSC/jobs.csv', index = False)