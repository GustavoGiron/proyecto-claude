import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/usuario/user.service';
import { User } from 'src/app/models/usuario/user.model';

@Component({
  selector: 'app-list-usuario',
  templateUrl: './list-usuario.component.html',
  styleUrls: ['./list-usuario.component.css']
})
export class ListUsuarioComponent implements OnInit {
  usuarios: User[] = [];
  error: string | null = null;
  loading = true;
  busqueda = '';
  paginaActual = 1;
  itemsPorPagina = 5;
  Math = Math;

  constructor(
    private router: Router,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.loading = true;
    this.error = null;

    this.userService.getAll().subscribe({
      next: (usuarios) => {
        this.usuarios = usuarios || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar usuarios:', err);
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  handleNuevoUsuario(): void {
    this.router.navigate(['/form-usuario']);
  }

  handleVerUsuario(id: number): void {
    this.router.navigate(['/form-usuario/ver', id]);
  }

  handleEditarUsuario(id: number): void {
    this.router.navigate(['/form-usuario/editar', id]);
  }

  handleEliminarUsuario(id: number): void {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      this.userService.delete(id).subscribe({
        next: () => {
          this.cargarUsuarios();
        },
        error: (err) => {
          alert('Ocurrió un error al eliminar el usuario: ' + err.message);
        }
      });
    }
  }

  // Búsqueda
  get usuariosFiltrados(): User[] {
    const termino = this.busqueda.toLowerCase().trim();
    if (!termino) return this.usuarios;

    return this.usuarios.filter(u =>
      u.username.toLowerCase().includes(termino) ||
      u.nombre.toLowerCase().includes(termino) ||
      u.apellido.toLowerCase().includes(termino) ||
      u.email.toLowerCase().includes(termino)
    );
  }

  // Paginación
  get totalUsuarios(): number {
    return this.usuariosFiltrados.length;
  }

  get totalPaginas(): number {
    return Math.ceil(this.totalUsuarios / this.itemsPorPagina);
  }

  get indiceInicio(): number {
    return (this.paginaActual - 1) * this.itemsPorPagina;
  }

  get indiceFin(): number {
    return this.indiceInicio + this.itemsPorPagina;
  }

  get usuariosPaginados(): User[] {
    return this.usuariosFiltrados.slice(this.indiceInicio, this.indiceFin);
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