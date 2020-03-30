import argparse
import os
import pdf2image
from PIL import Image
from google.cloud import vision
from pathlib import Path


def split_pdf_to_pages(pdf_file_path, output_directory):
    """Split pdf file to pages, and return list of page filenames."""
    images = pdf2image.convert_from_path(pdf_file_path, 400)

    page_filenames = []
    for i, image in enumerate(images):
        page_filename = output_directory / "page{}.png".format(i + 1)
        image.save(page_filename)
        page_filenames.append(page_filename)

    return page_filenames


def get_question_bounds(image_file_path, prev_question_num=""):
    """Find question bounds in image file."""

    # Read image file
    with open(image_file_path, 'rb') as image_file:
        image_content = image_file.read()
    image = vision.types.Image(content=image_content)

    # Use Vision API
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    questions_bounds = {}

    first_digit_in_curr_num_symbol = None
    curr_question_num = ""
    curr_question_right, curr_question_bottom = 0, 0

    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                curr_question_num = ""
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if symbol.text.isdigit():  # Part of question number
                            if not curr_question_num:  # Begins a new question number
                                first_digit_in_curr_num_symbol = symbol
                            curr_question_num += symbol.text
                        else:
                            if symbol.text == "." and curr_question_num and (not prev_question_num or int(curr_question_num) == int(prev_question_num) + 1):  # Question number ends
                                # Add bottom_right coordinate to previous question
                                if prev_question_num and prev_question_num in questions_bounds:
                                    questions_bounds[prev_question_num]["bottom_right"] = (curr_question_right, curr_question_bottom)

                                # Add top left coordinate to current question
                                questions_bounds[curr_question_num] = {
                                    "top_left": (first_digit_in_curr_num_symbol.bounding_box.vertices[0].x, first_digit_in_curr_num_symbol.bounding_box.vertices[0].y)}

                                # Move to next question
                                prev_question_num = curr_question_num
                                curr_question_right, curr_question_bottom = 0, 0
                            else:
                                curr_question_right = max(curr_question_right, symbol.bounding_box.vertices[2].x)
                                curr_question_bottom = max(curr_question_bottom, symbol.bounding_box.vertices[2].y)

                            curr_question_num = ""

    if prev_question_num and prev_question_num in questions_bounds:
        questions_bounds[prev_question_num]["bottom_right"] = (curr_question_right, curr_question_bottom)

    return questions_bounds, prev_question_num


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path of pdf exam file to analyze.")
    parser.add_argument("gcp_key_path", help="Path of Google Cloud Platform api key json file, for use of Vision API.")
    parser.add_argument("--output_directory", help="Path of directory to save results in, defaults to current directory", default=".")
    args = parser.parse_args()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.gcp_key_path

    # Create output directory
    output_directory = Path(args.output_directory)
    output_directory.mkdir(exist_ok=True)

    image_files = split_pdf_to_pages(args.pdf_path, output_directory)

    last_question_number = ""
    for i, image_file in enumerate(image_files):
        print("Processing page {}...".format(i + 1))
        page = Image.open(image_file)

        page_questions, last_question_number = get_question_bounds(image_file, last_question_number)
        print("Found questions {} to {}.".format(min(page_questions.keys()), max(page_questions.keys())))

        for question_num, question in page_questions.items():
            question_slice = page.crop((question["top_left"][0], question["top_left"][1], question["bottom_right"][0], question["bottom_right"][1]))
            question_slice.save(output_directory / "question{}.png".format(question_num))

    print("Done!")
