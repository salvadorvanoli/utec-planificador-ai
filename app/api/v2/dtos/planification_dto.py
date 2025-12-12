from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

# ==================== ENUMS ====================

class ShiftEnum(str, Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"

class DeliveryFormatEnum(str, Enum):
    IN_PERSON = "IN_PERSON"
    VIRTUAL = "VIRTUAL"
    HYBRID = "HYBRID"

class PartialGradingSystemEnum(str, Enum):
    PGS_1 = "PGS_1"
    PGS_2 = "PGS_2"
    PGS_3 = "PGS_3"
    PGS_4 = "PGS_4"
    PGS_5 = "PGS_5"
    PGS_6 = "PGS_6"
    PGS_7 = "PGS_7"
    PGS_8 = "PGS_8"
    PGS_9 = "PGS_9"
    PGS_10 = "PGS_10"
    PGS_11 = "PGS_11"
    PGS_12 = "PGS_12"

class SustainableDevelopmentGoalEnum(str, Enum):
    SDG_1 = "SDG_1"
    SDG_2 = "SDG_2"
    SDG_3 = "SDG_3"
    SDG_4 = "SDG_4"
    SDG_5 = "SDG_5"
    SDG_6 = "SDG_6"
    SDG_7 = "SDG_7"
    SDG_8 = "SDG_8"
    SDG_9 = "SDG_9"
    SDG_10 = "SDG_10"
    SDG_11 = "SDG_11"
    SDG_12 = "SDG_12"
    SDG_13 = "SDG_13"
    SDG_14 = "SDG_14"
    SDG_15 = "SDG_15"
    SDG_16 = "SDG_16"
    SDG_17 = "SDG_17"

class UniversalDesignLearningPrincipleEnum(str, Enum):
    MEANS_OF_ENGAGEMENT = "MEANS_OF_ENGAGEMENT"
    MEANS_OF_REPRESENTATION = "MEANS_OF_REPRESENTATION"
    MEANS_OF_ACTION_EXPRESSION = "MEANS_OF_ACTION_EXPRESSION"
    NONE = "NONE"

class CognitiveProcessEnum(str, Enum):
    REMEMBER = "REMEMBER"
    UNDERSTAND = "UNDERSTAND"
    APPLY = "APPLY"
    ANALYZE = "ANALYZE"
    EVALUATE = "EVALUATE"
    CREATE = "CREATE"
    NOT_DETERMINED = "NOT_DETERMINED"

class TransversalCompetencyEnum(str, Enum):
    COMMUNICATION = "COMMUNICATION"
    TEAMWORK = "TEAMWORK"
    LEARNING_SELF_REGULATION = "LEARNING_SELF_REGULATION"
    CRITICAL_THINKING = "CRITICAL_THINKING"
    NOT_DETERMINED = "NOT_DETERMINED"

class LearningModalityEnum(str, Enum):
    VIRTUAL = "VIRTUAL"
    IN_PERSON = "IN_PERSON"
    SIMULTANEOUS_IN_PERSON_VIRTUAL = "SIMULTANEOUS_IN_PERSON_VIRTUAL"
    AUTONOMOUS = "AUTONOMOUS"
    NOT_DETERMINED = "NOT_DETERMINED"

class TeachingStrategyEnum(str, Enum):
    LECTURE = "LECTURE"
    DEBATE = "DEBATE"
    TEAMWORK = "TEAMWORK"
    FIELD_ACTIVITY = "FIELD_ACTIVITY"
    PRACTICAL_ACTIVITY = "PRACTICAL_ACTIVITY"
    LABORATORY_PRACTICES = "LABORATORY_PRACTICES"
    TESTS = "TESTS"
    RESEARCH_ACTIVITIES = "RESEARCH_ACTIVITIES"
    FLIPPED_CLASSROOM = "FLIPPED_CLASSROOM"
    DISCUSSION = "DISCUSSION"
    SMALL_GROUP_TUTORIALS = "SMALL_GROUP_TUTORIALS"
    PROJECTS = "PROJECTS"
    CASE_STUDY = "CASE_STUDY"
    OTHER = "OTHER"
    NOT_DETERMINED = "NOT_DETERMINED"

class LearningResourceEnum(str, Enum):
    EXHIBITION = "EXHIBITION"
    BOOK_DOCUMENT = "BOOK_DOCUMENT"
    DEMONSTRATION = "DEMONSTRATION"
    WHITEBOARD = "WHITEBOARD"
    ONLINE_COLLABORATION_TOOL = "ONLINE_COLLABORATION_TOOL"
    ONLINE_LECTURE = "ONLINE_LECTURE"
    ONLINE_FORUM = "ONLINE_FORUM"
    ONLINE_EVALUATION = "ONLINE_EVALUATION"
    GAME = "GAME"
    SURVEY = "SURVEY"
    VIDEO = "VIDEO"
    INFOGRAPHIC = "INFOGRAPHIC"
    WEBPAGE = "WEBPAGE"
    OTHER = "OTHER"
    NOT_DETERMINED = "NOT_DETERMINED"

class DomainAreaEnum(str, Enum):
    INSTALLATION_DESIGN = "INSTALLATION_DESIGN"
    INSTALLATION_MANAGEMENT = "INSTALLATION_MANAGEMENT"
    RDI_PROJECTS = "RDI_PROJECTS"
    SERVICE_MANAGEMENT = "SERVICE_MANAGEMENT"

class ProfessionalCompetencyEnum(str, Enum):
    TECHNICAL_ASSISTANCE = "TECHNICAL_ASSISTANCE"
    EFFICIENT_MANAGEMENT = "EFFICIENT_MANAGEMENT"
    MAINTENANCE_PLANNING = "MAINTENANCE_PLANNING"
    INSTITUTIONAL_ADVISORY = "INSTITUTIONAL_ADVISORY"
    PERSONNEL_TRAINING = "PERSONNEL_TRAINING"
    COMPLIANCE_VERIFICATION = "COMPLIANCE_VERIFICATION"
    PROJECT_DESIGN_MANAGEMENT = "PROJECT_DESIGN_MANAGEMENT"
    DIRECTOR_ACTIVITIES = "DIRECTOR_ACTIVITIES"
    ESTABLISHMENT_MANAGEMENT = "ESTABLISHMENT_MANAGEMENT"

# ==================== DTOs ====================

class ActivityDTO(BaseModel):
    id: Optional[int] = None
    description: str
    durationInMinutes: int
    cognitiveProcesses: List[CognitiveProcessEnum] = []
    transversalCompetencies: List[TransversalCompetencyEnum] = []
    learningModality: LearningModalityEnum
    teachingStrategies: List[TeachingStrategyEnum] = []
    learningResources: List[LearningResourceEnum] = []

class ProgrammaticContentDTO(BaseModel):
    id: Optional[int] = None
    content: str
    activities: List[ActivityDTO] = []

class WeeklyPlanningDTO(BaseModel):
    id: Optional[int] = None
    weekNumber: int
    startDate: str
    bibliographicReferences: List[str] = []
    programmaticContents: List[ProgrammaticContentDTO] = []
    activities: List[ActivityDTO] = []

class ProgramDTO(BaseModel):
    id: Optional[int] = None
    name: str
    durationInTerms: int
    totalCredits: int

class TermDTO(BaseModel):
    id: Optional[int] = None
    number: int
    program: Optional[ProgramDTO] = None

class CurricularUnitDTO(BaseModel):
    id: Optional[int] = None
    name: str
    credits: int
    domainAreas: List[str] = []
    professionalCompetencies: List[str] = []
    term: Optional[TermDTO] = None

class CoursePlanningDTO(BaseModel):
    id: Optional[int] = None
    shift: ShiftEnum
    description: str
    startDate: str
    endDate: str
    partialGradingSystem: PartialGradingSystemEnum
    hoursPerDeliveryFormat: Dict[str, int] = {}
    isRelatedToInvestigation: bool = False
    involvesActivitiesWithProductiveSector: bool = False
    sustainableDevelopmentGoals: List[SustainableDevelopmentGoalEnum] = []
    universalDesignLearningPrinciples: List[UniversalDesignLearningPrincipleEnum] = []
    curricularUnit: Optional[CurricularUnitDTO] = None
    weeklyPlannings: List[WeeklyPlanningDTO] = []

class CoursePlanningRequestDTO(BaseModel):
    """Request DTO for course planning operations"""
    coursePlanning: CoursePlanningDTO

