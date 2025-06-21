import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { DashboardInicioComponent } from './components/dashboard-inicio/dashboard-inicio.component';
import { DashboardMantenimientosComponent } from './components/dashboard-mantenimientos/dashboard-mantenimientos.component';
import { DashboardProcesosComponent } from './components/dashboard-procesos/dashboard-procesos.component';
import { ListClienteComponent } from './components/list-cliente/list-cliente.component';
import { FormClienteComponent } from './components/form-cliente/form-cliente.component';
import { ListVendedorComponent } from './components/list-vendedor/list-vendedor.component';
import { FormVendedorComponent } from './components/form-vendedor/form-vendedor.component';

const routes: Routes = [
  { path: 'navbar', component: NavbarComponent },
  { path: 'dashboard-inicio', component: DashboardInicioComponent },
  { path: 'dashboard-mantenimientos', component: DashboardMantenimientosComponent },
  { path: 'dashboard-procesos', component: DashboardProcesosComponent },
  { path: 'formulario-cliente', component: FormClienteComponent },
  { path: 'formulario-cliente/:modo/:id', component: FormClienteComponent },
  { path: 'lista-cliente', component: ListClienteComponent },
  { path: 'formulario-vendedor', component: FormVendedorComponent },
  { path: 'formulario-vendedor/:modo/:id', component: FormVendedorComponent },
  { path: 'lista-vendedor', component: ListVendedorComponent },
  { path: '', redirectTo: '/dashboard-inicio', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }