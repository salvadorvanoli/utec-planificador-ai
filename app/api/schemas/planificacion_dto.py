from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ActividadDTO(BaseModel):
    descripcion: str
    duracionMin: int
    modalidad: str
    estrategiaEnseñanza: str
    procesosCognitivos: List[str] = []
    competenciasTransversales: List[str] = []
    recursos: List[str] = []
    contenidoVinculado: Optional[str] = None

class SemanaDTO(BaseModel):
    semana: int
    fecha: str
    contenidosProgramaticos: str
    actividades: List[ActividadDTO] = []
    recursosYBibliografia: List[str] = []

class PlanificacionDocenteDTO(BaseModel):
    descripcionGeneral: str
    objetivosDesarrolloSostenibleVinculados: List[str] = []
    principiosDUA: List[str] = []
    horasPresenciales: int = 0
    horasVirtuales: int = 0
    vinculacionConSectorProductivo: bool = False
    vinculadoALineaDeInvestigacion: bool = False
    sistemaDeCalificacion: str = ""
    semanas: List[SemanaDTO] = []

class PlanificacionRequestDTO(BaseModel):
    course_id: Optional[str] = None
    planificacionDocente: PlanificacionDocenteDTO
