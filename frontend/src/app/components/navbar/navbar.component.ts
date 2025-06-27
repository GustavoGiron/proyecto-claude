import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { AuthService } from '../../services/auth/auth.service';
import { PermissionService } from '../../services/auth/permission.service';
import { User, Module } from '../../models/auth/auth';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {
  currentUser: User | null = null;
  modules: Module[] = [];
  private subscriptions: Subscription[] = [];

  constructor(
    private authService: AuthService,
    private permissionService: PermissionService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Suscribirse al usuario actual
    this.subscriptions.push(
      this.authService.currentUser$.subscribe(user => {
        this.currentUser = user;
      })
    );

    // Suscribirse a los permisos
    this.subscriptions.push(
      this.permissionService.permissions$.subscribe(permissions => {
        this.modules = permissions ? permissions.modules : [];
      })
    );

    // Cargar permisos si no están cargados
    if (this.authService.isAuthenticated() && this.modules.length === 0) {
      this.permissionService.loadPermissions().subscribe();
    }
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.permissionService.clearPermissions();
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Logout error:', error);
        // Incluso si falla, limpiar y redirigir
        this.permissionService.clearPermissions();
        this.router.navigate(['/login']);
      }
    });
  }

  hasModule(moduleName: string): boolean {
    return this.permissionService.hasModule(moduleName);
  }

  getUserDisplayName(): string {
    if (!this.currentUser) return '';
    return `${this.currentUser.nombre} ${this.currentUser.apellido}`;
  }
}
