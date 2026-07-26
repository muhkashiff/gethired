import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_parser.clause_segmenter import ClauseSegmenter
from app.intelligence.utilities.knowledge.knowledge_parser.clause_rebuilder import ClauseRebuilder
from app.intelligence.utilities.knowledge.knowledge_parser.clause_normalizer import ClauseNormalizer

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import ActionExtractor
from app.intelligence.utilities.knowledge.knowledge_extractors.modifier_extractor import ModifierExtractor

segmenter = ClauseSegmenter()
rebuilder = ClauseRebuilder()
normalizer = ClauseNormalizer()

action_extractor = ActionExtractor()
modifier_extractor = ModifierExtractor()

examples = [

    "Implemented ISO 9001, trained staff and improved productivity by 25%.",

    "Managed supplier quality while reducing downtime by 40 hours.",

    "Successfully implemented FSSC 22000 reducing customer complaints by 60%.",

]

for sentence in examples:

    print("=" * 80)

    print(sentence)

    actions = action_extractor.extract_all(sentence)

    modifiers = modifier_extractor.extract(sentence)

    clauses = segmenter.segment(sentence, actions)

    clauses = rebuilder.rebuild(
        sentence,
        clauses,
        modifiers,
    )

    clauses = normalizer.normalize(
        clauses,
        actions,
    )

    for clause in clauses:

        print(clause.text)