from app.parser.experience.achievement_detector import AchievementDetector

sample = [

    "Achieved a remarkable 99%+ production line product yield.",

    "Sustained a stellar 99.5% plant-wide quality rating.",

    "Obtained a perfect 100% score in the Shell Mystery Shopper program.",

    "Improved supply chain efficiency and profitability.",

    "Reduced downtime by 35%.",

    "Saved $150,000 annually through waste reduction."

]

detector = AchievementDetector()

results = detector.parse(sample)

print("="*70)

for item in results:

    print(item)

    print("-"*70)