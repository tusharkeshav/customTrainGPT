# import pypdf
#
#
# def extract_left_section(pdf_file):
#     with open(pdf_file, 'rb') as file:
#         reader = pypdf.PdfReader(pdf_file)
#         # reader = pypdf.PdfReader(pdf_file).get_page(2).extract_text()
#         # print(reader)
#         # exit()
#         num_pages = reader.get_num_pages()
#
#         left_section_text = ''
#
#         for page_num in range(3, 4):
#             page = reader.get_page(page_num)
#             # Define the left boundary of the page
#             left_boundary = 0
#             # Define the right boundary of the page (you may need to adjust this value according to your PDF layout)
#             right_boundary = page.mediabox.width
#             print(right_boundary)
#             # Extract text from the left section of the page
#             left_text = page.extract_text()
#             left_section_text += left_text
#
#         return left_section_text
#
#
# pdf_file = '/home/akhil/Downloads/history_X_ch1.pdf'
# left_section_text = extract_left_section(pdf_file)
# print(left_section_text)


# from pdfquery import PDFQuery
#
# pdf = PDFQuery('/home/akhil/Downloads/history_X_ch1.pdf')
# pdf.load()
#
# pdf.tree.write('customers.xml', pretty_print = True)
# exit()
# # Use CSS-like selectors to locate the elements
# text_elements = pdf.pq('LTTextLineHorizontal')
#
# # Extract the text from the elements
# text = [t.text for t in text_elements]
#
# print(text)

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pprint import pprint


def extract_left_section_advanced(pdf_path):
    left_section_text = ""
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBox):
                x0, y0, x1, y1 = element.bbox  # Get bounding box coordinates
                # Adjust this condition based on your specific layout (e.g., check x-coordinate is within left section)
                if x0 < page_layout.width / 3:  # Check if element is in left third
                    left_section_text += element.get_text()
    return left_section_text


# Example usage (similar to previous example)
print(extract_left_section_advanced('/home/akhil/PycharmProjects/customTrainGPT/data/XI-biology-book/kebo102.pdf'))
exit()

def main():
    import os
    path = '/home/akhil/Documents/history_book'
    list_dir = os.listdir(path)
    save_path = '/home/akhil/PycharmProjects/customTrainGPT/history_complete_book/'
    for file in list_dir:
      with open(save_path + file.split('.')[0] + '.txt', 'x') as _file:
        extracted_text = extract_left_section_advanced(os.path.join(path, file))
        _file.write(extracted_text)

if __name__ == '__main__':
    main()
