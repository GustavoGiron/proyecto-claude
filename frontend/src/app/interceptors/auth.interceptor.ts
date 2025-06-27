import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth/auth.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Agregar token de autorización si existe
    const token = this.authService.getToken();
    let authReq = req;
    
    if (token) {
      authReq = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          // Token expirado, intentar refrescar
          return this.handle401Error(authReq, next);
        }
        return throwError(() => error);
      })
    );
  }

  private handle401Error(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Si es una request a /refresh, no reintentar
    if (req.url.includes('/api/auth/refresh')) {
      this.authService.clearStorage();
      this.router.navigate(['/login']);
      return throwError(() => new Error('Token refresh failed'));
    }

    return this.authService.refreshToken().pipe(
      switchMap((response) => {
        // Reintentar la request original con el nuevo token
        const newAuthReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${response.access_token}`
          }
        });
        return next.handle(newAuthReq);
      }),
      catchError((error) => {
        // Si el refresh falla, limpiar storage y redirigir al login
        this.authService.clearStorage();
        this.router.navigate(['/login']);
        return throwError(() => error);
      })
    );
  }
}