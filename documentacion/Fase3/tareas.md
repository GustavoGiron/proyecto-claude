Aquí tienes una redacción clara, estructurada y orientada a negocio de los **requisitos funcionales críticos de la fase 3**, con las tareas asignadas según el orden que indicaste:

---

## Requisitos funcionales críticos – Fase 3

### 1. **Funcionalidad de Login con Roles y Permisos**

**Responsables:** Edwin, Óscar
Desarrollar un sistema de autenticación que contemple perfiles con permisos diferenciados según el área gerencial:

* **Gerencia General:** Acceso total al sistema.
* **Gerencia de Ventas y Finanzas:** Permiso para registrar ventas, clientes y pagos.
* **Gerencia de Inventario:** Permiso para gestionar productos, ingresos y salidas de inventario.

---

### 2. **Integración con Proveedor de Correo para Alertas de Inventario**

**Responsables:** Edwin, Óscar (se puede incorporar apoyo adicional si es necesario)
Se debe integrar un proveedor de correo electrónico para enviar alertas automáticas cuando un producto caiga por debajo del umbral mínimo.

**Requisitos del correo de alerta:**

* Código del producto
* Nombre del producto
* Cantidad actual en inventario
* Cantidad mínima sugerida para reposición

> El umbral mínimo se deberá definir y gestionar desde backend (si procede).

---

### 3. **Validación y Pruebas Funcionales**

**Responsables:** Tavo, Tavico, Kevin
Una vez implementadas las funcionalidades de login y correo, se realizarán las siguientes pruebas:

* **5 pruebas unitarias**
* **3 pruebas de integración**
* **1 prueba de aceptación funcional**

Estas validaciones asegurarán el correcto comportamiento del sistema antes de pasar a producción.

---

### 4. **Implementación de CI/CD y Despliegue en la Nube**

**Responsable:** Rangel

* **Pipeline de CI/CD** que incluya:

  * Etapa de testing
  * Etapa de build
  * Etapa de deployment
* **Despliegue del sistema** en un entorno de producción en la nube (tecnología a definir).
* **Documentación del proceso** a través de un **video demostrativo**, mostrando la ejecución del deploy automatizado.

