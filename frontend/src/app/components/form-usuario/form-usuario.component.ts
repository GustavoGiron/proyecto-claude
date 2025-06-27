import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../services/usuario/user.service';
import { User } from '../../models/usuario/user.model';

declare var toastr: any;

@Component({
  selector: 'app-form-usuario',
  templateUrl: './form-usuario.component.html',
  styleUrls: ['./form-usuario.component.css']
})
export class FormUsuarioComponent implements OnInit {
  usuarioForm: FormGroup;
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
    private userService: UserService
  ) {
    this.usuarioForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      password: ['', Validators.required],
      role_id: [null, Validators.required],
      is_active: [true],
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.modo = params['modo'];
      this.id = params['id'];
      this.esCrear = !this.id;
      this.esVer = this.modo === 'ver';
      this.esEditar = this.modo === 'editar';

      if (this.id) this.cargarUsuario();

      if (this.esVer) {
        this.usuarioForm.disable();
      } else if (this.esEditar) {
        this.usuarioForm.get('username')?.disable();
        this.usuarioForm.get('password')?.enable();
      }
    });
  }

  cargarUsuario(): void {
    this.loading = true;
    this.error = null;

    this.userService.getById(this.id).subscribe({
      next: (usuario) => {
        this.usuarioForm.patchValue({
          username: usuario.username,
          email: usuario.email,
          nombre: usuario.nombre,
          apellido: usuario.apellido,
          role_id: usuario.role, // Ajusta si es necesario
          is_active: usuario.is_active
        });
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar usuario:', err);
        this.error = err.message;
        this.loading = false;
        toastr.error('Error al cargar los datos del usuario');
      }
    });
  }

  onSubmit(): void {
    if (this.esVer || this.usuarioForm.invalid) return;

    const usuarioData = this.usuarioForm.getRawValue();

    // Si está en modo edición y el campo password está vacío, eliminarlo del objeto
    if (this.esEditar && (!usuarioData.password || usuarioData.password.trim() === '')) {
      delete usuarioData.password;
    }

    if (this.esCrear) {
      this.userService.create(usuarioData).subscribe({
        next: () => {
          toastr.success('¡Usuario creado exitosamente!');
          this.usuarioForm.reset();
          setTimeout(() => this.router.navigate(['/lista-usuario']), 2000);
        },
        error: (err) => {
          const msg = err.error?.error || 'Error al crear usuario';
          toastr.error(msg);
        }
      });
    } else {
      this.userService.update(this.id, usuarioData).subscribe({
        next: () => {
          toastr.success('¡Usuario actualizado exitosamente!');
          setTimeout(() => this.router.navigate(['/lista-usuario']), 2000);
        },
        error: (err) => {
          const msg = err.error?.error || 'Error al actualizar usuario';
          toastr.error(msg);
        }
      });
    }
  }

  // onSubmit(): void {
  //   if (this.esVer || this.usuarioForm.invalid) return;

  //   const formData = this.usuarioForm.getRawValue();
  //   if (this.esCrear) {
  //     this.userService.create(formData).subscribe({
  //       next: () => {
  //         toastr.success('Usuario creado exitosamente');
  //         this.usuarioForm.reset();
  //         setTimeout(() => this.router.navigate(['/lista-usuario']), 2000);
  //       },
  //       error: (err) => {
  //         const msg = err.error?.error || 'Error al procesar la solicitud';
  //         toastr.error(msg);
  //       }
  //     });
  //   } else {
  //     this.userService.update(this.id, formData).subscribe({
  //       next: () => {
  //         toastr.success('Usuario actualizado exitosamente');
  //         setTimeout(() => this.router.navigate(['/lista-usuario']), 2000);
  //       },
  //       error: (err) => {
  //         const msg = err.error?.error || 'Error al procesar la solicitud';
  //         toastr.error(msg);
  //       }
  //     });
  //   }
  // }

  getTitulo(): string {
    if (this.esCrear) return 'Nuevo Usuario';
    if (this.esVer) return 'Ver Usuario';
    if (this.esEditar) return 'Editar Usuario';
    return 'Usuario';
  }

  cancelar(): void {
    this.router.navigate(['/lista-usuario']);
  }

  aceptar(): void {
    this.router.navigate(['/lista-usuario']);
  }
}
