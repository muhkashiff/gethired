"""
Production Experience Extractor

Converts the Experience section into structured Experience objects.
"""

import re

from app.parser.parsed_models import Experience


class ExperienceExtractor:

    def extract(self, lines):

        jobs = []

        current_job = None

        mode = "responsibility"

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # ---------------------------------
            # Detect Job Heading
            # ---------------------------------

            if self.is_job_heading(line):

                if current_job:
                    jobs.append(current_job)

                current_job = self.parse_job(line)

                mode = "responsibility"

                continue

            # ---------------------------------
            # Detect Accomplishment Section
            # ---------------------------------

            if "key accomplishment" in line.lower():

                mode = "achievement"

                continue

            if current_job is None:
                continue

            # ---------------------------------
            # Responsibilities
            # ---------------------------------

            if mode == "responsibility":

                current_job.responsibilities.append(line)

            # ---------------------------------
            # Achievements
            # ---------------------------------

            else:

                current_job.achievements.append(line)

        if current_job:

            jobs.append(current_job)

        return jobs

    # ==========================================================
    # Job Heading Detector
    # ==========================================================

    def is_job_heading(self, text):

        return bool(

            re.search(

                r"(19|20)\d{2}",

                text

            )

        )

    # ==========================================================
    # Parse Job Heading
    # ==========================================================

    def parse_job(self, text):

        job = Experience()

        years = re.findall(

            r"(19|20)\d{2}",

            text

        )

        if years:

            job.start_year = int(years[0])

            if len(years) > 1:

                job.end_year = int(years[1])

            else:

                job.current = True

        title = re.split(

            r"(19|20)\d{2}",

            text

        )[0]

        job.job_title = title.strip()

        company = ""

        if "|" in title:

            parts = title.split("|")

            job.job_title = parts[0].strip()

            company = parts[1].strip()

        job.company = company

        return job