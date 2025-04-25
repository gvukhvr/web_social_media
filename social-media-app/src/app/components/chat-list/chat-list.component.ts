import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; 

interface User {
  id: number;
  username: string;
}

@Component({
  selector: 'app-chat-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-list.component.html',
  styleUrls: ['./chat-list.component.css']
})
export class ChatListComponent implements OnInit {
  users: User[] = [];
  filteredUsers: User[] = [];
  searchTerm: string = '';

  @Output() chatSelected = new EventEmitter<User>();

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const token = localStorage.getItem('access');
    console.log('[DEBUG] TOKEN в LOCAL STORAGE:', token);
    if (token) {
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`
      });

      this.http.get<User[]>('http://localhost:8000/api/users/', { headers }).subscribe({
        next: (users) => {
          console.log('[DEBUG] ответ ПОЛЬЗОВАТЕЛЕЙ от API:', users);  
          this.users = users;
          this.filteredUsers = users;
        },
        error: (err) => {
          console.error('Error fetching users', err);
        }
      });
    } else {
      console.error('No token found in localStorage');
    }
  }

  searchUsers() {
    this.filteredUsers = this.users.filter(user =>
      user.username.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  selectUser(user: User) {
    this.chatSelected.emit(user);
  }
}
