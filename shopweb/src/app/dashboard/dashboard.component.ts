import { Component, OnInit } from '@angular/core';
import { Shop } from '../shop';
import { HeroService } from '../hero.service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  
  shops: Shop[] =[];

  constructor(private shopService: HeroService) { }

  ngOnInit() {
    this.getShops();
  }
  
  getShops(): void {
    this.shopService.getShops()
      .subscribe(shops => this.shops = shops.slice(1,4));
  }
}
