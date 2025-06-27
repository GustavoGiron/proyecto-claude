import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthService } from './auth.service';
import { PermissionsResponse, Permission, Module } from '../../models/auth/auth';

@Injectable({
  providedIn: 'root'
})
export class PermissionService {
  private permissionsSubject = new BehaviorSubject<PermissionsResponse | null>(null);
  public permissions$ = this.permissionsSubject.asObservable();

  constructor(private authService: AuthService) {}

  loadPermissions(): Observable<PermissionsResponse> {
    return this.authService.getPermissions().pipe(
      map(permissions => {
        this.permissionsSubject.next(permissions);
        return permissions;
      })
    );
  }

  hasPermission(module: string, action: string): boolean {
    const permissions = this.permissionsSubject.value;
    if (!permissions) {
      return false;
    }

    return permissions.permissions.some(
      p => p.module === module && p.action === action
    );
  }

  hasModule(moduleName: string): boolean {
    const permissions = this.permissionsSubject.value;
    if (!permissions) {
      return false;
    }

    return permissions.modules.some(m => m.nombre === moduleName);
  }

  getModules(): Module[] {
    const permissions = this.permissionsSubject.value;
    return permissions ? permissions.modules : [];
  }

  getPermissions(): Permission[] {
    const permissions = this.permissionsSubject.value;
    return permissions ? permissions.permissions : [];
  }

  getUserRole(): string | null {
    const permissions = this.permissionsSubject.value;
    return permissions ? permissions.role : null;
  }

  clearPermissions(): void {
    this.permissionsSubject.next(null);
  }
}