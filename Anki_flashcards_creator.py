# import required packages
import PyPDF2
import openai
import os

# Initialize OpenAI API with your key
openai.api_key = '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'

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Read PDF
def read_pdf(file_path):

    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])

    return text

# dividing text into smaller chunks:
def divide_text(text, section_size):
    sections = []
    start = 0
    end = section_size
    while start < len(text):
        section = text[start:end]
        sections.append(section)
        start = end
        end += section_size
    return sections

# Create Anki cards
def create_anki_cards(pdf_text,pdf_name):
    # Limit the number of prompts to avoid excessive API usage

    SECTION_SIZE = 1000
    divided_sections = divide_text(pdf_text, SECTION_SIZE)
    text = divided_sections[0]
    generated_flashcards = ' '
    for i, text in enumerate(divided_sections):
    
        ## You might need to change the Prompt to get consistent format.
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create anki flashcards with the provided text using a format: question;answer next line question;answer etc. Keep question and the corresponding answer on the same line {text}"}
            ]

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages, 
                temperature =0.7,
                max_tokens=2000
            )

        response_from_api = response['choices'][0]['message']['content']#.strip()
        generated_flashcards += response_from_api

        # if i==0:
        #     break

    # # Save the cards to a text file
    # with open("flashcards.txt", "w") as f:
    #     f.write(generated_flashcards)

    base_name = os.path.splitext(pdf_name)[0]
    flashcard_file_path = os.path.join(ROOT_DIRECTORY, f"{base_name}_flashcards.txt")

    with open(flashcard_file_path, "w", encoding="utf-8") as f:
        f.write(generated_flashcards)


# Main script execution
if __name__ == "__main__":

    source_directory = f'{ROOT_DIRECTORY}/SOURCE_DOCUMENTS'
    
    # Get a list of all files in the SOURCE_DOCUMENTS directory

    all_files = os.listdir(source_directory)
    
    # Filter out only the PDF files
    pdf_files = [file for file in all_files if file.endswith('.pdf')]
    
    # Iterate over each PDF file, read its content, and create Anki cards
    for pdf_file in pdf_files:
        pdf_path = os.path.join(source_directory, pdf_file)
        pdf_text = read_pdf(pdf_path)
        create_anki_cards(pdf_text,pdf_file)





