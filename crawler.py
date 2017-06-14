import re
import requests

from xml.etree import ElementTree as et


def main(link):
    """
    :param link: link to webpage
    :return: xml as string
    """
    if link.endswith('/'):
        link = link[:-1]
    subpages = [[link]]
    while subpages[-1]:
        print("subpahes %s", subpages)
        subpages.append(get_subpages(subpages[-1], link))

    header = """<?xml version="1.0" encoding="UTF-8"?>"""
    tree = et.Element('urlset', {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})

    for links_list in subpages:
        for link_found in links_list:
            url_element = et.SubElement(tree, 'url')
            loc_element = et.SubElement(url_element, 'loc')
            loc_element.text = link_found

    full_map = header + et.tostring(tree).decode('utf-8')
    return str(full_map)


def get_html(link):

    try:
        html = requests.get(link).content
    except:
        html = ''
    return html

def get_subpages(links, url):
    """
    Parse html to find all sublinks
    :param html: html doc
    :param url: url to main page 
    :return: 
    """
    if not url.endswith('/'):
        url = url+'/'

    sublinks = []
    for link in links:
        html = get_html(link)
        all_links = [l[6:-1] for l in re.findall('href=".*?"', html)]
        for link in all_links:
            if link.startswith(url):
                sublinks.append(link)
            elif link.startswith("/"):
                sublinks.append(url + link[1:])
            elif link.startswith("../"):
                sublinks.append(url + link[2:])
            else:
                if not link.startswith('http:'):
                    sublinks.append(url + link)
    # ignore main link
    ignorable = [url, url[:-1]]
    # todo: check if the link is actually there
    return [ link for link in sublinks if not link in ignorable]

