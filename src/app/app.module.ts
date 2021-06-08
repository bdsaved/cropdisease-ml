import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AlertsComponent } from './component/alerts/alerts.component';
import { HomeComponent } from './component/home/home.component';
import { ProfileComponent } from './component/profile/profile.component';
import { SettingsComponent } from './component/settings/settings.component';
import { TabsComponent } from './component/tabs/tabs.component';

@NgModule({
  declarations: [
    AppComponent, 
    HomeComponent, 
    ProfileComponent, 
    SettingsComponent,
    AlertsComponent,
    TabsComponent

  ],
  entryComponents: [],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }],
  bootstrap: [AppComponent],
})
export class AppModule {}
