[← Regresar al README](../../../README.md)

## Diagrama Despliegue
El diagrama de despliegue representa la infraestructura física y lógica del sistema de gestión de IMPORCOMGUA. Este diagrama muestra cómo los distintos componentes del sistema se distribuyen en los diferentes nodos físicos, así como las interacciones entre ellos a través de protocolos estándar.

### NODO USUARIO
El sistema cuenta con cuatro nodos principales. El primero es el nodo identificado como <<Usuario>>, que representa al cliente final utilizando un navegador web para acceder a la aplicación. Desde este punto, se establece una comunicación hacia el <<Servidor Aplicaciones>>, que aloja todos los módulos funcionales del sistema. El acceso se realiza mediante protocolos estándar como HTTP o HTTPS.

### Componente Distribuidora 
Dentro del <<Servidor Aplicaciones>> se encuentran los módulos centrales que componen la lógica del sistema. En primer lugar, se encuentra el componente "Distribuidora EntornoEjecutable", que representa el punto de arranque del sistema y el entorno general desde donde se coordinan las operaciones.

### Componente Inventario
El módulo Inventario gestiona todos los procesos relacionados al ingreso de mercancías, detalle de ingresos, productos, movimientos de inventario y el estado actualizado del stock.

### Componente Venta
El módulo Venta administra la creación de ventas y su detalle, además de coordinar con el cálculo de comisiones asociado a cada transacción. Este módulo tiene una dependencia directa con el módulo Inventario, ya que requiere verificar la existencia de productos antes de confirmar la venta.
También depende del módulo Pago, que se encarga de registrar los abonos realizados por los clientes, así como del módulo de Comisiones, responsable de calcular las comisiones correspondientes a los vendedores en base a las ventas realizadas.

### Componente Incidencia
El módulo Incidencia se encuentra desplegado dentro del servidor de aplicaciones y permite registrar y gestionar reportes relacionados a problemas ocurridos durante el proceso de venta o atención al cliente.

### Modulo Dispositivo Operativo
el diagrama muestra un nodo denominado <<Dispositivo Operativo>>, que representa dispositivos móviles o terminales de uso interno (por ejemplo, de vendedores o personal de bodega). Estos dispositivos se conectan al sistema a través de un componente API REST, que permite consumir servicios del backend 

### Modulo Servidor de Datos
 el sistema cuenta con un <<Servidor de Datos>> donde se encuentra alojada la base de datos MySQL. Todos los módulos funcionales del <<Servidor Aplicaciones>> interactúan con esta base de datos para consultar y almacenar la información necesaria, a través de conexiones seguras que utilizan el protocolo TCP/IP.

## Diagrama de Despliegue

![Diagrama despliegue](/documentacion/Fase1/despliegue/diagrama_de_despliegue.png)

[← Regresar al README](../../../README.md)