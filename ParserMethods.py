
import config

def next_sibling(node, times = 1):

    if times == -1:
        while node.next_sibling:
            node = node.next_sibling
    else:
        for i in range(times):
            node = node.next_sibling

    return node.string

def h3(node):
    return node.h3.string

def contents_string(node):
    text = "\n".join(eachElement.string for eachElement in node.contents if eachElement.string)
    return text

def h4_contents_1(node):
    if "Defendant:" not in node.h4.contents[0].string:
        return ""
    else:
        return node.h4.contents[0].string.replace("Defendant:", "")

def h4_substring(node):

    if "et al." in node.h4.string:
        return (node.h4.string.split("et al.")[0] + "et al.")
    elif "Securities Litigation" in node.h4.string:
        return node.h4.string.replace("Securities Litigation", "")
    elif "Litigation" in node.h4.string:
        return node.h4.string.replace("Litigation", "")
    elif "v." in node.h4.string:
        return node.h4.string.split("v.")[0]
    elif "vs." in node.h4.string:
        return node.h4.string.split("vs.")[0]
    else:
        return ""

def content_1(node):
    if node.contents[1]:
        return node.contents[1].string
    else:
        return ""

def get_plaintiff_name(node, section_name):
    lists = node.find("ol", class_="styled").contents
    lists = [one for one in lists if one != "\n"]

    plaintiff_dict = {}


    for i in range(len(lists)):
        prefix = section_name.upper() + "_PLAINTIFF_" + str(i + 1)
        if lists[i].contents[0].string:
            plaintiff_dict.update({prefix : lists[i].contents[0].string.encode("utf-8").strip("\n").strip()})
        else:
            plaintiff_dict.update({prefix: ""})

        if lists[i].contents[2].string:
            plaintiff_dict.update({(prefix + "_AD") : lists[i].contents[2].string.encode("utf-8").strip("\n").strip()})
        else:
            plaintiff_dict.update({(prefix + "_AD") : ""})

        if lists[i].contents[4].string:
            plaintiff_dict.update({(prefix + "_PHONE") : lists[i].contents[4].string.strip('"').encode("utf-8").strip("\n").strip()})
        else:
            plaintiff_dict.update({(prefix + "_PHONE") : ""})

    if section_name == "fic":
        if config.FIC_PLAINTIFF_COUNTER < len(lists):
            config.FIC_PLAINTIFF_COUNTER = len(lists)
            config.plaintiff_name_list.update({"fic": sorted(plaintiff_dict.keys(), key=lambda tag : (int(tag.split("_")[2]), tag))})

    elif section_name == "ref":
        if config.REF_PLAINTIFF_COUNTER < len(lists):
            config.REF_PLAINTIFF_COUNTER = len(lists)
            config.plaintiff_name_list.update({"ref": sorted(plaintiff_dict.keys(), key=lambda tag : (int(tag.split("_")[2]), tag))})

    else:
        print "section name is %s" % section_name

    return plaintiff_dict

def get_documents_list(node, section_name):
    lists = node.find_all("tr", class_ = "table-link")

    document_dict = {}
    for i in range(len(lists)):
        prefix = section_name.upper() + "_DOCUMENT_" + str(i + 1)

        if lists[i].contents[3].string:
            document_dict.update({prefix : lists[i].contents[3].string.encode("utf-8").strip("\n").strip()})
        else:
            document_dict.update({prefix : ""})

        if lists[i].contents[5].string:
            document_dict.update({prefix + "_DATE" : lists[i].contents[5].string.encode("utf-8").strip("\n").strip()})
        else:
            document_dict.update({prefix + "_DATE" : ""})

    keys = sorted(document_dict.keys(), key=lambda tag : (int(tag.split("_")[2]), tag))
    if section_name == "fic":
        if config.FIC_DOCUMENT_COUNTER < len(lists):
            config.FIC_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"fic" : keys})
    elif section_name == "ref":
        if config.REF_DOCUMENT_COUNTER < len(lists):
            config.REF_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"ref" : keys})
    elif section_name == "other":
        if config.OTH_DOCUMENT_COUNTER < len(lists):
            config.OTH_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"other" : keys})
    elif section_name == "state":
        if config.STATE_STC_DOCUMENT_COUNTER < len(lists):
            config.STATE_STC_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"state" : keys})
    elif section_name == "appeal":
        if config.COA_DOCUMENT_COUNTER < len(lists):
            config.COA_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"appeal" : keys})
    elif section_name == "supreme":
        if config.SC_DOCUMENT_COUNTER < len(lists):
            config.SC_DOCUMENT_COUNTER = len(lists)
            config.document_list.update({"supreme" : keys})
    else:
        print "section name is %s" % section_name

    return document_dict


mapping = {
    "next_sibling": next_sibling,
    "h3": h3,
    "contents_string": contents_string,
    "h4_contents_1": h4_contents_1,
    "content_1": content_1,
    "h4_substring": h4_substring,
    "get_plaintiff_name": get_plaintiff_name,
    "get_documents_list": get_documents_list
}