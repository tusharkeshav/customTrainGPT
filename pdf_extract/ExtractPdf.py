import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from logs.Logging import log
from ThreadManager import executor
from concurrent.futures import wait


class ExtractPdf:

    def __init__(self):
        pass

    def __extract_data_from_file(self, file_path: str, output_path: str):
        left_section_text = ""
        for page_layout in extract_pages(file_path):
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    x0, y0, x1, y1 = element.bbox  # Get bounding box coordinates
                    # Adjust this condition based on your specific layout (e.g., check x-coordinate is within left section)
                    if x0 < page_layout.width / 3:  # Check if element is in left third
                        left_section_text += element.get_text()
        self.__save_file(file_path=file_path, save_path=output_path, data=left_section_text)

    def extract_data_from_file(self, file_path: str, output_path: str):
        executor.submit(self.__extract_data_from_file, file_path=file_path, output_path=output_path)
        # return self.__extract_data_from_file(file_path=file_path, output_path=output_path)

    def extract_data_from_directory(self, input_dir: str, output_dir: str):
        log.info("Extracting data from directory: %s", input_dir)
        list_dir = os.listdir(input_dir)
        # print(list_dir)
        queue = []
        for file in list_dir:
            # self.__extract_data_from_file(file_path=os.path.join(input_dir, file), output_path=output_dir)
            thread = executor.submit(self.__extract_data_from_file, file_path=os.path.join(input_dir, file), output_path=output_dir)
            queue.append(thread)
        wait(queue)
        pass

    @staticmethod
    def __save_file(file_path: str, save_path: str, data: str):
        filename = file_path.split('/')[-1].split('.')[0]
        output_file_abs_path = os.path.join(save_path, filename + '.txt')
        try:
            if not os.path.exists(output_file_abs_path):
                with open(os.path.join(save_path, filename + '.txt'), 'x') as file:
                    file.write(data)
            else:
                log.warn('File %s already exists. Skipping writing it again', output_file_abs_path)
        except Exception as e:
            log.exception('Exception while saving file %s', output_file_abs_path, )
            raise ExtractPdfException('Exception while saving file %s', output_file_abs_path)

        log.info('Successfully extracted the data from input: %s and output written to: %s', file_path,
                 output_file_abs_path)
        return


# ExtractPdf().extract_data_from_directory(
#     dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/pdf',
#     save_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output')

class ExtractPdfException(Exception):
    pass
