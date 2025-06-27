import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { EnvConfig } from '../../env-config';
import {
  LoginRequest,
  LoginResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
  UserResponse,
  PermissionsResponse,
  User
} from '../../models/auth/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = EnvConfig.apiUrl;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Cargar usuario desde localStorage al inicializar
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      this.currentUserSubject.next(JSON.parse(storedUser));
    }
  }

  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/login`, credentials)
      .pipe(
        map(response => {
          // Guardar tokens y usuario en localStorage
          localStorage.setItem('access_token', response.access_token);
          localStorage.setItem('refresh_token', response.refresh_token);
          localStorage.setItem('user', JSON.stringify(response.user));
          
          // Actualizar el BehaviorSubject
          this.currentUserSubject.next(response.user);
          
          return response;
        }),
        catchError(this.handleError)
      );
  }

  refreshToken(): Observable<RefreshTokenResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      return throwError(() => new Error('No refresh token available'));
    }

    const request: RefreshTokenRequest = { refresh_token: refreshToken };
    
    return this.http.post<RefreshTokenResponse>(`${this.apiUrl}/auth/refresh`, request)
      .pipe(
        map(response => {
          localStorage.setItem('access_token', response.access_token);
          return response;
        }),
        catchError(this.handleError)
      );
  }

  getCurrentUser(): Observable<UserResponse> {
    return this.http.get<UserResponse>(`${this.apiUrl}/auth/me`)
      .pipe(
        map(response => {
          localStorage.setItem('user', JSON.stringify(response.user));
          this.currentUserSubject.next(response.user);
          return response;
        }),
        catchError(this.handleError)
      );
  }

  getPermissions(): Observable<PermissionsResponse> {
    return this.http.get<PermissionsResponse>(`${this.apiUrl}/auth/permissions`)
      .pipe(catchError(this.handleError));
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/logout`, {})
      .pipe(
        map(() => {
          this.clearStorage();
          return { message: 'Sesión cerrada exitosamente' };
        }),
        catchError(() => {
          // Incluso si el logout falla en el backend, limpiar el storage local
          this.clearStorage();
          return of({ message: 'Sesión cerrada localmente' });
        })
      );
  }

  clearStorage(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    const user = localStorage.getItem('user');
    return !!(token && user);
  }

  getCurrentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  private handleError(error: any) {
    console.error('Auth service error:', error);
    return throwError(() => error);
  }
}