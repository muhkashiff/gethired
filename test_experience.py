from app.parser.parsers.experience_parser import ExperienceParser

lines = [

    "QA Chemist | Coca-Cola Beverages Pakistan Ltd. | 2010 - 2016 | Lahore",

    "Managed quality system.",

    "Improved yield.",

    "Key Accomplishments",

    "Reduced waste by 20%.",

    "Implemented HACCP.",

    "Retail Store Manager | Shell | 2016 - 2024 | Canada",

    "Managed retail store.",

    "Increased sales.",

    "Achievements",

    "100% Mystery Shopper Score",

]

parser = ExperienceParser()

jobs = parser.parse(lines)

parser.print_jobs(jobs)