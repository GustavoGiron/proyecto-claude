[← Regresar al README](../../../README.md)

## Arquitectura del Sistema para IMPORCOMGUA

### Estilo Arquitectónico Seleccionado: Arquitectura por Capas

#### Justificación:
La arquitectura por capas proporciona una organización clara, modular y mantenible del sistema, adecuada para el desarrollo incremental propuesto en el proyecto. Su adopción responde a los siguientes factores:

- Separación estricta entre presentación, lógica y persistencia
- Facilita el testing de cada capa de forma independiente
- Aumenta la reutilización de componentes y servicios
- Favorece la escalabilidad y el mantenimiento a largo plazo
- Permite cumplir con los requerimientos funcionales y no funcionales definidos

### Estructura de Capas del Sistema

#### 1. Capa de Presentación (Presentation Layer)

**Responsabilidad:**
Interfaz de usuario accesible por gerentes, clientes, vendedores, aduanas y proveedores. Esta capa captura entradas, presenta datos y se comunica con la API del servidor.

**Tecnologías esperadas:**
- Angular (SPA)
- Api REST



**Componentes:**
- Formulario de registro de clientes, productos, vendedores, ventas e inventario
- Visualización de catálogos
- Pantallas para realizar buscar ventas


#### 2. Capa de Negocio (Business Logic Layer)

**Responsabilidad:**
Contiene la lógica central del sistema: reglas de validación, flujos de casos de uso y ejecución de operaciones según actores. Garantiza la integridad del negocio.

**Tecnologías esperadas:**
- Python (Flask)
- Swagger para documentación de la API
- Servicios organizados en módulos

**Componentes:**
- **Servicios de Registro**: Clientes, vendedores, productos, ventas, inventario
- **Servicios de Validación**: Datos del DUCA, porcentaje de comisión, formato de NIT, estado de cobro
- **Gestión de Estado**: Control de estado de ventas (vigente, anulada), pagos (parcial, pagado)


#### 3. Capa de Percistencia de los datos (Data Layer)

**Responsabilidad:**
Gestionar el acceso a la base de datos, incluyendo consultas, inserciones, actualizaciones y relaciones entre entidades.

**Tecnologías esperadas:**
- MySQL


**Componentes:**
- Consultas filtradas para búsquedas (por NIT, nombre, código de producto)
- Control de integridad: Relaciones foráneas y reglas de negocio reflejadas en la base

---

### Diagrama de Capas
![Diagrama de Capas](/documentacion/Fase1/diagramas/arquitectura/Capas.png)

## Diagrama de la Arquitectura

![Diagrama Bloques](/documentacion/Fase1/diagramas/arquitectura/diagrama_de_capas.png)

### Diagrama de Componentes
![Diagrama de Componentes](/documentacion/Fase1/diagramas/arquitectura/Componentes.png)

## Diagrama de Bloques

![Diagrama Bloques](/documentacion/Fase1/diagramas/arquitectura/diagrama_de_bloques.png)
---

# Elección de Frameworks para IMPORCOMGUA

## Frontend: Angular

### ¿Por qué Angular?

**Desde la perspectiva del negocio:**

- **Interfaz Moderna y Profesional**: Angular permite crear una experiencia de usuario atractiva que proyecta profesionalismo ante clientes y proveedores
- **Velocidad de Uso**: Las pantallas cargan rápido y responden inmediatamente, lo que significa que los vendedores pueden atender más clientes en menos tiempo
- **Facilidad de Capacitación**: La interfaz es intuitiva, similar a aplicaciones web modernas que el personal ya conoce
- **Adaptabilidad**: Se ve bien tanto en computadoras de escritorio como en tablets, útil para mostrar catálogos a clientes

**Ventajas operativas:**
- Los vendedores pueden trabajar sin interrupciones por pantallas lentas
- Menos errores de captura gracias a validaciones inmediatas
- El personal se adapta rápidamente al sistema
- Genera confianza en clientes por su apariencia profesional

---

## Backend: Python con Flask y Swagger 

### ¿Por qué Python?

**Desde la perspectiva del negocio:**

- **Desarrollo Rápido = Menor Costo**: Python permite crear funcionalidades más rápido, lo que reduce el tiempo y costo de desarrollo
- **Fácil de Mantener**: Cuando necesites agregar nuevas funciones o hacer cambios, será más económico y rápido
- **Talento Disponible**: Es más fácil encontrar programadores que conozcan Python en Guatemala, lo que significa menores costos de contratación
- **Confiabilidad**: Empresas como Netflix y Instagram usan Python, garantizando que es una tecnología madura y estable

### ¿Por qué Flask específicamente?

**Enfoque de negocio:**

- **Simplicidad = Menores Costos**: Flask es minimalista, lo que significa menos complejidad y menores costos de mantenimiento
- **Flexibilidad Total**: Permite adaptar el sistema exactamente a los procesos de IMPORCOMGUA sin limitaciones
- **Escalabilidad Controlada**: Puedes agregar funcionalidades según las necesites, sin pagar por características que no usas
- **Tiempo de Mercado**: Permite lanzar versiones funcionales rápidamente para que empieces a ver beneficios pronto

---

## Comunicación: API REST

### ¿Por qué API REST?

**Desde la perspectiva del negocio:**

- **Estándar Universal**: Cualquier programador puede entender y trabajar con APIs REST, reduciendo dependencia de personal específico
- **Integración Futura**: Cuando necesites conectar con sistemas del SAT, bancos o proveedores, REST es el estándar más aceptado
- **Aplicaciones Móviles**: Si en el futuro quieres una app móvil para vendedores en campo, usará la misma API
- **Monitoreo Simple**: Es fácil identificar problemas y optimizar el rendimiento

---

## Diagrama de elección 
![Diagrama de Elección de Frameworks](/documentacion/Fase1/diagramas/arquitectura/diagrama_eleccion_frameworks.png)

[← Regresar al README](../../../README.md)