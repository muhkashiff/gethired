"""
GetHired
Contact Information Extractor
"""

import re


class ContactExtractor:

    def __init__(self):
        pass

    # ------------------------
    # EMAIL
    # ------------------------
    def extract_email(self, text):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""

    # ------------------------
    # PHONE
    # ------------------------
    def extract_phone(self, text):

        pattern = r"(\+?\d[\d\s\-()]{7,}\d)"

        match = re.search(pattern, text)

        if match:
            return match.group().strip()

        return ""

    # ------------------------
    # LINKEDIN
    # ------------------------
    def extract_linkedin(self, text):

        pattern = r"(linkedin\.com/[^\s|]+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group()

        return ""

    # ------------------------
    # GITHUB
    # ------------------------
    def extract_github(self, text):

        pattern = r"(github\.com/[^\s|]+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group()

        return ""

    # ------------------------
    # LOCATION
    # ------------------------
    def extract_location(self, text):

        pattern = r"Location:\s*(.+)"
        
        match = re.search(pattern, text, re.IGNORECASE)

        location = match.group(1).strip()

        if "LinkedIn:" in location:
            location = location.split("LinkedIn:")[0].strip()

        return location
        
    # ------------------------
    # ALL
    # ------------------------
    def extract(self, header_lines):

        full_text = "\n".join(header_lines)

        return {

            "email":
                self.extract_email(full_text),

            "phone":
                self.extract_phone(full_text),

            "linkedin":
                self.extract_linkedin(full_text),

            "github":
                self.extract_github(full_text),

            "location":
                self.extract_location(full_text)
        }