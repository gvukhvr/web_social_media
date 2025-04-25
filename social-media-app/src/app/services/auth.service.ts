import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable,tap } from 'rxjs';


@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth/';

  constructor(private http: HttpClient) {}
  private readonly TOKEN_KEY = 'access';

  register(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}register/`, {
      username,
      email,
      password,
      confirm_password: password
    });
  }

  login(email: string, password: string) {
    return this.http.post<{ access: string }>('/api/token/', { email, password }).pipe(
      tap((response) => {
        localStorage.setItem(this.TOKEN_KEY, response.access);
      })
    );
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}user/`);
  }

  getToken(): string | null {
    return localStorage.getItem('access');
  }
  saveToken(token: string) {
    localStorage.setItem('access', token);
  }

  logout(): void {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  }

  getProfile() {
    const token = this.getToken();
    return this.http.get('http://localhost:8000/api/profile/', {
      headers: { Authorization: `Bearer ${token}` }
    });
  }
  
}
