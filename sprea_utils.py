# -*- coding: utf-8 -*-

import mechanicalsoup
from urllib.parse import urlparse,parse_qs,urlencode

URL = "http://sprea.it"

def loginIntoSprea(user,password):
    #logger.info('Starting get pdf data')
    # Create a browser object
    browser = mechanicalsoup.Browser()
    # request Page
    login_page = browser.get(URL)
    # grab the login form
    login_form = login_page.soup.find("form")
    # insert user and password
    login_form.find("input", {"id": "user"})["value"] = user
    login_form.find("input", {"id": "password"})["value"] = password
    response = browser.submit(login_form, login_page.url)
    if response.status_code == 200:
        #return logged browser
        return(browser)
    else:
        print("error")

def listCampaigns(user,password):
    #Login to sprea.it
    browser = loginIntoSprea(user,password)
    campaigns_page = browser.get(URL + "/digitali/")
    #Go to digital campaigns list page
    campaigns_main = campaigns_page.soup.find("main", {"itemprop": "mainContentOfPage" })
    campaigns_list = campaigns_main.find_all("div", {"class": "col-lg-2 col-md-4 col-xs-6" })
    # print title and link
    for campaign in campaigns_list:
        elements = campaign.find('a')
        print(elements['href'])
        print(elements.find('strong').text)

def CampaignBookView(user,password,campaign_url):
    #Login to sprea.it
    browser = loginIntoSprea(user,password)
    campaign_books_view = browser.get( URL + campaign_url )
    return(campaign_books_view)

def downloadPDFofCampaign(campaign_books_view,book_position):
    books_divs = campaign_books_view.soup.find_all("div", {"class": "col-lg-2 col-md-4 col-xs-6" })
    pdf_url = books_divs[book_position].find('a')['href']
    pdf_name = parse_qs((urlparse(pdf_url).query))['doc'][0]
    anagrafica = parse_qs((urlparse(pdf_url).query))['a'][0]
    pdf_title = parse_qs((urlparse(pdf_url).query))['o'][0]
    print(pdf_name)
    print(anagrafica)
    print(pdf_title)
