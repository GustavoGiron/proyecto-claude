import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Venta, DetalleVenta } from '../../models/venta/venta';
import { ClienteService } from '../../services/cliente/cliente.service';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { ProductoService } from '../../services/producto/producto.service';
import { VentaService } from '../../services/venta/venta.service';

declare var toastr: any;

@Component({
  selector: 'app-registrar-salida',
  templateUrl: './registrar-salida.component.html'
})
export class RegistrarSalidaComponent implements OnInit {
  busquedaForm!: FormGroup;
  salidaForm!: FormGroup;
  loading = false;
  mostrarResultados = false;
  mostrarVentaSeleccionada = false;
  mostrarRegistroSalida = false;
  ventas: Venta[] = [];
  ventaSeleccionada: Venta | null = null;

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
  }


  private inicializarFormularios(): void {
    this.busquedaForm = this.fb.group({
      numeroEnvio: [''],
      nombreCliente: ['']
    });

    this.salidaForm = this.fb.group({
      fecha_salida_bodega: [this.getFechaHoy(), Validators.required],
      referenciaEnvio: [{ value: '', disabled: true }],
    });
  }

  private getFechaHoy(): string {
    const today = new Date();
    return today.toISOString().split('T')[0];
  }

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
    this.mostrarVentaSeleccionada = true;
    this.mostrarRegistroSalida = true;
    
    this.salidaForm.patchValue({
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

  limpiarBusqueda(): void {
    this.busquedaForm.reset();
    this.resetearEstadosVisuales();
  }

  cancelarSalida(): void {
    if (confirm('¿Está seguro de que desea cancelar el registro de salida?')) {
      this.resetearFormularioSalida();
      this.resetearSeleccionVenta();
    }
  }

  private resetearEstadosVisuales(): void {
    this.mostrarResultados = false;
    this.mostrarVentaSeleccionada = false;
    this.mostrarRegistroSalida = false;
    this.ventaSeleccionada = null;
  }

  private resetearFormularioSalida(): void {
    this.salidaForm.patchValue({
      fecha_salida_bodega: this.getFechaHoy(),
      referenciaEnvio: ''
    });
  }

  private resetearSeleccionVenta(): void {
    this.mostrarVentaSeleccionada = false;
    this.mostrarRegistroSalida = false;
    this.ventaSeleccionada = null;
  }

  confirmarSalida(): void {
    if (!this.validarDatosSalida()) {
      return;
    }

    const salidaData: Venta = this.salidaForm.value;
    
    this.ventaService.registrarSalidaBodega(this.ventaSeleccionada!.id!, salidaData).subscribe({
      next: (resp) => {
        toastr.success('Salida de bodega registrada exitosamente');
        this.resetearFormularioCompleto();
      },
      error: (err) => {
        console.error('Error al registrar salida:', err);
        toastr.error('Error al registrar salida de bodega. Por favor, intente nuevamente.');
      }
    });
  }

  private validarDatosSalida(): boolean {
    if (this.salidaForm.invalid) {
      toastr.error('Por favor, complete todos los campos requeridos.');
      return false;
    }

    if (!this.ventaSeleccionada?.id) {
      toastr.error('Error: No se ha seleccionado una venta válida.');
      return false;
    }

    return true;
  }

  private resetearFormularioCompleto(): void {
    this.busquedaForm.reset();
    this.salidaForm.patchValue({
      fecha_salida_bodega: this.getFechaHoy(),
      referenciaEnvio: ''
    });
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