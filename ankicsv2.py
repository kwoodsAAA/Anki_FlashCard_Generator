import os

def convert_to_anki_format(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.lower().startswith("question:") or line.lower().startswith("q:"):
                question_line = line
                i += 1
                if lines[i].lower().startswith("answer:") or lines[i].lower().startswith("a:"):
                    answer_line = lines[i].strip()
                    question = question_line.split(":")[1].strip()
                    answer = answer_line.split(":")[1].strip()
                    outfile.write(f"{question};{answer}\n")
            i += 1

def merge_files_to_csv(directory, output_csv):
    with open(output_csv, 'w', encoding='utf-8') as csv_file:
        for filename in os.listdir(directory):
            if filename.startswith("anki_format_"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    csv_file.write(f.read())

if __name__ == "__main__":
    folder_path = "T:\KevinW\LocalGithub\Flashcards\Anki_FlashCard_Generator"
    output_folder = "T:\KevinW\LocalGithub\Flashcards\Anki_FlashCard_Generator\convertedoutput"
    combined_csv = "T:\\KevinW\LocalGithub\\Flashcards\\Anki_FlashCard_Generator\\all_flashcards.csv"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(folder_path, filename)
            output_filepath = os.path.join(output_folder, f"anki_format_{filename}")
            convert_to_anki_format(input_filepath, output_filepath)
    
    merge_files_to_csv(output_folder, combined_csv)
