# -*- coding: utf-8 -*-

#TODO
# rifattorizzare con classi login in __init__

import mechanicalsoup
import os
from urllib.parse import urlparse,parse_qs,urlencode

URL = "http://sprea.it"


class Sprea(object):
    def __init__(self, username, password):
        self.URL = "http://sprea.it"
        self.USERNAME = username
        self.PASSWORD = password

    def _login(self):
        # logger.info('Starting get pdf data')
        # Create a browser object
        browser = mechanicalsoup.Browser()
        # request Page
        login_page = browser.get(URL)
        # grab the login form
        login_form = login_page.soup.find("form")
        # insert user and password
        login_form.find("input", {"id": "user"})["value"] = self.USERNAME
        login_form.find("input", {"id": "password"})["value"] = self.PASSWORD
        response = browser.submit(login_form, login_page.url)
        if response.status_code == 200:
            # return logged browser
            return(browser)
        else:
            print("error")

    def listCampaigns(self):
        # Login to sprea.it
        browser = self._login()
        campaigns_page = browser.get(self.URL + "/digitali/")
        # Go to digital campaigns list page
        campaigns_main = campaigns_page.soup.find(
            "main",
            {"itemprop": "mainContentOfPage"}
        )
        campaigns_list = campaigns_main.find_all(
            "div",
            {"class": "col-lg-2 col-md-4 col-xs-6"}
        )
        # print title and link
        for campaign in campaigns_list:
            elements = campaign.find('a')
            print("{} {}".format(
                elements['href'],
                elements.find('strong').text)
            )

    def _goIntoCampaign(self, campaign_url):
        browser = self._login()
        campaign_books = browser.get(self.URL + campaign_url)
        return(campaign_books)

    def _manageDownloadDir(self, download_dir):
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def downloadOnePdfOfCampaign(
        self, campaign_url, book_position, download_dir="downloads"
    ):
        self._manageDownloadDir(download_dir)
        browser = self._goIntoCampaign(campaign_url)
        books_divs = browser.soup.find_all(
            "div",
            {"class": "col-lg-2 col-md-4 col-xs-6"}
        )
        pdf_url = books_divs[book_position].find('a')['href']
        pdf_name = parse_qs((urlparse(pdf_url).query))['doc'][0]
        anagrafica = parse_qs((urlparse(pdf_url).query))['a'][0]
        pdf_title = parse_qs((urlparse(pdf_url).query))['o'][0]
