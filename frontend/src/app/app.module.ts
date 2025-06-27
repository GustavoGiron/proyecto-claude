import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';

import { AuthInterceptor } from './interceptors/auth.interceptor';

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
import { LoginComponent } from './components/login/login.component';
import { LayoutComponent } from './components/layout/layout.component';
import { FormUsuarioComponent } from './components/form-usuario/form-usuario.component';
import { ListUsuarioComponent } from './components/list-usuario/list-usuario.component';

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
    LoginComponent,
    LayoutComponent,
    FormUsuarioComponent,
    ListUsuarioComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }