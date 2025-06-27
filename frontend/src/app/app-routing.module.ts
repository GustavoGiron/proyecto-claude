import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './components/login/login.component';
import { LayoutComponent } from './components/layout/layout.component';
import { DashboardInicioComponent } from './components/dashboard-inicio/dashboard-inicio.component';
import { DashboardMantenimientosComponent } from './components/dashboard-mantenimientos/dashboard-mantenimientos.component';
import { DashboardProcesosComponent } from './components/dashboard-procesos/dashboard-procesos.component';
import { ListClienteComponent } from './components/list-cliente/list-cliente.component';
import { FormClienteComponent } from './components/form-cliente/form-cliente.component';
import { ListVendedorComponent } from './components/list-vendedor/list-vendedor.component';
import { FormVendedorComponent } from './components/form-vendedor/form-vendedor.component';
import { ListProductoComponent } from './components/list-producto/list-producto.component';
import { FormProductoComponent } from './components/form-producto/form-producto.component';
import { FormInventarioComponent } from './components/form-inventario/form-inventario.component';
import { ListaInventarioComponent } from './components/lista-inventario/lista-inventario.component';
import { FormVentaComponent } from './components/form-venta/form-venta.component';
import { RegistrarSalidaComponent } from './components/registrar-salida/registrar-salida.component';
import { RegistrarPagoComponent } from './components/registrar-pago/registrar-pago.component';
import { FormUsuarioComponent } from './components/form-usuario/form-usuario.component';
import { ListUsuarioComponent } from './components/list-usuario/list-usuario.component';

const routes: Routes = [
  // Ruta pública para login
  { path: 'login', component: LoginComponent },
  
  // Rutas protegidas con layout
  {
    path: '',
    component: LayoutComponent,
    canActivate: [AuthGuard],
    children: [
      { path: 'dashboard', component: DashboardInicioComponent },
      { path: 'dashboard-inicio', component: DashboardInicioComponent },
      { path: 'dashboard-mantenimientos', component: DashboardMantenimientosComponent },
      { path: 'dashboard-procesos', component: DashboardProcesosComponent },
      { path: 'formulario-cliente', component: FormClienteComponent },
      { path: 'formulario-cliente/:modo/:id', component: FormClienteComponent },
      { path: 'lista-cliente', component: ListClienteComponent },
      { path: 'clientes', component: ListClienteComponent },
      { path: 'formulario-vendedor', component: FormVendedorComponent },
      { path: 'formulario-vendedor/:modo/:id', component: FormVendedorComponent },
      { path: 'lista-vendedor', component: ListVendedorComponent },
      { path: 'vendedores', component: ListVendedorComponent },
      { path: 'formulario-producto', component: FormProductoComponent },
      { path: 'formulario-producto/:modo/:id', component: FormProductoComponent },
      { path: 'lista-producto', component: ListProductoComponent },
      { path: 'productos', component: ListProductoComponent },
      { path: 'ingreso-inventario', component: FormInventarioComponent },
      { path: 'lista-inventario', component: ListaInventarioComponent },
      { path: 'inventario', component: ListaInventarioComponent },
      { path: 'registro-venta', component: FormVentaComponent },
      { path: 'ventas', component: FormVentaComponent },
      { path: 'registrar-salida', component: RegistrarSalidaComponent },
      { path: 'salidas', component: RegistrarSalidaComponent },
      { path: 'registrar-pago', component: RegistrarPagoComponent },
      { path: 'pagos', component: RegistrarPagoComponent },
      { path: 'form-usuario', component: FormUsuarioComponent },
      { path: 'form-usuario/:modo/:id', component: FormUsuarioComponent },
      { path: 'lista-usuario', component: ListUsuarioComponent },
      { path: 'usuarios', component: ListUsuarioComponent },
      
      // Redirección por defecto dentro del layout
      { path: '', redirectTo: '/dashboard', pathMatch: 'full' }
    ]
  },
  
  // Catch-all redirect
  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
