"""
Production Grade Experience Parser

Parses experience section using a state machine.

No large regex.
"""

from datetime import datetime

from app.parser.models.experience import Experience


class ExperienceParser:

    def __init__(self):

        self.current_year = datetime.now().year

    # -----------------------------------------------------
    # Public
    # -----------------------------------------------------

    def parse(self, lines):

        jobs = []

        current_job = None

        mode = "responsibility"

        for raw_line in lines:

            line = raw_line.strip()

            if not line:
                continue

            # ----------------------------------------
            # New Job
            # ----------------------------------------

            if self.is_job_header(line):

                if current_job:

                    jobs.append(current_job)

                current_job = self.create_job(line)

                mode = "responsibility"

                continue

            # ----------------------------------------
            # Achievement Section
            # ----------------------------------------

            if self.is_achievement_header(line):

                mode = "achievement"

                continue

            if current_job is None:

                continue

            # ----------------------------------------
            # Store Content
            # ----------------------------------------

            if mode == "responsibility":

                current_job.responsibilities.append(line)

            else:

                current_job.achievements.append(line)

        if current_job:

            jobs.append(current_job)

        return jobs

    # -----------------------------------------------------
    # Detect Job Header
    # -----------------------------------------------------

    def is_job_header(self, line):

        lower = line.lower()

        if "|" not in line:
            return False

        if any(word in lower for word in [
            "phone",
            "email",
            "linkedin",
            "github",
            "summary",
            "education",
            "skills",
            "language"
        ]):
            return False

        if any(char.isdigit() for char in line):

            return True

        return False

    # -----------------------------------------------------
    # Achievement Header
    # -----------------------------------------------------

    def is_achievement_header(self, line):

        lower = line.lower()

        return (
            "achievement" in lower
            or "accomplishment" in lower
            or "key accomplishment" in lower
        )

    # -----------------------------------------------------
    # Create Job Object
    # -----------------------------------------------------

    def create_job(self, line):

        job = Experience()

        job.raw_header = line

        self.parse_header(job)

        return job

    # -----------------------------------------------------
    # Parse Header
    # -----------------------------------------------------

    def parse_header(self, job):

        text = job.raw_header

        parts = [p.strip() for p in text.split("|")]

        if len(parts) >= 1:
            job.title = parts[0]

        if len(parts) >= 2:
            job.company = parts[1]

        for year in range(1980, self.current_year + 1):

            if str(year) in text:

                if job.start_year is None:

                    job.start_year = year

                else:

                    job.end_year = year

        if job.end_year is None:

            job.end_year = self.current_year

    # -----------------------------------------------------
    # Pretty Print
    # -----------------------------------------------------

    def print_jobs(self, jobs):

        for job in jobs:

            print("=" * 60)

            print(job.title)

            print(job.company)

            print(job.start_year)

            print(job.end_year)

            print()

            print("Responsibilities")

            for r in job.responsibilities:

                print("-", r)

            print()

            print("Achievements")

            for a in job.achievements:

                print("-", a)

            print()