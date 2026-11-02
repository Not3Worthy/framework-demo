import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MsalService } from '@azure/msal-angular';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  title = signal('Service Assistant');
  searchQuery = '';
  isLoading = false;
  results: any = null;
  errorMessage = '';

  constructor(
    private http: HttpClient,
    private authService: MsalService
  ) {}

  get username(): string {
    const activeAccount = this.authService.instance.getActiveAccount();
    return activeAccount?.name || activeAccount?.username || 'Technician';
  }

  onSearch(): void {
    if (!this.searchQuery.trim()) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.results = null;

    // Outgoing HTTP request automatically intercepted by MsalInterceptor to attach JWT
    this.http.get(`http://localhost:8000/api/search?q=${encodeURIComponent(this.searchQuery)}`)
      .subscribe({
        next: (data) => {
          this.results = data;
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Diagnostic search failed:', err);
          this.errorMessage = 'Failed to fetch diagnostic results. Please verify backend connection.';
          this.isLoading = false;
        }
      });
  }

  logout(): void {
    this.authService.logoutRedirect();
  }
}