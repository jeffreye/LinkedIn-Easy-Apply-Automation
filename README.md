# Linkedin-Easy-Apply-Automation

Latest Modified: Oct 6, 2018

This application targets the Easy apply option on LinkedIn. Provided with a city and job title, it searches for the available jobs with the given parameters and automatically applies for jobs that have easy apply option.

This tutorial is for educational puroposes only.

## Installation

* Python 2.7.*

* Selenium Webdriver
```sh
$ pip install selenium
```
* Download latest [Chrome Webdriver](http://chromedriver.chromium.org/downloads)

## Usage

Run the program with parameters
```sh
$ python LinkedInEasyApply.py <path-to-webdriver> <search-link>  <username> <password> <path-to-resume-file> <path-to-output>
```

e.g.
```sh
$ python LinkedInEasyApply.py "./chromedriver" "https://www.linkedin.com/jobs/search/?distance=25&f_E=2&f_F=it%2Ceng&f_JT=F&f_LF=f_AL&keywords=Software%20Engineer&location=United%20States&locationId=us%3A0"  "mylinkedin@gmail.com" "mypassword" "myresume.pdf" "output.csv"
```