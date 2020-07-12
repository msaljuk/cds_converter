#! /usr/bin/env python3

import json
from urllib.parse import urlparse
import os.path
import warnings
import requests

import numpy as np
import pandas as pd
import tabula

# ignore module deprecation warning from Pandas library
VisibleDeprecationWarning = np.VisibleDeprecationWarning
warnings.filterwarnings("ignore", category=VisibleDeprecationWarning)

def downloadPDFFile(url):
    '''
    Downloads the PDF file at the given URL
    and returns the file name.
    '''
    try:
        file_name = os.path.split(urlparse(url).path)[1]
        response = requests.get(url)
        with open(file_name, 'wb') as pdf:
            pdf.write(response.content)
            print("Downloaded the PDF File")
            return os.path.splitext(file_name)[0]
    except:
        print("Failed to download the PDF File")
        return None

def create_raw_json_file(file_name):
    '''
    Creates intermediate JSON file from PDF
    '''
    data_file = pd.DataFrame(tabula.read_pdf(file_name + '.pdf', pages='all', multiple_tables=True, lattice=True))
    data_file.to_json(file_name + '.json')
    print("Created raw/intermediate JSON File")

def compileValuesArray(dictionary):
    '''
    Takes all values in an object and appends them
    to an array. Returns that array
    '''
    out = []
    for each_key in dictionary:
        out.append(dictionary[each_key])
    return out

def createExcelWorksheet(file_name):
    '''
    Generates Excel worksheet from JSON file
    '''
    current_row_index = 0  # worksheet row number at which to append current table

    # set up Excel Writing
    writer = pd.ExcelWriter(file_name + '.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet(file_name)
    writer.sheets[file_name] = worksheet

    with open(file_name + '.json') as json_file:
        json_object = json.load(json_file)
        for each in json_object:
            for key in json_object[each]:
                df = pd.DataFrame({})
                for columns in json_object[each][key]:
                    data = compileValuesArray(json_object[each][key][columns])
                    df[columns] = data
                df.to_excel(writer, sheet_name=file_name, startrow=current_row_index, startcol=0)
                current_row_index += len(data) + 3
    # save to Excel
    writer.save()
    print("An Excel File by the name of " + file_name + ".pdf was created in your directory.")

# main runtime

def runPDFScraper(url):
    '''
    main function
    '''
    response = {'status': '', 'data': ''}

    file_name = downloadPDFFile(url)
    if file_name is not None:
        create_raw_json_file(file_name)
        createExcelWorksheet(file_name)
        # delete downloaded PDF file
        os.remove(file_name + '.pdf')
        # delete intermediate JSON file
        os.remove(file_name + '.json')
        response['status'] = "200 OK"
        response['data'] = file_name + '.xlsx'
        return response
    else:
        response['status'] = "500 ERROR"
        return response
