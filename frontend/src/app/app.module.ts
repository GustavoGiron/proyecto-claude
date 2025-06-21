import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { DashboardInicioComponent } from './components/dashboard-inicio/dashboard-inicio.component';
import { DashboardMantenimientosComponent } from './components/dashboard-mantenimientos/dashboard-mantenimientos.component';
import { DashboardProcesosComponent } from './components/dashboard-procesos/dashboard-procesos.component';
import { ListClienteComponent } from './components/list-cliente/list-cliente.component';
import { FormClienteComponent } from './components/form-cliente/form-cliente.component';
import { ListVendedorComponent } from './components/list-vendedor/list-vendedor.component';
import { FormVendedorComponent } from './components/form-vendedor/form-vendedor.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    DashboardInicioComponent,
    DashboardMantenimientosComponent,
    DashboardProcesosComponent,
    ListClienteComponent,
    FormClienteComponent,
    ListVendedorComponent,
    FormVendedorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }