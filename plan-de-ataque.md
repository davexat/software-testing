# Group 4 — Test Management with Kiwi TCMS (plan, 2 expositores)

## 1. Qué exige el enunciado y cómo lo cubrimos

| Requisito | Cómo se cumple |
|---|---|
| Demo en vivo, 15 min, en inglés | `demo-script.md`, cronometrado por bloques |
| Participación equitativa | 2 expositores, ~7:15 cada uno, cada uno con acciones en vivo propias |
| Aim, key features, benefits | Bloque 1 (aim), bloques 2–4 (features), bloque 5 (benefits) |
| **Cómo la herramienta cumple su tipo asignado** | Toda la narrativa es gestión: qué se prueba, quién, contra qué build, en qué estado, dónde está la evidencia |
| Repo público + README reproducible | Este repo: compose + seed por API + SUT + importador de resultados |
| Slides (opcional) | 8–10 slides, capturas, sin párrafos |
| Sin informe escrito | No se entrega documento |

**Trampa a evitar:** Kiwi TCMS también hace integración con bug trackers, reportes e ingesta de automatización. No derives a "mira, habla con GitHub". Cada feature debe aterrizar en una pregunta de gestión.

## 2. Tesis (repetir 3 veces)

> La gestión de pruebas es la capa que convierte un montón de ejecuciones en una respuesta trazable y auditable a *"¿este build se puede liberar?"*.
> Kiwi TCMS da esa capa gratis y self-hosted: **Test Plan → Test Case → Test Run → Test Execution → Report**.

## 3. Reparto (2 personas)

| Bloque | Quién | Tiempo | Acción en vivo |
|---|---|---|---|
| 1. Problema + qué es Kiwi | A | 0:00–3:00 | Abre el dashboard |
| 2. Producto, plan, casos | A | 3:00–7:15 | **Crea un test case en vivo** + muestra el historial |
| 3. Runs, ejecuciones, defecto | B | 7:15–11:00 | **Ejecuta la corrida**, falla uno, adjunta el defecto |
| 4. Automatización + Telemetry | B | 11:00–14:15 | **Corre pytest y el importador**, refresca reportes |
| 5. Beneficios, límites, repo | A + B | 14:15–15:00 | Slide final |

Cada uno habla ~7:15 y tiene al menos dos acciones en pantalla: la participación equitativa se ve, no se declara.

## 4. Estado verificado del repo

Todo el flujo se probó contra una instancia real de `kiwitcms/kiwi:latest`:

- `docker compose up -d` + `manage.py migrate` + `createsuperuser` → instancia en **https://localhost:8443**
- `seed/seed_demo.py` → crea classification, producto, versión 1.2, build-45, plan de regresión, 6 casos y la corrida manual con todo en IDLE
- `pytest --junitxml=junit.xml` → **4 passed, 1 failed** (defecto intencional en `app/auth.py`)
- `automation/report_results.py junit.xml` → crea la corrida automatizada y publica PASSED/PASSED/PASSED/PASSED/FAILED

Gotchas ya resueltos y documentados en el README:
- el puerto 8080 **siempre** redirige 301 a HTTPS: la app vive en **8443**
- las migraciones **no** corren solas: hay que ejecutar `manage.py migrate`
- una instancia nueva **no trae classifications**: el seed la crea
- certificado autofirmado: `TCMS_INSECURE_SSL=1` (solo local)

## 5. Checklist 30 minutos antes

1. `docker compose up -d` y esperar a que responda `https://localhost:8443`.
2. Correr el seed. Verificar que la corrida manual esté con **todo en IDLE** (si ya la ejecutaste ensayando, borra la corrida y vuelve a crearla).
3. `set -a; source .env; set +a` en **todas** las terminales que vayas a usar.
4. Aceptar el aviso de certificado autofirmado en el navegador **antes** de exponer.
5. Abrir en orden las pestañas: dashboard, plan, corrida manual, Telemetry.
6. Zoom del navegador a 125–150%. Fuente de la terminal grande.
7. Tener `docs/snippets.md` abierto en otra ventana para copiar/pegar.
8. Grabar un video de respaldo del flujo completo.

## 6. Control de riesgo

- Cronómetro visible para los dos; corte duro al terminar cada bloque.
- Nada de teclear textos largos en vivo: todo se pega desde `docs/snippets.md`.
- Si algo falla en vivo: "we have this recorded", pasas al video y sigues hablando. **No depures en escena.**
- La integración con GitHub/JIRA es opcional y depende de red externa. Si no la configuras con token antes, en el bloque 3 adjunta el defecto como enlace en la pestaña Bugs y menciona la integración como capacidad — no la intentes en vivo sin haberla probado.

## 7. Mejora opcional si sobra tiempo de preparación

Arreglar el defecto de `app/auth.py` (cambiar `> PASSWORD_MAX_AGE_DAYS + 1` por `> PASSWORD_MAX_AGE_DAYS`), crear `build-46` y volver a importar: Telemetry muestra entonces una tendencia de dos builds, que es la evidencia más vendedora del bloque 4.
