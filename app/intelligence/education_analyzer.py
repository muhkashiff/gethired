class EducationAnalyzer:

    LEVELS = [

        "PhD",

        "Doctor",

        "Master",

        "M.Sc",

        "MBA",

        "Bachelor",

        "Diploma",

        "Certificate"

    ]

    def analyze(self, education):

        highest = None

        for item in education:

            for level in self.LEVELS:

                if level.lower() in item.lower():

                    highest = level

                    break

            if highest:
                break

        return {

            "highest_degree": highest,

            "entries": education

        }