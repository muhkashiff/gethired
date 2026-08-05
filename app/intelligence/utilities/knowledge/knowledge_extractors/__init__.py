from .action_extractor import ActionExtractor
from .target_extractor import ObjectExtractor
from .metric_extractor import MetricExtractor
from .measurement_extractor import MeasurementExtractor
from .technology_extractor import TechnologyExtractor
from .standard_extractor import StandardExtractor
from .methodology_extractor import MethodologyExtractor
from .skills_extractor import SkillsExtractor
from .modifier_extractor import ModifierExtractor
from .certification_extractor import CertificationExtractor


EXTRACTORS = [

    ActionExtractor(),

    ObjectExtractor(),

    MetricExtractor(),

    MeasurementExtractor(),

    TechnologyExtractor(),

    StandardExtractor(),

    MethodologyExtractor(),

    SkillsExtractor(),

    ModifierExtractor(),

    CertificationExtractor(),

]