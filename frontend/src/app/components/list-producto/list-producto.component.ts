import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ProductoService } from '../../services/producto/producto.service';
import { Producto } from '../../models/producto/producto';

@Component({
  selector: 'app-list-producto',
  templateUrl: './list-producto.component.html'
})
export class ListProductoComponent implements OnInit {
  productos: Producto[] = [];
  error: string | null = null;
  loading = true;
  busqueda = '';
  paginaActual = 1;
  itemsPorPagina = 3;
  Math = Math;

  constructor(
    private router: Router,
    private productoService: ProductoService
  ) { }

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos(): void {
    this.loading = true;
    this.error = null;

    this.productoService.obtenerProductos().subscribe({
      next: (productos) => {
        this.productos = productos || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar productos:', err);
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  handleNuevoProducto(): void {
    this.router.navigate(['/formulario-producto']);
  }

  handleVerProducto(codigo: number): void {
    this.router.navigate(['/formulario-producto/ver', codigo]);
  }

  handleEditarProducto(id: number): void {
    this.router.navigate(['/formulario-producto/editar', id]);
  }

  handleEliminarProducto(id: number): void {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
      this.productoService.eliminarProducto(id).subscribe({
        next: () => {
          this.cargarProductos();
        },
        error: (err) => {
          alert('Ocurrió un error al eliminar el producto.'+ ' ' + err.message);
        }
      });
    }
  }

  // Búsqueda
  get productosFiltrados(): Producto[] {
    const termino = this.busqueda.toLowerCase().trim();
    if (!termino) return this.productos;

    return this.productos.filter(p => {
      const nombre = p.nombre_producto.toLowerCase();
      const codigo = p.codigo_producto.toLowerCase();

      return nombre.includes(termino) || codigo.includes(termino);
    });
  }

  // Paginación
  get totalProductos(): number {
    return this.productosFiltrados.length;
  }

  get totalPaginas(): number {
    return Math.ceil(this.totalProductos / this.itemsPorPagina);
  }

  get indiceInicio(): number {
    return (this.paginaActual - 1) * this.itemsPorPagina;
  }

  get indiceFin(): number {
    return this.indiceInicio + this.itemsPorPagina;
  }

  get productosPaginados(): Producto[] {
    return this.productosFiltrados.slice(this.indiceInicio, this.indiceFin);
  }

  get paginasArray(): number[] {
    return Array.from({ length: this.totalPaginas }, (_, index) => index + 1);
  }

  handleCambioPagina(nuevaPagina: number): void {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

  handleBusquedaChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.busqueda = input.value;
    this.paginaActual = 1;
  }
}
