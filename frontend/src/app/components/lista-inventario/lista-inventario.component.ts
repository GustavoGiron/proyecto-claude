import { Component, OnInit } from '@angular/core';
import { InventarioService } from '../../services/inventario/inventario.service';
import { InventarioStock } from '../../models/inventario/inventario';

declare var toastr: any;

@Component({
  selector: 'app-lista-inventario',
  templateUrl: './lista-inventario.component.html',
  styleUrls: ['./lista-inventario.component.css']
})
export class ListaInventarioComponent implements OnInit {
  inventarios: InventarioStock[] = [];
  inventariosFiltrados: InventarioStock[] = [];
  loading = false;
  error: string | null = null;
  busqueda = '';
  paginaActual = 1;
  itemsPorPagina = 10;
  Math = Math;

  constructor(private inventarioService: InventarioService) { }

  ngOnInit(): void {
    this.cargarInventario();
  }

  cargarInventario(): void {
    this.loading = true;
    this.error = null;
    
    this.inventarioService.getInventarioStock().subscribe({
      next: (inventarios) => {
        this.inventarios = inventarios;
        this.inventariosFiltrados = inventarios;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar inventario:', err);
        this.error = err.message || 'Error al cargar el inventario';
        this.loading = false;
        toastr.error('Error al cargar el inventario', '', {
          positionClass: 'toast-top-right',
          timeOut: 3000,
          closeButton: false,
          progressBar: false
        });
      }
    });
  }

  handleBusquedaChange(event: any): void {
    this.busqueda = event.target.value;
    this.filtrarInventarios();
    this.paginaActual = 1; // Reset a la primera página al buscar
  }

  filtrarInventarios(): void {
    if (!this.busqueda.trim()) {
      this.inventariosFiltrados = this.inventarios;
    } else {
      const busquedaLower = this.busqueda.toLowerCase();
      this.inventariosFiltrados = this.inventarios.filter(item =>
        item.producto.nombre_producto.toLowerCase().includes(busquedaLower) ||
        item.producto.codigo_producto.toLowerCase().includes(busquedaLower)
      );
    }
  }

  handleCambioPagina(pagina: number): void {
    if (pagina >= 1 && pagina <= this.totalPaginas) {
      this.paginaActual = pagina;
    }
  }

  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  recargar(): void {
    this.cargarInventario();
  }

  // Getters para el template
  get totalInventarios(): number {
    return this.inventariosFiltrados.length;
  }

  get totalProductos(): number {
    return this.inventarios.length;
  }

  get totalStock(): number {
    return this.inventarios.reduce((sum, item) => sum + item.stock_total, 0);
  }

  get totalDisponible(): number {
    return this.inventarios.reduce((sum, item) => sum + item.stock_disponible, 0);
  }

  get totalPaginas(): number {
    return Math.ceil(this.totalInventarios / this.itemsPorPagina);
  }

  get indiceInicio(): number {
    return (this.paginaActual - 1) * this.itemsPorPagina;
  }

  get indiceFin(): number {
    return this.paginaActual * this.itemsPorPagina;
  }

  get inventariosPaginados(): InventarioStock[] {
    return this.inventariosFiltrados.slice(this.indiceInicio, this.indiceFin);
  }

  get paginasArray(): number[] {
    const paginas: number[] = [];
    const maxPaginas = 5; // Mostrar máximo 5 números de página
    let inicio = Math.max(1, this.paginaActual - 2);
    let fin = Math.min(this.totalPaginas, inicio + maxPaginas - 1);
    
    // Ajustar inicio si estamos cerca del final
    if (fin - inicio < maxPaginas - 1) {
      inicio = Math.max(1, fin - maxPaginas + 1);
    }
    
    for (let i = inicio; i <= fin; i++) {
      paginas.push(i);
    }
    
    return paginas;
  }
}