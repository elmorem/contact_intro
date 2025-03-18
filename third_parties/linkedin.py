import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrapes a LinkedIn profile page for information."""
    load_dotenv(override=True)
    linkedin_username = os.environ.get("LINKEDIN_USERNAME")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")

    if mock:
        return {
            "name": "John Doe",
            "headline": "Software Engineer at Example Corp",
            "location": "San Francisco, CA",
            "summary": "Experienced software engineer with a passion for developing innovative programs.",
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Example Corp",
                    "duration": "Jan 2020 - Present",
                }
            ],
            "education": [
                {
                    "degree": "BSc Computer Science",
                    "school": "University of Example",
                    "duration": "2015 - 2019",
                }
            ],
        }
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data
