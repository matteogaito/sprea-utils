# -*- coding: utf-8 -*-

import mechanicalsoup
import os
import time
import requests
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

import inspect

import logging
log = logging.getLogger(__name__)

URL = "http://sprea.it"


class Sprea(object):
    def __init__(self, username, password):
        self.URL = "http://sprea.it"
        self.DOWNLOAD_URL = "http://pdf.sprea.it/r/php/downloader.php"
        self.USERNAME = username
        self.PASSWORD = password

    def _login(self):
        # Create a browser object
        browser = mechanicalsoup.Browser()
        # request Page
        login_page = browser.get(URL)
        # grab the login form
        login_form = login_page.soup.find("form")
        log.info("Enter user and password into user and password field")
        # insert user and password
        login_form.find("input", {"id": "user"})["value"] = self.USERNAME
        login_form.find("input", {"id": "password"})["value"] = self.PASSWORD
        response = browser.submit(login_form, login_page.url)
        if response.status_code == 200:
            log.info("return logged browser")
            return(browser)
        else:
            log.error("Login error")

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
        log.info("Starting {}".format(inspect.stack()[1][3]))
        log.info("Login...")
        browser = self._login()
        log.info("Go into {}".format(campaign_url))
        campaign_books = browser.get(self.URL + campaign_url)
        log.info("Ready to return logged browser with a book list of given campain url")
        return(campaign_books)

    def _manageDownloadDir(self, download_dir):
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def getOnePdfUrlofCampaign(self, campaign_url, book_position):
        log.info("Starting {}".format(inspect.stack()[1][3]))
        log.info("Get browser logged page on {}".format(campaign_url))
        browser = self._goIntoCampaign(campaign_url)
        log.info("Get pdf div")
        books_divs = browser.soup.find_all("div", {"class": "col-lg-2 col-md-4 col-xs-6"})
        log.info("Books divs {} by position".format(books_divs[book_position]))
        pdf_url = books_divs[book_position].find('a')['href']
        log.info("Pdf url {}, ready to return".format(pdf_url))
        return(pdf_url)

    def downloadPDFbyURL(self, pdf_url, download_dir="downloads"):
        log.info("Starting downloadPDFbyURL")
        self._manageDownloadDir(download_dir)
        pdf_info = self._getPdfInfo(pdf_url)
        pdf_path = download_dir + '/' + pdf_info['name']

        log.info("Executing post for download")
        prepare_pdf_for_download = requests.post(
            self.DOWNLOAD_URL,
            data = {'id_anagrafica': pdf_info['anagrafica'], 'doc': pdf_info['name']}
        )
        time.sleep(5)
        if prepare_pdf_for_download.text:
            dpdfurl = urlopen(prepare_pdf_for_download.text)
            try:
                with open(pdf_path, 'wb') as pdf:
                    pdf.write(dpdfurl.read())
                    pdf.close()
                    log.info("Pdf downloaded")
                    return(pdf_path)
            except IOError as e:
                log.error("Error {}".format(e))

    def downloadOnePdfOfCampaign(self, campaign_url, book_position, download_dir="downloads"):
        log.info("Starting {}".format(inspect.stack()[1][3]))
        pdf_url = self.getOnePdfUrlofCampaign(self, campaign_url, book_position)
        self.downloadPDFbyURL(self, pdf_url, download_dir)

    def _getPdfInfo(self, pdf_url):
        pdf_info = {}
        pdf_info['name'] = parse_qs((urlparse(pdf_url).query))['doc'][0]
        pdf_info['anagrafica'] = parse_qs((urlparse(pdf_url).query))['a'][0]
        pdf_info['title'] = parse_qs((urlparse(pdf_url).query))['o'][0]
        log.info("Pdf info Name: {}, Title: {}".format(pdf_info['name'], pdf_info['title']))
        return(pdf_info)
