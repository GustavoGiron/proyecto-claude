import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Venta, DetalleVenta } from '../../models/venta/venta';
import { ClienteService } from '../../services/cliente/cliente.service';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { ProductoService } from '../../services/producto/producto.service';
import { VentaService } from '../../services/venta/venta.service';

declare var toastr: any;

@Component({
  selector: 'app-registrar-pago',
  templateUrl: './registrar-pago.component.html'
})
export class RegistrarPagoComponent implements OnInit {
  busquedaForm!: FormGroup;
  pagoForm!: FormGroup;
  loading = false;
  mostrarResultados = false;
  mostrarVentaSeleccionada = false;
  mostrarRegistroPago = false;
  ventas: Venta[] = [];
  ventaSeleccionada: Venta | null = null;
  numero_envio = '';

  constructor(
    private fb: FormBuilder,
    private clienteService: ClienteService,
    private vendedorService: VendedorService,
    private productoService: ProductoService,
    private ventaService: VentaService,
  ) {
    this.inicializarFormularios();
  }

  ngOnInit(): void {
    this.setFechaActual();
  }

  private inicializarFormularios(): void {
    // Formulario de búsqueda
    this.busquedaForm = this.fb.group({
      numeroEnvio: [''],
      nombreCliente: ['']
    });

    // Formulario de pago
    this.pagoForm = this.fb.group({
      numero_recibo_caja: [''],
      fecha_pago: ['', Validators.required],
      banco: ['', Validators.required],
      numero_cuenta: ['', Validators.required],
      numero_transferencia: ['', Validators.required],
      monto_abono: ['', [Validators.required, Validators.min(0.01)]],
    });

    // Validador personalizado para el monto
    this.pagoForm.get('monto_abono')?.valueChanges.subscribe(value => {
      this.validarMontoAbono(value);
    });
  }

  private setFechaActual(): void {
    const today = new Date().toISOString().split('T')[0];
    this.pagoForm.patchValue({ fechaPago: today });
  }

  private validarMontoAbono(monto: number): void {
    if (this.ventaSeleccionada && monto > (this.ventaSeleccionada.saldo_pendiente ?? 0)) {
      this.pagoForm.get('monto_abono')?.setErrors({
        excedesSaldo: {
          message: `El monto no puede ser mayor al saldo actual (Q ${(this.ventaSeleccionada.saldo_pendiente ?? 0)})`
        }
      });
    }
  }

  // Implementación de búsqueda adaptada del componente RegistrarSalidaComponent
  buscarVentas(): void {
    const { numeroEnvio, nombreCliente } = this.busquedaForm.value;

    if (!this.validarCriteriosBusqueda(numeroEnvio, nombreCliente)) {
      return;
    }

    this.loading = true;
    this.limpiarResultadosAnteriores();

    if (numeroEnvio?.trim()) {
      this.buscarPorNumeroEnvio(numeroEnvio);
    } else {
      this.buscarPorNombreCliente(nombreCliente);
    }
  }

  private validarCriteriosBusqueda(numeroEnvio: string, nombreCliente: string): boolean {
    if (!numeroEnvio?.trim() && !nombreCliente?.trim()) {
      toastr.warning('Por favor, ingrese al menos un criterio de búsqueda.');
      return false;
    }
    return true;
  }

  private limpiarResultadosAnteriores(): void {
    this.ventas = [];
    this.mostrarResultados = false;
  }

  private buscarPorNumeroEnvio(numeroEnvio: string): void {
    this.ventaService.obtenerVenta(numeroEnvio).subscribe({
      next: (venta) => {
        this.procesarVentas([venta]);
      },
      error: (err) => {
        this.manejarErrorBusqueda(err);
      }
    });
  }

  private buscarPorNombreCliente(nombreCliente: string): void {
    this.clienteService.obtenerCliente(nombreCliente).subscribe({
      next: (cliente) => {
        this.ventaService.obtenerVentasPorCliente(cliente.nombre_contacto).subscribe({
          next: (ventas: Venta[]) => {
            this.procesarVentas(ventas);
          },
          error: (err) => {
            this.manejarErrorBusqueda(err);
          }
        });
      },
      error: (err) => {
        this.manejarErrorBusqueda(err);
      }
    });
  }

  private procesarVentas(ventas: Venta[]): void {
    this.ventas = ventas;

    if (ventas.length > 0) {
      this.cargarDatosAdicionales(ventas);
      this.mostrarResultados = true;
    } else {
      toastr.info('No se encontraron ventas con los criterios especificados.');
    }

    this.loading = false;
  }

  private cargarDatosAdicionales(ventas: Venta[]): void {
    ventas.forEach(venta => {
      this.cargarDatosVendedor(venta);
      this.cargarDatosProductos(venta);
    });
  }

