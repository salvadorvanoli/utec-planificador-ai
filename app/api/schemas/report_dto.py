from pydantic import BaseModel
from typing import Dict, List, Any

class EstadisticasCursoDTO(BaseModel):
    procesosCognitivos: Dict[str, int] = {}
    competenciasTransversales: Dict[str, int] = {}
    modalidades: Dict[str, int] = {}
    estrategiasDeEnseñanza: Dict[str, int] = {}
    recursosMasUtilizados: List[str] = []
    ODSvinculados: Dict[str, int] = {}
    promedioDuracionActividadesMin: int = 0
    totalSemanas: int = 0
    totalHorasPresenciales: int = 0
    totalHorasVirtuales: int = 0

class ReportRequest(BaseModel):
    course_id: str
    estadisticas: EstadisticasCursoDTO

class ReportResponse(BaseModel):
    success: bool = True
    reporte: Dict = {}
    recomendaciones: List[str] = []
    calificacion_general: str = ""
