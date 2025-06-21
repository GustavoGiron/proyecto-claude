import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardMantenimientosComponent } from './dashboard-mantenimientos.component';

describe('DashboardMantenimientosComponent', () => {
  let component: DashboardMantenimientosComponent;
  let fixture: ComponentFixture<DashboardMantenimientosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardMantenimientosComponent]
    });
    fixture = TestBed.createComponent(DashboardMantenimientosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
