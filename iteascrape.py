#!/usr/bin/env python3

"""
# iteascrape.py

Scrape ITEA Journal PDFs held at `<https://itea.org/images/journal/{year}-{month}/document.pdf>`.

Licensed under "MIT No Attribution" (MIT-0).
"""

import os
import random
import shutil
import time

import requests


WAIT_SECONDS_SCALE = 60
YEARS = range(2012, 2024 + 1)
MONTHS = ['March', 'June', 'September', 'December']


def download_pdf(source_url, target_name):
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests/39217788#39217788
    with requests.get(source_url, stream=True) as response:
        response.raise_for_status()
        with open(target_name, 'wb') as file:
            shutil.copyfileobj(response.raw, file)


def main():
    print('Started.')

    for year in YEARS:
        for month in MONTHS:
            source_url = f'https://itea.org/images/journal/{year}-{month}/document.pdf'
            target_name = f'output/itea-{year}-{month}.pdf'

            if os.path.isfile(target_name):
                print(f'- `{target_name}` already scraped;')
                continue

            wait_seconds = random.uniform(0.7, 2) * WAIT_SECONDS_SCALE
            print(f'Waiting {wait_seconds:.1f} seconds...')
            time.sleep(wait_seconds)
            try:
                download_pdf(source_url, target_name)
                print(f'- `{target_name}` successfully scraped;')
            except requests.exceptions.RequestException as exception:
                print(f'- {type(exception).__name__} raised for <{source_url}>;')

    print('Finished.')


if __name__ == '__main__':
    main()
