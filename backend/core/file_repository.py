import uuid
import os
from pathlib import Path

class FileRepository:
    
    class FileId():
        def __init__(self):
            self.id = str(uuid.uuid4())
    
    PDF_REPO_FOLDER = './pdf_repo/' # relative from app folder
    
    def __init__(self):
        # Initialize class
        pass
        
    def get(self, file_name):
        """
        Get file contents from disk
        """
        try:
            with open(FileRepository.PDF_REPO_FOLDER + file_name, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None
        
    def put(self, content):
        """
        Add file contents to disk
        """
        file_name = str(uuid.uuid4())
        try:
            with open(FileRepository.PDF_REPO_FOLDER + file_name, 'wb') as f:
                f.write(content)
        except FileNotFoundError:
            return None

        return file_name
        
    def remove(self, file_name):
        """
        Remove file from disk
        """
        os.remove(FileRepository.PDF_REPO_FOLDER + file_name)
            
    def exists(self, file_name):
        """
        Check if file exists in disk
        """
        if Path(FileRepository.PDF_REPO_FOLDER + file_name).exists():
            return True
        else:
            return False