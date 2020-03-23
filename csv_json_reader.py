#!/usr/bin/python3
"""
This script will read the passed json or csv file and will print analysis results
"""
__author__ = "Manveer Singh"

import argparse
import os.path
import pandas
import sys
import string
from datetime import datetime, timedelta


def parse_args():
    """
    This function reads the arguments passed
    :return: arugments object
    """
    parser = argparse.ArgumentParser("Script reads the json or csv file and prints out the analysis result")
    parser.add_argument('-f', "--file", required=True, type=str,
                        help="Pass the CSV or Json file path to read")
    args = parser.parse_args()
    return args


def get_file_extension(file):
    """
    This function will get the extension of the file.
    :param file: file name
    :return: extension of the file
    """
    # 2nd element in the splitext tuple gives extension of the file
    # used casefold() for caseless matching to cover cases like .JSON & .json files, etc
    extension = os.path.splitext(file)[1][1:].strip().casefold()
    return extension


def file_reader(file):
    """
    Reads the file using Pandas library
    :param file: the path of the file which needs to be loaded
    :return: pandas data frame object
    """
    file_data = None
    extension = get_file_extension(file)
    try:
        if extension == 'csv':
            file_data = pandas.read_csv(file, sep=',')
        elif extension == 'json':
            file_data = pandas.read_json(file)
        else:
            raise NotImplementedError("The file format which is passed is not supported")
    except IOError:
        raise IOError("Error while opening file")
    return file_data


def get_avg_siblings(file_data):
    """
    Method to get the average siblings in whole records
    :param file_data: the pandas data frame object
    :return: average number of siblings in whole data sets
    """
    # Mean method on pandas data frame returns the average of the values for the requested axis
    return int(round(file_data['siblings'].mean()))


def get_top_food(file_data):
    """
    This method get the top food choices from the provided data
    :param file_data: the pandas data frame object
    :return: top 3 food choices
    """
    # To remove unwanted whitespaces and perform same case matching on the food names
    file_data['favourite_food'] = file_data['favourite_food'].apply(lambda data_str: string.capwords(data_str))
    # value_counts() gives the counts of unique elements in the defined column in descending order
    # head(3) gives the first 3 rows
    return file_data['favourite_food'].value_counts().head(3)


def convert_time(time_str):
    """
    Converts the hh:mm i.e hours and minutes to seconds
    :param time_str: the time str in format hh:mm
    :return: number of seconds
    """
    hours, minutes = map(int, time_str.split(':'))
    # If hours is negative then we are converting minutes to be negative
    if hours < 0:
        minutes = minutes*(-1)
    # total_seconds() method is used to get the seconds from hours and minutes
    return int(timedelta(hours=int(hours), minutes=int(minutes)).total_seconds())


def get_birthday_mnths(file_data):
    """
    This method gets the number of birthdays in each month
    :param file_data: the pandas data frame object
    :return: each month with number of birthdays
    """
    birth_mnths = {'January': 0, 'February': 0, 'March': 0,
                   'April': 0, 'May': 0, 'June': 0,
                   'July': 0, 'August': 0, 'September': 0,
                   'October': 0, 'November': 0, 'December': 0}

    # Converting hh:mm format to seconds
    file_data['birth_timezone'] = file_data['birth_timezone'].apply(convert_time)
    # Converting birth_timestamp in seconds from milli seconds
    file_data['birth_timestamp'] = file_data['birth_timestamp'].apply(lambda timestamp: timestamp/1000)
    # Adding the timezone seconds to the timestamp to make it local time
    file_data['birth_timestamp'] += file_data['birth_timezone']

    for index, epoch in file_data['birth_timestamp'].items():
        # Used utcfromtimestamp() because epoch is now in local time as timezone offset is adjusted
        # Used %B string in strftime() returns the full month
        birth_mnth = datetime.utcfromtimestamp(epoch).strftime('%B')
        birth_mnths[birth_mnth] += 1
    return birth_mnths


if __name__ == "__main__":
    all_args = parse_args()
    if not os.path.isfile(all_args.file):
        print(f"File name passed: {all_args.file} doesn't exists")
        sys.exit(1)
    data = file_reader(all_args.file)
    avg_sibling = get_avg_siblings(data)
    top_food = get_top_food(data)
    birth_months = get_birthday_mnths(data)
    print(f"Average siblings: {avg_sibling}\n")
    print("Favourite foods:")
    for item, count in top_food.items():
        print(f"- {item:15} {count}")
    print("\nBirths per Month:")
    for month, freq in birth_months.items():
        print(f"- {month:11} {freq}")

