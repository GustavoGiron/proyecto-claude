import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ClienteService } from '../../services/cliente/cliente.service';
import { Cliente } from '../../models/cliente/cliente';

@Component({
  selector: 'app-list-cliente',
  templateUrl: './list-cliente.component.html'
})
export class ListClienteComponent implements OnInit {
  clientes: Cliente[] = [];
  error: string | null = null;
  loading = true;
  busqueda = '';
  paginaActual = 1;
  itemsPorPagina = 3;
  Math = Math;

  constructor(
    private router: Router,
    private clienteService: ClienteService
  ) { }

  ngOnInit(): void {
    this.cargarClientes();
  }

  cargarClientes(): void {
    this.loading = true;
    this.error = null;

    this.clienteService.obtenerClientes().subscribe({
      next: (clientes) => {

        this.clientes = clientes || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  handleNuevoCliente(): void {
    this.router.navigate(['/formulario-cliente']);
  }

  handleVerCliente(id: string): void {
    this.router.navigate(['/formulario-cliente/ver', id]);
  }

  handleEditarCliente(id: string): void {
    this.router.navigate(['/formulario-cliente/editar', id]);
  }

  handleEliminarCliente(codigo: string): void {
    if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
      this.clienteService.eliminarCliente(codigo).subscribe({
        next: () => {
          this.cargarClientes();
        },
        error: (err) => {
          console.error('Error al eliminar cliente:', err);
          alert('Ocurrió un error al eliminar el cliente.');
        }
      });
    }
  }


  // Búsqueda
  get clientesFiltrados(): Cliente[] {
    const terminoBusqueda = this.busqueda.toLowerCase().trim();
    if (!terminoBusqueda) return this.clientes;

    return this.clientes.filter(cliente => {
      const nombreContacto = (cliente.nombre_contacto || '').toLowerCase();
      const nombreNegocio = (cliente.nombre_negocio || '').toLowerCase();
      const telefono = (cliente.telefono || '').toLowerCase();

      return nombreContacto.includes(terminoBusqueda) ||
        nombreNegocio.includes(terminoBusqueda) ||
        telefono.includes(terminoBusqueda);
    });
  }

  // Paginación
  get totalClientes(): number {
    return this.clientesFiltrados.length;
  }

  get totalPaginas(): number {
    return Math.ceil(this.totalClientes / this.itemsPorPagina);
  }

  get indiceInicio(): number {
    return (this.paginaActual - 1) * this.itemsPorPagina;
  }

  get indiceFin(): number {
    return this.indiceInicio + this.itemsPorPagina;
  }

  get clientesPaginados(): Cliente[] {
    return this.clientesFiltrados.slice(this.indiceInicio, this.indiceFin);
  }

  get paginasArray(): number[] {
    return Array.from({ length: this.totalPaginas }, (_, index) => index + 1);
  }

  // Cambio de página
  handleCambioPagina(nuevaPagina: number): void {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

  // Resetear página al buscar
  handleBusquedaChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.busqueda = target.value;
    this.paginaActual = 1;
  }
}