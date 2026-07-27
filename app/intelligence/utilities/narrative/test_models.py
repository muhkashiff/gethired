import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

sys.path.append(str(ROOT))

from evidence_humanizer import EvidenceHumanizer

humanizer = EvidenceHumanizer()

examples = [

    "Led cross-functional teams.",

    "Implemented FSSC 22000.",

    "Managed Supplier Quality.",

    "Improved production yield to 99%.",

    "Reduced complaints by 60%.",

    "Certified facility to FSSC 22000."

]

for item in examples:

    print(humanizer.humanize(item))