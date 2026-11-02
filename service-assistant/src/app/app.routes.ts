import { Routes } from '@angular/router';
import { MsalGuard } from '@azure/msal-angular';
import { DashboardComponent } from '../components/dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    canActivate: [MsalGuard], // Protects the main route with MSAL Guard
  },
  {
    path: '**',
    redirectTo: '' // Fallback redirect to protected root
  }
];