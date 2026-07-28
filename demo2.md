# Kiwi TCMS — Guión de Demo en Vivo (10–15 minutos, 5 expositores)
**Grupo 4 — Tipo de herramienta: Gestión de pruebas**

Indicaciones escénicas en *[corchetes]*. Texto hablado en texto plano.
**E1** a **E5** = los cinco expositores, en orden.

---

## Glosario de conceptos técnicos

Antes de empezar, estos son los términos que usaremos y su significado:

| Término | Qué significa |
|---|---|
| **Build** (compilación) | Una versión específica del software que se construyó para probar. Ejemplo: "build-45" es la versión 45 del producto. Cada vez que los desarrolladores cambian código, se genera un build nuevo que hay que probar. |
| **Test Case** (caso de prueba) | Un escenario que se va a verificar. Tiene pasos, resultado esperado y prioridad. Ejemplo: "login con contraseña válida devuelve token". |
| **Test Plan** (plan de pruebas) | Un conjunto de casos agrupados bajo una estrategia: qué se prueba, contra qué versión, y con qué criterios de salida. |
| **Test Run** (carrera de pruebas) | Una ejecución concreta de los casos de un plan, contra un build específico, con resultados registrados. Es el "evento" de testing. |
| **Test Execution** (ejecución de prueba) | Cada fila dentro de un Test Run: un caso, un resultado (PASSED/FAILED/BLOCKED), quién lo ejecutó, y contra qué build. |
| **Gestión de pruebas** | No es ejecutar tests — es **controlar el proceso**: qué se probó, quién lo hizo, contra qué versión, qué falló, y dónde queda la evidencia. |

---

## BLOQUE 1 — E1 — El problema que resuelve (0:00 → 2:00)

*[Slide: título del grupo y herramienta]*

Buenos días. Somos el Grupo 4. Nuestra herramienta es **Kiwi TCMS**, un sistema de gestión de pruebas de código abierto.

*[Slide: imagen de un spreadsheet con una X roja]*

Primero, el problema. Imaginen un equipo de cinco testers, dos versiones del producto y cuatrocientos casos de prueba. Para decidir si se puede liberar, necesitan responder cuatro preguntas: ¿qué casos están en alcance para esta versión? ¿Quién es responsable de cada uno? ¿Contra **qué build** se ejecutaron? Y cuando uno falló, ¿dónde queda la evidencia y el defecto asociado?

La mayoría de equipos responde eso con un spreadsheet. Pero un spreadsheet no versiona, no puede vincular un fallo con un bug, no puede decir quién cambió un resultado esperado el martes pasado, y no puede mezclar resultados manuales con automatizados.

Esa brecha es exactamente lo que una herramienta de gestión de pruebas llena. Kiwi TCMS no ejecuta tests — **los organiza y da trazabilidad**.

---

## BLOQUE 2 — E2 — La jerarquía del producto (2:00 → 4:30)

