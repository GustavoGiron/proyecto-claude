import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { Router } from '@angular/router';
import { ClienteService } from '../../services/cliente/cliente.service';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { ProductoService } from '../../services/producto/producto.service';
import { VentaService } from '../../services/venta/venta.service';
import { Cliente } from '../../models/cliente/cliente';
import { Vendedor } from '../../models/vendedor/vendedor';
import { Producto } from '../../models/producto/producto';
import { VentaRequest } from '../../models/venta/venta';

declare var toastr: any;

@Component({
  selector: 'app-form-venta',
  templateUrl: './form-venta.component.html'
})
export class FormVentaComponent implements OnInit {
  ventaForm: FormGroup;
  loading = false;
  clientes: Cliente[] = [];
  vendedores: Vendedor[] = [];
  productos: Producto[] = [];
  clienteSeleccionado: Cliente | null = null;
  totalVenta = 0;
  tiposPagoDisponibles: string[] = [];

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private clienteService: ClienteService,
    private vendedorService: VendedorService,
    private productoService: ProductoService,
    private ventaService: VentaService
  ) {
    this.ventaForm = this.fb.group({
      fecha_venta: ['', Validators.required],
      fecha_salida_bodega: [''],
      numero_envio: ['', Validators.required],
      cliente_id: ['', Validators.required],
      nit_cliente: [{ value: '', disabled: true }],
      tipo_pago: ['', Validators.required],
      dias_credito: [0, [Validators.required, Validators.min(0)]],
      vendedor_id: ['', Validators.required],
      numero_factura_dte: [''],
      nombre_factura: [''],
      nit_factura: [''],
      observaciones: [''],
      productos: this.fb.array([])
    });
  }

  ngOnInit(): void {
    this.cargarDatosIniciales();
    this.configurarEventos();
    this.establecerFechaActual();
    this.agregarProductoVacio();
  }

  establecerFechaActual(): void {
    const hoy = new Date();
    const fechaFormateada = hoy.toISOString().split('T')[0];
    this.ventaForm.patchValue({
      fecha_venta: fechaFormateada
    });
  }

  cargarDatosIniciales(): void {
    this.loading = true;

    // Cargar clientes
    this.clienteService.obtenerClientes().subscribe({
      next: (clientes) => {
        this.clientes = clientes;
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        toastr.error('Error al cargar la lista de clientes');
      }
    });

    // Cargar vendedores
    this.vendedorService.obtenerVendedores().subscribe({
      next: (vendedores) => {
        this.vendedores = vendedores;
      },
      error: (err) => {
        console.error('Error al cargar vendedores:', err);
        toastr.error('Error al cargar la lista de vendedores');
      }
    });

    // Cargar productos
    this.productoService.obtenerProductos().subscribe({
      next: (productos) => {
        this.productos = productos;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar productos:', err);
        toastr.error('Error al cargar la lista de productos');
        this.loading = false;
      }
    });
  }

  configurarEventos(): void {
    // Escuchar cambios en cliente seleccionado
    this.ventaForm.get('cliente_id')?.valueChanges.subscribe(clienteId => {
      this.onClienteChange(clienteId);
    });

    // Escuchar cambios en tipo de pago
    this.ventaForm.get('tipo_pago')?.valueChanges.subscribe(tipoPago => {
      this.onTipoPagoChange(tipoPago);
    });
  }

  onClienteChange(clienteId: string): void {
    if (clienteId) {
      this.clienteSeleccionado = this.clientes.find(c => c.id?.toString() === clienteId) || null;

      if (this.clienteSeleccionado) {
        this.ventaForm.patchValue({
          nit_cliente: this.clienteSeleccionado.nit || ''
        });

        this.tiposPagoDisponibles = this.obtenerTiposPagoDisponibles();
        this.ventaForm.get('tipo_pago')?.setValue('');
        
        if (this.tiposPagoDisponibles.length === 1) {
          this.ventaForm.get('tipo_pago')?.setValue(this.tiposPagoDisponibles[0]);
        }
      }
    } else {
      this.clienteSeleccionado = null;
      this.tiposPagoDisponibles = [];
      this.ventaForm.patchValue({
        nit_cliente: '',
        tipo_pago: ''
      });
    }
  }

  obtenerTiposPagoDisponibles(): string[] {
    if (!this.clienteSeleccionado) {
      return [];
    }

    const tiposPago: string[] = [];
    
    if (this.clienteSeleccionado.tipo_venta_autoriz === 'Contado') {
      tiposPago.push('Contado');
    }

    if (this.clienteSeleccionado.tipo_venta_autoriz === 'Credito') {
      tiposPago.push('Credito');
    }

    if (this.clienteSeleccionado.tipo_venta_autoriz === 'Ambas') {
      tiposPago.push('Contado');
      tiposPago.push('Credito');
    }

    return tiposPago;
  }

  esTipoPagoDisponible(tipoPago: string): boolean {
    return this.tiposPagoDisponibles.includes(tipoPago);
  }

  onTipoPagoChange(tipoPago: string): void {
    const diasCreditoControl = this.ventaForm.get('dias_credito');

    if (tipoPago === 'Contado') {
      diasCreditoControl?.setValue(0);
      diasCreditoControl?.disable();
    } else if (tipoPago === 'Credito') {
      diasCreditoControl?.enable();
      if (diasCreditoControl?.value === 0) {
        diasCreditoControl?.setValue(30); // Valor por defecto para crédito
      }
    }
  }

  get productosFormArray(): FormArray {
    return this.ventaForm.get('productos') as FormArray;
  }

  crearProductoFormGroup(): FormGroup {
    return this.fb.group({
      producto_id: ['', Validators.required],
      cantidad_fardos: [0, [Validators.required, Validators.min(1)]],
      unidades_por_fardo: [{ value: 0, disabled: true }],
      unidades_totales: [{ value: 0, disabled: true }],
      precio_por_fardo_paquete: [0, [Validators.required, Validators.min(0.01)]],
      subtotal: [{ value: 0, disabled: true }]
    });
  }

  agregarProductoVacio(): void {
    const productoGroup = this.crearProductoFormGroup();
    this.configurarCalculosProducto(productoGroup, this.productosFormArray.length);
    this.productosFormArray.push(productoGroup);
  }

  configurarCalculosProducto(productoGroup: FormGroup, index: number): void {
    // Escuchar cambios en producto seleccionado
    productoGroup.get('producto_id')?.valueChanges.subscribe(productoId => {
      this.onProductoChange(productoId, productoGroup);
    });

    // Escuchar cambios en cantidad de fardos
    productoGroup.get('cantidad_fardos')?.valueChanges.subscribe(() => {
      this.calcularUnidadesTotales(productoGroup);
      this.calcularSubtotal(productoGroup);
    });

    // Escuchar cambios en precio unitario
    productoGroup.get('precio_por_fardo_paquete')?.valueChanges.subscribe(() => {
      this.calcularSubtotal(productoGroup);
    });
  }

  onProductoChange(productoId: string, productoGroup: FormGroup): void {
    if (productoId) {
      const producto = this.productos.find(p => p.id?.toString() === productoId);

      if (producto) {
        productoGroup.patchValue({
          unidades_por_fardo: producto.unidades_por_fardo_paquete
        });
        this.calcularUnidadesTotales(productoGroup);
        this.calcularSubtotal(productoGroup);
      }
    } else {
      productoGroup.patchValue({
        unidades_por_fardo: 0,
        unidades_totales: 0,
        subtotal: 0
      });
      this.calcularTotalVenta();
    }
  }

  calcularUnidadesTotales(productoGroup: FormGroup): void {
    const cantidadFardos = productoGroup.get('cantidad_fardos')?.value || 0;
    const unidadesPorFardo = productoGroup.get('unidades_por_fardo')?.value || 0;
    const unidadesTotales = cantidadFardos * unidadesPorFardo;

    productoGroup.patchValue({
      unidades_totales: unidadesTotales
    });
  }

  calcularSubtotal(productoGroup: FormGroup): void {
    const cantidadFardos = productoGroup.get('cantidad_fardos')?.value || 0;
    const precioFardoPaquete = productoGroup.get('precio_por_fardo_paquete')?.value || 0;
    const subtotal = cantidadFardos * precioFardoPaquete;

    productoGroup.patchValue({
      subtotal: subtotal
    });

    this.calcularTotalVenta();
  }

  calcularTotalVenta(): void {
    this.totalVenta = 0;

    this.productosFormArray.controls.forEach(control => {
      const subtotal = control.get('subtotal')?.value || 0;
      this.totalVenta += subtotal;
    });

    // Aplicar IVA del 12%
    const IVA = 0.12;
    this.totalVenta += this.totalVenta * IVA;
  }

  agregarProducto(): void {
    this.agregarProductoVacio();
  }

  eliminarProducto(index: number): void {
    if (this.productosFormArray.length > 1) {
      this.productosFormArray.removeAt(index);
      this.calcularTotalVenta();
    } else {
      toastr.warning('Debe mantener al menos un producto en la venta');
    }
  }

  onSubmit(): void {
    if (this.ventaForm.invalid) {
      this.marcarCamposComoTocados();
      toastr.error('Por favor complete todos los campos requeridos');
      return;
    }

    // Validar productos válidos
    const detalles = this.productosFormArray.controls
      .filter(control => {
        const productoId = control.get('producto_id')?.value;
        const cantidad = control.get('cantidad_fardos')?.value || 0;
        return productoId && cantidad > 0;
      })
      .map(control => {
        const value = control.getRawValue();
        return {
          producto_id: parseInt(value.producto_id),
          cantidad: value.cantidad_fardos,
          precio_por_fardo_paquete: parseFloat(value.precio_por_fardo_paquete)
        };
      });

    if (detalles.length === 0) {
      toastr.error('Debe agregar al menos un producto válido a la venta');
      return;
    }

    // Construir solo los campos aceptados por el backend
    const ventaData: VentaRequest = {
      cliente_id: parseInt(this.ventaForm.get('cliente_id')?.value),
      vendedor_id: parseInt(this.ventaForm.get('vendedor_id')?.value),
      tipo_pago: this.ventaForm.get('tipo_pago')?.value === 'Credito' ? 'Credito' : 'Contado',
      dias_credito: parseInt(this.ventaForm.get('dias_credito')?.value) || 0,

      fecha_venta: this.ventaForm.get('fecha_venta')?.value || undefined,

      numero_factura_dte: this.ventaForm.get('numero_factura_dte')?.value || '',
      nombre_factura: this.ventaForm.get('nombre_factura')?.value || '',
      nit_cliente: this.ventaForm.get('nit_cliente')?.value || '',
      nit_factura: this.ventaForm.get('nit_factura')?.value || '',

      detalles
    };

    this.loading = true;

    this.ventaService.crearVenta(ventaData).subscribe({
      next: () => {
        this.loading = false;
        toastr.success('¡Venta registrada exitosamente!');
        setTimeout(() => this.router.navigate(['/dashboard-procesos']), 2000);
      },
      error: (err) => {
        this.loading = false;
        console.error('Error al crear venta:', err);
        const msg = err.error?.error || 'Error al procesar la solicitud';
        toastr.error(msg);
      }
    });
  }

  marcarCamposComoTocados(): void {
    Object.keys(this.ventaForm.controls).forEach(key => {
      const control = this.ventaForm.get(key);
      if (control) {
        control.markAsTouched();
      }
    });

    // Marcar también los productos
    this.productosFormArray.controls.forEach(control => {
      Object.keys(control.value).forEach(key => {
        const field = control.get(key);
        if (field) {
          field.markAsTouched();
        }
      });
    });
  }

  cancelar(): void {
    this.router.navigate(['/dashboard-procesos']);
  }

  // Métodos auxiliares para validación en template
  esInvalido(campo: string): boolean {
    const control = this.ventaForm.get(campo);
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  esInvalidoProducto(index: number, campo: string): boolean {
    const control = this.productosFormArray.at(index).get(campo);
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  obtenerMensajeError(campo: string): string {
    const control = this.ventaForm.get(campo);
    if (control?.errors) {
      if (control.errors['required']) {
        return 'Este campo es requerido';
      }
      if (control.errors['min']) {
        return 'El valor debe ser mayor a 0';
      }
    }
    return '';
  }

  obtenerProductoNombre(productoId: string): string {
    const producto = this.productos.find(p => p.id?.toString() === productoId);
    return producto ? `${producto.codigo_producto} - ${producto.nombre_producto}` : '';
  }
}