import { Configuration, BrowserCacheLocation } from '@azure/msal-browser';

export const msalConfig: Configuration = {
  auth: {
    clientId: 'YOUR_ENTRA_CLIENT_ID', // From your Entra App Registration
    authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID', 
    redirectUri: 'http://localhost', // Matches your SPA redirect URI in Entra
  },
  cache: {
    cacheLocation: BrowserCacheLocation.LocalStorage,
    // storeAuthStateInCookie: false,
  }
};

export const protectedResources = {
  fastApi: {
    endpoint: 'http://localhost:8000/api', // Your FastAPI backend base URL
    scopes: ['api://YOUR_ENTRA_CLIENT_ID/access_as_user'] // Expose an API scope in Entra
  }
};