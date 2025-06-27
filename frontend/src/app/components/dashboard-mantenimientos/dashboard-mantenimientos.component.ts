import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { PermissionService } from '../../services/auth/permission.service';

@Component({
  selector: 'app-dashboard-mantenimientos',
  templateUrl: './dashboard-mantenimientos.component.html',
  styleUrls: ['./dashboard-mantenimientos.component.css']
})
export class DashboardMantenimientosComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription[] = [];

  constructor(private permissionService: PermissionService) {}

  ngOnInit(): void {
    // Cargar permisos si no están cargados
    if (!this.permissionService.getPermissions().length) {
      this.subscriptions.push(
        this.permissionService.loadPermissions().subscribe()
      );
    }
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  hasPermission(module: string, action: string): boolean {
    return this.permissionService.hasPermission(module, action);
  }

  hasModule(moduleName: string): boolean {
    return this.permissionService.hasModule(moduleName);
  }
}
