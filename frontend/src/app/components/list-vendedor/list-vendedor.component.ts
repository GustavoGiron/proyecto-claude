import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { Vendedor } from '../../models/vendedor/vendedor';

@Component({
  selector: 'app-list-vendedor',
  templateUrl: './list-vendedor.component.html'
})
export class ListVendedorComponent implements OnInit {
  vendedores: Vendedor[] = [];
  error: string | null = null;
  loading = true;
  busqueda = '';
  paginaActual = 1;
  itemsPorPagina = 3;
  Math = Math;

  constructor(
    private router: Router,
    private vendedorService: VendedorService
  ) { }

  ngOnInit(): void {
    this.cargarVendedores();
  }

  cargarVendedores(): void {
    this.loading = true;
    this.error = null;

    this.vendedorService.obtenerVendedores().subscribe({
      next: (vendedores) => {
        this.vendedores = vendedores || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar vendedores:', err);
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  handleNuevoVendedor(): void {
    this.router.navigate(['/formulario-vendedor']);
  }

  handleVerVendedor(codigo: string): void {
    this.router.navigate(['/formulario-vendedor/ver', codigo]);
  }

  handleEditarVendedor(codigo: string): void {
    this.router.navigate(['/formulario-vendedor/editar', codigo]);
  }

  handleEliminarVendedor(codigo: string): void {
    if (confirm('¿Estás seguro de que deseas eliminar este vendedor?')) {
      this.vendedorService.eliminarVendedor(codigo).subscribe({
        next: () => {
          this.cargarVendedores();
        },
        error: (err) => {
          console.error('Error al eliminar vendedor:', err);
          alert('Ocurrió un error al eliminar el vendedor.');
        }
      });
    }
  }

  // Búsqueda
  get vendedoresFiltrados(): Vendedor[] {
    const terminoBusqueda = this.busqueda.toLowerCase().trim();
    if (!terminoBusqueda) return this.vendedores;

    return this.vendedores.filter(vendedor => {
      const nombres = (vendedor.nombres || '').toLowerCase();
      const apellidos = (vendedor.apellidos || '').toLowerCase();
      const nombreCompleto = `${nombres} ${apellidos}`;

      return nombres.includes(terminoBusqueda) ||
        apellidos.includes(terminoBusqueda) ||
        nombreCompleto.includes(terminoBusqueda);
    });
  }

  // Paginación
  get totalVendedores(): number {
    return this.vendedoresFiltrados.length;
  }

  get totalPaginas(): number {
    return Math.ceil(this.totalVendedores / this.itemsPorPagina);
  }

  get indiceInicio(): number {
    return (this.paginaActual - 1) * this.itemsPorPagina;
  }

  get indiceFin(): number {
    return this.indiceInicio + this.itemsPorPagina;
  }

  get vendedoresPaginados(): Vendedor[] {
    return this.vendedoresFiltrados.slice(this.indiceInicio, this.indiceFin);
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