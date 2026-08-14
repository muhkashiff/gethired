from app.intelligence.enrichment.industry_detector import IndustryDetector

detector = IndustryDetector()

industry = detector.detect(

    title="QA Chemist",

    company="Coca-Cola Beverages Pakistan",

    responsibilities=[

        "Implemented HACCP",
        "Managed FSSC22000",
        "Performed food safety audits"

    ],

    achievements=[

        "Improved production yield to 99%"

    ],

    technologies=[

        "SAP QM",
        "Minitab"

    ],

    skills=[

        "Food Safety",
        "Quality Assurance"

    ]

)

print("=" * 60)
print("DETECTED INDUSTRY")
print("=" * 60)
print(industry)