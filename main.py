import json
import re
from typing import Optional

print("abc".find("bc"))

import pytesseract

from pdf2image import convert_from_path
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import pandas

from files.resourses.constants import official_emails
from files.data.structure import Structure
import logging

uniq_emails = set()
raw_data = []

logging.basicConfig(level=logging.DEBUG)
main_logger = logging.getLogger(__name__)


def get_files_list(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles


def open_file():
    file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=(("Все файлы", "*.*"),))
    if file_path:
        print(f"Вы выбрали файл: {file_path}")
        convert_PDF_to_IMG(file_path)
    else:
        print("Файл не выбран.")


def choose_folder():
    folder_path = filedialog.askdirectory(title="Выберите папку с файлами")
    return folder_path


def generate_IMG_data():
    path = choose_folder()
    print(path)
    files_pathes = get_files_list(path)
    # for idx, file in enumerate(files_pathes):
    #    print(f"{idx}. {file}")

    MAX_VALUE = len(files_pathes)

    progress_bar.config(
        maximum=MAX_VALUE,
    )

    progress_bar_label.pack()
    progress_bar.pack(fill="x", expand=True)

    for idx, file in enumerate(files_pathes):
        progress_value.set(idx)
        progress_bar_label.config(text=f"Обработано {idx + 1}/{MAX_VALUE}")
        progress_bar.step(float(idx * 100) / MAX_VALUE)
        print(f"{idx} Обработан файл: {file}")
        if file.endswith(".pdf"):
            convert_PDF_to_IMG(f"{path}/{file}", output_directory="files/temp/")
        root.update_idletasks()
        root.after(1000)
    progress_bar_label.destroy()
    progress_bar_label.destroy()


def generate_DOC_data():
    path = f"files/scanned_images/"
    images_pathes = get_files_list(path)
    # for idx, img in enumerate(images_pathes):
    #     print(f"{idx}. {img}")

    MAX_VALUE = len(images_pathes)
    progress_bar.config(
        maximum=MAX_VALUE,
    )


    data = dict()

    for idx, img in enumerate(images_pathes):
        progress_value.set(idx)
        progress_bar_label.config(text=f"Обработано {idx + 1}/{MAX_VALUE}")
        progress_bar.step(float(idx))
        print(f"{idx} Обработан файл: {img}")
        # FIXME: убрать проверку на page_1
        if img.startswith("page_1") and img.endswith(".jpg"):
            progress_bar_label.pack()
            progress_bar.pack(fill="x", expand=True)
            print(path + img)
            image = Image.open(path + img)

            eng_text = extract_text_from_image(
                image=image,
                lang='eng'
            )

            rus_text = extract_text_from_image(
                image=image,
                lang='rus'
            )

            print(eng_text)
            email = get_email_from_text(eng_text)
            print("total:  " + email)
            number, surname, fathers_name = get_N_and_name_from_text(rus_text)
            structure = Structure(name=fathers_name,
                                  surname=surname,
                                  number=number,
                                  email=email
                                  )
            raw_data.append(structure)

        root.update_idletasks()
        root.after(1000)

    progress_bar.destroy()
    progress_bar_label.destroy()


def save_to_JSON():
    pass


def save_to_XLSX():
    pass


def convert_PDF_to_IMG(file_path, output_directory="files/images"):
    images = convert_from_path(
        pdf_path=file_path,
        dpi=600
    )
    if len(images) > 0:
        first_image = images[0]
        first_image.save(f"{output_directory}/page_1_{datetime.now()}.jpg", "JPEG")
    else:
        main_logger.error("[convert_PDF_to_IMG]: No images found")
    # for idx, image in enumerate(images):
    # print(f"{idx}")
    # image.save(f"{output_directory}/page_{idx + 1}_{datetime.now()}.jpg", "JPEG")


def get_dict_from_IMG():
    image_path = filedialog.askopenfilename(title="Выберите файл", filetypes=(("Все файлы", "*.*"),))
    if image_path:
        image = Image.open(image_path)

        eng_text = extract_text_from_image(
            image=image,
            lang='eng'
        )

        rus_text = extract_text_from_image(
            image=image,
            lang='rus'
        )

        # print(eng_text)
        email = get_email_from_text(eng_text)
        name = get_N_and_name_from_text(rus_text)
        # print(name, ": ", email)
        return name, email


