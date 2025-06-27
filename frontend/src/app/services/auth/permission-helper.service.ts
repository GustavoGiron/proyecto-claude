import { Injectable } from '@angular/core';
import { PermissionService } from './permission.service';

@Injectable({
  providedIn: 'root'
})
export class PermissionHelperService {
  constructor(private permissionService: PermissionService) {}

  // Métodos específicos para cada módulo
  canViewClientes(): boolean {
    return this.permissionService.hasPermission('Clientes', 'read');
  }

  canCreateClientes(): boolean {
    return this.permissionService.hasPermission('Clientes', 'create');
  }

  canUpdateClientes(): boolean {
    return this.permissionService.hasPermission('Clientes', 'update');
  }

  canDeleteClientes(): boolean {
    return this.permissionService.hasPermission('Clientes', 'delete');
  }

  canViewProductos(): boolean {
    return this.permissionService.hasPermission('Productos', 'read');
  }

  canCreateProductos(): boolean {
    return this.permissionService.hasPermission('Productos', 'create');
  }

  canUpdateProductos(): boolean {
    return this.permissionService.hasPermission('Productos', 'update');
  }

  canDeleteProductos(): boolean {
    return this.permissionService.hasPermission('Productos', 'delete');
  }

  canViewInventario(): boolean {
    return this.permissionService.hasPermission('Inventario', 'read');
  }

  canCreateInventario(): boolean {
    return this.permissionService.hasPermission('Inventario', 'create');
  }

  canUpdateInventario(): boolean {
    return this.permissionService.hasPermission('Inventario', 'update');
  }

  canDeleteInventario(): boolean {
    return this.permissionService.hasPermission('Inventario', 'delete');
  }

  canViewVentas(): boolean {
    return this.permissionService.hasPermission('Ventas', 'read');
  }

  canCreateVentas(): boolean {
    return this.permissionService.hasPermission('Ventas', 'create');
  }

  canUpdateVentas(): boolean {
    return this.permissionService.hasPermission('Ventas', 'update');
  }

  canDeleteVentas(): boolean {
    return this.permissionService.hasPermission('Ventas', 'delete');
  }

  canViewVendedores(): boolean {
    return this.permissionService.hasPermission('Vendedores', 'read');
  }

  canCreateVendedores(): boolean {
    return this.permissionService.hasPermission('Vendedores', 'create');
  }

  canUpdateVendedores(): boolean {
    return this.permissionService.hasPermission('Vendedores', 'update');
  }

  canDeleteVendedores(): boolean {
    return this.permissionService.hasPermission('Vendedores', 'delete');
  }

  canViewPagos(): boolean {
    return this.permissionService.hasPermission('Pagos', 'read');
  }

  canCreatePagos(): boolean {
    return this.permissionService.hasPermission('Pagos', 'create');
  }

  canUpdatePagos(): boolean {
    return this.permissionService.hasPermission('Pagos', 'update');
  }

  canDeletePagos(): boolean {
    return this.permissionService.hasPermission('Pagos', 'delete');
  }

  canViewReportes(): boolean {
    return this.permissionService.hasPermission('Reportes', 'read');
  }

  canUpdateConfiguracion(): boolean {
    return this.permissionService.hasPermission('Configuración', 'update');
  }

  // Verificar acceso a módulos
  hasModuleDashboard(): boolean {
    return this.permissionService.hasModule('Dashboard');
  }

  hasModuleClientes(): boolean {
    return this.permissionService.hasModule('Clientes');
  }

  hasModuleProductos(): boolean {
    return this.permissionService.hasModule('Productos');
  }

  hasModuleInventario(): boolean {
    return this.permissionService.hasModule('Inventario');
  }

  hasModuleIngresos(): boolean {
    return this.permissionService.hasModule('Ingresos');
  }

  hasModuleSalidas(): boolean {
    return this.permissionService.hasModule('Salidas');
  }

  hasModuleVentas(): boolean {
    return this.permissionService.hasModule('Ventas');
  }

  hasModulePagos(): boolean {
    return this.permissionService.hasModule('Pagos');
  }

  hasModuleVendedores(): boolean {
    return this.permissionService.hasModule('Vendedores');
  }

  hasModuleReportes(): boolean {
    return this.permissionService.hasModule('Reportes');
  }

  hasModuleConfiguracion(): boolean {
    return this.permissionService.hasModule('Configuración');
  }

  // Verificar si es administrador
  isAdmin(): boolean {
    return this.permissionService.getUserRole() === 'Gerencia General';
  }

  // Verificar si es gerente de ventas
  isGerenteVentas(): boolean {
    return this.permissionService.getUserRole() === 'Gerencia de Ventas y Finanzas';
  }

  // Verificar si es gerente de inventario
  isGerenteInventario(): boolean {
    return this.permissionService.getUserRole() === 'Gerencia de Inventario';
  }
}