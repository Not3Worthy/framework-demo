import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'Service Assistant';
  searchQuery = '';
  results: any = null;
  isLoading = false;

  constructor(private http: HttpClient) {}

  onSearch() {
    if (!this.searchQuery.trim()) return;
    
    this.isLoading = true;
    
    this.http.get(`http://localhost:8000/api/search?q=${encodeURIComponent(this.searchQuery)}`)
      .subscribe({
        next: (data) => {
          this.results = data;
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Search error:', err);
          this.isLoading = false;
        }
      });
  }
}