import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ProductoService } from '../../services/producto/producto.service';
import { Producto } from '../../models/producto/producto';

declare var toastr: any;

@Component({
  selector: 'app-form-producto',
  templateUrl: './form-producto.component.html'
})
export class FormProductoComponent implements OnInit {
  productoForm: FormGroup;
  loading = false;
  error: string | null = null;
  modo: string = '';
  id: number = 0;
  esCrear = false;
  esVer = false;
  esEditar = false;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private productoService: ProductoService
  ) {
    this.productoForm = this.fb.group({
      codigo_producto: ['', Validators.required],
      nombre_producto: ['', Validators.required],
      unidad_medida: ['', Validators.required],
      unidades_por_fardo_paquete: [0, [Validators.required, Validators.min(1)]]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.modo = params['modo'];
      this.id = params['id'];
      this.esCrear = !this.id;
      this.esVer = this.modo === 'ver';
      this.esEditar = this.modo === 'editar';

      if (this.id) {
        this.cargarProducto();
      }

      if (this.esVer) {
        this.productoForm.disable();
      } else if (this.esEditar) {
        this.productoForm.get('codigo_producto')?.disable(); // Evitar modificar código en edición
      }
    });
  }

  cargarProducto(): void {
    this.loading = true;
    this.error = null;
  
    this.productoService.obtenerProducto(this.id).subscribe({
      next: (producto) => {
  
        this.productoForm.patchValue({
          codigo_producto: producto.codigo_producto || '',
          nombre_producto: producto.nombre_producto || '',
          unidad_medida: producto.unidad_medida || '',
          unidades_por_fardo_paquete: producto.unidades_por_fardo_paquete || 0
        });
  
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar producto:', err);
        this.error = err.message;
        this.loading = false;
        toastr.error('Error al cargar los datos del producto', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }
  

  onSubmit(): void {
    if (this.esVer || this.productoForm.invalid) return;

    const productoData: Producto = {
      ...this.productoForm.getRawValue()
    };

    if (this.esCrear) {
      this.productoService.crearProducto(productoData).subscribe({
        next: () => {
          toastr.success('¡Producto creado exitosamente!');
          this.productoForm.reset();
          setTimeout(() => this.router.navigate(['/lista-producto']), 2000);
        },
        error: (err) => {
          const msg = err.error?.error || 'Error al procesar la solicitud';
          toastr.error(msg);
        }
      });
    } else {
      this.productoService.actualizarProducto(this.id, productoData).subscribe({
        next: () => {
          toastr.success('¡Producto actualizado exitosamente!');
          setTimeout(() => this.router.navigate(['/lista-producto']), 2000);
        },
        error: (err) => {
          const msg = err.error?.error || 'Error al procesar la solicitud';
          toastr.error(msg);
        }
      });
    }
  }

  getTitulo(): string {
    if (this.esCrear) return 'Nuevo Producto';
    if (this.esVer) return 'Ver Producto';
    if (this.esEditar) return 'Editar Producto';
    return 'Producto';
  }

  cancelar(): void {
    this.router.navigate(['/lista-producto']);
  }

  aceptar(): void {
    this.router.navigate(['/lista-producto']);
  }
}
