import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { Vendedor } from '../../models/vendedor/vendedor';

declare var toastr: any;

@Component({
  selector: 'app-form-vendedor',
  templateUrl: './form-vendedor.component.html'
})
export class FormVendedorComponent implements OnInit {
  vendedorForm: FormGroup;
  loading = false;
  error: string | null = null;
  modo: string = '';
  id: string = '';
  esCrear = false;
  esVer = false;
  esEditar = false;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private vendedorService: VendedorService
  ) {
    this.vendedorForm = this.fb.group({
      nombres: ['', Validators.required],
      apellidos: ['', Validators.required],
      telefono: ['', [Validators.required, Validators.pattern(/^\d+$/)]], 
      porcentaje_comision: ['', Validators.required],
      direccion: ['']
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
        this.cargarVendedor();
      }

      if (this.esVer) {
        this.vendedorForm.disable();
      }
    });
  }

  cargarVendedor(): void {
    this.loading = true;
    this.error = null;

    this.vendedorService.obtenerVendedor(this.id).subscribe({
      next: (response) => {
        console.log('Respuesta del backend:', response);
        this.vendedorForm.patchValue({
          nombres: response.nombres || '',
          apellidos: response.apellidos || '',
          telefono: response.telefono || '',
          porcentaje_comision: response.porcentaje_comision || '',
          direccion: response.direccion || ''
        });
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar vendedor:', err);
        this.error = err.message;
        this.loading = false;
        toastr.error('Error al cargar los datos del vendedor', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  onSubmit(): void {
    if (this.esVer) return;

    if (this.vendedorForm.valid) {
      const vendedorData: Vendedor = this.vendedorForm.value;

      if (this.esCrear) {
        this.vendedorService.crearVendedor(vendedorData).subscribe({
          next: (response) => {
            toastr.success('¡Vendedor creado exitosamente!', '', {
              positionClass: 'toast-top-right',
              timeOut: 1000,
              closeButton: false,
              progressBar: false
            });

            this.vendedorForm.reset();

            setTimeout(() => {
              this.router.navigate(['/lista-vendedor']);
            }, 2000);
          },
          error: (err) => {
            const errorMessage = err.error?.error || 'Error al procesar la solicitud';
            toastr.error(errorMessage, '', {
              positionClass: 'toast-top-right',
              timeOut: 3000,
              closeButton: false,
              progressBar: false
            });
          }
        });
      } else {
        this.vendedorService.actualizarVendedor(this.id, vendedorData).subscribe({
          next: (response) => {
            toastr.success('¡Vendedor actualizado exitosamente!', '', {
              positionClass: 'toast-top-right',
              timeOut: 1000,
              closeButton: false,
              progressBar: false
            });

            setTimeout(() => {
              this.router.navigate(['/lista-vendedor']);
            }, 2000);
          },
          error: (err) => {
            const errorMessage = err.error?.error || 'Error al procesar la solicitud';
            toastr.error(errorMessage, '', {
              positionClass: 'toast-top-right',
              timeOut: 3000,
              closeButton: false,
              progressBar: false
            });
          }
        });
      }
    }
  }

  getTitulo(): string {
    if (this.esCrear) return 'Nuevo Vendedor';
    if (this.esVer) return 'Ver Vendedor';
    if (this.esEditar) return 'Editar Vendedor';
    return 'Vendedor';
  }

  cancelar(): void {
    this.router.navigate(['/lista-vendedor']);
  }

  aceptar(): void {
    this.router.navigate(['/lista-vendedor']);
  }
}