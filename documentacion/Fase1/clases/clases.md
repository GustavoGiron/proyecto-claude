[← Regresar al README](../../../README.md)

## Diagrama Clases

El diagrama de clases representa la estructura estática del sistema de información desarrollado para IMPORCOMGUA. Permite identificar las entidades clave, sus atributos, y las relaciones entre ellas.

El modelo fue construido con base en los requerimientos funcionales del sistema, y agrupa las clases por módulo funcional. Cada clase representa una entidad de negocio o componente lógico necesario para el flujo del sistema.

### Principales clases del sistema

Cliente y Vendedor: representan los actores principales del sistema comercial.

Producto, Inventario, IngresoMercancia y sus detalles: permiten la trazabilidad del stock.

Venta, DetalleVenta y Pago: gestionan el ciclo completo de venta y cobranza.

Comisión: se deriva de las ventas realizadas por los vendedores.

Incidencia: permite la gestión de problemas o reclamos.

Departamento y Municipio: clases referenciales para ubicar clientes y vendedores.

### Relaciones destacadas

Venta depende de Inventario para verificar stock.

Pago depende de Venta para validar saldos pendientes.

Comisión depende de Venta para su cálculo.

DetalleVenta y DetalleIngreso usan composición, ya que no pueden existir sin su entidad principal.

Clases como Cliente, Producto, Vendedor se relacionan con múltiples módulos, lo que justifica su agrupación en un módulo de catálogos.

## Diagrama de Clases

![Diagrama Clases](/documentacion/Fase1/clases/diagrama_de_clases.png)

[← Regresar al README](../../../README.md)