*[Abrir en navegador: https://localhost:8443, ya logueado]*

En Kiwi, todo empieza por declarar **qué se está probando**. La estructura es jerárquica, y es importante entenderla antes de navegar la herramienta.

**Product** (producto): es el software que se testea. Nosotros tenemos un "Solinal Demo Shop", una tienda web pequeña.

**Version** (versión): cada producto tiene versiones. La nuestra es la versión 1.2. Cuando se lance la 1.3, se trabaja con una versión nueva.

**Build** (compilación): aquí es donde se pone concreto. Un build es una **construcción específica del software** — cada vez que los desarrolladores hacen cambios y compilan el código, el resultado es un build. Nosotros tenemos "build-45". Testear contra un build específico significa que sabemos exactamente qué versión del código produjo el resultado.

*[Abrir Testing → Products → Solinal Demo Shop → versión 1.2 → build-45]*

Esto no es papelera — es lo que después nos permite decir que un test **pasó en el build 45**, que es la diferencia entre un resultado suelto y un resultado **trazable**.

*[Abrir Testing → Test Plans → "Regression - Authentication 1.2"]*

El **Test Plan** es la estrategia: qué casos entran, contra qué versión, y cuáles son los criterios de salida. Por ejemplo: "todos los casos P1 deben pasar en el build de release". Cuando llegue la versión 1.3, se clona el plan en vez de reescribirlo.

---

## BLOQUE 3 — E3 — Crear y revisar casos de prueba (4:30 → 7:00)

*[Dentro del plan, mostrar la lista de casos]*

Un **Test Case** es un activo reutilizable: precondiciones, pasos, resultado esperado, y un campo que lo vincula al test automatizado que lo cubre. Note que existe **independientemente de cualquier ejecución** — el mismo caso puede vivir en el plan de smoke, en el de regresión, y en tres versiones a la vez.

Cada columna de gestión es una decisión: **prioridad** (P1 = crítico, P2 = importante), **categoría**, **estado de automatización**, **tester asignado**. Así es como un lead decide qué correr cuando quedan dos días y cuatrocientos casos — filtra por P1 y ejecuta esos primero.

*[Abrir el caso "Login with an expired password is rejected"]*

Muestren los pasos, el resultado esperado, y el campo `script` que lo conecta al test automatizado.

*[Crear UN caso en vivo — pegar desde docs/snippets.md]*

Resumen: *"Session expires after 30 minutes of inactivity"*. Categoría Functional, prioridad P2, estado Confirmed. Pasos y resultado esperado — pegar. Guardar. Agregarlo al plan de regresión.

*[Mostrar la pestaña Historial del caso]*

Un detalle clave para gestión: **cada cambio está versionado**. Kiwi registra quién cambió qué campo y cuándo. En un proyecto auditado, ese historial **es** un entregable.

---

## BLOQUE 4 — E4 — Ejecución manual y defecto (7:00 → 9:30)

*[Abrir Testing → Test Runs → "Manual regression - build-45"]*

Un plan es una *definición*. Un **Test Run** es un *evento*: toma los casos de un plan y los ancla a un build, un manager y un tester asignado.

*[Señalar las filas de ejecución]*

Dentro del run están las **Test Executions** — una fila por caso, cada una con su estado: IDLE, RUNNING, PASSED, FAILED, BLOCKED. Un mismo caso puede tener veinte resultados diferentes en veinte runs, y cada uno queda registrado con su build y fecha.

Esa separación entre **caso** y **ejecución** es la idea central de la gestión de pruebas, y es exactamente lo que un spreadsheet no puede representar.

*[Ejecutar: marcar tres ejecuciones como PASSED]*

Yo soy el tester asignado, ejecuto y registro. Pasó. Pasó. Pasó.

*[Marcar "Login with an expired password is rejected" como FAILED, agregar comentario]*

Este falla: la contraseña tenía noventa y un días de antigüedad y el sistema aún dejó entrar al usuario. Marco el estado como **failed** y agrego un comentario con lo que observé. Ese comentario es la cadena de evidencia.

*[Abrir la pestaña Bugs de la ejecución y adjuntar el defecto]*

Kiwi se integra con rastreadores de issues — GitHub, JIRA, Bugzilla, Redmine — para que una ejecución fallida pueda abrir un issue pre-llenado con el caso, sus pasos y el build, y mantenerlo vinculado. Aquí está ese defecto, permanentemente adjunto a esta ejecución.

*[Mostrar la barra de progreso del run]*

Y arriba del run: cuántos pasaron, fallaron, están bloqueados o aún esperan. Ese es el número de "¿estamos listos para release?" que un manager realmente pregunta.

---

## BLOQUE 5 — E5 — Automatización, reportes y cierre (9:30 → 12:00)

*[Terminal al lado del navegador]*

Todo lo anterior fue manual. Pero la mayoría de equipos también tiene tests automatizados, y una herramienta de gestión que los ignora vuelve a partir la foto en dos.

Kiwi resuelve eso con una **API JSON-RPC**, un cliente Python oficial, y plugins para pytest, JUnit XML y TAP. Nosotros escribimos un importador (~100 líneas) para mostrar la API directamente.

*[Correr: `.venv/bin/python -m pytest --junitxml=junit.xml`]*

Esta es la suite automatizada del mismo producto. Cuatro tests pasan, uno falla — el mismo defecto de contraseña expirada, dejado intencionalmente en el código.

*[Correr: `.venv/bin/python automation/report_results.py junit.xml`]*

Este script envía el reporte a Kiwi a través de la API.

*[Refrescar en el navegador la pestaña de Test Runs]*

Miren qué pasó en el servidor: **se creó un nuevo Test Run automáticamente**, en el mismo producto, plan y build, con una ejecución por caso y el estado real de cada uno. Sin entrada manual de datos, y cada test automatizado vinculado al caso de prueba que lo describe.

*[Abrir Telemetry → Testing status matrix, luego Execution trends]*

Esto nos lleva a reportes. Bajo **Telemetry**, Kiwi trae dashboards diseñados para preguntas de gestión: la *testing status matrix*, que muestra qué casos pasan o fallan por build; *execution trends* en el tiempo; y desgloses por tester, prioridad y componente. Aquí se nota que un componente falla repetidamente en tres builds — un patrón invisible dentro de cualquier resultado individual.

*[Slide final: beneficios, límites, repo]*

Para resumir:

**Beneficios** como herramienta de gestión de pruebas:
- **Gratis y self-hosted** — TestRail y Zephyr cobran por usuario; Kiwi es GPL y los datos quedan en tu infraestructura.
- **Fuente única de verdad** para resultados manuales y automatizados.
- **Trazabilidad** de plan a caso a run a defecto, con historial completo de cambios.
- **Proceso estructurado out of the box** — roles, asignaciones, notificaciones.

**Límites**: la interfaz se ve anticuada, alguien tiene que administrar y respaldar la instancia, y el soporte comunitario es best-effort.

Todo lo que vieron es reproducible. Nuestro repositorio público tiene el Docker Compose, el script seed, la suite pytest, el importador de resultados y un README que los lleva a este estado exacto.

Cierre: las otras herramientas de este curso hacen que los tests **corran**. Kiwi TCMS hace que la práctica de testing sea **auditable** — convierte un montón de resultados en una respuesta defensible a "¿se puede liberar este build?".

Gracias. Preguntas.

---

## Banco de respuestas para preguntas (30–60 s cada una)

- **"¿Por qué no Jira con Xray o Zephyr?"** — Son plugins de pago, por usuario. Kiwi es independiente y gratuito, y se integra con Jira como rastreador de issues sin requerirlo.
- **"¿Ejecuta los tests?"** — No, y ese es el punto. La ejecución viene de testers o de CI; los resultados fluyen por la API o los plugins.
- **"¿Trazabilidad de requisitos?"** — Los casos llevan una referencia a requisitos, y la estructura plan-por-versión da cobertura por release.
- **"¿Cómo escala?"** — Django con base de datos relacional; instancias públicas manejan decenas de miles de casos. El límite real es la disciplina de proceso, no la herramienta.
- **"¿Qué esfuerzo de adopción?"** — Menos de un día para la instancia y configuración del producto. El costo real es escribir la biblioteca de casos, que se paga con cualquier herramienta.
- **"¿Se conecta a CI?"** — Sí: nuestro importador es ~100 líneas contra la API, y existen plugins oficiales para pytest, JUnit XML y TAP.
