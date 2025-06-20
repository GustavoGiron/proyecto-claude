[← Regresar al README](../../../README.md)

# Requerimientos No Funcionales - IMPORCOMGUA Web

## Atributos de Calidad.

### Disponibilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF001 |
| Nombre | Sistema siempre accesible |
| Descripción | El sistema debe estar disponible para usarse durante todo el horario laboral sin caídas frecuentes. |
| Criterios de aceptación | El sistema debe funcionar correctamente al menos el 99% del tiempo en días laborales. |

### Escalabilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF002 |
| Nombre | 	Preparado para el crecimiento |
| Descripción | El sistema debe funcionar bien aunque se agreguen más clientes, productos o empleados en el futuro. |
| Criterios de aceptación | El sistema debe seguir funcionando sin problemas cuando se duplique la cantidad de datos actuales. |

### Usabilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF003 |
| Nombre | Fácil de usar para cualquier empleado |
| Descripción | Las pantallas deben ser claras y fáciles de entender, sin necesidad de capacitar mucho al personal. |
| Criterios de aceptación | Los usuarios deben poder usar el sistema sin ayuda después de una explicación breve. |

### Mantenibilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF004 |
| Nombre | Fácil de actualizar y corregir |
| Descripción | Si algo falla o hay que hacer un cambio, el sistema debe poder actualizarse sin complicaciones. |
| Criterios de aceptación | Los técnicos pueden realizar cambios o correcciones en poco tiempo siguiendo la documentación del sistema. |

### Confiabilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF005 |
| Nombre | El sistema debe funcionar bien todo el tiempo |
| Descripción | El sistema no debe fallar o mostrar errores constantemente mientras se está usando. |
| Criterios de aceptación | No debe haber más de 1 falla grave por mes durante el uso normal. |

---

## Restricciones.

### Restricciones Tecnológicas


| Campo | Detalle |
|-------|---------| 
| ID | RNF006 |
| Nombre | Implementación de Arquitectura por Capas |
| Descripción | El backend debe seguir estrictamente la arquitectura por capas definida en el diseño |
| Criterios de aceptación | Implementar capa de presentación (MVC), capa de negocio (patrón de servicio) y capa de acceso a datos (patrón repositorio) como está especificado |

### Restricciones de Compatibilidad

| Campo | Detalle |
|-------|---------| 
| ID | RNF007 |
| Nombre | Soporte de Navegadores Empresariales |
| Descripción | El sistema debe funcionar en los navegadores utilizados en el entorno empresarial guatemalteco |
| Criterios de aceptación | El sistema se debe visualizar correctamente en navegadores comunes como Chrome y Brave. |

[← Regresar al README](../../../README.md)