# Matrices de Trazabilidad

---

## 1. Matriz de Requerimientos

### 1.1 Requerimientos Funcionales

| ID    | Nombre                                   | Módulo / Atributo           |
|-------|------------------------------------------|-----------------------------|
| RF001 | Crear Cliente                            | Gestión de Clientes         |
| RF002 | Generar Código de Cliente Automático     | Gestión de Clientes         |
| RF003 | Configurar Tipo de Venta Autorizado      | Gestión de Clientes         |
| RF004 | Crear Producto                           | Gestión de Productos        |
| RF005 | Definir Unidades de Medida               | Gestión de Productos        |
| RF006 | Crear Vendedor                           | Gestión de Vendedores       |
| RF007 | Configurar Porcentaje de Comisión        | Gestión de Vendedores       |
| RF008 | Registrar Ingreso de Inventario          | Gestión de Inventario       |
| RF009 | Calcular Unidades Totales Automáticamente| Gestión de Inventario       |
| RF010 | Consultar Stock Actualizado              | Gestión de Inventario       |
| RF011 | Crear Venta                              | Gestión de Ventas           |
| RF012 | Calcular Total de Venta                  | Gestión de Ventas           |
| RF013 | Calcular Comisión de Vendedor            | Gestión de Ventas           |
| RF014 | Reservar Productos Vendidos              | Gestión de Ventas           |
| RF015 | Buscar Venta para Despacho               | Gestión de Despachos        |
| RF016 | Registrar Salida de Bodega               | Gestión de Despachos        |
| RF017 | Actualizar Inventario por Despacho       | Gestión de Despachos        |
| RF018 | Buscar Venta para Cobro                  | Gestión de Cobros           |
| RF019 | Registrar Pago                           | Gestión de Cobros           |
| RF020 | Calcular Saldo Pendiente                 | Gestión de Cobros           |
| RF021 | Actualizar Estado de Cobro               | Gestión de Cobros           |
| RF022 | Generar Alertas de Cobros Pendientes     | Asistente Comercial         |
| RF023 | Alertar Inventario Bajo                  | Asistente Comercial         |

### 1.2 Requerimientos No Funcionales

| ID     | Nombre                                   | Módulo / Atributo                  |
|--------|------------------------------------------|------------------------------------|
| RNF001 | Tiempo de Respuesta en Ventas            | Rendimiento                        |
| RNF002 | Capacidad de Usuarios Simultáneos        | Rendimiento                        |
| RNF003 | Velocidad de Consulta de Inventario      | Rendimiento                        |
| RNF004 | Generación de Reportes Comerciales       | Rendimiento                        |
| RNF005 | Rendimiento del Asistente Comercial      | Rendimiento                        |
| RNF006 | Disponibilidad en Horario Comercial      | Disponibilidad                     |
| RNF007 | Recuperación ante Fallos                 | Disponibilidad                     |
| RNF008 | Crecimiento de Volumen de Ventas         | Escalabilidad                      |
| RNF009 | Expansión del Catálogo de Productos      | Escalabilidad                      |
| RNF010 | Facilidad de Uso para Vendedores         | Usabilidad                         |
| RNF011 | Simplicidad en Gestión de Inventario     | Usabilidad                         |
| RNF012 | Claridad en Proceso de Cobros            | Usabilidad                         |
| RNF013 | Protección de Información Comercial      | Seguridad                          |
| RNF014 | Integridad de Transacciones Comerciales  | Seguridad                          |
| RNF015 | Precisión en Cálculos Comerciales        | Confiabilidad                      |
| RNF016 | Consistencia de Datos de Inventario      | Confiabilidad                      |
| RNF017 | Arquitectura Cliente-Servidor Obligatoria| Restricciones Tecnológicas         |
| RNF018 | Implementación de Arquitectura por Capas | Restricciones Tecnológicas         |
| RNF019 | Soporte de Navegadores Empresariales     | Restricciones de Compatibilidad    |
| RNF020 | Cumplimiento Fiscal Guatemala            | Restricciones Regulatorias         |

---

## 2. Matriz de Requerimientos vs Stakeholders

### 2.1 Requerimientos Funcionales vs Stakeholders

| ID    | Administrador | Oper. Almacén | Asist. Ventas | Encargado Cobros | Gerente |
|-------|:-------------:|:-------------:|:-------------:|:----------------:|:-------:|
| RF001 |      X        |               |               |                  |         |
| RF002 |      X        |               |               |                  |         |
| RF003 |      X        |               |               |                  |         |
| RF004 |      X        |               |               |                  |         |
| RF005 |      X        |               |               |                  |         |
| RF006 |      X        |               |               |                  |         |
| RF007 |      X        |               |               |                  |         |
| RF008 |               |      X        |               |                  |         |
| RF009 |               |      X        |               |                  |         |
| RF010 |               |      X        |               |                  |         |
| RF011 |               |               |       X       |                  |         |
| RF012 |               |               |       X       |                  |         |
| RF013 |               |               |       X       |                  |         |
| RF014 |               |               |       X       |                  |         |
| RF015 |               |      X        |               |                  |         |
| RF016 |               |      X        |               |                  |         |
| RF017 |               |      X        |               |                  |         |
| RF018 |               |               |               |        X         |         |
| RF019 |               |               |               |        X         |         |
| RF020 |               |               |               |        X         |         |
| RF021 |               |               |               |        X         |         |
| RF022 |               |               |               |                  |    X    |
| RF023 |               |               |               |                  |    X    |

### 2.2 Requerimientos No Funcionales vs Stakeholders

| ID     | Administrador | Oper. Almacén | Asist. Ventas | Encargado Cobros | Gerente |
|--------|:-------------:|:-------------:|:-------------:|:----------------:|:-------:|
| RNF001 |               |               |       X       |                  |         |
| RNF002 |      X        |               |               |                  |    X    |
| RNF003 |               |      X        |       X       |                  |         |
| RNF004 |               |               |               |                  |    X    |
| RNF005 |               |               |               |                  |    X    |
| RNF006 |      X        |      X        |       X       |        X         |    X    |
| RNF007 |      X        |               |               |                  |         |
| RNF008 |               |               |               |                  |    X    |
| RNF009 |      X        |               |               |                  |         |
| RNF010 |               |               |       X       |                  |         |
| RNF011 |               |      X        |               |                  |         |
| RNF012 |               |               |               |        X         |         |
| RNF013 |      X        |               |               |                  |    X    |
| RNF014 |      X        |               |               |        X         |         |
| RNF015 |               |               |       X       |                  |         |
| RNF016 |               |      X        |               |                  |         |
| RNF017 |      X        |               |               |                  |         |
| RNF018 |      X        |               |               |                  |         |
| RNF019 |      X        |      X        |       X       |        X         |    X    |
| RNF020 |               |               |               |        X         |         |

---

## 3. Matriz de Stakeholders vs Casos de Uso

| Stakeholder         | CU001 | CU002 | CU003 | CU004 | CU005 | CU006 | CU007 | CU008 | CU009 |
|---------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Administrador       |   X   |   X   |   X   |       |       |       |       |       |       |
| Oper. de Almacén    |       |       |       |   X   |   X   |       |   X   |       |       |
| Asist. de Ventas    |       |       |       |       |   X   |   X   |       |       |       |
| Encargado de Cobros |       |       |       |       |       |       |       |   X   |       |
| Gerente             |       |       |       |       |       |       |       |       |   X   |



[← Regresar al README](../../../README.md)