import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ShopsComponent } from './shops/shops.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ShopDetailComponent } from './shop-detail/shop-detail.component';


const routes: Routes = [
  { path: 'detail/:id', component: ShopDetailComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent},
  { path: 'shops', component: ShopsComponent}
];


@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  declarations: [],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }

