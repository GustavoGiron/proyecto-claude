[← Regresar al README](../../../README.md)

## Core del Negocio – IMPORCOMGUA

### **Descripción general del Core**

El core del negocio de **IMPORCOMGUA** se enfoca en resolver las limitaciones operativas derivadas de su crecimiento reciente, principalmente aquellas asociadas a procesos manuales, registros desorganizados y baja trazabilidad. Para ello, se implementa una solución tecnológica web modular, orientada a la automatización de procesos clave como ventas, inventario, gestión de productos, clientes y vendedores, así como la integración de procesos de importación mediante aduanas. Esta plataforma busca mejorar la eficiencia operativa, reducir errores, facilitar el seguimiento de transacciones y preparar a la empresa para escalar sus operaciones en el futuro cercano.

---

### **Stakeholders principales**

* **Gerente**: toma decisiones estratégicas, aprueba condiciones especiales y administra ventas, inventarios y catálogos.
* **Clientes**: destinatarios finales de los productos; participan en procesos de compra y pago.
* **Proveedores**: suministran productos para el inventario y colaboran en la gestión del catálogo.
* **Aduanas**: validan y registran la documentación legal de productos importados (DUCA).
* **Vendedores**: realizan ventas, gestionan registros y comisiones.

---

### **Operaciones principales del negocio**

#### Gestión de inventario

* Registro de ingreso de productos con validaciones de aduana (DUCA, cantidades, unidades).
* Reserva de productos asociados a ventas específicas.
* Registro de salidas de inventario hacia clientes.

#### Gestión comercial y ventas

* Registro detallado de ventas con validaciones de crédito disponible, stock y cálculo automático de comisiones.
* Aplicación y validación de condiciones comerciales especiales como descuentos o promociones.
* Control y seguimiento de estados de venta: pendiente, despachado, anulado.

#### Gestión de cobros

* Registro y gestión de pagos parciales o totales de los clientes.
* Actualización automática del saldo y estados de cobro.
* Asociación directa de pagos con ventas específicas y clientes.

#### Gestión de entidades clave

* **Clientes**: datos fiscales, crédito, preferencias comerciales, ubicación.
* **Vendedores**: comisiones, estado activo/inactivo.
* **Productos**: catálogo, unidades de medida, conversiones, validación con proveedores.

#### Gestión operativa y estratégica

* Generación automática de alertas por:

  * Clientes morosos o inactivos.
  * Inventario bajo.
  * Cobros pendientes.

## Caso de uso de alto nivel

![CDU](/documentacion/Fase1/diagramas/casos_de_uso/CDU.png)

## Primera descomposición

![CDU\_PRIMERA\_DESCOMPOSICION](/documentacion/Fase1/diagramas/casos_de_uso/CDU_Primera_Descomposicion.png)

---

[← Regresar al README](../../../README.md)
