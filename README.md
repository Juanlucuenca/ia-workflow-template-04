# AI Template — Clase 04 - Programacion Asistida por IAs

Materiales de clase y una app TEMPLATE para **"Principios del Desarrollo Ágil con IA: Escala tu Productividad con Agentes de Código"**.

Este repo empaqueta un TEMPLATE para aplicar el flujo completa de cómo construir software con un enfoque AI-first:

- **La metodología** — el concepto de capa de IA, el loop PIV, y las reglas que se componen con el tiempo
- **Una capa de IA portable** — comandos y skills que podés dropper en cualquier proyecto hoy
- **Una app demo viva** — un template full-stack React + FastAPI usado como canvas para el flujo de desarrollo con IA

---

## La Metodología

### La Capa de IA — Tu Segundo Repositorio

Todo codebase ahora tiene dos capas: el código en sí, y la capa de IA — todo el contexto que le dice a tu agente cómo trabajar en tu proyecto.

Tres componentes:

- **Reglas globales (`AGENT.md`)** — siempre cargadas. Stack tecnológico, patrones de código, estándares de testing, comandos de deploy. Mantenerlas ajustadas.
- **Contexto bajo demanda** — docs de referencia, guías de estilo, patrones de API. Se cargan solo cuando son relevantes para no inflar cada sesión.
- **Comandos y skills** — flujos de trabajo empaquetados y reutilizables. `/create-prd`, `/prime`, `/plan`, `/implement`. Acá es donde estandarizás cómo construye tu equipo.

Cuando la carpeta `.agents/` está en source control junto con el código, las mejoras de IA funcionan exactamente como las mejoras de código: pull requests, revisiones, y todo el equipo se beneficia.

---

### El Loop PIV — Planificar, Implementar, Validar

La metodología central para un desarrollo asistido por IA confiable y repetible.

**Planificar.** `/prime` carga el contexto (ticket de Jira, árbol del codebase, git log reciente, etc.). Luego `/plan` produce un plan estructurado con una estrategia de validación incorporada — antes de escribir una sola línea de código. Los sub-agentes hacen investigación paralela, pero nunca implementación.

**Implementar.** Reset de contexto, luego `/implement` ejecuta el plan en una ventana fresca. El plan es todo lo que el agente necesita.

**Validar.** Una pirámide de cinco capas:

```
Capa 5: Testing manual              ← Vos (golden path + casos borde)
Capa 4: Revisión de código          ← Vos (con asistencia de IA)
Capa 3: Integración / E2E           ← Agente + automatización de browser
Capa 2: Tests unitarios             ← Agente, itera
Capa 1: Type checking + linting     ← Agente, itera
```

El objetivo es empujar la línea entre las capas 3 y 4 lo más abajo posible.

---

### Las Cinco Reglas de Oro

1. **Convertí todo en comando.** Si escribís algo más de dos veces, debe ser un comando. Reutilizable, compartible, evolucionable.
2. **Reducí las suposiciones.** Preguntas antes del PRD. Revisá el PRD antes de las historias. Revisá el plan antes de ejecutar. Lo más peligroso en el desarrollo con IA no es que el modelo se equivoque — es que el modelo asuma. Cada pregunta que hace es una suposición que no está haciendo.
3. **El contexto es rey.** Reset entre planificación e implementación. Sub-agentes solo para investigación. Contexto bajo demanda en lugar de un `AGENT.md` inflado.
4. **El git log es memoria.** Comiteá frecuentemente y con mensajes descriptivos. Tu agente lee este historial en cada `/prime`.
5. **El sistema evoluciona.** Cada bug que comete tu agente es una oportunidad de mejorar la capa de IA para que nunca vuelva a cometer ese error. Tu sistema se compone.

---

## Qué Hay en Este Repo

```
.agents/
├── AGENT.md                   # Reglas del proyecto para el agente
├── commands/                   # Flujos de trabajo reutilizables
│   ├── prime, prime-server, prime-client, prime-endpoint, prime-components
│   ├── create-prd, prd-interactive, create-rules
│   ├── create-stories
│   ├── plan, implement
│   ├── validate, review, security-review
│   └── install
└── skills/                     # Skills especializadas (browser, etc.)

frontend/                       # SPA en React 19 + Vite
backend/                        # API REST en FastAPI
```

---

## Referencia de Comandos

| Comando | Propósito |
|---------|-----------|
| `/install` | Instalar dependencias e iniciar servidores |
| `/prime` | Cargar contexto del codebase para planificar |
| `/prime-server` | Contexto enfocado en el backend |
| `/prime-client` | Contexto enfocado en el frontend |
| `/prime-endpoint` | Aprender cómo construir nuevos endpoints |
| `/prime-components` | Aprender cómo construir componentes |
| `/create-rules` | Generar o actualizar `AGENT.md` para un nuevo codebase |
| `/create-prd` | Generar un PRD desde un brain dump |
| `/prd-interactive` | Generación de PRD paso a paso |
| `/create-stories` | Convertir un PRD en historias de usuario |
| `/plan` | Producir un plan de implementación detallado con estrategia de validación |
| `/implement` | Ejecutar un plan en una ventana de contexto fresca |
| `/validate` | Correr lint + type check + tests, reportar fallas |
| `/review` | Revisión de código para PRs |
| `/security-review` | Revisión de seguridad de los cambios pendientes |

---

## La App Demo

Un template full-stack deliberadamente simple que sirve de canvas para el flujo de trabajo PIV. El punto de partida tiene lo mínimo indispensable — la clase agrega funcionalidades en vivo usando los comandos de arriba.

**Stack:** React 19, Vite, React Router 7, Tailwind CSS v4, shadcn/ui, FastAPI, SQLAlchemy 2.x, SQLite, Pydantic v2.

### Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload    # http://localhost:8000

# Frontend (en otra terminal)
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

Sin Docker. Sin servicios externos. Sin auth.

### Comandos

```bash
# Frontend (desde frontend/)
npm run dev        # Servidor de desarrollo
npm run build      # Build de producción
npm run lint       # ESLint
npm run preview    # Vista previa del build

# Backend (desde backend/)
uvicorn app.main:app --reload    # Servidor de desarrollo
curl http://localhost:8000/health
# Swagger UI: http://localhost:8000/docs
```

### Arquitectura

El backend sigue un patrón en capas por recurso — seguir el módulo `pais` como referencia:

```
backend/app/
├── models/        # Modelos ORM
├── schemas/       # Validación con Pydantic
├── repositories/  # Consultas a la DB (sin lógica de negocio)
├── services/      # Lógica de negocio
└── routers/       # Endpoints HTTP
```

Para patrones de frontend, routing y componentes: `frontend/AGENT.md`.  
Para arquitectura del backend y el patrón de recursos: `backend/AGENT.md`.

---

## Usar Esta Capa de IA en Tu Propio Proyecto

La carpeta `.agents/` es portable. Para adoptarla:

1. Copiar `.agents/` a tu repo
2. Correr `/create-rules` para generar un `AGENT.md` ajustado a tu stack
3. Empezar con `/prime`, luego un brain dump en `/create-prd`, luego `/plan`, luego `/implement`

El estándar de tu equipo para cómo construye está ahora en source control y es revisable.
