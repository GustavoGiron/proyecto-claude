# Prueba de Aceptación - Sistema IMPORCOMGUA

## Objetivo de la Prueba

Validar que el sistema IMPORCOMGUA cumple con todos los requerimientos funcionales críticos del negocio, incluyendo la gestión de roles, flujos de ventas completos, control de inventario y procesamiento de pagos, desde la perspectiva del usuario final.

## Escenario de Prueba: "Proceso Completo de Venta con Control de Roles"

### Descripción del Escenario

Este escenario simula el flujo completo de negocio de IMPORCOMGUA, desde el ingreso de mercadería hasta el pago final, validando las restricciones de roles y la integridad del sistema.

### Criterios de Aceptación

**CA-01:** El sistema debe permitir el acceso basado en roles correctamente  
**CA-02:** Se debe poder registrar ingreso de inventario con todos los campos requeridos  
**CA-03:** La gestión de clientes debe funcionar correctamente  
**CA-04:** El proceso de venta debe calcular totales automáticamente  
**CA-05:** El sistema debe registrar pagos y actualizar saldos  
**CA-06:** Las comisiones deben calcularse automáticamente  
**CA-07:** El control de acceso debe restringir funciones según el rol  
**CA-08:** Los reportes deben reflejar información actualizada

## Flujo de Prueba Detallado

### **FASE 1: Preparación y Validación de Roles**

#### 1.1 Acceso al Sistema

- **Acción:** Acceder a la URL del sistema desplegado
- **Datos de Prueba:**
  - Usuario: `test` / Password: `Test1234`
  - Usuario: `gerente_ventas` / Password: `ventas123`
  - Usuario: `gerente_inventario` / Password: `inventario123`
- **Resultado Esperado:**
  - Login exitoso para todos los usuarios
  - Dashboard personalizado según el rol
  - Menú de navegación acorde a los permisos del rol

### **FASE 2: Gestión de Inventario (Rol: Gerente de Inventario)**

#### 2.1 Registro de Producto

- **Usuario:** `gerente_inventario`
- **Módulo:** Productos
- **Acción:** Crear nuevo producto
- **Datos de Prueba:**

```
- Código: PROD001
- Nombre: Juego de Mesa Monopoly
- Descripción: Juego de mesa clásico importado
- Unidades por fardo: 12
- Precio sugerido: Q45.00
- Stock mínimo: 50
```

- **Resultado Esperado:** Producto creado exitosamente

#### 2.2 Ingreso de Inventario

- **Acción:** Registrar ingreso de mercadería

- **Datos de Prueba:**

```
- Fecha de ingreso: [Fecha actual]
- Producto: Juego de Mesa Monopoly
- Cantidad en fardos: 10
- Unidades por fardo: 12 (automático)
- Unidades totales: 120 (calculado automáticamente)
- No. Contenedor: CONT2025001
- No. De Duca: DUCA123456
- Fecha de Duca: [Fecha actual]
- Observaciones: Primer ingreso de prueba
```

- **Resultado Esperado:**

  - Ingreso registrado exitosamente
  - Stock actualizado a 120 unidades
  - Campos calculados automáticamente

### **FASE 3: Gestión de Clientes y Vendedores (Rol: Gerente de Ventas)**

#### 3.1 Registro de Cliente

- **Usuario:** `gerente_ventas`
- **Módulo:** Clientes
- **Datos de Prueba:**

```
- Nombre del contacto: María González
- Nombre del negocio: Juguetería La Esperanza
- Departamento: Guatemala
- Municipio: Guatemala
- Dirección: 12 calle 15-20 zona 1
- NIT: 12345678
- Encargado en bodega: Carlos Méndez
- Teléfono: 2234-5678
```

- **Resultado Esperado:**
  - Cliente creado con código automático (GT01)
  - Todos los campos guardados correctamente

#### 3.2 Registro de Vendedor

- **Datos de Prueba:**

```
- Nombre: Juan Pérez
- Email: juan.perez@imporcomgua.com
- Teléfono: 5555-1234
- Porcentaje de comisión: 10%
- Estado: Activo
```

### **FASE 4: Proceso de Venta Completo**

#### 4.1 Creación de Venta

- **Usuario:** `gerente_ventas`

- **Módulo:** Ventas
- **Datos de Prueba:**

```
- Fecha de venta: [Fecha actual]
- Cliente: Juguetería La Esperanza
- Vendedor: Juan Pérez
- Tipo de pago: Crédito
- Días de crédito: 30
- Número de envío: ENV2025001

Detalle de productos:
- Producto: Juego de Mesa Monopoly
- Cantidad en fardos: 5
- Cantidad en unidades: 60 (automático)
- Precio por fardo: Q540.00
- Total: Q2,700.00 (automático)
```

- **Resultado Esperado:**
  - Venta creada exitosamente
  - Estado: "Vigente"
  - Estado de cobro: "Pendiente"
  - Cálculo automático de totales
  - Comisión calculada automáticamente (Q270.00)
  - Stock actualizado (120 - 60 = 60 unidades)

#### 4.2 Validación de Cálculos Automáticos

- **Verificar:**
  - Total de venta = Q2,700.00
  - Comisión = Q270.00 (10% de Q2,700.00)
  - Saldo pendiente = Q2,700.00
  - Stock restante = 60 unidades

### **FASE 5: Gestión de Pagos**

#### 5.1 Registro de Pago Parcial

- **Usuario:** `gerente_ventas`
- **Módulo:** Pagos
- **Datos de Prueba:**

```
- Venta: [Venta creada anteriormente]
- Número de recibo: RC-001-2025
- Banco: Banco Industrial
- Número de cuenta: 123456789
- Monto abono: Q1,500.00
- Fecha de pago: [Fecha actual]
```

- **Resultado Esperado:**
  - Pago registrado exitosamente
  - Saldo pendiente actualizado: Q1,200.00
  - Estado de cobro: "Pago Parcial"

#### 5.2 Registro de Pago Final

- **Datos de Prueba:**

```
- Número de recibo: RC-002-2025
- Monto abono: Q1,200.00
```

- **Resultado Esperado:**
  - Saldo pendiente: Q0.00
  - Estado de cobro: "Pagado"
