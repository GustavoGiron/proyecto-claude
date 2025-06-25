import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
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
    ListProductoComponent,
    FormProductoComponent,
    FormInventarioComponent,
    ListaInventarioComponent,
    FormVentaComponent,
    RegistrarSalidaComponent,
    RegistrarPagoComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }