import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AlertsComponent } from './component/alerts/alerts.component';
import { HomeComponent } from './component/home/home.component';
import { ProfileComponent } from './component/profile/profile.component';
import { SettingsComponent } from './component/settings/settings.component';

const routes: Routes = [
  { path: "home", component: HomeComponent},
  { path: "settings", component: SettingsComponent},
  { path: "alerts", component: AlertsComponent},
  { path: "profile", component: ProfileComponent},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
