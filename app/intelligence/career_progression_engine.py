import re


class MetricsAnalyzer:

    PERCENT = re.compile(r"\d+(\.\d+)?%")
    MONEY = re.compile(r"\$[\d,]+")
    NUMBER = re.compile(r"\b\d+\b")

    def analyze(self, lines):

        metrics = []

        for line in lines:

            if (
                self.PERCENT.search(line)
                or self.MONEY.search(line)
                or self.NUMBER.search(line)
            ):
                metrics.append(line)

        return metrics