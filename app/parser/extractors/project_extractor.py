from .base_extractor import BaseExtractor


class ProjectExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)