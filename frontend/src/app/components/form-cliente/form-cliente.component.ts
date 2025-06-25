import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ClienteService } from '../../services/cliente/cliente.service';
import { DepartamentoService } from '../../services/departamento/departamento.service';
import { Cliente } from '../../models/cliente/cliente';
import { Departamento, Municipio } from '../../models/departamento/departamento';

declare var toastr: any;

@Component({
  selector: 'app-form-cliente',
  templateUrl: './form-cliente.component.html'
})
export class FormClienteComponent implements OnInit {
  clienteForm: FormGroup;
  loading = false;
  error: string | null = null;
  modo: string = '';
  id: string = '';
  esCrear = false;
  esVer = false;
  esEditar = false;

  // Listas para los dropdowns
  departamentos: Departamento[] = [];
  municipios: Municipio[] = [];
  loadingDepartamentos = false;
  loadingMunicipios = false;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private clienteService: ClienteService,
    private departamentoService: DepartamentoService
  ) {
    this.clienteForm = this.fb.group({
      nombre_contacto: ['', Validators.required],
      nombre_negocio: [''],
      departamento_id: ['', Validators.required],
      municipio_id: ['', Validators.required],
      direccion: [''],
      nit: [''],
      encargado_bodega: [''],
      telefono: ['', [Validators.required, Validators.pattern(/^\d+$/)]], 
      tipo_venta_autoriz: ['', Validators.required],
      observaciones: ['']
    });
  }

  ngOnInit(): void {
    this.cargarDepartamentos();

    this.route.params.subscribe(params => {
      this.modo = params['modo'];
      this.id = params['id'];
      this.esCrear = !this.id;
      this.esVer = this.modo === 'ver';
      this.esEditar = this.modo === 'editar';

      if (this.id) {
        this.cargarCliente();
      }

      if (this.esVer) {
        this.clienteForm.disable();
      }
    });

    // Escuchar cambios en departamento para cargar municipios
    this.clienteForm.get('departamento_id')?.valueChanges.subscribe(departamentoId => {
      if (departamentoId) {
        this.cargarMunicipios(Number(departamentoId));
        this.clienteForm.get('municipio_id')?.setValue('');
        this.clienteForm.get('municipio_id')?.enable();
      } else {
        this.municipios = [];
        this.clienteForm.get('municipio_id')?.disable();
      }
    });

    this.clienteForm.get('municipio_id')?.disable();
  }

  cargarDepartamentos(): void {
    this.loadingDepartamentos = true;

    this.clienteForm.get('departamento_id')?.disable();

    this.departamentoService.obtenerDepartamentos().subscribe({
      next: (departamentos: Departamento[]) => {
       
        this.departamentos = departamentos;
        this.loadingDepartamentos = false;

        if (!this.esVer) {
          this.clienteForm.get('departamento_id')?.enable();
        }
      },
      error: (err) => {
        console.error('Error al cargar departamentos:', err);
        this.loadingDepartamentos = false;
        this.departamentos = [];

        if (!this.esVer) {
          this.clienteForm.get('departamento_id')?.enable();
        }

        toastr.error('Error al cargar departamentos', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  cargarMunicipios(departamentoId: number): void {
    this.loadingMunicipios = true;
  

    this.clienteForm.get('municipio_id')?.disable();

    this.departamentoService.obtenerMunicipiosPorDepartamento(departamentoId).subscribe({
      next: (municipios: Municipio[]) => {
        this.municipios = municipios;
        this.loadingMunicipios = false;

        if (!this.esVer) {
          this.clienteForm.get('municipio_id')?.enable();
        }
      },
      error: (err) => {
        console.error('Error al cargar municipios:', err);
        this.loadingMunicipios = false;
        this.municipios = [];

        if (!this.esVer) {
          this.clienteForm.get('municipio_id')?.enable();
        }

        toastr.error('Error al cargar municipios', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  cargarCliente(): void {
    this.loading = true;
    this.error = null;

    this.clienteService.obtenerCliente(this.id).subscribe({
      next: (cliente) => {

        this.clienteForm.patchValue({
          nombre_contacto: cliente.nombre_contacto || '',
          nombre_negocio: cliente.nombre_negocio || '',
          departamento_id: cliente.departamento_id || '',
          municipio_id: cliente.municipio_id || '',
          direccion: cliente.direccion || '',
          nit: cliente.nit || '',
          encargado_bodega: cliente.encargado_bodega || '',
          telefono: cliente.telefono || '',
          tipo_venta_autoriz: cliente.tipo_venta_autoriz || '',
          observaciones: cliente.observaciones || ''
        });

        if (cliente.departamento_id) {
          this.cargarMunicipios(Number(cliente.departamento_id));
        }

        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar cliente:', err);
        this.error = err.message;
        this.loading = false;
        toastr.error('Error al cargar los datos del cliente', '', {
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

    if (this.clienteForm.valid) {
      const clienteData: Cliente = this.clienteForm.value;

      if (this.esCrear) {
        this.clienteService.crearCliente(clienteData).subscribe({
          next: (response) => {
            toastr.success('¡Cliente creado exitosamente!', '', {
              positionClass: 'toast-top-right',
              timeOut: 1000,
              closeButton: false,
              progressBar: false
            });

            this.clienteForm.reset();

            setTimeout(() => {
              this.router.navigate(['/lista-cliente']);
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
        this.clienteService.actualizarCliente(this.id, clienteData).subscribe({
          next: (response) => {
            toastr.success('¡Cliente actualizado exitosamente!', '', {
              positionClass: 'toast-top-right',
              timeOut: 1000,
              closeButton: false,
              progressBar: false
            });

            setTimeout(() => {
              this.router.navigate(['/lista-cliente']);
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
    if (this.esCrear) return 'Nuevo Cliente';
    if (this.esVer) return 'Ver Cliente';
    if (this.esEditar) return 'Editar Cliente';
    return 'Cliente';
  }

  cancelar(): void {
    this.router.navigate(['/lista-cliente']);
  }

  aceptar(): void {
    this.router.navigate(['/lista-cliente']);
  }
}