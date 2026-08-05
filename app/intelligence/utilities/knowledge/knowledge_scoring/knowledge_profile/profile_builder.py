"""
Enterprise Knowledge Profile Builder

Enterprise V12
"""

from .profile_models import SummaryProfile

from app.intelligence.utilities.knowledge.knowledge_scoring.base.capability_reasoner import CapabilityReasoner

from ..evidence.generic_evidence_builder import GenericEvidenceBuilder

from ..evidence.evidence_models import DomainEvidence
from ..evidence.evidence_models import LeadershipEvidence
from ..evidence.evidence_models import ATSEvidence
from ..evidence.evidence_models import BusinessValueEvidence
from ..evidence.evidence_models import TechnicalEvidence
from ..evidence.evidence_models import ExecutiveEvidence

from ..mappings.domain_mapping import DOMAIN_MAPPING
from ..mappings.technical_mapping import TECHNICAL_MAPPING
from ..mappings.leadership_mapping import LEADERSHIP_MAPPING
from ..mappings.executive_mapping import EXECUTIVE_MAPPING
from ..mappings.business_value_mapping import BUSINESS_VALUE_MAPPING
from ..mappings.ats_mapping import ATS_MAPPING

from ..scoring.domain_score_engine import DomainScoreEngine
from ..scoring.technical_score_engine import TechnicalScoreEngine
from ..scoring.leadership_score_engine import LeadershipScoreEngine
from ..scoring.executive_score_engine import ExecutiveScoreEngine
from ..scoring.business_value_score_engine import BusinessValueScoreEngine
from ..scoring.ats_score_engine import ATSScoreEngine

from ..predictors.seniority_predictor import SeniorityPredictor
from ..predictors.executive_predictor import ExecutivePredictor
from ..predictors.career_predictor import CareerPredictor


class ProfileBuilder:

    def __init__(self):

        self.reasoner = CapabilityReasoner()

        self.builder = GenericEvidenceBuilder()

        self.domain_engine = DomainScoreEngine()
        self.technical_engine = TechnicalScoreEngine()
        self.leadership_engine = LeadershipScoreEngine()
        self.executive_engine = ExecutiveScoreEngine()
        self.business_engine = BusinessValueScoreEngine()
        self.ats_engine = ATSScoreEngine()

        self.seniority = SeniorityPredictor()
        self.executive = ExecutivePredictor()
        self.career = CareerPredictor()

    # -------------------------------------------------------------

    def build(

        self,

        graph,

    ):

        # ---------------------------------------------------------
        # Capability Reasoning
        # ---------------------------------------------------------

        capability_evidence = self.reasoner.reason(graph)

        # ---------------------------------------------------------
        # Evidence Objects
        # ---------------------------------------------------------

        domain = self.builder.build(
            capability_evidence,
            DOMAIN_MAPPING,
            DomainEvidence,
        )

        technical = self.builder.build(
            capability_evidence,
            TECHNICAL_MAPPING,
            TechnicalEvidence,
        )

        leadership = self.builder.build(
            capability_evidence,
            LEADERSHIP_MAPPING,
            LeadershipEvidence,
        )

        executive = self.builder.build(
            capability_evidence,
            EXECUTIVE_MAPPING,
            ExecutiveEvidence,
        )

        business = self.builder.build(
            capability_evidence,
            BUSINESS_VALUE_MAPPING,
            BusinessValueEvidence,
        )

        ats = self.builder.build(
            capability_evidence,
            ATS_MAPPING,
            ATSEvidence,
        )

        # ---------------------------------------------------------
        # Scores
        # ---------------------------------------------------------

        domain_score = self.domain_engine.score(domain)

        technical_score = self.technical_engine.score(technical)

        leadership_score = self.leadership_engine.score(leadership)

        executive_score = self.executive_engine.score(executive)

        business_score = self.business_engine.score(business)

        ats_score = self.ats_engine.score(ats)

        # ---------------------------------------------------------
        # Predictors
        # ---------------------------------------------------------

        seniority = self.seniority.predict(
            leadership_score,
            executive_score,
            business_score,
        )

        executive_ready = self.executive.predict(
            executive_score,
            leadership_score,
            business_score,
        )

        career = self.career.predict(
            domain_score,
            technical_score,
            leadership_score,
            executive_score,
            business_score,
        )

        # ---------------------------------------------------------
        # Final Profile
        # ---------------------------------------------------------

        return SummaryProfile(

            domain_score=domain_score,

            technical_score=technical_score,

            leadership_score=leadership_score,

            executive_score=executive_score,

            business_value_score=business_score,

            ats_score=ats_score,

            seniority=seniority,

            executive_readiness=executive_ready,

            career_level=career,

        )