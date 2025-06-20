[← Regresar al README](../../../README.md)
# Prototipos Realizados para la Elaboración de Interfaces

Se diseñaron una serie de prototipos orientados a la experiencia del usuario para cubrir las funcionalidades principales del sistema de IMPORCOMGUA. Estos prototipos buscan representar la estructura visual e interacción básica que tendrá el sistema final, facilitando así la validación temprana con los usuarios clave. A continuación, se describen los prototipos creados:

---

## Panel Principal

Descripción: Esta es la pantalla de inicio del sistema, diseñada para ofrecer una vista general y rápida del estado actual de la empresa. Presenta métricas clave y alertas inteligentes que permiten al usuario tomar decisiones informadas de manera proactiva.

Funcionalidades:
- **Resumen de Métricas Clave:** Muestra el total de ventas del mes, el número de productos en stock y la cantidad de clientes activos.
- **Alertas Inteligentes:** Notifica sobre situaciones críticas, como productos con stock bajo, recomendando acciones inmediatas.

![panel principal](/documentacion/Fase1/diagramas/prototipos/panelPrincipal.png)

## Panel de Mantenimientos

Descripción: Pantalla de inicio donde el usuario puede seleccionar la funcionalidad que desea gestionar. Opciones Disponibles:

- Gestionar clientes
- Gestionar productos
- Gestionar vendedores

![panel de mantenimientos](/documentacion/Fase1/diagramas/prototipos/panelMantenimientos.png)


## Clientes

### Lista de Clientes

Funcionalidades:

- Visualización de clientes registrados
- Edición de cliente
- Eliminación de cliente
- Acceso a vista detallada del cliente

![lista de clientes](/documentacion/Fase1/diagramas/prototipos/listaClientes.png)

### Formulario de Nuevo Cliente

Campos incluidos:

- Nombre del contacto
- Nombre del negocio
- Departamento y Municipio (listas dependientes)
- Dirección, NIT, Teléfono, Encargado en bodega
- Tipo de venta autorizado (Crédito, Contado, Ambas)
- Observaciones

![formulario de cliente](/documentacion/Fase1/diagramas/prototipos/formCliente.png)


## Productos

### Lista de Productos

Funcionalidades:

- Visualización de productos registrados
- Edición de producto
- Eliminación de producto
- Acceso a vista detallada del producto

![lista de productos](/documentacion/Fase1/diagramas/prototipos/listaProductos.png)

### Formulario de Nuevo Producto

Campos incluidos:

- Código
- Nombre
- Unidad de medida
- Unidades por fardo/paquete

![formulario de producto](/documentacion/Fase1/diagramas/prototipos/formProducto.png)

## Vendedores

### Lista de Vendedores

Funcionalidades:

- Visualización de vendedores registrados
- Edición de vendedor
- Eliminación de vendedor
- Acceso a vista detallada del vendedores

![lista de vendedores](/documentacion/Fase1/diagramas/prototipos/listaVendedores.png)

### Formulario de Nuevo Vendedor

Campos incluidos:

- Nombres y Apellidos
- Teléfono, Dirección
- Porcentaje de comisión

![formulario de vendedor](/documentacion/Fase1/diagramas/prototipos/formVendedor.png)


## Panel de Procesos

Descripción: Pantalla de inicio donde el usuario puede seleccionar la funcionalidad que desea gestionar. Opciones Disponibles:

- Registrar ingreso
- Registrar venta
- Registrar salida
- Registrar pago

![panel de procesos](/documentacion/Fase1/diagramas/prototipos/panelProcesos.png)

## Formulario de Ingreso de inventario

Campos incluidos:

- Fecha de ingreso
- Producto
- Cantidad en fardos/paquetes
- Unidades por fardo/paquete
- Unidades totales
- No. contenedor
- No. de DUCA
- Fecha de DUCA
- No. de DUCA rectificada
- Fecha de DUCA rectificada 
- Observaciones

![formulario ingreso de inventario](/documentacion/Fase1/diagramas/prototipos/formInventario.png)


## Formulario de Registro de Venta

Campos incluidos:

- Fecha de venta
- Fecha de salida de bodega
- Número de envío
- Cliente 
- NIT cliente
- Tipo de pago
- Días de crédito
- Vendedor
- Número de factura DTE
- Nombre de factura
- NIT factura
- Sección de productos vendidos
    - Producto
    - Cantidad
    - Unidades
    - Precio
    - Total de la venta
- Observaciones

![formulario registro de ventas](/documentacion/Fase1/diagramas/prototipos/formVenta.png)

## Registro de Salida

Este flujo permite registrar oficialmente la salida de productos desde la bodega tras la confirmación de una venta.

**Pasos del flujo:**

1. **Búsqueda del envío:**  
Se permite buscar el número de envío o el cliente asociado. El sistema muestra un resumen de la venta:

![formulario registro de salida](/documentacion/Fase1/diagramas/prototipos/registrarSalida.png)

![resultado de busqueda](/documentacion/Fase1/diagramas/prototipos/resultadoVenta.png)

2. **Detalle de la venta:**  
Se muestra la información completa del envío, incluyendo:
    - Número de envío
    - Cliente
    - Fecha de venta
    - Vendedor
    - Tipo de pago
    - Productos vendidos
    - Total

![informacion](/documentacion/Fase1/diagramas/prototipos/infoVenta.png)


3. **Registro de salida:**  
Se ingresan los siguientes datos:
    - Fecha de salida de bodega
    - Número de envío
    - Observaciones de salida

![registrar salida](/documentacion/Fase1/diagramas/prototipos/registrarSalidaVenta.png)


4. **Confirmación:**  
El usuario puede **Cancelar** o **Confirmar Salida**, lo cual actualiza el estado del envío en el sistema.

## Registro de Pago

Este flujo permite registrar oficialmente el pago de una venta.

**Pasos del flujo:**

1. **Búsqueda del envío:**  
Se permite buscar el número de envío o el cliente asociado. El sistema muestra un resumen de la venta:

![formulario registro de pago](/documentacion/Fase1/diagramas/prototipos/registrarPago.png)

![resultado de busqueda](/documentacion/Fase1/diagramas/prototipos/resultadoPago.png)

2. **Detalle de la venta:**  
Se muestra la información completa del envío, incluyendo:
    - Número de envío
    - Cliente
    - Fecha de venta
    - Total
    - Pagado
    - Saldo
    - Estado de cobro
    - Historial de pagos
    - Productos vendidos

![informacion](/documentacion/Fase1/diagramas/prototipos/infoVentaPago.png)


3. **Registro de nuevo pago:**  
Se ingresan los siguientes datos:
    - Número de recibo de caja
    - Fecha de pago
    - Banco
    - No. cuenta
    - No. de transferencia o deposito
    - Monto de abono
    - Saldo actual
    - Numero de envio

![registrar nuevo pago](/documentacion/Fase1/diagramas/prototipos/registrarNuevoPago.png)

4. **Confirmación:**  
El usuario puede **Cancelar** o **Confirmar Pago**, lo cual actualiza los pagos de la venta en el sistema.
  

[← Regresar al README](../../../README.md)