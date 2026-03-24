from io import BytesIO
from typing import List
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF

from core.file_repository import FileRepository

from shared.logger import Logger
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from PIL import Image

class PdfActions():
    def __init__(self):
        self.logger = Logger.get_current_logger()
        #pass

    def shrink(self, fileid, quality):
        """
        Shrink pdf content by reducing quality of images in pages
        """
        self.logger.info("Shrink file: " + fileid)
        file_content = FileRepository().get(fileid)
        pdf_stream = BytesIO(file_content)
        reader = PdfReader(pdf_stream)
        writer = PdfWriter(clone_from=reader)
        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=quality)
        """ fileid_result = fileid.replace('.pdf', '') + "_shrinked.pdf"
        with open(fileid_result, "wb") as f:
            writer.write(f) """
        fileid_result = FileRepository().put(self.__pdfwriter_to_bytes(writer))
        self.logger.info("fileid_result: " + fileid_result)
        return fileid_result
    
    def shrink1(self, fileid, zoom):
        file_content = FileRepository().get(fileid)
        doc = fitz.open(stream=file_content, filetype="pdf")
        new_doc = fitz.open()

        for page in doc:
            # Render page as image at lower scale
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = fitz.Pixmap(pix, 0) if pix.alpha else pix

            # Create new page with the image
            img_pdf = fitz.open()
            rect = fitz.Rect(0, 0, img.width, img.height)
            img_pdf.insert_page(-1, width=img.width, height=img.height)
            img_pdf[-1].insert_image(rect, pixmap=img, compress=True)
            new_doc.insert_pdf(img_pdf)

        # Create an in-memory bytes buffer
        output_buffer = BytesIO()

        new_doc.save(output_buffer, deflate=True)
        new_doc.close()
        # Move to start of the buffer
        output_buffer.seek(0)
        
        res_bytes = output_buffer.read()

    def shrink2(self, fileid, img_quality, dpi=150, compression_effort=5):
        """
        Shrink pdf content by reducing quality of pixel map of pages using dpi parameter
        """
        file_content = FileRepository().get(fileid)
        # Load PDF from bytes
        input_buffer = BytesIO(file_content)
        doc: fitz.Document = fitz.open(stream=input_buffer, filetype="pdf")

        new_doc = fitz.open()  # empty PDF

        #for page_index in range(len(doc)):
        #    page = doc[page_index]
        page: fitz.Page
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)
            
            img_buffer = BytesIO()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(img_buffer, format="JPEG", quality=img_quality)
            img_buffer.seek(0)

            rect = fitz.Rect(0, 0, pix.width, pix.height)
            new_page = new_doc.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_buffer.read())

        output_buffer = BytesIO()
        new_doc.save(
            output_buffer, 
            deflate=True, 
            clean=True, 
            compression_effort=compression_effort)
        doc.close()
        new_doc.close()

        output_buffer.seek(0)
        out_bytes = output_buffer.read()
    
        fileid_result = FileRepository().put(out_bytes)
        self.logger.info("fileid_result: " + fileid_result)
        return fileid_result

    def rotate(self, fileid, rotate_degree):
        """
        Rotate pdf content
        """
        self.logger.info("Rotate file: " + fileid)
        file_content = FileRepository().get(fileid)
        pdf_stream = BytesIO(file_content)
        reader = PdfReader(pdf_stream)
        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(rotate_degree)
            writer.add_page(page)
        """ fileid_result = fileid.replace('.pdf', '') + "_rotated.pdf"
        with open(fileid_result, "wb") as f:
            writer.write(f) """
        fileid_result = FileRepository().put(self.__pdfwriter_to_bytes(writer))
        self.logger.info("fileid_result: " + fileid_result)
        return fileid_result

    def resize_pdf(self, fileid, scale: float):
        """
        Resize pdf content
        """
        self.logger.info("Resize file: " + fileid)
        file_content = FileRepository().get(fileid)
        pdf_stream = BytesIO(file_content)
        reader = PdfReader(pdf_stream)
        writer = PdfWriter()

        for page in reader.pages:
            page.scale(scale, scale)
            writer.add_page(page)

        fileid_result = FileRepository().put(self.__pdfwriter_to_bytes(writer))
        self.logger.info("fileid_result: " + fileid_result)
        return fileid_result

    def __pdfwriter_to_bytes(self, writer: PdfWriter):
        with BytesIO() as bytes_stream:
            writer.write(bytes_stream)
            return bytes_stream.getvalue()
        
    def merge_pdf_files(self, fileid_list: List):
        """
        Merge pdf files
        """
        self.logger.info("Merge files: " + str(fileid_list))
        merger = PdfWriter()
        for fileid in fileid_list:
            input_stream = BytesIO(FileRepository().get(fileid))
            merger.append(input_stream)
        fileid_result = FileRepository().put(self.__pdfwriter_to_bytes(merger))
        self.logger.info("fileid_result: " + fileid_result)
        return fileid_result
    
    def create_watermark_pdf(self):
        """
        Create an empty pdf with watermark
        """
        # Create BytesIO buffer
        buffer = BytesIO()
        # Create a new PDF with Reportlab
        c = canvas.Canvas(buffer, pagesize=A4)
        # Set font and size
        c.setFont("Helvetica", 60)
        # Set transparency
        c.setFillAlpha(0.3)
        # Rotate text 45 degrees
        c.rotate(45)
        # Add watermark text
        c.drawString(2*inch, 0*inch, "WATERMARK")
        # Save the PDF
        c.save()
        # Get bytes from buffer
        pdf_bytes = buffer.getvalue()
        buffer.close()
        #return pdf_bytes
        # Save content into file
        fileid_result = FileRepository().put(pdf_bytes)
        return fileid_result
        
if __name__ == '__main__':
    print(PdfActions().create_watermark_pdf())