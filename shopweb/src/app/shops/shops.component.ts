import { Component, OnInit } from '@angular/core';
import { Shop } from '../shop';
import { SHOPS } from '../mock-shops';

@Component({
  selector: 'app-shops',
  templateUrl: './shops.component.html',
  styleUrls: ['./shops.component.css']
})
export class ShopsComponent implements OnInit {

  shop: Shop = {
    id: 1,
    name: 'Walmat',
    stats: 199
  };
  
  shops = SHOPS;

  constructor() { }

  ngOnInit() {
  }

  selectedShop: Shop;
  onSelect(shop: Shop): void {
    this.selectedShop = shop;
  }

}
