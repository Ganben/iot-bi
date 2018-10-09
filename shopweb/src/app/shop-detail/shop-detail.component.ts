import { Component, OnInit, Input } from '@angular/core';
import { Shop } from '../shop';
import { HeroService } from '../hero.service';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-shop-detail',
  templateUrl: './shop-detail.component.html',
  styleUrls: ['./shop-detail.component.css']
})
export class ShopDetailComponent implements OnInit {

  @Input() shop: Shop;

  constructor(
    private route: ActivatedRoute,
    private shopService: HeroService,
    private location: Location
  ) { }


  ngOnInit(): void {
    this.getShop();
  }
  
  getShop(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.shopService.getShop(id).subscribe(shop => this.shop = shop);
  }

  goBack(): void {
    this.location.back();
  }

}
