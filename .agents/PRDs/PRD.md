# PRD - AI Data Analysis Platform (Sprint 1)

## 1. Executive Summary
Esta aplicación es una herramienta de análisis de datos impulsada por IA que permite a los usuarios interactuar con bases de datos PostgreSQL mediante lenguaje natural. El sistema utiliza un agente inteligente (Pydantic-AI) para traducir consultas de usuario en SQL seguro, ejecutar las consultas y devolver análisis detallados. En este primer Sprint, nos centramos en la funcionalidad core: un chatbot con persistencia local y capacidades de introspección de base de datos.

## 2. Mission
Empoderar a los usuarios para extraer insights de sus bases de datos sin necesidad de escribir SQL, manteniendo una experiencia fluida, rápida y persistente localmente.

## 3. Target Users
- Analistas de datos que buscan agilizar consultas repetitivas.
- Desarrolladores que necesitan explorar esquemas de base de datos rápidamente.
- Usuarios técnicos que prefieren una interfaz conversacional para análisis exploratorio.

## 4. MVP Scope
### In Scope
- [x] Interfaz de Chatbot con renderizado Markdown.
- [x] Persistencia de sesiones en SQLite (historial de mensajes).
- [x] Agente Pydantic-AI integrado con OpenRouter.
- [x] Herramienta para listar tablas de PostgreSQL.
- [x] Herramienta para obtener metadata/esquemas de tablas relevantes.
- [x] Herramienta para ejecutar queries `SELECT` con límites de seguridad.
- [x] Manejo de errores y auto-corrección de queries SQL por el agente.

### Out of Scope
- [ ] Autenticación de usuarios (Login/Sign-up).
- [ ] Visualización de gráficos (Charts/Dashboards).
- [ ] Soporte para múltiples motores de DB (solo PostgreSQL para datos).
- [ ] Exportación de datos a CSV/Excel.

## 5. User Stories
- **As a user**, I want to see my previous conversations so I can continue my analysis where I left off.
- **As a user**, I want to ask "What tables are available?" so I can understand the data structure.
- **As a user**, I want to ask complex questions like "Who are the top 10 customers by sales?" and get a formatted answer.
- **As a user**, I want the agent to automatically fix small SQL errors so I don't have to worry about technical syntax.
- **As a user**, I want to see the results in a clean Markdown format for readability.

## 6. Core Architecture & Patterns
- **Backend:** FastAPI (Python) siguiendo el patrón Repository/Service.
- **Agent Framework:** Pydantic-AI para la orquestación del LLM y herramientas.
- **Frontend:** React (Vite) con una arquitectura de componentes modulares.
- **Persistence:** 
    - **SQLite:** Para metadatos de la aplicación y logs de conversación.
    - **PostgreSQL:** Base de datos externa para consultas de análisis.
- **Communication:** REST API para chat y gestión de sesiones.

## 7. Tools/Features (Agent Design)
- **`get_tables`**: Lista todas las tablas accesibles en la base de datos configurada.
- **`get_table_schema`**: Devuelve las columnas y tipos de datos de una tabla específica.
- **`execute_query`**: 
    - **Restricción:** Solo permite comandos `SELECT`.
    - **Seguridad:** Aplica un `LIMIT 50` forzado si el usuario o el agente no lo especifican.
    - **Reintentos:** Máximo 3-5 intentos de corrección en caso de error de sintaxis.

## 8. Technology Stack
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy (para SQLite y Postgres).
- **AI Stack:** Pydantic-AI, OpenRouter (LLM: e.g., GPT-4o o Claude 3.5 Sonnet).
- **Frontend:** React, Tailwind CSS, Lucide React (iconos), React Markdown.
- **Database:** PostgreSQL (Data), SQLite (App State).

## 9. Security & Configuration
- **Environment Variables:** Las credenciales de DB y API Keys de OpenRouter se manejan vía `.env`.
- **Query Safety:** El agente tiene un prompt de sistema estricto para evitar operaciones de escritura (`INSERT`, `UPDATE`, `DELETE`, `DROP`).
- **Local Scope:** La aplicación corre localmente sin exposición pública en el MVP.

## 10. API Specification
- `GET /sessions`: Lista todas las sesiones de chat guardadas.
- `POST /sessions`: Crea una nueva sesión.
- `GET /sessions/{id}/messages`: Recupera el historial de una sesión.
- `POST /chat`: Envía un mensaje al agente (incluye `session_id`).

## 11. Success Criteria
- [ ] El agente responde correctamente sobre la estructura de la DB el 100% de las veces.
- [ ] Las consultas SQL generadas son válidas para PostgreSQL.
- [ ] El historial de chat se mantiene tras recargar la página (vía SQLite).
- [ ] El tiempo de respuesta del agente (latencia) es aceptable para una experiencia fluida.

## 12. Implementation Phases
### Phase 1: Estructura de Datos y Backend (Core)
- Configuración de modelos SQLAlchemy para SQLite (Sesiones/Mensajes).
- Configuración de la conexión a PostgreSQL.
- Implementación de los endpoints básicos de sesión.

### Phase 2: El Agente Inteligente
- Integración de Pydantic-AI con OpenRouter.
- Implementación de las 3 herramientas básicas (`get_tables`, `schema`, `query`).
- Definición del System Prompt de análisis.

### Phase 3: Frontend y Chat UI
- Creación de la interfaz de chat interactiva.
- Integración con la API de sesiones y mensajes.
- Renderizado de Markdown para las respuestas del agente.

### Phase 4: Validación y Pulido
- Pruebas de auto-corrección de queries.
- Ajustes de estilo y manejo de estados de carga (loading states).

## 14. Risks & Mitigations
- **Riesgo:** Generación de queries SQL alucinatorias. **Mitigación:** Herramientas de introspección obligatorias antes de ejecutar queries.
- **Riesgo:** Exposición de datos sensibles. **Mitigación:** Acceso limitado a `SELECT` y uso de variables de entorno seguras.
- **Riesgo:** Consumo excesivo de tokens en OpenRouter. **Mitigación:** Límites de queries por interacción y truncado de resultados largos.

## 15. Appendix
- [Pydantic-AI Docs](https://ai.pydantic.dev/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenRouter API](https://openrouter.ai/docs)
