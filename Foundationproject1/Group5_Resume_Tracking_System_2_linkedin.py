# Group5_Resume_Tracking_System

# Anand Pratap Singh (12020084)
# Francis David Vuppuluri (12020028)
# Lavanya SN (12020075)
# Puneet Srivastava (12020026)
# Sangeeta Thakur (12020088)


import pandas as pd
import openpyxl
import pickle
from linkedin_scraper import Person, actions
from selenium import webdriver
import utils.config
import requests
from bs4 import BeautifulSoup
import candidates
import time
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# get the names of all students of AMPBA 2021w batch

df = pd.read_excel('FP1 Mid Review Schedule-24th April.xlsx',
                   engine='openpyxl', skiprows=1)

df.columns

df = df[['Member-1 (Name & PGID)', 'Member-2(Name & PGID)',
         'Member-3 (Name & PGID)', 'Member-4 (Name & PGID)',
         'Member-5 (Name & PGID)']]

df.fillna(",", inplace=True)

nameOnly = df.applymap(lambda x: np.nan if type(x) == float else x.split(',')[
                       0].strip().lower().replace('\t', ' '))


names = nameOnly.values.tolist()

names = [j for sub in names for j in sub if j != '']


driver = webdriver.Chrome('/Users/puneet/Downloads/chromedriver-3')

# login to Linkedin account
actions.login(driver, utils.config.username, utils.config.password)

nameList = names

# search the names in the name list, and fetch the first profile that appears in the Linkedin search option
# save the profile links in a list which would be used to extract data from those profiles

profileUrlList = []
for name in nameList:

    searchUrl = 'https://www.linkedin.com/search/results/all/?keywords=' + \
        name.replace(" ", "%20") + '&origin=GLOBAL_SEARCH_HEADER'

    driver.get(searchUrl)

    profileSoup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        profileUrl = profileSoup.find_all(
            "a", attrs={"class": "app-aware-link"})[1]['href']
    except:
        continue

    print(profileUrl)

    profileUrlList.append(profileUrl)

driver.quit()


# traverse through each of the link and etract the following information

candidateDf = pd.DataFrame(
    columns=['Name', 'Location', 'Job Titles', 'About', 'Educations', 'Top Skills', 'Years of Experience'])

driver = webdriver.Chrome('/Users/puneet/Downloads/chromedriver-3')

# login to Linkedin account
actions.login(driver, utils.config.username, utils.config.password)

candidateList = profileUrlList

# remove a non profile URL
candidateList.remove('https://www.linkedin.com/company/esdsdc/')


index = 0
for candidate in candidateList:
    # print(candidate)
    driver.get(candidate)  # get the page source code for a given candidate

    for i in range(3):

        driver.execute_script(
            'window.scrollBy(0, document.body.scrollHeight/3);')  # scroll the page by 1/3rd the length so that all the skills load
        time.sleep(4)

    candidateSoup = BeautifulSoup(driver.page_source, 'html.parser')

    # get the following information, all of them are self explanatory
    skills = candidateSoup.find_all(
        "span", attrs={"class": "pv-skill-category-entity__name-text t-16 t-black t-bold"})

    name = candidateSoup.find("h1", attrs={
        "class": "text-heading-xlarge inline t-24 v-align-middle break-words"}).text

    currentLocation = candidateSoup.find("span", attrs={
        "class": "text-body-small inline t-black--light break-words"}).text

    jobTitle = candidateSoup.find(
        "div", attrs={"class": "text-body-medium break-words"}).text

    educations = candidateSoup.find_all(
        "h3", attrs={"class": "pv-entity__school-name t-16 t-black t-bold"})

    totalExp = candidateSoup.find_all(
        "span", attrs={"class": "pv-entity__bullet-item-v2"})

    try:
        about = candidateSoup.find(
            "div", attrs={"style": "line-height:1.9rem;max-height:5.699999999999999rem;"}).text
    except:
        about = ''

    skill_set = []
    for skill in skills:
        skill_set.append(skill.text.replace('\n', '').strip())

    educationList = []
    for education in educations:
        educationList.append(education.text.replace('\n', '').strip())

    totalExpList = []
    for exp in totalExp:
        if exp.text.replace('\n', '').strip() != 'No Expiration Date':
            totalExpList.append(exp.text.replace('\n', '').strip())

    # Append the fetched values to a dataframe
    candidateDf.at[index, 'Educations'] = educationList
    candidateDf.at[index, 'About'] = about
    candidateDf.at[index, 'Years of Experience'] = totalExpList
    candidateDf.at[index, 'Name'] = name
    candidateDf.at[index, 'Location'] = currentLocation
    candidateDf.at[index, 'Job Titles'] = jobTitle.strip()
    candidateDf.at[index, 'Top Skills'] = skill_set

    index += 1

driver.quit()

candidateDf.to_csv('CandidatesFromLinkedIn.csv', index=False)
