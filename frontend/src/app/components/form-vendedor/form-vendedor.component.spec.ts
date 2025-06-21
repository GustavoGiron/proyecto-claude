import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormVendedorComponent } from './form-vendedor.component';

describe('FormVendedorComponent', () => {
  let component: FormVendedorComponent;
  let fixture: ComponentFixture<FormVendedorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FormVendedorComponent]
    });
    fixture = TestBed.createComponent(FormVendedorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
