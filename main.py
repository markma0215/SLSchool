
import urllib2
import time
import datetime
from bs4 import BeautifulSoup
import config
from CrawlerCompany import CrawlCompany

def getHTMLPage(url):
    success = False
    times = 0
    html_page = ""
    while success is False and times < 5:
        try:
            print "The URL is: %s" % (url)
            response = urllib2.urlopen(url)
            times += 1
            if response.getcode() == 200:  # response code
                success = True
                html_page = response.read()

        except Exception, e:
            print e
            time.sleep(3)  # sleep for 3 seconds
            print "%s Error for URL %s: program sleeps for 3 seconds and try again" % (datetime.datetime.now(), url)

    if html_page == "":
        print "tried 5 times to get list page, failed"
        return ""
    else:
        return html_page

def getEachCompanyLink(url):
    company_list_page = getHTMLPage(url)
    if not company_list_page:
        print "fetch company list page failed, continue to next list page (skip 20 companies)"
        return []

    soup = BeautifulSoup(company_list_page, 'html.parser')
    company_links_tag = soup.find_all("tr", class_ = "table-link")
    company_links = []
    for eachTag in company_links_tag:
        company_links.append(config.base + str(eachTag['onclick']).replace("window.location=", "").strip("'"))

    if company_links == []:
        print "fetch company links failed, continue to next list page (skip 20 companies)"
        return []
    else:
        return company_links

def crawlCompanyInfo(url):
    if not url:
        print "in crawlCompanyInfo function, url is empty, skip"

    html_page = getHTMLPage(url)
    config.sequence += 1
    CrawlCompany.Crawl(html_page)
    time.sleep(3)

def crawller(url):
    company_links = getEachCompanyLink(url)
    if not company_links:
        print "crawl this page company failed, url = " + url
        print "continue to next page"
        return

    for i in range(len(company_links)):
        crawlCompanyInfo(company_links[i])


def main():
    if config.start_page == 2:
        crawller(config.home_page)
        print "writing file...."
        CrawlCompany.write_file()
        print "done"

    for page_num in range(config.start_page, 232):
        one_list_page = config.home_page + "&page=" + str(page_num)
        print "crawling list page %s" % page_num
        crawller(one_list_page)
        print "writing file...."
        CrawlCompany.write_file()
        print "done"


if __name__ == "__main__":
    main()
