import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  username: string = '';
  avatar: string = '';
  avatarFile: File | null = null;

  constructor(private http: HttpClient, private authService: AuthService) {}

  ngOnInit(): void {
    this.getProfile();
  }

  getProfile() {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    this.http.get<any>('http://localhost:8000/api/profile/', { headers }).subscribe({
      next: (res) => {
        this.username = res.username;
        this.avatar = res.avatar;
      },
      error: () => alert('Ошибка загрузки профиля')
    });
  }

  onFileSelected(event: any) {
    this.avatarFile = event.target.files[0];
  }

  saveProfile() {
    const formData = new FormData();
    formData.append('username', this.username);
    if (this.avatarFile) {
      formData.append('avatar', this.avatarFile);
    }

    const token = this.authService.getToken();
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    this.http.put<any>('http://localhost:8000/api/profile/', formData, { headers }).subscribe({
      next: () => {
        alert('Профиль обновлён!');
        this.getProfile(); 
      },
      error: () => alert('Ошибка обновления профиля')
    });
    
  }
}
