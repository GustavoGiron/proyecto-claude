
[← Regresar al README](../../../README.md)

# Sprint Retrospective

## Integrante 1: Kevin Estuardo Secaida Molina
### ¿Qué se hizo bien durante el Sprint?
- Se logró reutilizar el formulario de clientes para crear y editar, mejorando la experiencia de usuario.
- Se implementó correctamente la carga dinámica de municipios según el departamento seleccionado.
- Se resolvió el error de validación del campo tipo_venta_autoriz al corregir la inconsistencia entre 'Crédito' y 'Credito'.

### ¿Qué se hizo mal durante el Sprint?
- Hubo errores iniciales por no validar adecuadamente los tipos de datos antes de enviarlos al backend.
- Se presentaron problemas con la actualización de listas en tiempo real sin recargar la página.
- Se usó numero_cliente como identificador en lugar de codigo_cliente, lo cual causó confusiones.

### ¿Qué mejoras se deben implementar para el próximo sprint?
- Validar campos obligatorios antes de enviar el formulario, mostrando alertas claras al usuario.
- Asegurar consistencia entre frontend y backend en cuanto a nombres de campos y tipos de dato.
- Mejorar la experiencia del usuario al eliminar o actualizar elementos, mostrando mensajes de éxito/error más visibles.
---

# Integrante 2: Pedro Luis Pu Tavico

### ¿Qué se hizo bien durante el Sprint?
Se implemento correctamente el apartado de mantenimiento, donde se pueden realizar las acciones crear, editar y eliminar. Se avanzo con la parte de procesos en las cuales se trabajaron lo que es venta e inventario.

### ¿Qué se hizo mal durante el Sprint?
Nos costó adaptar el patrón de diseño acordado para el frontend, lo cual generó confusión en la distribución y responsabilidad de componentes.

### ¿Qué mejoras se deben implementar para el próximo sprint?
Coordinar de forma más temprana los contratos entre frontend y backend (nombres de campos, rutas, formatos).

---

## Integrante 3: Carlos Raul Rangel Robelo

### ¿Qué se hizo bien durante el Sprint?
- La estructuración del backend y tambien el uso de tefcnologias sacando su maximo provecho como swagger con su documentación OpenApi.

### ¿Qué se hizo mal durante el Sprint?
- La distribucción de tareas del backend para que quedaran secuenciales.

### ¿Qué mejoras se deben implementar para el próximo sprint?
- Una mejor duistribucción de tareas.

---

## Integrante 4: [Nombre del integrante]

### ¿Qué se hizo bien durante el Sprint?
- [Respuesta del integrante]

### ¿Qué se hizo mal durante el Sprint?
- [Respuesta del integrante]

### ¿Qué mejoras se deben implementar para el próximo sprint?
- [Respuesta del integrante]

---

## Integrante 5: Oscar Eduardo Morales Girón

### ¿Qué se hizo bien durante el Sprint?
- Se realizaron los diagramas de casos de uso expandidos corregidos, diagramas de capas y componentes.
- Se implemento el correcto funcionamiento del modulo Productos para el backend.

### ¿Qué se hizo mal durante el Sprint?
- Se invirtió tiempo extra corrigiendo diagramas enfocados al sistema y no al negocio.
- Se añadieron sistemas externos que no estaban en los requisitos, provocando retrabajo extra.
- Costo comprender a profundidad el empleo correcto de los casos de uso expandidos y su planteo.

### ¿Qué mejoras se deben implementar para el próximo sprint?
- Evitar trabajo extra al realizar compotentes, diagramas y procesos no enfocados a las necesidades de el proyecto.

---

### Integrante 6 - Ediwn Sandoval Lopez

### ¿Qué se hizo bien durante el Sprint?
- Implementacion de scripts para migrate y rollback.
- Implementacion del modulo inventario, crud complento
- Implementacion del modulo ingreso de mercancia
- Implementacion de inventario en ingreso de mercancia

### ¿Qué se hizo mal durante el Sprint?
- Al inicio del modulo de ingreso de mercancia, no se actualizaba inventario.

### ¿Qué mejoras se deben implementar para el próximo sprint?
- Merorar los filtros actuales al consultar historial.

---

## Tablero Final del Sprint

![Tablero Sprint](./images/JiraFinal.png)

---

## Sprint Backlog - Estado Final

| Elemento del Sprint Backlog | Estado | Justificación |
|------------------------------|--------|---------------|
| Backend/Inventario | ✅ Completado | Implementación completa del CRUD y migración exitosa |
| Frontend/Inventario | ✅ Completado | Interfaz funcional implementada correctamente |
| Backend/Producto | ✅ Completado | Módulo completamente funcional con todas las operaciones |
| Frontend/Producto | ✅ Completado | Interfaz de usuario implementada y funcional |
| Backend/Vendedor | ✅ Completado | CRUD completo y operaciones implementadas |
| Frontend/Vendedor | ✅ Completado | Formularios y validaciones implementados correctamente |
| Backend/Cliente | ✅ Completado | Módulo completo con carga dinámica de municipios |
| Frontend/Cliente | ✅ Completado | Formulario reutilizable para crear/editar implementado |
| Backend/Venta | ❌ No completado | Dificultades en la integración con el módulo de inventario |
| Frontend/Venta | ❌ No completado | Problemas de integración con backend impidieron completar las solicitudes |


[← Regresar al README](../../../README.md)
