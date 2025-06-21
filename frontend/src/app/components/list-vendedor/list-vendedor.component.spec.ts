import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListVendedorComponent } from './list-vendedor.component';

describe('ListVendedorComponent', () => {
  let component: ListVendedorComponent;
  let fixture: ComponentFixture<ListVendedorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ListVendedorComponent]
    });
    fixture = TestBed.createComponent(ListVendedorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
