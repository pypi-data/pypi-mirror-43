# -*- coding: utf-8 -*-
"""
Utility functions.
"""

import re
import requests
from lxml import etree
from re import search, IGNORECASE, findall
import os
import pandas as pd

###############################################
### Parameters

mission_product_dict = {
        'trmm': {
                'base_url': 'https://disc2.gesdisc.eosdis.nasa.gov:443',
                'process_level': 'TRMM_L3',
                'version': 7,
                'products': {
                        '3B42_Daily': '{mission}_{product}.{version}/{year}/{month:02}/{product}.{date}.{version}.nc4',
                        '3B42': '{mission}_{product}.{version}/{year}/{dayofyear:03}/{product}.{date}.{hour}.{version}.HDF'
                            }
                },
        'gpm': {
                'base_url': 'https://gpm1.gesdisc.eosdis.nasa.gov:443',
                'process_level': 'GPM_L3',
                'version': 5,
                'products': {
                        '3IMERGDE': '{mission}_{product}.{version:02}/{year}/{month:02}/3B-DAY-E.MS.MRG.3IMERG.{date}-S000000-E235959.V{version:02}.nc4',
                        '3IMERGDL': '{mission}_{product}.{version:02}/{year}/{month:02}/3B-DAY-L.MS.MRG.3IMERG.{date}-S000000-E235959.V{version:02}.nc4',
                        '3IMERGDF': '{mission}_{product}.{version:02}/{year}/{month:02}/3B-DAY.MS.MRG.3IMERG.{date}-S000000-E235959.V{version:02}.nc4',
                        '3IMERGHHE': '{mission}_{product}.{version:02}/{year}/{dayofyear:03}/3B-HHR-E.MS.MRG.3IMERG.{date}-S{time_start}-E{time_end}.{minutes}.V{version:02}B.HDF5',
                        '3IMERGHHL': '{mission}_{product}.{version:02}/{year}/{dayofyear:03}/3B-HHR-L.MS.MRG.3IMERG.{date}-S{time_start}-E{time_end}.{minutes}.V{version:02}B.HDF5',
                        '3IMERGHH': '{mission}_{product}.{version:02}/{year}/{dayofyear:03}/3B-HHR.MS.MRG.3IMERG.{date}-S{time_start}-E{time_end}.{minutes}.V{version:02}B.HDF5'
                            }
                }
        }

master_datasets = {'3B42_Daily': ['precipitation', 'randomError', 'HQprecipitation', 'IRprecipitation'],
                   '3B42': ['precipitation', 'relativeError', 'HQprecipitation', 'IRprecipitation'],
                   '3IMERGHHE': ['precipitationQualityIndex', 'IRkalmanFilterWeight', 'precipitationCal', 'HQprecipitation', 'probabilityLiquidPrecipitation', 'randomError', 'IRprecipitation'],
                   '3IMERGHHL': ['precipitationQualityIndex', 'IRkalmanFilterWeight', 'precipitationCal', 'HQprecipitation', 'probabilityLiquidPrecipitation', 'randomError', 'IRprecipitation'],
                   '3IMERGHH': ['precipitationQualityIndex', 'IRkalmanFilterWeight', 'precipitationCal', 'HQprecipitation', 'probabilityLiquidPrecipitation', 'randomError', 'IRprecipitation'],
                   '3IMERGDE': ['precipitationCal', 'HQprecipitation', 'randomError'],
                   '3IMERGDL': ['precipitationCal', 'HQprecipitation', 'randomError'],
                   '3IMERGDF': ['precipitationCal', 'HQprecipitation', 'randomError']}




###############################################
### Functions



def min_max_dates(missions=None, products=None):
    """
    Function to parse the NASA Hyrax dap server via the catalog xml.

    Parameters
    ----------
    missions : str, list of str, or None
        The missions to parse. None will parse all available.
    products : str, list of str, or None
        The products to parse. None will parse all available.

    Returns
    -------
    DataFrame
        indexed by mission and product
    """
    if isinstance(missions, str):
        missions = [missions]
    elif missions is None:
        missions = list(mission_product_dict.keys())
    if isinstance(products, str):
        products = [products]

    min_max_dates = {}

    for m1 in missions:
        base_url = '/'.join([mission_product_dict[m1]['base_url'], 'opendap',  mission_product_dict[m1]['process_level']])
