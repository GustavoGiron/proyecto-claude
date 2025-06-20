[← Regresar al README](../../../README.md)

# CASOS DE USO EXPANDIDOS 

## **MÓDULO: MANEJO DE INVENTARIO**

### CU001 – Registrar Salida de Inventario

| Campo                         | Detalle                                                                                                                                                                                 |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**                        | CU001                                                                                                                                                                                   |
| **Módulo al que pertenece**   | Manejo de Inventario                                                                                                                                                                    |
| **Actor principal**           | Gerente                                                                                                                                                                                 |
| **Actores secundarios**       | Sistema de Ventas                                                                                                                                                                       |
| **Precondiciones**            | - Venta debe estar registrada<br>- Usuario autenticado con permisos de gerente                                                                                                          |
| **Postcondiciones**           | - Stock actualizado<br>- Registro de salida asociado a la venta                                                                                                                         |
| **Escenario principal**       | 1. Gerente busca la venta por número de envío o cliente<br>2. Visualiza productos asociados<br>3. Ingresa fecha de salida<br>4. Sistema descarga catálogo<br>5. Se actualiza inventario |
| **Escenario alternativo**     | - Venta no encontrada<br>- Stock insuficiente                                                                                                                                           |
| **Requerimientos especiales** | - Trazabilidad de movimientos<br>- Validación de productos contra inventario<br>- Descarga del catálogo al momento del registro                                                         |

![CU-001](../diagramas/casos_de_uso/CU-001.png)

---


## **MÓDULO: MANEJO DE INVENTARIO**

### CU002 – Registrar Ingreso de Inventario

| Campo                         | Detalle                                                                                                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**                        | CU002                                                                                                                                                                  |
| **Módulo al que pertenece**   | Manejo de Inventario                                                                                                                                                   |
| **Actor principal**           | Gerente                                                                                                                                                                |
| **Actores secundarios**       | Aduana                                                                                                                                                                 |
| **Precondiciones**            | - Usuario autenticado<br>- Productos importados con DUCA                                                                                                               |
| **Postcondiciones**           | - Inventario actualizado<br>- Información legal (DUCA) registrada                                                                                                      |
| **Escenario principal**       | 1. Gerente inicia ingreso<br>2. Carga catálogo de productos<br>3. Visualiza lista de productos<br>4. Valida datos generales y de importación<br>5. Registra el ingreso |
| **Escenario alternativo**     | - DUCA incompleta o inválida<br>- Datos no coinciden con catálogo                                                                                                      |
| **Requerimientos especiales** | - Validación con criterios de aduana<br>- Asociación entre productos y DUCA<br>- Cálculo automático de unidades                                                        |

![CU-002](../diagramas/casos_de_uso/CU-002.png)

---

## **MÓDULO: CATÁLOGO DE PRODUCTOS**

### CU003 – Gestión de Productos

| Campo                         | Detalle                                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **ID**                        | CU003                                                                                                                                |
| **Módulo al que pertenece**   | Catálogo de Productos                                                                                                                |
| **Actor principal**           | Gerente                                                                                                                              |
| **Actores secundarios**       | Proveedores                                                                                                                          |
| **Precondiciones**            | - Usuario autenticado                                                                                                                |
| **Postcondiciones**           | - Producto creado, modificado o eliminado                                                                                            |
| **Escenario principal**       | 1. Buscar producto<br>2. Registrar nuevo producto (con datos completos)<br>3. Modificar o eliminar si aplica                         |
| **Escenario alternativo**     | - Producto ya existe (duplicado)<br>- Error en unidad de medida                                                                      |
| **Requerimientos especiales** | - Validación del código del producto<br>- Relación con unidad de medida<br>- Permitir búsquedas por nombre, unidad u otros criterios |

![CU-003](../diagramas/casos_de_uso/CU-003.png)

---


## **MÓDULO: CATÁLOGO DE VENDEDORES**

### CU004 – Gestión de Vendedores

| Campo                         | Detalle                                                                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **ID**                        | CU004                                                                                                                   |
| **Módulo al que pertenece**   | Catálogo de Vendedores                                                                                                  |
| **Actor principal**           | Gerente                                                                                                                 |
| **Actores secundarios**       | Vendedores                                                                                                              |
| **Precondiciones**            | - Usuario autenticado                                                                                                   |
| **Postcondiciones**           | - Vendedor registrado, modificado o eliminado                                                                           |
| **Escenario principal**       | 1. Buscar vendedor<br>2. Registrar nuevo vendedor (nombre, dirección, comisión)<br>3. Editar o eliminar si es necesario |
| **Escenario alternativo**     | - Comisión inválida<br>- Código de vendedor ya existente                                                                |
| **Requerimientos especiales** | - Validación del porcentaje de comisión<br>- Búsquedas por nombre, comisión u otros criterios                           |

