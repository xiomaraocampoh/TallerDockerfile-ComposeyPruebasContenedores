---

**CORPORACIÓN UNIVERSITARIA EMPRESARIAL ALEXANDER VON HUMBOLDT**
**Facultad de Ingeniería — Programa de Ingeniería de Software**

**Asignatura:** Pruebas de Software
**Docente:** Jose Alfredo Ramírez Espinosa
**Corte:** 2 — Examen Parcial
**Semestre:** V — 2026-1
**Tiempo:** 60 minutos
**Valor:** 50% del corte 2

---

### INSTRUCCIONES GENERALES

Lee el enunciado completo antes de comenzar. Administra bien el tiempo: un repositorio con análisis sólido, commits que evidencian el proceso y un pipeline en verde vale más que código sin metodología.

**Tecnología:** Puedes usar el lenguaje de programación y las herramientas de tu preferencia. Python con `uv` y `pytest`, Java con Maven y JUnit 5, JavaScript con Jest, o cualquier combinación que domines, siempre que permita implementar TDD, BDD con Gherkin, pruebas de rendimiento y un pipeline de CI/CD en GitHub Actions.

**Recursos permitidos:** Puedes consultar documentación oficial, tus apuntes, el material del curso, repositorios de referencia propios o públicos, y cualquier recurso escrito o en línea.

**Recursos NO permitidos:** Queda estrictamente prohibido el uso de herramientas de inteligencia artificial en cualquier forma: GitHub Copilot, ChatGPT, Claude, Gemini, Cursor, Tabnine u otras similares. El código, los tests, los escenarios Gherkin y el análisis deben ser de autoría propia. El incumplimiento de esta restricción anula el examen.

**Entrega:** Publica el link de tu repositorio GitHub en el foro del curso exactamente cuando el docente indique el cierre. Repositorios enviados después no se reciben.

---

### ENUNCIADO

La empresa **RecargaYa S.A.S.** necesita un módulo para calcular el valor final de recargas de celular. Las reglas son: el monto de recarga debe estar entre $1.000 y $50.000, de lo contrario se rechaza; recargas de $10.000 o más reciben un 10% de datos de bonificación; recargas de $30.000 o más reciben un 25% de datos de bonificación; y los usuarios con plan premium obtienen un 5% adicional sobre cualquier bonificación. Construye este módulo usando TDD con los ciclos Red-Green-Refactor visibles en los commits, diseña una tabla de casos de prueba aplicando partición de equivalencia y valores límite para el campo de monto, escribe mínimo 5 escenarios BDD en Gherkin incluyendo un `Scenario Outline`, expón el módulo como API REST, agrega un script de Locust o equivalente que verifique que el P95 sea menor a 300ms con 30 usuarios simultáneos, y conecta todo en un pipeline de GitHub Actions que corra los tests en cada push. La entrega es un repositorio GitHub público con el pipeline en verde y un `README.md` con los comandos para ejecutar cada tipo de prueba.

---

### CRITERIOS DE EVALUACIÓN

| Criterio | Puntos |
|---|---|
| Tabla de casos de prueba en el README (partición de equivalencia + valores límite) | 15 |
| Ciclo TDD evidenciado en commits 🔴🟢🔵 | 15 |
| Tests unitarios completos con cobertura ≥ 80% | 15 |
| Escenarios BDD en Gherkin (mínimo 5, incluyendo Scenario Outline) | 20 |
| Script de rendimiento con verificación de P95 | 15 |
| Pipeline de GitHub Actions en verde | 15 |
| README con instrucciones claras para correr cada tipo de prueba | 5 |
| **Total** | **100** |

---

*El repositorio debe ser público al momento de la entrega. Un repositorio privado equivale a no entregar.*