"""Application constants."""

# SDG (Sustainable Development Goals) descriptions
SDG_DESCRIPTIONS = {
    "SDG_1": "Fin de la pobreza - Poner fin a la pobreza en todas sus formas en todo el mundo",
    "SDG_2": "Hambre cero - Poner fin al hambre, lograr la seguridad alimentaria y la mejora de la nutrición",
    "SDG_3": "Salud y bienestar - Garantizar una vida sana y promover el bienestar para todos",
    "SDG_4": "Educación de calidad - Garantizar una educación inclusiva, equitativa y de calidad",
    "SDG_5": "Igualdad de género - Lograr la igualdad entre los géneros y empoderar a todas las mujeres y niñas",
    "SDG_6": "Agua limpia y saneamiento - Garantizar la disponibilidad de agua y su gestión sostenible",
    "SDG_7": "Energía asequible y no contaminante - Garantizar el acceso a una energía asequible, segura y sostenible",
    "SDG_8": "Trabajo decente y crecimiento económico - Promover el crecimiento económico sostenido e inclusivo",
    "SDG_9": "Industria, innovación e infraestructura - Construir infraestructuras resilientes y promover la innovación",
    "SDG_10": "Reducción de las desigualdades - Reducir la desigualdad en y entre los países",
    "SDG_11": "Ciudades y comunidades sostenibles - Lograr que las ciudades sean más inclusivas y sostenibles",
    "SDG_12": "Producción y consumo responsables - Garantizar modalidades de consumo y producción sostenibles",
    "SDG_13": "Acción por el clima - Adoptar medidas urgentes para combatir el cambio climático",
    "SDG_14": "Vida submarina - Conservar y utilizar sosteniblemente los océanos y recursos marinos",
    "SDG_15": "Vida de ecosistemas terrestres - Gestionar sosteniblemente los bosques y detener la pérdida de biodiversidad",
    "SDG_16": "Paz, justicia e instituciones sólidas - Promover sociedades justas, pacíficas e inclusivas",
    "SDG_17": "Alianzas para lograr los objetivos - Revitalizar la Alianza Mundial para el Desarrollo Sostenible"
}


def get_sdg_description(sdg_code: str) -> str:
    """Get the description for a specific SDG code."""
    return SDG_DESCRIPTIONS.get(sdg_code, f"Descripción no disponible para {sdg_code}")


def get_all_sdgs_with_descriptions() -> dict:
    """Get all SDG codes with their descriptions."""
    return SDG_DESCRIPTIONS.copy()
# Core module for application configuration and constants

