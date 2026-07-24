class CertificationAnalyzer:

    IMPORTANT = [

        "PMP",

        "Lean",

        "Six Sigma",

        "PCQI",

        "BRCGS",

        "ISO",

        "AWS",

        "Azure",

        "Google",

        "Scrum",

        "FSSC",

        "HACCP"

    ]

    def analyze(self, certifications):

        found = []

        for cert in certifications:

            for keyword in self.IMPORTANT:

                if keyword.lower() in cert.lower():

                    found.append(keyword)

        return {

            "certifications": certifications,

            "recognized": list(set(found))

        }