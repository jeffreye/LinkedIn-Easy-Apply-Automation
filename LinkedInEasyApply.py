import time
import json
import JobData
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import ReportingModule as Report
import datetime as dt
from sys import argv

'''
Reference: https://stackoverflow.com/questions/37088589/selenium-wont-open-a-new-url-in-a-new-tab-python-chrome
https://stackoverflow.com/questions/28431765/open-web-in-new-tab-selenium-python
https://stackoverflow.com/questions/39281806/python-opening-multiple-tabs-using-selenium
'''
print(argv)
webdriver_path = argv[1]
calijobslink = argv[2] #"https://www.linkedin.com/jobs/search/?distance=25&f_E=2&f_F=it%2Ceng&f_JT=F&f_LF=f_AL&keywords=Software%20Engineer&location=United%20States&locationId=us%3A0" 
username = argv[3] # your email here
password = argv[4] # your password here
resumeLocation = argv[5] # your resume location on local machine
output_path = argv[6]

currentPageJobsList = []
allEasyApplyJobsList=[]
failedEasyApplyJobsList=[]
appliedEasyApplyJobsList=[]

def init_driver():
    driver = webdriver.Chrome(executable_path = webdriver_path)
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef

def login(driver, username, password):
    driver.get("https://www.linkedin.com/")
    try:
        user_field = driver.find_element_by_class_name("login-email")
        pw_field = driver.find_element_by_class_name("login-password")
        login_button = driver.find_element_by_id("login-submit")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef

def searchJobs(driver):

    start = 0
    while True:
        driver.get(calijobslink + '&start=%d' % start)
        scheight = .1
        while scheight < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
            scheight += .01
        alljobsonpage = driver.find_element_by_class_name('jobs-search-results__list').find_elements_by_class_name("card-list__item")
        links = []
        for i in alljobsonpage:
            # time.sleep(1)   
            try:

                # easy apply text
                i.find_element_by_class_name("job-card-search__easy-apply-text")

                # click and retrieve more info
                i.click()

                # wait for easy apply button to show up
                time.sleep(0.5)

                title = i.find_element_by_class_name('job-card-search__title').get_attribute('innerText').strip()
                company = i.find_element_by_class_name('job-card-search__company-name').get_attribute('innerText').strip()
                city = i.find_element_by_class_name('job-card-search__location').get_attribute('innerText').strip()
                link = driver.find_element_by_css_selector("a.jobs-details-top-card__job-title-link").get_attribute('href')

                status = driver.find_element_by_class_name('jobs-s-apply')
                if 'Applied' in status.get_attribute('innerHTML'):
                    print('applied')
                    continue
                else:
                    print(link)

                job = JobData.JobData(title,company, link, city)
                links.append(job)
                # time.sleep(1)   
            except Exception as e:
                print(e)
                print("Not Easy Apply")
            print("____________________________")
        loopThroughJobs(driver,links)
        start += 25
        del currentPageJobsList[:]
        
    print("____________________________")


def loopThroughJobs(driver,jobsList):
    for i in jobsList:
        print("____________________________")
        if(applyToJob(driver, i.link)):
            print(i.company)
            print(i.jobTitle)

    allwindows = driver.window_handles
    if(len(allwindows) == 2):
        driver.switch_to_window(allwindows[1])
        driver.close()
        driver.switch_to_window(allwindows[0])

def applyToJob(driver,job):
    driver.execute_script( "window.open('"+job+"', 'CurrJob');")
    company_window = driver.window_handles[1]
    driver.switch_to_window(company_window)
    time.sleep(2)
    # Dont Change This setting
    scheight = 4
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += 4

    driver.execute_script("window.scrollTo(0, 0);")

    # Unlock this section for applying jobs
    try:
        # div = driver.find_element_by_class_name("jobs-details-top-card__actions")
        applyButton = driver.find_element_by_class_name("jobs-s-apply__button")
        applyButton.click()
        time.sleep(5)
    except:
        print("Found None")

    # a new tab opened
    if len(driver.window_handles) == 3:
        driver.switch_to_window(driver.window_handles[2])
        try:
            # auth
            driver.execute_script('$("#ember617-answer").click()')
        except:
            pass

        try:
            # h1b
            driver.execute_script('$("#ember622-answer").click()')
        except:
            pass

        try:
            driver.execute_script('$("#follow-company-question").click()')
        except:
            pass

        time.sleep(1)
        try:
            #submit
            driver.execute_script('$("button.continue-btn").click()')
        except Exception as e:
            print('fail')
            print(e)
            failedEasyApplyJobsList.append(job)
            return False
        else:
            appliedEasyApplyJobsList.append(job)
            print("applied " + job)
            return True
        finally:
            time.sleep(1)
            # close this tab and switch back
            driver.close()
            driver.switch_to_window(company_window)
    else:

        try:
            driver.find_element_by_id('file-browse-input').send_keys(resumeLocation)
            driver.execute_script('$("#follow-company").click()')
            time.sleep(3)
            # submit
            driver.find_element_by_css_selector('button.jobs-apply-form__submit-button').click()
        except Exception as e:
            print('fail')
            print(e)
            failedEasyApplyJobsList.append(job)
            return False
        else:
            print("applied " + job)
            appliedEasyApplyJobsList.append(job)
            return True
        finally:
            time.sleep(1)

    return False


def sendReportToEmail():
    try:
        appliedjobs = "\n".join(str(i) for i in appliedEasyApplyJobsList)
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Applied Jobs',appliedjobs)
        failedjobs = "\n".join(str(i) for i in failedEasyApplyJobsList)
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Need your attention to complete applications',failedjobs)
    except:
        Report.send_email(Report.EmailID,Report.Password,Report.Recipient,'Warning Email',"Failed to Generate Report")

def writeToFile(filename,data,filemode):
    f= open(filename,filemode)
    f.write(data)
    f.close()  

def saveReportAsCSV():
    appliedjobs = "\n".join(str(i) for i in appliedEasyApplyJobsList)
    failedjobs = "\n".join(str(i) for i in failedEasyApplyJobsList)
    filename = output_path
    f1 = '{0}-{1}.{2}'.format('applied',filename,'csv')
    f2 = '{0}-{1}.{2}'.format('failed',filename,'csv')
    writeToFile(f1,appliedjobs,"w+")
    writeToFile(f2,failedjobs,"w+")
    


if __name__ == "__main__":
    driver = init_driver()
    time.sleep(3)
    print ("Logging into Linkedin account ...")
    login(driver, username, password)
    time.sleep(1)
    searchJobs(driver)
    # sendReportToEmail()
    saveReportAsCSV()






