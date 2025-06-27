import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule, FormGroup, Validators, FormArray, AbstractControl } from '@angular/forms';
import {MatExpansionModule} from '@angular/material/expansion'
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import { FileUploadComponent } from '../file-upload/file-upload.component';
import { FileEditService } from '../services/file-edit.service';
import { MergePdfFiles } from '../data/merge_pdf_files';

import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { FileEditActions, EditAction } from '../data/edit-actions';

@Component({
  selector: 'app-pdfedit',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatSelectModule, MatExpansionModule, FileUploadComponent],
  templateUrl: './pdfedit.component.html',
  styleUrl: './pdfedit.component.css'
})
export class PdfeditComponent {

  constructor(private fileUploadService: FileEditService) {}

  mergeFilesForm = new FormGroup({
    'fileid1': new FormControl('', [Validators.required]),
    'fileid2': new FormControl('', [Validators.required]),
  });

  onFileSelected(event: any, target_input: HTMLInputElement) {
    const selectedFile = event.target['files'][0];
    this.sendFile(selectedFile).subscribe(
      {
        next: (res: string) => {
          console.log('File uploaded successfully:', res);
          target_input.value = res;
          // Dispatch input event to trigger Angular's ngModel update
          target_input.dispatchEvent(new Event('input'));
        }
      }
    );
  }

  sendFile(selectedFile: File): Observable<string> {
    const formData = new FormData();
    formData.append('file', selectedFile, selectedFile.name);
    // Process the selected file
    return this.fileUploadService.upload(selectedFile).pipe(map(i => i['file_id']));
  }
  
  onSubmitMergeForm() {
    if (!this.mergeFilesForm.valid){
      console.log('form is not valid')
      return
    }
    let mergePdfFiles: MergePdfFiles = {
      fileid_list: [this.mergeFilesForm.value.fileid1 ?? '', this.mergeFilesForm.value.fileid2 ?? '']
    }	
    this.fileUploadService.mergePdfFiles(mergePdfFiles).subscribe(
      {
        next: (res: any) => {
          console.log('Files merged successfully:', res['file_id']);
        },
        error: error => {
          console.error('Error merging files:', error);
        }
      }
    );
  }

  chosenEditOption = ""

  pdfEditActionsForm = new FormGroup({
    'fileid': new FormControl('', [Validators.required]),
    'actionForms': new FormArray([]),
  });

  get actionFormsAsFormArray(): FormArray {
    return this.pdfEditActionsForm.get('actionForms') as FormArray;
  }

  getKeyValuesAsFormArray(control: AbstractControl): FormArray {
    return control.get('keyValues') as FormArray;
  }

  addEditAction() {
    if (this.checkValueEmpty(this.chosenEditOption)) {
      return
    }
    let form = this.createPdfEditActionForm();
    const keyValuesForm = form.get('keyValues') as FormArray;
    if (this.chosenEditOption == 'ROTATE') {
      form.controls['type'].setValue('ROTATE');
      const keyValueForm = this.createKeyValueForm();
      keyValueForm.controls['key'].setValue('rotate_degree');
      keyValuesForm.push(keyValueForm);
    }
    else if (this.chosenEditOption == 'SHRINK') {
      form.controls['type'].setValue('SHRINK');
      const keyValueForm = this.createKeyValueForm();
      keyValueForm.controls['key'].setValue('quality');
      keyValuesForm.push(keyValueForm);
    }
    this.actionFormsAsFormArray.push(form);
  }

  createPdfEditActionForm() {
    return new FormGroup({
      'type': new FormControl('', [Validators.required]),
      'keyValues': new FormArray([]),
    });
  }

  createKeyValueForm() {
    return new FormGroup({
      'key': new FormControl('', [Validators.required]),
      'value': new FormControl('', [Validators.required]),
    });
  }

  deleteItem(i: number) {
    this.actionFormsAsFormArray.removeAt(i);
  }

  onSubmitEditActionsForm() {
    if (!this.pdfEditActionsForm.valid){
      console.log('form is not valid')
      return
    }
    
    let formValue = this.pdfEditActionsForm.value;
    let data: FileEditActions = {
      'file_id': formValue.fileid ?? '',
      'webactions': (formValue.actionForms ?? []).map(i => ({
        'type': i['type'] as string, 
        'params': this.convertObject((i['keyValues'] ?? []) as Array<Record<string, any>>)
      })) as EditAction[]
    }

    this.fileUploadService.executeFileEditActions(data).subscribe(
      {
        next: (res: any) => {
          console.log('File edit actions executed successfully:', res['file_id']);
          this.fileUploadService.getFile(res['file_id']).subscribe((response) => {
            const blob = response.body!;
            const contentDisposition = response.headers.get('Content-Disposition');
            const filename = this.getFilenameFromHeader(contentDisposition) || 'downloaded-file';

            this.downloadFile(blob, filename);
          });
        },
        error: error => {
          console.error('Error file edit actions:', error);
        }
      }
    );
  }

  private downloadFile(blob: any, filename: string) {
    const a = document.createElement('a');
    const url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  convertObject(input: Array<Record<string, any>>) {
    let object: { [key: string]: any } = {}
    input.forEach(i => {
      object[i['key']] = i['value']
    })
    return object
  }

  checkValueEmpty(input: any) {
    return input === null || input === undefined || input === '';
  }

  saveFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  getFilenameFromHeader(header: string | null): string | null {
    if (!header) return null;
    const matches = /filename="?([^"]+)"?/.exec(header);
    return matches?.[1] ?? null;
  }

}
