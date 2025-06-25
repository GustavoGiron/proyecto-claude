import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ClienteService } from '../../services/cliente/cliente.service';
import { VendedorService } from '../../services/vendedor/vendedor.service';
import { ProductoService } from '../../services/producto/producto.service';
import { InventarioService } from '../../services/inventario/inventario.service';
import { InventarioStock } from '../../models/inventario/inventario';

declare var toastr: any;

@Component({
  selector: 'app-dashboard-inicio',
  templateUrl: './dashboard-inicio.component.html',
  styleUrls: ['./dashboard-inicio.component.css']
})
export class DashboardInicioComponent implements OnInit {
  
  loading: boolean = false;
  clientes: any[] = [];
  vendedores: any[] = [];
  productos: any[] = [];
  inventarioStock: InventarioStock[] = [];
  totalProductos: number = 0;
  totalClientes: number = 0;
  totalVendedores: number = 0;
  productosStockBajo: any[] = [];
  mostrarAlertas: boolean = true;
  stockMinimo: number = 10;

  ultimaActualizacion: string = '';

  constructor(
    private formBuilder: FormBuilder,
    private clienteService: ClienteService,
    private vendedorService: VendedorService,
    private productoService: ProductoService,
    private inventarioService: InventarioService
  ) {}

  ngOnInit(): void {
    this.cargarDatosIniciales();
    this.ultimaActualizacion = new Date().toLocaleString();
  }

  cargarDatosIniciales(): void {
    this.loading = true;
    let cargasCompletadas = 0;
    const totalCargas = 4; // Increased to 4 to include inventory stock

    // Función para verificar si todas las cargas están completas
    const verificarCargaCompleta = () => {
      cargasCompletadas++;
      if (cargasCompletadas === totalCargas) {
        this.loading = false;
        this.actualizarEstadisticas();
        this.verificarStockBajo();
        this.ultimaActualizacion = new Date().toLocaleString();
      }
    };

    // Cargar clientes
    this.clienteService.obtenerClientes().subscribe({
      next: (clientes) => {
        this.clientes = clientes;
        this.totalClientes = clientes.length;
        verificarCargaCompleta();
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        if (typeof toastr !== 'undefined') {
          toastr.error('Error al cargar la lista de clientes');
        }
        verificarCargaCompleta();
      }
    });

    // Cargar vendedores
    this.vendedorService.obtenerVendedores().subscribe({
      next: (vendedores) => {
        this.vendedores = vendedores;
        this.totalVendedores = vendedores.length;
        verificarCargaCompleta();
      },
      error: (err) => {
        console.error('Error al cargar vendedores:', err);
        if (typeof toastr !== 'undefined') {
          toastr.error('Error al cargar la lista de vendedores');
        }
        verificarCargaCompleta();
      }
    });

    // Cargar productos
    this.productoService.obtenerProductos().subscribe({
      next: (productos) => {
        this.productos = productos;
        this.totalProductos = productos.length;
        verificarCargaCompleta();
      },
      error: (err) => {
        console.error('Error al cargar productos:', err);
        if (typeof toastr !== 'undefined') {
          toastr.error('Error al cargar la lista de productos');
        }
        verificarCargaCompleta();
      }
    });

    // Cargar inventario stock
    this.inventarioService.getInventarioStock().subscribe({
      next: (inventarioStock) => {
        this.inventarioStock = inventarioStock;
        verificarCargaCompleta();
      },
      error: (err) => {
        console.error('Error al cargar inventario stock:', err);
        if (typeof toastr !== 'undefined') {
          toastr.error('Error al cargar el inventario de stock');
        }
        verificarCargaCompleta();
      }
    });
  }

  actualizarEstadisticas(): void {
    // Actualizar contadores
    this.totalClientes = this.clientes.length;
    this.totalVendedores = this.vendedores.length;
    this.totalProductos = this.productos.length;
  }

  verificarStockBajo(): void {
    // Filtrar productos con stock bajo usando datos de inventario
    this.productosStockBajo = this.inventarioStock
      .filter(item => item.stock_disponible <= this.stockMinimo)
      .map(item => ({
        id: item.id,
        producto_id: item.producto_id,
        nombre: item.producto.nombre_producto,
        codigo: item.producto.codigo_producto,
        stock: item.stock_disponible,
        stock_total: item.stock_total,
        stock_apartado: item.stock_apartado,
        fecha_actualizacion: item.fecha_ultima_actualizacion
      }));
  }

  toggleAlertas(): void {
    this.mostrarAlertas = !this.mostrarAlertas;
  }

  cerrarAlerta(index: number): void {
    this.productosStockBajo.splice(index, 1);
  }

  // Métodos auxiliares para el template
  obtenerIconoAlerta(): string {
    return this.mostrarAlertas ? 'fas fa-eye-slash' : 'fas fa-eye';
  }

  hayAlertas(): boolean {
    return this.productosStockBajo.length > 0;
  }

  obtenerMensajeStock(producto: any): string {
    const stock = producto.stock || 0;
    const nombre = producto.nombre || producto.codigo || 'Producto sin nombre';
    return `${nombre} tiene solo ${stock} unidades disponibles. Se recomienda realizar nuevo pedido.`;
  }

  // New method to get stock status for a product
  obtenerEstadoStock(producto: any): string {
    const stock = producto.stock || 0;
    if (stock === 0) {
      return 'Sin stock';
    } else if (stock <= this.stockMinimo) {
      return 'Stock crítico';
    } else if (stock <= this.stockMinimo * 2) {
      return 'Stock bajo';
    } else {
      return 'Stock normal';
    }
  }

  // Method to get color class based on stock level
  obtenerClaseColorStock(producto: any): string {
    const stock = producto.stock || 0;
    if (stock === 0) {
      return 'text-red-600';
    } else if (stock <= this.stockMinimo) {
      return 'text-red-500';
    } else if (stock <= this.stockMinimo * 2) {
      return 'text-yellow-500';
    } else {
      return 'text-green-500';
    }
  }
}