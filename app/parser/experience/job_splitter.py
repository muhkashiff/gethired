"""
GetHired

Production Job Splitter V2

Splits the Experience section into individual jobs.

Priority
--------
1. Known Job Title
2. Year (only when not already inside a new header)
"""

import re

from app.knowledge.job_title_loader import JobTitleKnowledge


class JobSplitter:

    def __init__(self):

        self.job_titles = JobTitleKnowledge()

        self.year_pattern = re.compile(
            r"(19|20)\d{2}\s*[-–]\s*((19|20)\d{2}|Present|Current)",
            re.IGNORECASE
        )

    # ==========================================================
    # Split Experience
    # ==========================================================

    def split(self, experience_lines):

        jobs = []

        current_job = []

        waiting_for_date = False

        for line in experience_lines:

            line = line.strip()

            if not line:
                continue

            # ---------------------------------------------
            # Is this line a Job Title?
            # ---------------------------------------------

            title = self.job_titles.lookup(line)

            if title:

                # Save previous job

                if current_job:

                    jobs.append(current_job)

                    current_job = []

                current_job.append(line)

                waiting_for_date = True

                continue

            # ---------------------------------------------
            # Date immediately after Job Title
            # ---------------------------------------------

            if waiting_for_date and self.year_pattern.search(line):

                current_job.append(line)

                waiting_for_date = False

                continue

            # ---------------------------------------------
            # Normal content
            # ---------------------------------------------

            current_job.append(line)

        if current_job:

            jobs.append(current_job)

        return jobs