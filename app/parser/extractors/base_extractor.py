class BaseExtractor:

    def clean(self, lines):

        cleaned = []

        for line in lines:

            line = line.strip()

            if line:

                cleaned.append(line)

        return cleaned