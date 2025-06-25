import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormInventarioComponent } from './form-inventario.component';

describe('FormInventarioComponent', () => {
  let component: FormInventarioComponent;
  let fixture: ComponentFixture<FormInventarioComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FormInventarioComponent]
    });
    fixture = TestBed.createComponent(FormInventarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
