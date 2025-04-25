import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatListComponent } from '../chat-list/chat-list.component';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatListComponent],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: any[] = [];
  newMessage = '';
  selectedUser: any = null;
  socket$: WebSocketSubject<any> | null = null;
  roomId: number | null = null;
  chatRooms: any[] = [];
  searchTerm: string = '';
  searchResults: any[] = [];
  avatar: string = '';
  username: string = '';


  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadChatRooms();
    this.authService.getProfile().subscribe({
      next: (res: any) => {
        this.avatar = res.avatar;
        this.username = res.username;

      },
      error: () => console.warn('Не удалось загрузить профиль')
    });
    
    
  }

  // Получение токена
  getToken(): string | null {
    return localStorage.getItem('access');
  }

  // Загружаем все чаты пользователя
  loadChatRooms() {
    const token = this.getToken();
    if (token) {
      const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
      this.http.get<any[]>('http://localhost:8000/api/chatrooms/', { headers }).subscribe({
        next: (rooms) => {
          this.chatRooms = rooms;
        },
        error: (err) => {
          console.error('Ошибка при загрузке чатов', err);
        }
      });
    }
  }

  // Поиск пользователей
  searchUsers() {
    const token = this.getToken();
    if (token && this.searchTerm.trim()) {
      const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
      this.http.get<any[]>(`http://localhost:8000/api/users/?search=${this.searchTerm}`, { headers })
        .subscribe({
          next: users => this.searchResults = users,
          error: err => console.error('Ошибка при поиске пользователей', err)
        });
    } else {
      this.searchResults = [];
    }
  }

  // Открытие чата с пользователем
  openChatWith(user: any) {
    const token = this.getToken();
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    this.http.post<any>('http://localhost:8000/api/chatroom/', { user_id: user.id }, { headers }).subscribe({
      next: (room) => {
        this.roomId = room.id;
        this.selectedUser = user;

        // Подключение к чату и загрузка сообщений
        this.connectToChat(room.id);

        // Добавляем чат в список, если его там ещё нет
        const exists = this.chatRooms.some(r => r.id === room.id);
        if (!exists) {
          this.chatRooms.push(room);
        }

        this.searchResults = [];
        this.searchTerm = '';
      },
      error: (err) => {
        console.error('Ошибка при открытии чата', err);
      }
    });
  }

  // Выбор пользователя из списка чатов
  onUserSelected(user: any) {
    this.selectedUser = user;
    this.openChatWith(user);
  }

  // Подключение к сокету для выбранной комнаты
  connectToChat(roomId: number) {
    if (this.socket$) this.socket$.complete();

    const token = this.getToken();
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    this.http.get<any[]>(`http://localhost:8000/api/messages/${roomId}/`, { headers }).subscribe({
      next: (msgs) => {
        this.messages = msgs;
      },
      error: (err) => {
        console.error('Ошибка при загрузке сообщений', err);
      }
    });
    this.socket$ = webSocket(`ws://localhost:8000/ws/chat/${roomId}/?token=${token}`);
    this.socket$.subscribe({
      next: (msg: any) => {
        this.messages.push(msg);
      },
      error: (err) => {
        console.error('Ошибка WebSocket', err);
      }
    });
  }

  // Отправка сообщения в чат
  sendMessage() {
    if (this.newMessage.trim() && this.socket$) {
      this.socket$.next({
        message: this.newMessage.trim()
      });
      this.newMessage = '';
    }
  }
  // Логаут пользователя
  onLogout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
