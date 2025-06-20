[← Regresar al README](../../../README.md)

## Core del Negocio – IMPORCOMGUA 

### **Descripción general del Core**

El core del negocio de IMPORCOMGUA se enfoca en resolver las limitaciones operativas derivadas de su crecimiento reciente, principalmente aquellas asociadas a procesos manuales, registros desorganizados y baja trazabilidad. Para ello, se implementa una solución tecnológica web modular, orientada a la automatización de procesos clave como ventas, inventario, cobranza, gestión de comisiones y control de clientes y vendedores. Esta plataforma busca mejorar la eficiencia operativa, reducir errores, facilitar el seguimiento de transacciones y preparar a la empresa para escalar sus operaciones en el futuro cercano.

---

### **Stakeholders principales**

* **Gerencia**: toma decisiones comerciales y aprueba condiciones especiales.
* **Administrador web**: gestiona accesos, configuraciones y catálogos.
* **Asistente de Ventas**: registran ventas, aplican condiciones especiales y consultan comisiones.
* **Personal de bodega**: registra ingresos y salidas de productos.
* **Personal de cobranzas**: gestiona pagos y saldos pendientes.
* **Clientes**: destinatarios finales de los productos y servicios.

---

### **Operaciones principales del negocio**

#### Gestión de inventario

* Ingreso de inventario (DUCA, cantidades, conversión de unidades).
* Reserva de productos por venta.
* Registro de salida de productos al cliente.

#### Gestión comercial y ventas

* Registro de ventas con validaciones de crédito, stock y comisiones.
* Aplicación de condiciones comerciales especiales (descuentos, promociones).
* Generación automática de totales, comisiones y número de pedido.
* Control del estado de las ventas: pendiente, despachado, anulado.

#### Gestión de cobros

* Registro de pagos parciales o totales.
* Cálculo y actualización automática de saldo y estado de cobro.
* Asociación de pagos a número de envío y cliente.

#### Gestión de entidades clave

* Clientes (NIT, crédito, tipo de venta, ubicación).
* Vendedores (porcentaje de comisión, estado activo/inactivo).
* Productos (presentaciones, unidades, códigos, conversiones).

#### Gestión operativa y estratégica

* Generación de alertas por:

  * Clientes morosos o inactivos.
  * Inventario bajo.
  * Cobros pendientes.
* Panel de monitoreo gerencial.


## Caso de uso de alto nivel
![CDU](/documentacion/Fase1/diagramas/casos_de_uso/CDU.png)

## Primera descomposición

![CDU_PRIMERA_DESCOMPOSICION](/documentacion/Fase1/diagramas/casos_de_uso/CDU_Primera_Descomposicion.png)

---

[← Regresar al README](../../../README.md)