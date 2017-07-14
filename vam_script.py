#!/usr/bin/env python

import os
import argparse
import json
import urllib
import urllib2

API_SEARCH_URL = "http://www.vam.ac.uk/api/json/museumobject/search?"
API_IMAGE_URL = "http://media.vam.ac.uk/media/thira/collection_images/"
API_RESULT_LIMIT = 45

def user_input(results):
    print(str(results) + " results found.")

    while True:
        answer = raw_input("Do you want to continue? [y/n]")
        if answer is "n":
            print("Bye!")
            exit()
        if answer is "y":
            break

def format_search_string(string):
    string = string.replace(" ", "+")
    string = string.replace(",", "%2C")
    return string

def create_search_query(args):
    query = []
    if args.query != "":
        q = format_search_string(args.query)
        query.append("q=" + q)
    if args.namesearch != "":
        namesearch = format_search_string(args.namesearch)
        query.append("namesearch=" + namesearch)
    if args.objectnamesearch != "":
        objectnamesearch = format_search_string(args.objectnamesearch)
        query.append("objectnamesearch=" + objectnamesearch)
    if args.materialsearch != "":
        materialsearch = format_search_string(args.materialsearch)
        query.append("materialsearch=" + materialsearch)
    if args.placesearch != "":
        placesearch = format_search_string(args.placesearch)
        query.append("placesearch=" + placesearch)
    if args.before != "":
        before = args.before
        query.append("before=" + before)
    if args.after != "":
        after = args.after
        query.append("after=" + after)
    if args.images != "1":
        images = "0"
        query.append("images=" + images)

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
            records.append(record)

    return records

def create_folder(directory):
    cwd = os.getcwd()
    path = cwd + '/' + directory
    if not os.path.isdir(path):
        os.mkdir(directory)
    os.chdir(path)
    os.mkdir("json")

def get_image_url(name):
    url = API_IMAGE_URL
    identifier = name[0:6]
    url = url + identifier + "/" + name + ".jpg"
    return url

def safe_image_info(record):
    fields = record['fields']
    default = "Unknown"
    
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
        url = get_image_url(image_id)
        filename = image_id + ".jpg"
        if not os.path.isfile(filename):
            urllib.urlretrieve(url, filename)
            safe_image_info(record)

def save_to_file(file_name, data):
    file_name = "json/" + file_name
    with open(file_name, "w") as json_file:
        data = json.dumps(data, indent=4)
        json_file.write(data)

def Main():
    print("Running script...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default='images', help='specify download directory')
    parser.add_argument('-q', '--query', default='', help='specify default search query')
    parser.add_argument('-n', '--namesearch', default='', help='specify your name search')
    parser.add_argument('-o', '--objectnamesearch', default='', help='specify object search term')
    parser.add_argument('-m', '--materialsearch', default='', help='specify material search')
    parser.add_argument('-p', '--placesearch', default='', help='specify place search')
    parser.add_argument('-b', '--before', default='', help='specify time search before')
    parser.add_argument('-a', '--after', default='', help='specify time search after')
    parser.add_argument('-i', '--images', default='1', help='specify if you want results without images')
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

    i = 1
    while processed < results:
        print("Process images from: " + uri)

        data = data_from_uri(uri)
        file_name = "vam_json_record_" + str(i) + ".json"
        save_to_file(file_name, data)

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

        i = i + 1

    print("Found " + str(file_count) + " image files out of " + str(results) + " entries.")
    print("Finished.")

if __name__ == '__main__':
    Main()
