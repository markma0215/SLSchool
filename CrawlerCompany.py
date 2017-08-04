from bs4 import BeautifulSoup
import config
import sys
import re
import copy
from ParserMethods import mapping
import csv
import os.path
import time
import traceback


class CrawlCompany():
    data = {}
    one_page_data = []

    @classmethod
    def Crawl(cls, html_page):
        if not html_page:
            print "html page is empty, skip this company"
            return
        cls.data = {"sequence": config.sequence}
        cls.crawl(html_page)
        cls.one_page_data.append(copy.deepcopy(cls.data))



    @classmethod
    def crawl(cls, html_page):

        soup = BeautifulSoup(html_page, "lxml")
        sections = soup.find_all("section")
        for each in sections:
            if each["id"] == "fic" or each["id"] == "summary" or each["id"] == "company" or each["id"] == "ref":
                cls.crawlSection(each)

            if each["id"] == "fic" or each["id"] == "ref":

                cls.data.update(mapping["get_plaintiff_name"](each, each["id"]))

            if each["id"] in config.table_names:
                table = each.find("table", class_ = "table table-bordered table-striped table-hover")
                if not table:
                    print "no table in this section: %s" % each["id"]
                    sys.exit(1)

                cls.data.update(mapping["get_documents_list"](table, each["id"]))


    @classmethod
    def crawlSection(cls, section):

        case_info = copy.deepcopy(config.section_name[section["id"]])

        for each in case_info:
            try:
                config_info = case_info[each]
                if config_info[0] == 0:
                    node = section.find(config_info[1], class_=config_info[2])
                else:
                    node = section.find_all(config_info[1], class_=config_info[2])[config_info[0]]

                if config_info[3]:
                    if "," in config_info[3]:
                        method_name = config_info[3].split(",")[0]
                        times = int(config_info[3].split(",")[1])
                        text = mapping[method_name](node, times)
                    else:
                        text = mapping[config_info[3]](node)
                else:
                    text = node.string

                if config_info[4]:
                    text = re.search(config_info[4], text).group(0)

                if config_info[5]:
                    text = text.strip('"')

                text = text.strip()

                if not text:
                    print each + " : the text is empty"
                    if each == "REF_PLAINTIFF" or each == "FIC_PLAINTIFF":
                        sys.exit(1)
                    else:
                        time.sleep(10)

                case_info.update({each: text.encode("utf-8")})


            except:
                sys.exc_type, sys.exc_value, sys.exc_traceback = sys.exc_info()
                traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)

                time.sleep(1)
                print each + " raised a problem"
                print "Exit the program, please check this page html format"
                print "FIC_PLAINTIFF_COUNTER is %s" % config.FIC_PLAINTIFF_COUNTER
                print "FIC_DOCUMENT_COUNTER is %s" % config.FIC_DOCUMENT_COUNTER
                print "REF_PLAINTIFF_COUNTER is %s" % config.REF_PLAINTIFF_COUNTER
                print "REF_DOCUMENT_COUNTER is %s" % config.REF_DOCUMENT_COUNTER
                print "OTH_DOCUMENT_COUNTER is %s" % config.OTH_DOCUMENT_COUNTER
                print "COA_DOCUMENT_COUNTER is %s" % config.COA_DOCUMENT_COUNTER
                print "STATE_STC_DOCUMENT_COUNTER us %s" % config.STATE_STC_DOCUMENT_COUNTER
                print "SC_DOCUMENT_COUNTER is %s" % config.SC_DOCUMENT_COUNTER
                sys.exit(1)

        cls.data.update(case_info)

    @classmethod
    def write_file(cls):

        existed_data = []
        if os.path.isfile("crawling_data.csv"):
            with open("crawling_data.csv", "rb") as csvfile:
                reader = csv.DictReader(csvfile)
                existed_data = [row for row in reader]

        column_names = [] + config.summary_name_list + config.company_name_list + \
            config.fic_name_list + config.plaintiff_name_list["fic"] + config.document_list["fic"] + \
            config.ref_name_list + config.plaintiff_name_list["ref"] + config.document_list["ref"] + \
            config.document_list["other"] + config.document_list["state"] + config.document_list["appeal"] + \
            config.document_list["supreme"]


        existed_data += cls.one_page_data
        with open("crawling_data.csv", "wb") as csvfile:
            writer = csv.DictWriter(csvfile, restval="", fieldnames=column_names)
            writer.writeheader()
            writer.writerows(existed_data)

        cls.data.clear()
        cls.one_page_data = []


