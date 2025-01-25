"""
Handle scraping CAB for a full listing of course details; downloading/updating data files locally
"""

import json
import os
import time
from datetime import UTC, datetime

from requests.exceptions import RequestException
from tqdm import tqdm

import main

SRCDB = "202420"
REQUESTS_PER_SECOND = 10


def scrape_all_course_details(srcdb: str):
    """
    Pull details for all courses from database

    srcdb: CAB database ID for the current semester (e.g. 202420 for Spring 2025)
    """
    # TODO: filter by whether hash changed since last time
    try:
        fetched_db = main.get_all_courses(srcdb)["results"]
    except RequestException as e:
        print(f"Error fetching database {srcdb}: {e}")
        return

    datetime_zulu = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}"  # e.g. 20250125T143059Z

    iter_results = {}  # assemble dict of all course details
    for course in tqdm(fetched_db):
        course_key = course["key"]

        try:  # pull specific course details from cab
            course_details = main.get_course_details(srcdb, "key", course_key)
            iter_results[course_key] = course_details

        except RequestException as e:
            print(f"Error pulling details for key:{course_key}: {e}")

        finally:
            time.sleep(1 / REQUESTS_PER_SECOND)

    # dump results to file
    dir = os.path.join("data", srcdb)
    os.makedirs(dir, exist_ok=True)

    with open(f"data/{srcdb}/{datetime_zulu}.json", "w") as f:
        json.dump(iter_results, f)


if __name__ == "__main__":
    scrape_all_course_details(SRCDB)
