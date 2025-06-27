import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { PermissionService } from '../../services/auth/permission.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  error = '';
  returnUrl = '';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private permissionService: PermissionService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });

    // Redirigir al dashboard si ya está autenticado
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnInit(): void {
    // Obtener la URL de retorno de los query params
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';

    const credentials = {
      username: this.loginForm.value.username,
      password: this.loginForm.value.password
    };

    this.authService.login(credentials).subscribe({
      next: (response) => {
        // Cargar permisos después del login exitoso
        this.permissionService.loadPermissions().subscribe({
          next: () => {
            this.router.navigate([this.returnUrl]);
          },
          error: (error) => {
            console.error('Error loading permissions:', error);
            // Incluso si falla la carga de permisos, redirigir al dashboard
            this.router.navigate([this.returnUrl]);
          }
        });
      },
      error: (error) => {
        this.loading = false;
        if (error.status === 401) {
          this.error = 'Usuario o contraseña incorrectos';
        } else if (error.status === 400) {
          this.error = 'Datos inválidos';
        } else {
          this.error = 'Error al iniciar sesión. Intente nuevamente.';
        }
        console.error('Login error:', error);
      }
    });
  }

  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }
}