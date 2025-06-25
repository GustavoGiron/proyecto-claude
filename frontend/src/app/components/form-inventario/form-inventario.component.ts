import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductoService } from '../../services/producto/producto.service';
import { InventarioService } from '../../services/inventario/inventario.service';
import { Producto } from '../../models/producto/producto';
import { Inventario, IngresoMercancia, DetalleIngreso } from '../../models/inventario/inventario';

declare var toastr: any;

@Component({
  selector: 'app-form-inventario',
  templateUrl: './form-inventario.component.html'
})
export class FormInventarioComponent implements OnInit {
  inventarioForm: FormGroup;
  loading = false;
  productos: Producto[] = [];
  productoSeleccionado: Producto | null = null;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private productoService: ProductoService,
    private inventarioService: InventarioService
  ) {
    this.inventarioForm = this.fb.group({
      fecha_ingreso: ['', Validators.required],
      producto_id: ['', Validators.required],
      cantidad_fardos_paquetes: [0, [Validators.required, Validators.min(1)]],
      unidades_por_fardo_paquete: [{ value: 0, disabled: true }, Validators.required],
      unidades_totales: [{ value: 0, disabled: true }, Validators.required],
      numero_contenedor: ['', Validators.required],
      numero_duca: ['', Validators.required],
      fecha_duca: ['', Validators.required],
      numero_duca_rectificada: [''],
      fecha_duca_rectificada: [''],
      observaciones: ['']
    });
  }

  ngOnInit(): void {
    this.cargarProductosActivos();
    this.configurarCalculosAutomaticos();
    this.establecerFechaActual();
  }

  establecerFechaActual(): void {
    const hoy = new Date();
    const fechaFormateada = hoy.toISOString().split('T')[0];
    this.inventarioForm.patchValue({
      fecha_ingreso: fechaFormateada
    });
  }

  cargarProductosActivos(): void {
    this.loading = true;

    this.productoService.obtenerProductoActivo().subscribe({
      next: (productos) => {
        this.productos = productos;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar productos activos:', err);
        this.loading = false;
        toastr.error('Error al cargar la lista de productos activos', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  cargarProductos(): void {
    this.loading = true;

    this.productoService.obtenerProductos().subscribe({
      next: (productos) => {
        this.productos = productos;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar productos:', err);
        this.loading = false;
        toastr.error('Error al cargar la lista de productos', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  configurarCalculosAutomaticos(): void {
    // Escuchar cambios en el producto seleccionado
    this.inventarioForm.get('producto_id')?.valueChanges.subscribe(productoId => {
      this.onProductoChange(productoId);
    });

    // Escuchar cambios en cantidad de fardos para recalcular unidades totales
    this.inventarioForm.get('cantidad_fardos_paquetes')?.valueChanges.subscribe(() => {
      this.calcularUnidadesTotales();
    });
  }

  onProductoChange(productoId: string): void {
    if (productoId) {
      this.productoSeleccionado = this.productos.find(p => p.id?.toString() === productoId) || null;
      
      if (this.productoSeleccionado) {
        this.inventarioForm.patchValue({
          unidades_por_fardo_paquete: this.productoSeleccionado.unidades_por_fardo_paquete
        });
        this.calcularUnidadesTotales();
      }
    } else {
      this.productoSeleccionado = null;
      this.inventarioForm.patchValue({
        unidades_por_fardo_paquete: 0,
        unidades_totales: 0
      });
    }
  }

  calcularUnidadesTotales(): void {
    const cantidadFardos = this.inventarioForm.get('cantidad_fardos_paquetes')?.value || 0;
    const unidadesPorFardo = this.inventarioForm.get('unidades_por_fardo_paquete')?.value || 0;
    const unidadesTotales = cantidadFardos * unidadesPorFardo;
    
    this.inventarioForm.patchValue({
      unidades_totales: unidadesTotales
    });
  }

  onSubmit(): void {
    if (this.inventarioForm.invalid) {
      this.marcarCamposComoTocados();
      toastr.error('Por favor complete todos los campos requeridos', '', {
        positionClass: 'toast-top-right',
        timeOut: 3000,
        closeButton: false,
        progressBar: false
      });
      return;
    }

    const formData = this.inventarioForm.getRawValue();
    
    const ingresoData: IngresoMercancia = {
      fecha_ingreso: formData.fecha_ingreso,
      numero_contenedor: formData.numero_contenedor,
      numero_duca: formData.numero_duca,
      fecha_duca: formData.fecha_duca,
      numero_duca_rectificada: formData.numero_duca_rectificada || undefined,
      fecha_duca_rectificada: formData.fecha_duca_rectificada || undefined,
      observaciones: formData.observaciones || undefined,
      usuario_creacion: 'usuario_actual',
      detalles: [{
        producto_id: parseInt(formData.producto_id),
        cantidad_fardos_paquetes: formData.cantidad_fardos_paquetes,
        unidades_por_fardo_paquete: formData.unidades_por_fardo_paquete,
        usuario_creacion: 'usuario_actual'
      }]
    };

    this.loading = true;

    this.inventarioService.crearIngreso(ingresoData).subscribe({
      next: () => {
        this.loading = false;
        toastr.success('¡Ingreso de inventario registrado exitosamente!', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
        this.inventarioForm.reset();
        this.establecerFechaActual();
        setTimeout(() => this.router.navigate(['/lista-inventario']), 2000);
      },
      error: (err) => {
        this.loading = false;
        console.error('Error al crear inventario:', err);
        const msg = err.error?.error || 'Error al procesar la solicitud';
        toastr.error(msg, '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  marcarCamposComoTocados(): void {
    Object.keys(this.inventarioForm.controls).forEach(key => {
      const control = this.inventarioForm.get(key);
      if (control) {
        control.markAsTouched();
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/dashboard-procesos']);
  }

  // Métodos auxiliares para validación en template
  esInvalido(campo: string): boolean {
    const control = this.inventarioForm.get(campo);
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  obtenerMensajeError(campo: string): string {
    const control = this.inventarioForm.get(campo);
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
}