![CU-004](../diagramas/casos_de_uso/CU-004.png)

---


## **MÓDULO: CATÁLOGO DE CLIENTES**

### CU005 – Gestión de Clientes

| Campo                         | Detalle                                                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **ID**                        | CU005                                                                                                                           |
| **Módulo al que pertenece**   | Catálogo de Clientes                                                                                                            |
| **Actor principal**           | Gerente                                                                                                                         |
| **Actores secundarios**       | Clientes                                                                                                                        |
| **Precondiciones**            | - Usuario autenticado                                                                                                           |
| **Postcondiciones**           | - Cliente registrado, modificado o eliminado                                                                                    |
| **Escenario principal**       | 1. Buscar cliente<br>2. Registrar cliente nuevo (nombre, NIT, tipo de venta, ubicación)<br>3. Editar o eliminar según necesidad |
| **Escenario alternativo**     | - Código o NIT duplicado<br>- Error en selección de municipio vs. departamento                                                  |
| **Requerimientos especiales** | - Validación jerárquica entre municipio y departamento<br>- Formato automático de códigos<br>- Búsqueda por criterios múltiples |

![CU-005](../diagramas/casos_de_uso/CU-005.png)

---

## **MÓDULO: VENTAS**

### CU006 – Registrar Venta y Pago

| Campo                         | Detalle                                                                                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**                        | CU006                                                                                                                                              |
| **Módulo al que pertenece**   | Ventas                                                                                                                                             |
| **Actor principal**           | Gerente                                                                                                                                            |
| **Actores secundarios**       | Clientes                                                                                                                                           |
| **Precondiciones**            | - Cliente y vendedor deben estar registrados                                                                                                       |
| **Postcondiciones**           | - Venta registrada<br>- Estado del cobro actualizado según abono                                                                                   |
| **Escenario principal**       | 1. Registrar venta (cliente, productos, tipo de pago)<br>2. Calcular totales y crédito<br>3. Registrar abono (parcial o total)                     |
| **Escenario alternativo**     | - Saldo pendiente no coincide<br>- Pago parcial registrado                                                                                         |
| **Requerimientos especiales** | - Control de saldo y fecha de pago total<br>- Multiplicidad de abonos permitida<br>- Diferenciación entre contado y crédito con reglas automáticas |

![CU-006](../diagramas/casos_de_uso/CU-006.png)

---

## **MÓDULO: SOPORTE – ACTUALIZACIÓN DE CATÁLOGOS**

### CSU007 – Actualización de Catálogos (Soporte)

| Campo                         | Detalle                                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------------------------- |
| **ID**                        | CSU007                                                                                              |
| **Módulo al que pertenece**   | Soporte: Actualización de Catálogos                                                                 |
| **Actor principal**           | Sistema de Catálogos                                                                                |
| **Actores secundarios**       | Catálogo de Clientes, Productos y Vendedores                                                         |
| **Precondiciones**            | Catálogos base cargados                                                                              |
| **Postcondiciones**           | Catálogos sincronizados con datos externos                                                          |
| **Escenario principal**       | 1. Seleccionar tipo de catálogo<br>2. Ejecutar actualización<br>3. Confirmar resultados               |
| **Requerimientos especiales** | —                                                                                                    |

![CSU-007](../diagramas/casos_de_uso/CSU-007.png)

---

## **MÓDULO: SOPORTE – MANEJO DE INVENTARIO**

### CSU008 – Sincronización de Inventario Externo (Soporte)

| Campo                         | Detalle                                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------------------------- |
| **ID**                        | CSU008                                                                                              |
| **Módulo al que pertenece**   | Soporte: Manejo de Inventario                                                                       |
| **Actor principal**           | Sistema de Inventario                                                                               |
| **Actores secundarios**       | Catálogo de Clientes, Productos y Vendedores                                                         |
| **Precondiciones**            | Inventario local y catálogos cargados                                                               |
| **Postcondiciones**           | Inventario externo actualizado                                                                      |
| **Escenario principal**       | 1. Iniciar sincronización<br>2. Enviar datos al sistema externo<br>3. Registrar acuse de recibo       |
| **Requerimientos especiales** | —                                                                                                    |

![CSU-008](../diagramas/casos_de_uso/CSU-008.png)

---

[← Regresar al README](../../../README.md)