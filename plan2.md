# Grupo 4 — Plan de Presentación: Gestión de Pruebas con Kiwi TCMS

## Objetivo

Mostrar cómo Kiwi TCMS resuelve el problema de **gestionar el proceso de testing** — no ejecutar tests, sino controlar qué se probó, quién, contra qué build, y qué evidencia queda. La demo recorre el ciclo completo: planificación → casos → ejecución → automatización → reporte.

## Requisitos del curso y cómo se cubren

| Requisito | Cómo se cumple |
|---|---|
| Demo en vivo, 10–15 min | `demo2.md`, cronometrado por bloques |
| Participación de todos | 5 expositores, ~2.5 min cada uno, cada uno con acciones en vivo |
| Aim, key features, benefits | Bloque 1 (aim), bloques 2–4 (features), bloque 5 (benefits) |
| Tipo asignado: gestión de pruebas | Toda la narrativa es gestión: qué se prueba, quién, contra qué build, qué evidencia queda |
| Repo público + README | Compose + seed por API + SUT + importador de resultados |

**Trampa a evitar:** Kiwi TCMS también integra con bug trackers, tiene reportes e ingesta de automatización. Cada feature debe aterrizar en una pregunta de gestión, no en "mira, habla con GitHub".

## Glosario que los expositores deben explicar

Los expositores deben familiarizarse con estos conceptos antes de presentar:

- **Build**: construcción específica del software para testing. Un build nuevo = cambios en el código que hay que verificar.
- **Test Case**: escenario verificable con pasos y resultado esperado. Es reutilizable entre planes y versiones.
- **Test Plan**: estrategia de testing para una versión: qué casos, qué prioridades, criterios de salida.
- **Test Run**: ejecución concreta de un plan contra un build, con resultados registrados.
- **Test Execution**: cada resultado individual dentro de un run: caso + estado + tester + build.
- **Gestión de pruebas**: control del proceso de testing, no ejecución de tests.

## Reparto (5 personas)

| Bloque | Quién | Tiempo | Qué hace en vivo |
|---|---|---|---|
| 1. Problema + qué es gestión de pruebas | E1 | 0:00–2:00 | Presenta el problema sin abrir la herramienta |
| 2. Jerarquía Product → Version → Build → Plan | E2 | 2:00–4:30 | Navega la estructura en el navegador |
| 3. Crear caso + ver historial | E3 | 4:30–7:00 | **Crea un caso en vivo** y muestra el historial |
| 4. Ejecución manual + defecto | E4 | 7:00–9:30 | **Ejecuta la corrida**, falla uno, adjunta defecto |
| 5. Automatización + reportes + cierre | E5 | 9:30–12:00 | **Corre pytest y el importador**, muestra Telemetry |

Cada expositor habla ~2.5 minutos y tiene al menos una acción en pantalla.

## Estado verificado del repo

Todo el flujo se probó contra una instancia real de `kiwitcms/kiwi:latest`:

- `docker compose up -d` + `manage.py migrate` + `createsuperuser` → instancia en **https://localhost:8443**
- `seed/seed_demo.py` → crea classification, producto, versión 1.2, build-45, plan de regresión, 6 casos y la corrida manual con todo en IDLE
- `pytest --junitxml=junit.xml` → **4 passed, 1 failed** (defecto intencional en `app/auth.py`)
- `automation/report_results.py junit.xml` → crea la corrida automatizada y publica PASSED/PASSED/PASSED/PASSED/FAILED

## Checklist 30 minutos antes

1. `docker compose up -d` y esperar a que responda `https://localhost:8443`.
2. Correr el seed. Verificar que la corrida manual esté con **todo en IDLE** (si ya la ejecutaste ensayando, borra la corrida y vuelve a crearla).
3. `set -a; source .env; set +a` en **todas** las terminales que vayas a usar.
4. Aceptar el aviso de certificado autofirmado en el navegador **antes** de exponer.
5. Abrir en orden las pestañas: dashboard, plan, corrida manual, Telemetry.
6. Zoom del navegador a 125–150%. Fuente de la terminal grande.
7. Tener `docs/snippets.md` abierto en otra ventana para copiar/pegar.
8. Grabar un video de respaldo del flujo completo.

## Control de riesgo

- Cronómetro visible para los cinco; corte duro al terminar cada bloque.
- Nada de teclear textos largos en vivo: todo se pega desde `docs/snippets.md`.
- Si algo falla en vivo: "tenemos esto grabado", pasas al video y sigues hablando. **No depures en escena.**
- La integración con GitHub/JIRA es opcional y depende de red externa. Si no la configuras con token antes, en el bloque 4 adjunta el defecto como enlace en la pestaña Bugs y menciona la integración como capacidad — no la intentes en vivo sin haberla probado.

## Mejora opcional si sobra tiempo

Arreglar el defecto de `app/auth.py` (cambiar `> PASSWORD_MAX_AGE_DAYS + 1` por `> PASSWORD_MAX_AGE_DAYS`), crear `build-46` y volver a importar: Telemetry muestra entonces una tendencia de dos builds, que es la evidencia más vendedora del bloque 5.
