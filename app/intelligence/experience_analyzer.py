import re


class ExperienceAnalyzer:

    YEAR_PATTERN = re.compile(r"(19|20)\d{2}")

    def analyze(self, experience_lines):

        result = {
            "positions": [],
            "companies": [],
            "years": [],
            "titles": [],
            "total_years": 0,
        }

        start_year = None
        end_year = None

        for line in experience_lines:

            years = self.YEAR_PATTERN.findall(line)

            years = re.findall(r"(19\d{2}|20\d{2})", line)

            if len(years) >= 2:

                s = int(years[0])
                e = int(years[1])

                result["years"].append((s, e))

                if start_year is None or s < start_year:
                    start_year = s

                if end_year is None or e > end_year:
                    end_year = e

            if "|" in line:

                parts = line.split("|")

                title = parts[0].strip()

                result["titles"].append(title)

                if len(parts) > 1:
                    company = parts[1].strip()

                    result["companies"].append(company)

        if start_year and end_year:

            result["total_years"] = end_year - start_year

        return result