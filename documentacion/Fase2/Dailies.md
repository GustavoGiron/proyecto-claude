[← Regresar al README](../../../README.md)

# Daily Standups - Fase 2

## Daily 1 - 17/06/2025

### Integrante 1 - Kevin Estuardo Secaida Molina
- **¿Qué hice ayer?**: Corrección en la documentación de la fase 1, revisión de los casos de uso y actualización del tablero Kanban.
- **¿Qué haré hoy?**: Iniciar la documentación de la fase 2, enfocándome en los dailies y el sprint planning.
- **¿Tengo algún impedimento?**: No, todo en orden.

### Integrante 2 - Pedro Luis Pu Tavico
- **¿Qué hice ayer?**: Ayer revisé los aspectos que necesitan ser corregidos en la documentación de los requerimientos tanto funcionales como no funcionales.
- **¿Qué haré hoy?**: Hoy voy a realizar las correcciones y mejoras necesarias en la documentación de los requerimientos funcionales y no funcionales correspondientes a la fase 1 del proyecto.
- **¿Tengo algún impedimento?**: No tengo ningún impedimento por el momento.

### Integrante 3 - Carlos Raul Rangel Robelo
- **¿Qué hice ayer?**: Avancé en el análisis y definición de la estructura base del proyecto backend. Revisé los patrones de diseño adecuados para organizar los controladores, servicios y repositorios de forma modular.
- **¿Qué haré hoy?**: Implementar la base del proyecto con la estructura MVC usando Flask, asegurando que se incluya el patrón Repository para separar la lógica de acceso a datos, y un servicio base para manejo de errores con logs centralizados. También dejaré definidos los primeros ejemplos de endpoints por módulo, para que el resto del equipo pueda basarse en ellos y construir sus funcionalidades.
- **¿Tengo algún impedimento?**: No.

### Integrante 4 - Gustavo Alejandro Giron Arriola
- **¿Qué hice ayer?**: Ayer revise la retroalimentacion respecto al diagrama de bloques y la arquitectura y analice las correciones a implementar en dicho diagrama asi como en la arquitectura. 
- **¿Qué haré hoy?**: Implemente las correcciones en la arquitectura y el digrama en base al analisis y retroalimentacion previa.
- **¿Tengo algún impedimento?**: no hubo ningun tipo de inconvenientes.

### Integrante 5 - Oscar Eduardo Morales Girón

* **¿Qué hice ayer?**: Me enfoqué en el análisis y diseño de los casos de uso (DCU) del sistema. Elaboré y modifiqué los diagramas correspondientes, incluyendo los DCU de alto nivel, primera descomposición y los de soporte. Validé su coherencia frente al enunciado y requerimientos funcionales, asegurando que los flujos representados se alinearan con los procesos reales de IMPORCOMGUA. Además, redacté las descripciones textuales completas de los casos de uso principales y de soporte, siguiendo la estructura formal requerida para la documentación de la fase 1.
* **¿Qué haré hoy?**: Ajustaré los diagramas si se reciben observaciones, y apoyaré en la integración de estos elementos al repositorio del proyecto. También colaboraré en validar la consistencia entre diagramas y futuras implementaciones técnicas.
* **¿Tengo algún impedimento?**: No, todo en orden.


### Integrante 6 - Ediwn Sandoval Lopez
- **¿Qué hice ayer?**: Ayer estuve revisando el script de la base de datos, generando migrations para la creacion de la base de datos por comando.
- **¿Qué haré hoy?**: Terminar las migrations para la db, y empezar con el modelado y primeras rutas para Inventario y Productos.
- **¿Tengo algún impedimento?**: Si, no han subido la estructura de carpetas hablado en el sprint.

---

## Daily 2 - 18/06/2025

### Integrante 1 - Kevin Estuardo Secaida Molina
- **¿Qué hice ayer?**:  Trabajé en la integración del formulario de clientes con el backend, corrigiendo problemas en la carga dinámica de municipios según departamento seleccionado. También realicé ajustes en la lista de clientes para que permita editar y crear usando el mismo formulario.
- **¿Qué haré hoy?**: Voy a terminar de validar que la edición de clientes funcione correctamente con el backend, solucionando el problema de validación del campo numero_cliente. Además, mejoraré la experiencia de usuario al regresar desde el formulario y añadiré mensajes claros cuando ocurra un error.
- **¿Tengo algún impedimento?**: Sí. Hoy encontramos un problema de inconsistencia entre frontend y backend:
→ El frontend usa numero_cliente como identificador único del cliente, pero el backend espera id para operaciones como edición y eliminación.
Esto causaba errores al actualizar, ya que se intentaba guardar un cliente con un numero_cliente que ya existía (porque se estaba usando como ID sin verificar que no esté duplicado).
Se está trabajando en sincronizar esta lógica para evitar conflictos.

