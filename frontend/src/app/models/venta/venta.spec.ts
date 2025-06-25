
import { Venta } from './venta';

function createVenta(overrides: Partial<Venta> = {}): Venta {
  return {
    fecha_venta: '2025-04-05',
    fecha_salida_bodega: '',
    numero_envio: 'ENV-001',
    cliente_id: 1,
    nit_cliente: '123456789',
    tipo_pago: 'Contado',
    dias_credito: 0,
    vendedor_id: 1,
    numero_factura_dte: '',
    nombre_factura: '',
    nit_factura: '',
    observaciones: '',
    productos: overrides.productos ?? [], // Asegura que siempre sea un array
    ...overrides
  };
}
// import { Venta } from './venta';

// describe('Venta', () => {
//   it('should create an instance', () => {
//     expect(new Venta()).toBeTruthy();
//   });
// });
