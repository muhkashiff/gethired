from .base_extractor import BaseExtractor


class EducationExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)