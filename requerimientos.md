Documento de requerimientos
Planificador Docente con Agente de IA - UTEC
Acta de Reunión y Análisis de requerimientos
Versión 1.3
Autores: Joaquín Jozami, Salvador Vanoli, Valentín Veintemilla
Tutor: Nicolás Escobar
7 de septiembre de 2025
Índice general
Historia de revisiones 2
Historia de reuniones 3
1. Reuniones 4
1.1. Reunión 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.1.1. Objetivos de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.1.2. Temas de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.2. Reunión 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.2.1. Objetivos de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.2.2. Temas de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3. Reunión 3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
1.3.1. Objetivos de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . 6
1.3.2. Temas de la reunión . . . . . . . . . . . . . . . . . . . . . . . . . . 6
2. Requerimientos 8
2.1. Requerimientos funcionales . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
2.1.1. Gestión de usuarios y roles . . . . . . . . . . . . . . . . . . . . . . . 8
2.1.2. Planificador docente . . . . . . . . . . . . . . . . . . . . . . . . . . 8
2.1.3. Asistente pedagógico (Agente de IA) . . . . . . . . . . . . . . . . . 9
2.1.4. Panel estadístico y reportes . . . . . . . . . . . . . . . . . . . . . . 10
2.1.5. Integración . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.2. Requerimientos no funcionales . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.2.1. Usabilidad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.2.2. Rendimiento y escalabilidad . . . . . . . . . . . . . . . . . . . . . . 10
2.2.3. Seguridad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
2.2.4. Compatibilidad y accesibilidad . . . . . . . . . . . . . . . . . . . . . 11
2.2.5. Disponibilidad y confiabilidad . . . . . . . . . . . . . . . . . . . . . 11
2.2.6. Mantenibilidad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
1
Historia de revisiones
Fecha
(dd/mm/yyyy)
Versión Descripción Autor
15/08/2025 1.0 Primera revisión Grupo N°2
21/08/2025 1.1 Agregados requerimientos no funcionales Grupo N°2
28/08/2025 1.2 Normas APA, indexado numérico Grupo N°2
07/09/2025 1.3 Agregado índice, historias, reformulado requerimientos, agregadas descripciones de
reuniones
Grupo N°2
2
Historia de reuniones
Fecha
(dd/mm/yyyy)
Responsables Participantes
15/08/2025 Joaquín Jozami, Salvador Vanoli, Valentin
Veintemilla
Pablo Tambasco
29/08/2025 Joaquín Jozami, Salvador Vanoli, Valentin
Veintemilla
Pablo Tambasco
05/09/2025 Joaquín Jozami, Salvador Vanoli, Valentin
Veintemilla
Pablo Tambasco
3
Capítulo 1
Reuniones
1.1. Reunión 1
1.1.1. Objetivos de la reunión
Presentar el proyecto de planificador docente, entender la problemática actual, recopilar requisitos iniciales y alinear expectativas con el cliente.
1.1.2. Temas de la reunión
Situación actual
Los docentes utilizan un Excel para planificar cursos. Resulta en trabajo duplicado,
poca aceptación y baja adopción.
Se necesita centralizar y sistematizar la información de planificación.
Objetivos del proyecto
Desarrollar un planificador digital accesible.
Permitir carga semanal de contenidos, modalidades, recursos y enfoques educativos.
Generar reportes y estadísticas centralizadas.
Incluir un asistente pedagógico con IA1 para sugerencias y detección de problemas.
Persistencia de datos históricos y reutilización de recursos.
Integraciones necesarias
Se nos aclaró que en un primer momento no necesita estar integrado a plataformas
como Moodle.
Será necesario consumir y guardar datos sensibles dentro de la base de datos de
UTEC.
1
IA: Inteligencia Artificial.
4
Ideas complementarias
Aportamos ideas que puedan aportar al proyecto, como plantillas para no repetir
trabajo y accesos rápidos.
Preguntas y dudas
Ronda de dudas y preguntas sobre el proyecto.
1.2. Reunión 2
1.2.1. Objetivos de la reunión
Revisar y profundizar en los requisitos discutidos en la reunión anterior, definir roles de usuario con mayor precisión y acordar próximos entregables de documentación y
prototipos.
1.2.2. Temas de la reunión
Roles y accesos
Docente
Secretarios
Coordinadores
Responsables de educación
Registro e integración
Usuarios se registran mediante correo institucional UTEC.
Creación de cuentas de profesores gestionada por secretaría/analistas/responsables
de educación.
Funcionalidad de IA
Discusión abierta:
¿La IA debe sugerir de forma proactiva o solo cuando el docente la consulte?
Se busca clarificar la modalidad de interacción en próximos encuentros.
Histórico de datos
Existirá un histórico de planificaciones pasadas.
Cambios realizados durante el año se registran en un log de modificaciones.
5
Requerimientos adicionales
Botón para generar reporte basado en estadísticas.
Descarga de planificaciones a PDF.
Recursos y próximos pasos
Pendiente reunión con UTEC para definir recursos disponibles (cloud, infraestructura).
Solicitud al cliente de validar la lista de requisitos recopilada.
Preparar un resumen/presentación para la próxima semana con: especificaciones
generales del sistema y bosquejos de interfaz de usuario (Moqups2
).
1.3. Reunión 3
1.3.1. Objetivos de la reunión
Validar las interfaces diseñadas y la lista de requerimientos con el cliente. Aclarar
dudas sobre secciones editables del planificador, roles de usuarios, calendario académico
y gestión de permisos.
1.3.2. Temas de la reunión
Presentación
Durante la primera mitad de la reunión se presentó la propuesta de interfaces y
requerimientos del sistema, con el objetivo de obtener la validación del cliente.
La segunda parte se destinó a preguntas, aclaraciones y nuevas definiciones.
Planificador docente
Aclaración de secciones modificables y no modificables por el docente.
Importancia de definir el SCP3 antes de comenzar la cursada.
Calendario académico
Pregunta sobre si los semestres son iguales en todas las carreras y sedes.
Se identificó la necesidad de manejar casos donde una cursada comienza más tarde.
El Superusuario deberá cargar el calendario anual.
El docente podrá modificar las semanas según necesidades particulares.
2https://moqups.com/
3Sistema de calificación. Documento de referencia: https://utec.edu.uy/uploads/documento/
f1e4666a692bfe32a9a94d626f7eaea8b314b533.pdf.
6
Roles y permisos
Debe existir un superusuario con capacidad de asignar roles (coordinadores, docentes, etc.) y gestionar cursos.
Aún pendiente definir si será una serie de superusuarios para toda UTEC o si habrá
uno por sede (a coordinar con infraestructura).
Tema permisos: se debe definir si el sistema tendrá su propia gestión de permisos o
si debe integrarse con uno ya existente. Muchas solicitudes de permisos se gestionan
actualmente con infraestructura.
Escalabilidad
Pendiente definir con infraestructura el número de usuarios concurrentes que debe
soportar el sistema.
Sugerencias
Incorporar la posibilidad de descargar un PDF con los datos del panel estadístico,
incluyendo la información aportada por el asistente pedagógico (EduBot).
Acuerdos
La descripción de la unidad curricular será responsabilidad del docente.
Existirá un superusuario encargado de roles y calendario anual (modalidad a definir
con infraestructura).
El sistema deberá registrar modificaciones en los campos sensibles (ej. SCP) y
asignar responsabilidad al usuario que los cambie.
Próximos pasos
Coordinar con infraestructura.
7
Capítulo 2
Requerimientos
2.1. Requerimientos funcionales
2.1.1. Gestión de usuarios y roles
RF-2.1.1.1 El sistema deberá permitir el registro y autenticación de usuarios usando el correo institucional.
RF-2.1.1.2 El sistema deberá permitir el acceso de secretarios, coordinadores y
responsables de educación para cargar perfiles de docentes y cursos asignados.
RF-2.1.1.3 El sistema deberá permitir a coordinadores y responsables de educación acceder a toda la información y monitores.
RF-2.1.1.4 El sistema deberá permitir a los estudiantes acceder y descargar planillas simplificadas con la planificación del curso, sin necesidad de logueo.
RF-2.1.1.5 El sistema deberá diferenciar los permisos de acceso según las funcionalidades. Los roles de usuario tendrán un conjunto de estos permisos de funcionalidad.
RF-2.1.1.6 Será necesaria la existencia de un super usuario con permisos para
crear unidades curriculares y semestres, además de poder asignar roles. Este super
usuario podrá realizar todas estas acciones en un solo ITR1
.
2.1.2. Planificador docente
RF-2.1.2.1 El docente deberá poder crear y actualizar un plan de estudio para
cada curso asignado.
RF-2.1.2.2 El planificador deberá permitir que el docente especifique, para cada
clase o semana, la siguiente información:
• Datos temporales: semana y fecha.
• Contenidos programáticos y secuencia de actividades.
◦ Para cada actividad a su vez, se especificará:
1
ITR: Institutos Tecnológicos Regionales; sedes de la Universidad UTEC.
8
⋄ Procesos cognitivos vinculados.
⋄ Competencias transversales vinculadas.
⋄ Estrategia de enseñanza utilizada.
⋄ Recursos.
⋄ Descripción.
⋄ Duración en minutos.
⋄ Modalidad.
⋄ Contenido programático vinculado.
• Recursos y bibliografía.
Además, podrá especificar para la cursada en general:
• Descripción.
• Objetivos de Desarrollo Sostenible2 vinculados.
• Principios del diseño universal del aprendizaje.
• Horas virtuales y presenciales.
• Si se realizan actividades de vinculación con el medio/sector productivo y si
está vinculado a líneas de investigación.
• Sistema de Calificación (SCP).
RF-2.1.2.3 El sistema deberá permitir reutilizar recursos y planificaciones de cursos pasados.
RF-2.1.2.4 El sistema deberá permitir descargar la planificación en PDF con la
información de interés a cada tipo de usuario.
RF-2.1.2.5 El planificador deberá almacenar la información en una base de datos
con persistencia histórica.
RF-2.1.2.6 El sistema deberá registrar los cambios realizados a la planificación
posterior al inicio de la cursada.
RF-2.1.2.7 El sistema deberá permitir compartir la planificación con otros docentes, permitiéndoles colaborar.
2.1.3. Asistente pedagógico (Agente de IA)
RF-2.1.3.1 El sistema deberá incluir un agente de IA nutrido con contenido educativo y buenas prácticas.
RF-2.1.3.2 El agente deberá brindar sugerencias de mejora a partir de las planificaciones cargadas.
RF-2.1.3.3 El agente deberá detectar inconsistencias pedagógicas.
RF-2.1.3.4 El agente deberá acceder a reportes y estadísticas.
2Documento de referencia ODS: https://utec.edu.uy/uploads/documento/
c2e22b59e99bcc5cbadef100414327045a5bc82f.pdf.
9
RF-2.1.3.5 El agente deberá responder consultas de los docentes mediante un
chatbot3
.
RF-2.1.3.6 El agente deberá ofrecer la posibilidad de generar reportes estadísticos.
2.1.4. Panel estadístico y reportes
RF-2.1.4.1 El sistema deberá ofrecer la posibilidad de generar reportes en base a
la planificación y los datos estadísticos.
RF-2.1.4.2 El sistema deberá permitir la visualización de estadísticas por materia
para profesores y por carrera para coordinadores y responsables de educación.
RF-2.1.4.3 El sistema deberá incluir gráficas sobre competencias, procesos cognitivos, modalidades de las actividades y recursos.
RF-2.1.4.4 El sistema deberá permitir filtrar información.
RF-2.1.4.5 El sistema deberá permitir descargar las estadísticas como PDF.
2.1.5. Integración
RF-2.1.5.1 El sistema deberá integrarse con bases de datos de UTEC.
RF-2.1.5.2 El sistema deberá permitir la carga automática de datos desde transcripciones de clases (opcional).
2.2. Requerimientos no funcionales
2.2.1. Usabilidad
RNF-2.2.1.1 El sistema deberá ofrecer una interfaz intuitiva y accesible para
docentes.
RNF-2.2.1.2 El planificador deberá ofrecer plantillas prediseñadas.
RNF-2.2.1.3 El sistema deberá estar disponible en idioma español (es-UY).
RNF-2.2.1.4 El sistema deberá cumplir con los estándares gráficos institucionales
de UTEC (paleta de colores, tipografía, logos y lineamientos de diseño oficial4
).
2.2.2. Rendimiento y escalabilidad
RNF-2.2.2.1 El sistema deberá soportar al menos 200 docentes simultáneos.
RNF-2.2.2.2 El sistema deberá tener un tiempo de respuesta inferior a 5 segundos.
RNF-2.2.2.3 El sistema deberá contar con una arquitectura escalable.
3Programa de software que simula conversaciones con usuarios para brindar información o asistencia
automática.
4Guía de identidad UTEC: https://utec.edu.uy/uploads/documento/
82a36430707aab6fe708f8fbdf9497a1723251db.pdf
10
2.2.3. Seguridad
RNF-2.2.3.1 El sistema deberá ofrecer autenticación segura con el correo institucional.
RNF-2.2.3.2 El sistema deberá cifrar la información sensible en la base de datos.
RNF-2.2.3.3 El sistema deberá restringir el acceso por funcionalidad y rol.
2.2.4. Compatibilidad y accesibilidad
RNF-2.2.4.1 El sistema deberá ser accesible desde navegadores modernos.
RNF-2.2.4.2 El sistema deberá cumplir con la norma WCAG 2.1 AA5
.
RNF-2.2.4.3 El sistema deberá ser accesible desde dispositivos móviles en modalidad AWP6
(opcional).
2.2.5. Disponibilidad y confiabilidad
RNF-2.2.5.1 El sistema deberá garantizar una disponibilidad mínima del 95 % en
inicios de períodos lectivos.
RNF-2.2.5.2 El sistema deberá realizar copias de seguridad automáticas y contar
con mecanismos de recuperación ante fallos.
2.2.6. Mantenibilidad
RNF-2.2.6.1 El sistema deberá contar con documentación de arquitectura y APIs7
.
RNF-2.2.6.2 El sistema deberá tener tests automáticos integrativos integrados
con GitHub Actions.
RNF-2.2.6.3 El sistema deberá seguir buenas prácticas de desarrollo y centralizar
el código en un repositorio.
5https://www.w3.org/TR/WCAG21/
6Aplicación Web Progresiva: es una aplicación web que combina lo mejor de los sitios web y las apps
nativas, ofreciendo funcionalidades como uso offline, notificaciones y acceso desde la pantalla de inicio del
dispositivo.
7API: conjunto de reglas y protocolos que permite que diferentes aplicaciones se comuniquen e intercambien datos entre sí.
11