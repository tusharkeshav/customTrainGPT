import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pprint import pprint


class ExtractPdf:

    def __init__(self):
        pass

    def extract_data_from_file(self, pdf_path: str, save_path: str):
        left_section_text = ""
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    x0, y0, x1, y1 = element.bbox  # Get bounding box coordinates
                    # Adjust this condition based on your specific layout (e.g., check x-coordinate is within left section)
                    if x0 < page_layout.width / 3:  # Check if element is in left third
                        left_section_text += element.get_text()
        self.__save_file(file_path=pdf_path, save_path=save_path, data=left_section_text)

    def extract_data_from_directory(self, dir_path: str, save_path: str):
        list_dir = os.listdir(dir_path)
        # print(list_dir)
        for file in list_dir:
            self.extract_data_from_file(os.path.join(dir_path, file), save_path)
        pass

    @staticmethod
    def __save_file(file_path: str, save_path: str, data: str):
        filename = file_path.split('/')[-1].split('.')[0]
        # print(f"file+path: {file_path}")
        # print(f"filename: {filename}")
        if not os.path.exists(os.path.join(save_path, filename + '.txt')):
            with open(os.path.join(save_path, filename + '.txt'), 'x') as file:
                file.write(data)
        return


# ExtractPdf().extract_data_from_directory(
#     dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/pdf',
#     save_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output')
