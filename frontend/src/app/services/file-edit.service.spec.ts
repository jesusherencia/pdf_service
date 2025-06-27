import { TestBed } from '@angular/core/testing';

import { FileEditService } from './file-edit.service';

describe('FileEditService', () => {
  let service: FileEditService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FileEditService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