  private cargarDatosVendedor(venta: Venta): void {
    this.vendedorService.obtenerVendedorPorId(venta.vendedor_id).subscribe({
      next: (vendedor) => {
        venta.nombre_vendedor = `${vendedor.nombres} ${vendedor.apellidos}`;
      },
      error: (err) => {
        console.error('Error al cargar vendedor:', err);
        toastr.error('Error al cargar información del vendedor');
      }
    });
  }

  private cargarDatosProductos(venta: Venta): void {
    venta.detalles.forEach(detalle => {
      this.productoService.obtenerProducto(detalle.producto_id).subscribe({
        next: (producto) => {
          detalle.nombre_producto = producto.nombre_producto;
        },
        error: (err) => {
          console.error('Error al cargar producto:', err);
          toastr.error('Error al cargar información del producto');
        }
      });
    });
  }

  private manejarErrorBusqueda(err: any): void {
    console.error('Error en la búsqueda:', err);
    this.loading = false;
    this.ventas = [];
    toastr.error('Error al realizar la búsqueda. Por favor, intente nuevamente.');
  }

  seleccionarVenta(venta: Venta): void {
    this.ventaSeleccionada = venta;
    this.numero_envio = this.ventaSeleccionada.numero_envio;
    this.mostrarVentaSeleccionada = true;
    this.mostrarRegistroPago = true;

    // Actualizar campos del formulario de pago
    this.pagoForm.patchValue({
      saldoActual: `Q ${(venta.saldo_pendiente ?? 0)}`,
      referenciaEnvio: venta.numero_envio
    });

    this.scrollToVentaSeleccionada();
  }

  private scrollToVentaSeleccionada(): void {
    setTimeout(() => {
      const element = document.getElementById('venta-seleccionada-section');
      element?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  getEstadoClass(estado: string): string {
    switch (estado.toUpperCase()) {
      case 'PAGADA': return 'text-green-600';
      case 'PARCIAL': return 'text-yellow-600';
      case 'PENDIENTE': return 'text-red-600';
      default: return 'text-gray-600';
    }
  }

  onSubmitPago(): void {
    if (!this.validarDatosPago()) {
      return;
    }

    const pagoData = this.pagoForm.getRawValue();

    this.ventaService.registrarPago(this.ventaSeleccionada!.id!, pagoData).subscribe({
      next: (resp) => {
        toastr.success('Pago registrado exitosamente');
        this.resetearFormularioCompleto();
      },
      error: (err) => {
        console.error('Error al registrar pago:', err);
        toastr.error('Error al registrar pago. Por favor, intente nuevamente.');
      }
    });
  }

  private validarDatosPago(): boolean {
    if (this.pagoForm.invalid) {
      toastr.error('Por favor, complete todos los campos requeridos.');
      return false;
    }

    if (!this.ventaSeleccionada?.id) {
      toastr.error('Error: No se ha seleccionado una venta válida.');
      return false;
    }

    return true;
  }

  cancelarRegistroPago(): void {
    if (confirm('¿Está seguro de que desea cancelar el registro de pago?')) {
      this.resetearFormularioPago();
      this.resetearSeleccionVenta();
    }
  }

  private resetearFormularioPago(): void {
    this.pagoForm.reset();
    this.setFechaActual();
  }

  private resetearSeleccionVenta(): void {
    this.mostrarVentaSeleccionada = false;
    this.mostrarRegistroPago = false;
    this.ventaSeleccionada = null;
  }

  private resetearFormularioCompleto(): void {
    this.busquedaForm.reset();
    this.resetearFormularioPago();
    this.resetearEstadosVisuales();
  }

  private resetearEstadosVisuales(): void {
    this.mostrarResultados = false;
    this.mostrarVentaSeleccionada = false;
    this.mostrarRegistroPago = false;
    this.ventaSeleccionada = null;
  }

  limpiarBusqueda(): void {
    this.busquedaForm.reset();
    this.resetearEstadosVisuales();
  }

  getEstadoEntregaClass(estado: string): string {
    switch (estado.toUpperCase()) {
      case 'ENTREGADO': return 'text-green-600 font-medium';
      case 'PENDIENTE': return 'text-red-600 font-medium';
      default: return 'text-gray-600';
    }
  }

  getEstadoVentaClass(estado: string): string {
    switch (estado.toUpperCase()) {
      case 'VIGENTE': return 'text-green-600 font-medium';
      default: return 'text-gray-600 font-medium';
    }
  }

  getEstadoCobroClass(estado: string): string {
    switch (estado.toUpperCase()) {
      case 'PAGADA': return 'text-green-600 font-medium';
      case 'PARCIAL': return 'text-yellow-600 font-medium';
      case 'PENDIENTE': return 'text-red-600 font-medium';
      default: return 'text-gray-600 font-medium';
    }
  }

  getTipoPagoClass(estado: string): string {
    switch (estado.toUpperCase()) {
      case 'CONTADO': return 'text-green-600 font-medium';
      case 'CREDITO': return 'text-blue-600 font-medium';
      default: return 'text-gray-600 font-medium';
    }
  }
}