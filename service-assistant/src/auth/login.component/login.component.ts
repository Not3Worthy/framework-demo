import { Component, OnInit } from '@angular/core';
import { MsalService } from '@azure/msal-angular';
import { AuthenticationResult } from '@azure/msal-browser';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  username: string = '';

  constructor(private authService: MsalService) {}

  ngOnInit(): void {
    // Handles the redirect response back from Microsoft Entra ID safely
    this.authService.handleRedirectObservable().subscribe({
      next: (result: AuthenticationResult | null) => {
        if (result?.account) {
          this.authService.instance.setActiveAccount(result.account);
          this.updateUsername();
        }
      },
      error: (error) => console.error('Authentication redirect error:', error)
    });

    this.updateUsername();
  }

  get isLoggedIn(): boolean {
    return this.authService.instance.getActiveAccount() !== null;
  }

  updateUsername(): void {
    const activeAccount = this.authService.instance.getActiveAccount();
    if (activeAccount) {
      this.username = activeAccount.username || activeAccount.name || 'User';
    }
  }

  login(): void {
    // Initiates full-page redirect to Microsoft login
    this.authService.loginRedirect();
  }

  logout(): void {
    this.authService.logoutRedirect();
  }
}