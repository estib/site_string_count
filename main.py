__author__ = 'Steve Lechner’

# This program will visit every accessible site in a domain and search for a
# given string. It will do this by counting the string's occurrence on the
# domain's home page, then collecting all the urls available in that page, and
# then recursively repeating this activity on each yet unvisited url that it
# finds. The program will output the search links and counts in a csv file.
# It will print how much time it took to run.

import requests
import csv
from bs4 import BeautifulSoup
import datetime


def get_new_links(url, url_list, search_string):
    '''
    This function will take the a url, a list of previously visited urls, and
    a string-to-be-counted-on-each-web-page. It will visit the main url, count
    the occurrences of the search_string, and then add any urls found on the
    page that share the original domain and (if they are not on the list of
    previously visited urls. It will then recursively call itself on each of
    the newly found urls. It then returns the url list with its counts of
    the search_string on each visited page.
    '''

    # get the domain from the url
    if url.find('.com') > 0:
        url_base = url[:url.find('.com') + 4]
    elif url.find('.org') > 0:
        url_base = url[:url.find('.org') + 4]
    elif url.find('.net') > 0:
        url_base = url[:url.find('.net') + 4]

    # get the last web directory
    url_base_2 = str(url_base + '/' +
                     url[url.find(url_base) + len(url_base) + 1:
                         url.rfind('/', 0, len(url)-1) + 1])

    # make sure it doesn't have any of those back-up directory strings
    if url_base_2.count("../") > 0:
        url_base_2 = url_base + '/' + url_base_2[url_base_2.find('../') + 3:]

    # get site
    site_stuff = requests.get(url)
    site_text = site_stuff.text
    site_soup = BeautifulSoup(site_text)
    all_site_text = site_soup.get_text()
    all_site_text = all_site_text.lower()

    # count the number of instances of the string
    num = all_site_text.count(search_string.lower())

    # find other urls
    link_list = site_soup.find_all('a')
    for each in link_list:
        if each.has_attr('href'):
            link = str(each.get('href'))
            if link.count("../") == 0:  # avoid the "../" strings. They make
                # the searching of urls redundant.
                if (
                        link[:4] != "http" and
                        link[:5] != "file:" and
                        link[len(link) - 4:] != ".pdf" and
                        link[0] != "#"
                ):  # also avoid new domains, downloading files, pdfs, or
                    # internal hyperlinks.
                    if link.find("#") > 0:
                        link = link[:link.find('#') - 1]
                    # if not in list, then run recursively
                    in_url_list = False
                    for each_url in url_list:
                        if each_url[0] == url_base_2 + link:
                            in_url_list = True
                    if in_url_list is False:
                        url_list[len(url_list):] = [((url_base_2 + link), num)]
                        # and just in case stuff goes wrong, save a draft of
                        # the results every 25 links.
                        if len(url_list) % 25 == 0:
                            with open("/Users/stephenlechner/Google Drive/Steve Docs/General_Crawler_Results_-_" +
                                      search_string + "_DRAFT.csv", "wb") \
                                    as draft_doc:
                                draft_writer = csv.writer(draft_doc)
                                draft_writer.writerow(list((
                                    "Webpage",
                                    str("Number of times " + search_string +
                                        " found:")
                                )))
                                for each_url in url_list:
                                    draft_writer.writerow(list(each_url))

                        url_list = get_new_links(
                            url_base_2 + link,
                            url_list,
                            search_string
                        )
    return url_list


start = datetime.datetime.now()

main_site = raw_input("What is the main site you'd like to crawl through?")

target = raw_input(
    "And what interesting thing would you like to search for in that site?"
)

target = target.lower()

a_link_list = list()

a_link_list = get_new_links('http://' + main_site, a_link_list, target)

with open("/Users/stephenlechner/Google Drive/Steve Docs/General_Crawler_Results_-_" +
          main_site + "_" + target + ".csv", "wb") as write_doc:
    doc_writer = csv.writer(write_doc)
    doc_writer.writerow(list((
        "Webpage",
        str("Number of times " + target + " found:")
    )))
    for every in a_link_list:
        doc_writer.writerow(list(every))

print(
    "It took this long to run this program:",
    str(datetime.datetime.now() - start)
)
