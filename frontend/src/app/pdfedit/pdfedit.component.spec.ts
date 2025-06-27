import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PdfeditComponent } from './pdfedit.component';

describe('PdfeditComponent', () => {
  let component: PdfeditComponent;
  let fixture: ComponentFixture<PdfeditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PdfeditComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PdfeditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
