import { Component, OnInit } from '@angular/core';
import { Shop } from '../shop';
import { SHOPS } from '../mock-shops';
import { HeroService } from '../hero.service';

@Component({
  selector: 'app-shops',
  templateUrl: './shops.component.html',
  styleUrls: ['./shops.component.css']
})
export class ShopsComponent implements OnInit {
  
  shops: Shop[];

  constructor(private shopService: HeroService) { }

  ngOnInit() {
    this.getShops();
  }

  getShops(): void {
    this.shopService.getShops()
      .subscribe(shops => this.shops = shops);
  }


}
