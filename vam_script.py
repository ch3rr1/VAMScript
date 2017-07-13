#!/usr/bin/env python

import os
import argparse
import json
import urllib
import urllib2

API_SEARCH_URL = "http://www.vam.ac.uk/api/json/museumobject/search?"
API_IMAGE_URL = "http://media.vam.ac.uk/media/thira/collection_images/"
API_RESULT_LIMIT = 45

file_index = 1

def user_input(results):
    print(str(results) + " results found.")

    while True:
        answer = raw_input("Do you want to continue? [y/n]")

        if answer is "n":
            print("Bye!")
            exit()
        if answer is "y":
            break

def create_search_query(args):
    query = []
    if args.objectnamesearch != "":
        query.append("objectnamesearch=" + args.objectnamesearch)
    if args.materialsearch != "":
        materialsearch = args.materialsearch
        materialsearch = materialsearch.replace(" ", "+")
        materialsearch = materialsearch.replace(",", "%2C")
        query.append("materialsearch=" + materialsearch)

    query_string = ""
    for element in query:
        query_string = query_string + "&" + element
    
    if query_string != "":
        query_string = query_string[1:]
    
    return query_string

def create_search_uri(search_query):
    
    limit = str(API_RESULT_LIMIT)
    uri = API_SEARCH_URL + search_query + "&limit=" + limit + "&offset=0"
    return uri

def update_uri(uri, offset):
    parts = uri.split("&offset=")
    if len(parts) is 2:
        uri = parts[0] + "&offset=" + str(offset)
    return uri

def data_from_uri(uri):
    response = urllib2.urlopen(uri)
    data = json.load(response)
    return data

def results_from_data(data):
    results = data['meta']['result_count']
    return int(results)

def records_from_data(data):
    records = []

    for record in data['records']:
        fields = record['fields']
        if 'primary_image_id' in fields:
            #image_id = fields['primary_image_id']
            #image_ids.append(image_id)
            records.append(record)

    return records

def create_folder(directory):
    cwd = os.getcwd()
    path = cwd + '/' + directory
    if not os.path.isdir(path):
        os.mkdir(directory)
    os.chdir(path)

def get_image_url(name):
    url = API_IMAGE_URL
    identifier = name[0:6]
    url = url + identifier + "/" + name + ".jpg"
    return url

def safe_image_info(record):
    fields = record['fields']
    
    image_id = fields['primary_image_id'].encode('utf-8').strip()
    artist = fields['artist'].encode('utf-8').strip()
    date_text = fields['date_text'].encode('utf-8').strip()
    object_number = fields['object_number'].encode('utf-8').strip()
    object_name = fields['object'].encode('utf-8').strip()
    place = fields['place'].encode('utf-8').strip()
    title = fields['title'].encode('utf-8').strip()

    info = "ID: " + image_id + "\n\tArtist: " + artist + "\n\tDate: " \
        + date_text + "\n\tObject: " + object_number + "\n\tName: " \
        + object_name + "\n\tPlace: " + place + "\n\tTitle: " + title + "\n\n"
    
    with open('image_info.txt', 'a') as info_file:
        info_file.write(info)


def download_images(records):
    for record in records:
        fields = record['fields']
        image_id = fields['primary_image_id']
        artist = fields['artist']
        if artist is "" or not artist:
            artist = "Unknown"
        date_text = fields['date_text']
        if date_text is "" or not date_text:
            date_text = "Unknown"
        url = get_image_url(image_id)
        filename = artist + "_" + date_text + "_" + image_id + ".jpg"
        if not os.path.isfile(filename):
            urllib.urlretrieve(url, filename)
            safe_image_info(record)

def Main():
    print("Running script...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default='images', help='specify download directory')
    parser.add_argument('-o', '--objectnamesearch', default='', help='specify search term e.g. teapots')
    parser.add_argument('-m', '--materialsearch', default='', help='specify material search')
    args = parser.parse_args()

    # create json request uri
    query = create_search_query(args)
    uri = create_search_uri(query)

    data = data_from_uri(uri)
    results = results_from_data(data)
    processed = 0
    limit = str(API_RESULT_LIMIT)
    file_count = 0
    
    # ask user for permission to continue
    user_input(results)

    create_folder(args.directory)

    print("Processing " + str(results) + " entries:")
    print(str(processed) + "/" + str(results))

    while int(processed) < results:
        data = data_from_uri(uri)
        records = records_from_data(data)
        download_images(records)
        processed = processed + API_RESULT_LIMIT
        offset = processed
        uri = update_uri(uri, offset)
        file_count = file_count + len(records)

        if processed < results:
            print(str(processed) + "/" + str(results))
        else:
            print(str(results) + "/" + str(results))

    print("Found " + str(file_count) + " image files out of " + str(results) + " entries.")
    print("Finished.")

if __name__ == '__main__':
    Main()
