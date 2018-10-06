import { Component, OnInit } from '@angular/core';
import { Shop } from '../shop';

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

  constructor() { }

  ngOnInit() {
  }

}
