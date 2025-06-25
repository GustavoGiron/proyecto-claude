import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrarSalidaComponent } from './registrar-salida.component';

describe('RegistrarSalidaComponent', () => {
  let component: RegistrarSalidaComponent;
  let fixture: ComponentFixture<RegistrarSalidaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RegistrarSalidaComponent]
    });
    fixture = TestBed.createComponent(RegistrarSalidaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
