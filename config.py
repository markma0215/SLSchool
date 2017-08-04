
sequence = 0
home_page = "http://securities.stanford.edu/filings.html?sort=cld_fic_filing_dt"
base = "http://securities.stanford.edu/"


FIC_PLAINTIFF_COUNTER = 0
FIC_DOCUMENT_COUNTER = 0

REF_PLAINTIFF_COUNTER = 0
REF_DOCUMENT_COUNTER = 0

OTH_DOCUMENT_COUNTER = 0

COA_DOCUMENT_COUNTER = 0

STATE_STC_DOCUMENT_COUNTER = 0

SC_DOCUMENT_COUNTER = 0

start_page = 2

# key is the column name
# value is process conditions: [0: html page only has unique this kind of elemnet or multiple get the first one, 1: has many elemnets and get index one;
#                               "xxxx": tag name
#                               "xxxx": class name
#                               "xxxx": sub tag
#                               "xxxx": regular expression to extract text
#                               true/false: need to remove head and end double quote
#                               ]

summary_name_list = ["sequence", "LITIGATION_NAME", "CASE_STATUS", "SETTLEMENT_DATE", "FILING_DATE", "CASE_SUMMARY"]
summary = {
    "LITIGATION_NAME" : [0, "div", "page-header hidden-tablet hidden-desktop", "h3", "", False],
    "CASE_STATUS": [0, "span", "icon-check", "next_sibling,1", "", True],
    "SETTLEMENT_DATE": [0, "span", "icon-check", "next_sibling,-1", "(\d\d/){2}\d{4}", True],
    "FILING_DATE": [0, "p", "lead", "", "[\w\s]+,\s\d{4}", False],
    "CASE_SUMMARY": [0, "div", "span12", "contents_string", "", False]
}

company_name_list = ["DEFENDANT", "SECTOR", "INDUSTRY", "HEADQUARTERS", "TICKER", "EXCHANGE", "MARKET_STATUS"]
company = {
    "DEFENDANT": [0, "div", "page-header", "h4_contents_1", "", False],
    "SECTOR": [0, "div", "span4", "content_1", "", True],
    "INDUSTRY": [1, "div", "span4", "content_1", "", True],
    "HEADQUARTERS": [2, "div", "span4", "content_1", "", True],
    "TICKER": [3, "div", "span4", "content_1", "", True],
    "EXCHANGE": [4, "div", "span4", "content_1", "", True],
    "MARKET_STATUS": [5, "div", "span4", "content_1", "", True],
}

fic_name_list = ["FIC_PLAINTIFF", "FIC_COURT", "FIC_DOCKET", "FIC_JUDGE", "FIC_DATE_FILED", "FIC_CLASS_PERIOD_START", "FIC_CLASS_PERIOS_END"]
fic = {
    "FIC_PLAINTIFF": [0, "div", "page-header", "h4_substring", "", False],
    "FIC_COURT": [0, "div", "span4", "content_1", "", True],
    "FIC_DOCKET": [1, "div", "span4", "content_1", "", True],
    "FIC_JUDGE": [2, "div", "span4", "content_1", "", True],
    "FIC_DATE_FILED": [3, "div", "span4", "content_1", "", True],
    "FIC_CLASS_PERIOD_START": [4, "div", "span4", "content_1", "", True],
    "FIC_CLASS_PERIOS_END": [5, "div", "span4", "content_1", "", True]
}

ref_name_list = ["REF_PLAINTIFF", "REF_COURT", "REF_DOCKET", "REF_JUDGE", "REF_DATE_FILED", "REF_CLASS_PERIOD_START", "REF_CLASS_PERIOS_END"]
ref = {
    "REF_PLAINTIFF": [0, "div", "page-header", "h4_substring", "", False],
    "REF_COURT": [0, "div", "span4", "content_1", "", True],
    "REF_DOCKET": [1, "div", "span4", "content_1", "", True],
    "REF_JUDGE": [2, "div", "span4", "content_1", "", True],
    "REF_DATE_FILED": [3, "div", "span4", "content_1", "", True],
    "REF_CLASS_PERIOD_START": [4, "div", "span4", "content_1", "", True],
    "REF_CLASS_PERIOS_END": [5, "div", "span4", "content_1", "", True]
}

plaintiff_name_list = {
    "fic": [],
    "ref": []
}

document_list = {
    "fic": [],
    "ref": [],
    "other": [],
    "state": [],
    "appeal": [],
    "supreme": []
}

section_name = {
    "summary": summary,
    "company": company,
    "fic": fic,
    "ref": ref
}
table_names = ["fic", "ref", "other", "state", "appeal", "supreme"]


def init():
    # init column name list
    if FIC_PLAINTIFF_COUNTER != 0 and plaintiff_name_list["fic"] == []:
        temp = []
        for i in range(FIC_PLAINTIFF_COUNTER):
            prefix = "FIC_PLAINTIFF_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_AD")
            temp.append(prefix + "_PHONE")
            plaintiff_name_list.update({"fic", temp})

    if REF_PLAINTIFF_COUNTER != 0 and plaintiff_name_list["ref"] == []:
        temp = []
        for i in range(REF_PLAINTIFF_COUNTER):
            prefix = "REF_PLAINTIFF_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_AD")
            temp.append(prefix + "_PHONE")
            plaintiff_name_list.update({"ref", temp})

    if FIC_DOCUMENT_COUNTER != 0 and document_list["fic"] == []:
        temp = []
        for i in range(FIC_DOCUMENT_COUNTER):
            prefix = "FIC_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"fic", temp})

    if REF_DOCUMENT_COUNTER != 0 and document_list["ref"] == []:
        temp = []
        for i in range(REF_DOCUMENT_COUNTER):
            prefix = "REF_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"ref", temp})

    if OTH_DOCUMENT_COUNTER != 0 and document_list["other"] == []:
        temp = []
        for i in range(OTH_DOCUMENT_COUNTER):
            prefix = "OTHER_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"other", temp})

    if COA_DOCUMENT_COUNTER != 0 and document_list["appeal"] == []:
        temp = []
        for i in range(COA_DOCUMENT_COUNTER):
            prefix = "APPEAL_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"appeal", temp})

    if STATE_STC_DOCUMENT_COUNTER != 0 and document_list["state"] == []:
        temp = []
        for i in range(STATE_STC_DOCUMENT_COUNTER):
            prefix = "STATE_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"state", temp})

    if SC_DOCUMENT_COUNTER != 0 and document_list["supreme"] == []:
        temp = []
        for i in range(SC_DOCUMENT_COUNTER):
            prefix = "STATE_DOCUMENT_" + str(i + 1)
            temp.append(prefix)
            temp.append(prefix + "_DATE")

        document_list.update({"supreme", temp})