#        print(base_url)
        if products is None:
            product_dict = mission_product_dict[m1]['products']
        else:
            product_dict = {p: mission_product_dict[m1]['products'][p] for p in products if p in mission_product_dict[m1]['products']}
            if not product_dict:
                raise ValueError('No products associated with ' + m1 + ' mission.')

        for p in product_dict:
            print(p)
            file_path = product_dict[p]
            path_split = os.path.split(file_path)
            mission_product = path_split[0].split('/')[0]

            mission_product1 = mission_product.format(mission=m1.upper(), product=p, version=mission_product_dict[m1]['version'])
            base_url2 = '/'.join([base_url, mission_product1, 'catalog.xml'])

            ## Get all years
            page1 = requests.get(base_url2)
            et = etree.fromstring(page1.content)
            dataset = et.getchildren()[2].getchildren()

            min_attrib = dataset[0].attrib
            min_year = min_attrib['name']

            max_attrib = dataset[-1].attrib
            max_year = max_attrib['name']

            ## min date
            min_base_url = '/'.join([base_url, mission_product1, min_year,  'catalog.xml'])
            page1 = requests.get(min_base_url)
            et = etree.fromstring(page1.content)
            dataset = et.getchildren()[2].getchildren()[0]

            min_mon = dataset.attrib['name']

            min_base_url2 = '/'.join([base_url, mission_product1, min_year, min_mon, 'catalog.xml'])

            page1 = requests.get(min_base_url2)
            et = etree.fromstring(page1.content)
            dataset = et.getchildren()[2].getchildren()[0]

            min_file = dataset.attrib['name']
            min_date1 = re.search('.\d\d\d\d\d\d\d\d', min_file).group()[1:]
#            min_time1 = re.search('S\d\d\d\d\d\d', min_file).group()[1:]
#            min_date = pd.to_datetime(min_date1 + ' ' + min_time1, infer_datetime_format=True)
            min_date = pd.to_datetime(min_date1, infer_datetime_format=True)

            ## max date
            max_base_url = '/'.join([base_url, mission_product1, max_year, 'catalog.xml'])
            page1 = requests.get(max_base_url)
            et = etree.fromstring(page1.content)
            dataset = et.getchildren()[2].getchildren()[-1]

            max_mon = dataset.attrib['name']

            max_base_url2 = '/'.join([base_url, mission_product1, max_year,  max_mon, 'catalog.xml'])

            page1 = requests.get(max_base_url2)
            et = etree.fromstring(page1.content)
            dataset = et.getchildren()[2].getchildren()[-1]

            max_file = dataset.attrib['name']
            max_date1 = re.search('.\d\d\d\d\d\d\d\d', max_file).group()[1:]
#            max_time1 = re.search('E\d\d\d\d\d\d', max_file).group()[1:]
#            max_date = pd.to_datetime(max_date1 + ' ' + max_time1, infer_datetime_format=True)
            max_date = pd.to_datetime(max_date1, infer_datetime_format=True)

            ## combine
            min_max_dates.update({p: [m1, min_date, max_date]})

    ## Convert to dataframe
    min_max = pd.DataFrame.from_dict(min_max_dates, orient='index').reset_index()
    min_max.columns = ['product', 'mission', 'start_date', 'end_date']
    min_max1 = min_max.set_index(['mission', 'product'])

    return min_max1


def rd_dir(data_dir, ext):
    """
    Function to read a directory of files and create a list of files associated with a spcific file extension. Can also create a list of file numbers from within the file list (e.g. if each file is a station number.)
    """

    files = [filename for filename in os.listdir(data_dir) if search('.' + ext + '$', filename, IGNORECASE)]

    return files




















