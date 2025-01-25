"""
Handle interfacing with CAB
"""

from typing import Optional

import requests

API_URL = "https://cab.brown.edu/api/"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}


def get_all_courses(srcdb: str) -> Optional[dict]:
    """
    Scrapes all classes from cab

    srcdb: CAB database ID for the current semester (e.g. 202420 for Spring 2025)

    Returns dictionary of cab json output
    """
    r = requests.post(
        API_URL,
        params={"page": "fose", "route": "search"},
        headers=REQUEST_HEADERS,
        json={  # TODO: add ability to specify criteria through a dictionary
            "other": {"srcdb": srcdb},
            "criteria": [
                {"field": "is_ind_study", "value": "N"},
                {"field": "is_canc", "value": "N"},
            ],
        },
    )

    r.raise_for_status()
    return r.json()


def get_course_details(srcdb: str, key_type: str, key: str) -> Optional[dict]:
    """
    Scrapes details for a specific class from cab

    srcdb: CAB database ID for the current semester (e.g. 202420 for Spring 2025)
    key_type: Type of key ("key", "crn", etc.)
    key: The corresponding key of the course to look up

    Returns dictionary of cab json output
    """
    r = requests.post(
        API_URL,
        params={"page": "fose", "route": "details"},
        headers=REQUEST_HEADERS,
        json={"key": f"{key_type}:{key}", "srcdb": srcdb},
    )

    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    print(get_course_details("202420", "key", "1"))