def get_N_and_name_from_text(text):
    re_number = re.compile(r'(?:№\s+)([0-9\/-]+)(?:\s+)')
    re_surname = re.compile(r'([А-Я]{1}[а-я]+[\s]+[А-Я]{1}.[А-Я]{1}\.)')
    re_fathers_name = re.compile(r'(?:Уважаемая|Уважаемый)(?:\s+)(\w+\s+\w+)(?:!)')
    number = re_number.search(text)
    number = number.groups()[0] if number else None
    surname = re_surname.search(text)
    surname = surname.groups()[0] if surname else None
    fathers_name = re_fathers_name.search(text)
    fathers_name = fathers_name.groups()[0] if fathers_name else None
    return [number, surname, fathers_name]


def extract_text_from_image(image: Image, lang: str):
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def get_email_from_text(text: str) -> Optional[str]:
    emails_set = set()


    #re_rule_1 = re.compile(r"(?:\s{2,})([\w\.\s-]+@[\w\.-]+\.\w+)")
    #re_rule_2 = re.compile(r"(?:\s{2,})|(?:\.\d\d\s)([\w\.\s-]+@[\w\.-]+\.\w+)")
    #re_rule_3 = re.compile(r"(?:[\"\n]+)([\w\.\s-]+@[\w\.-]+\.\w+)")
    #re_rule_4 = re.compile(r"(?:(\d\d\d\d)[\"\n\s]+)|(?:\d\d\.\d\d.\d\d[\"\n\s]+)([\w\.\_\s-]+@[\w\.-]+\.\w{2,4})")
    re_rule_5 = re.compile(r"(?:(\s[ortORT]+\s\d\d.\d\d.\d{2,4})?(\n\d\d\d\d\s)?[\.\"\s\n]+)([\w\.\_\(\s-]+@[\w\.-]+\.\w{2,4})(?:\n)")
    re_rule_6 = re.compile(r"(?:\n\d\d\d\d\s)([\w\.\_\s-]+@[\w\.-]+\.\w{2,4})(?:\n)")
    re_rule_7 = re.compile(r"(?:\.{1}\n\n)([\w\.\_\s-]+@?[\w\.-]+\.\w{2,4})(?:\n)")
    re_rule_8 = re.compile(r"([\w\.\_-]+@[\w\.-]+\.\w{2,4})(?:\n)")
    re_rule_9 = re.compile(r"(?:(\s[ortORT]+\s\d\d.\d\d.\d{2,4})?(\n\d\d\d\d)?[\.\"\s\n]{2}?[\.\"\s\noFORT]*)([\w\.\_\(\s-]+@[\w\.-]+\.\w{2,4})(?:\n)")

    emails_list = list()
    emails_list1 = re_rule_5.findall(text)
    emails_list2 = re_rule_6.findall(text)
    emails_list3 = re_rule_7.findall(text)
    emails_list4 = re_rule_8.findall(text)
    emails_list5 = re_rule_9.findall(text)
    emails_list = emails_list4 + emails_list2 + emails_list3 + emails_list1 + emails_list5

    for email in emails_list:
        print(email)
        if email in official_emails:
            continue
        if type(email) != tuple:
            if len(email) < 25:
                emails_set.add(email)
        else:
            emails_set.add(email[-1])
    print(emails_set)

    emails_list = list(emails_set)
    print(emails_list)

    # emails = emails[1] if len(emails) > 1 else (emails[0] if len(emails) > 0 else None)

    # TODO: необходимо пройтись циклом и убрать email если будут другие офиц
    try:

        # TODO: добавить в множество имейл для проверки
        if official_emails[0] in emails_list:
            emails_list.remove(official_emails[0])

            emails_list[0] = emails_list[0].replace(" ", "")
            emails_list[0] = emails_list[0].replace("(", "")
            emails_list[0] = emails_list[0].replace(")", "")
            return emails_list[0]
        else:
            return emails_list[0].replace(" ", "")
    except IndexError:
        main_logger.error("[get_email_from_text] Email not found")
        return "Email не распознан"


def save_DOCs(json: dict):
    pandas.read_json("input.json").to_excel("files/data/output.xlsx")
    with open("files/data/output.txt", 'w+') as f:
        for key, value in json.items():
            f.write(f"{key}: {value}\n")



root.mainloop()
