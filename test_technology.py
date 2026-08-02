from app.intelligence.utilities.knowledge.knowledge_extractors.technology_extractor import TechnologyExtractor

sample = [

    "Developed predictive models using Python, SQL and Power BI.",

    "Created dashboards using Tableau and Excel.",

    "Managed SAP QM and SAP MM modules.",

    "Performed statistical analysis using Minitab.",

    "Containerized applications using Docker.",

    "Deployed applications to Microsoft Azure.",

    "Version control using Git and GitHub."

]

extractor = TechnologyExtractor()

technologies = extractor.extract(sample)

print("=" * 70)
print("TECHNOLOGIES")
print("=" * 70)

for tech in technologies:

    print(tech)

print("=" * 70)
print("TOTAL:", len(technologies))