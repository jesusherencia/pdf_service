import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpEvent, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CreatedFile } from '../data/created-file';
import { MergePdfFiles } from '../data/merge_pdf_files';
import { FileEditActions } from '../data/edit-actions';

@Injectable({
  providedIn: 'root',
})
export class FileEditService {
  private baseUrl = 'http://localhost:8000/api/pdf_file';

  constructor(private http: HttpClient) {}

  upload(file: File): Observable<CreatedFile> {
    // use a form data to send file
    const formData: FormData = new FormData();
    formData.append('file', file);
    const headers = new HttpHeaders({ 'enctype': 'multipart/form-data' });
    return this.http.post<CreatedFile>(`${this.baseUrl}/upload`, formData, { headers: headers });
  }

  mergePdfFiles(mergePdfFiles: MergePdfFiles): Observable<CreatedFile> {
    return this.http.post<CreatedFile>(`${this.baseUrl}/merge`, mergePdfFiles);
  }

  getFiles(): Observable<any> {
    return this.http.get(`${this.baseUrl}/pdf_files`);
  }

  getFile(fileid: string): Observable<HttpResponse<Blob>> {
    return this.http.get(`${this.baseUrl}/${fileid}`, {
      responseType: 'blob', // 👈 important
      observe: 'response'
    });
  }

  executeFileEditActions(fileEditActions: FileEditActions): Observable<CreatedFile> {
    return this.http.post<CreatedFile>(`${this.baseUrl}/webactions`, fileEditActions);
  }
}
