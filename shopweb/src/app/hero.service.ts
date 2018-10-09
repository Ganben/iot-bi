import { Injectable } from '@angular/core';
import { Shop } from './shop';
import { SHOPS } from './mock-shops';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class HeroService {

  constructor(private messageService: MessageService) { }

  getShops(): Observable<Shop[]> {
    this.messageService.add('ShopService: fetched shops');
    return of(SHOPS);
  }

  getShop(id: number): Observable<Shop> {
    this.messageService.add(`ShopService: fetched shop id=${id}`);
    return of(SHOPS.find(shop => shop.id === id));
  } 
}