### Integrante 2 - Pedro Luis Pu Tavico
- **¿Qué hice ayer?**: Ayer realice las correcciones y mejoras necesarias en la documentación de los requerimientos funcionales y no funcionales correspondientes a la fase 1 del proyecto.
- **¿Qué haré hoy?**: Hoy voy a realizar parte del frontend, específicamente la vista de clientes.
- **¿Tengo algún impedimento?**: No tengo ningún impedimento por el momento.

### Integrante 3 - Gustavo Alejandro Giron Arriola
- **¿Qué hice ayer?**: Implemente las correcciones en la arquitectura y el digrama en base al analisis y retroalimentacion previa.
- **¿Qué haré hoy?**: Trabajare en el backend el apartado de Vendedor.
- **¿Tengo algún impedimento?**: no hubo ningun impedimento.

### Integrante 4 - Carlos Raul Rangel Robelo
- **¿Qué hice ayer?**: Generé el codigo_cliente basado en departamento, ajusté repositorios y corregí Swagger.
- **¿Qué haré hoy?**: Escribir pruebas unitarias de clientes e integrar con frontend.
- **¿Tengo algún impedimento?**: No.

### Integrante 5 – Oscar Eduardo Morales Girón

* **¿Qué hice ayer?**: Me asignaron la implementación del módulo **Productos** en el backend, por lo que no ajusté diagramas (no recibí observaciones), no integré esos elementos al repositorio, no validé la consistencia entre diagramas y futuras implementaciones técnicas.
* **¿Qué haré hoy?**: Trabajaré directamente en los componentes de “Productos”:
  * Revisar y ajustar el modelo en `productos_model.py`.
  * Afinar las validaciones y esquemas en `productos_dto.py`.
  * Optimizar métodos CRUD y búsquedas en `productos_repo.py`.
  * Depurar y robustecer la lógica de negocio en `productos_service.py`.
  * Verificar y probar los endpoints REST en `productos_api.py`.
* **¿Tengo algún impedimento?**: Sí. Necesito confirmar con el equipo de frontend el formato exacto de la respuesta de los endpoints de productos (estructura y nombres de campos) para garantizar una integración correcta.


### Integrante 6 - Ediwn Sandoval Lopez
- **¿Qué hice ayer?**: Ayer estuve terminando la migrations de la base de datos.
- **¿Qué haré hoy?**: Hoy voy a estar viendo el script migrate, para ejecutar el migrate y rollback
- **¿Tengo algún impedimento?**: No.
---

## Daily 3 - 19/06/2025

### Integrante 1 - Kevin Estuardo Secaida Molina
- **¿Qué hice ayer?**: Terminé de validar que la edición de clientes funcione correctamente con el backend, solucionando el problema de validación del campo numero_cliente. También mejoré la experiencia de usuario al regresar desde el formulario. El módulo de clientes está completamente funcional, validando correctamente todos los campos esperados.
- **¿Qué haré hoy?**: Voy a trabajar en la implementación del módulo de vendedores, creando el formulario y asegurando que se integre correctamente con el backend. También revisaré los endpoints necesarios para las operaciones CRUD de vendedores.
- **¿Tengo algún impedimento?**: Si, dado que aun no se han subido los endpoints de vendedores al repositorio, no podré avanzar con la integración del formulario hasta que estén disponibles.

### Integrante 2 - Pedro Luis Pu Tavico
- **¿Qué hice ayer?**: Ayer inicié con la implementación del frontend, trabajando específicamente en la vista de clientes.
- **¿Qué haré hoy?**: Hoy realicé la creación del dashboard principal y desarrollé los módulos de mantenimiento para el sistema.
- **¿Tengo algún impedimento?**: No tengo ningún impedimento por el momento.

### Integrante 3 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 4 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 5 – Oscar Eduardo Morales Girón

* **¿Qué hice ayer?**: Implementé el módulo Productos en el backend: definí la entidad, creé el repositorio con métodos CRUD y búsqueda, desarrollé la lógica de negocio, elaboré los schemas de validación y expuse los endpoints REST. 
* **¿Qué haré hoy?**: Validaré que el core de negocio concuerde con los casos de uso existentes y actualizaré los stakeholders en los diagramas de fase 1. Además, revisaré que la documentación describa correctamente estos procesos.
* **¿Tengo algún impedimento?**: Sí. Necesito confirmar con el equipo de frontend el formato exacto de la respuesta de los endpoints de Productos (estructura y nombres de campos) para garantizar una integración correcta.

### Integrante 6 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

## Daily 4 - 20/06/2025

### Integrante 1 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 2 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 3 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 4 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

### Integrante 5 - [Nombre]
- **¿Qué hice ayer?**: [Actividades del día anterior]
- **¿Qué haré hoy?**: [Actividades planificadas para hoy]
- **¿Tengo algún impedimento?**: [Sí/No - Descripción si aplica]

[← Regresar al README](../../../README.md)
