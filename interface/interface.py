import ttkbootstrap
from ttkbootstrap.widgets import *

root = ttkbootstrap.Window(themename="vapor")
root.title("Email extractor")
root.geometry("300x400")
root.resizable(False, False)
# 1 картинка
imgPdfBtn = Image.open("files/ico/img.png")
imgPdfBtn = imgPdfBtn.resize((100, 60))
iconPdfBtn = ImageTk.PhotoImage(imgPdfBtn, size=(100, 60))
# 2 картинка
pdfTxtBtn = Image.open("files/ico/img_1.png")
pdfTxtBtn = pdfTxtBtn.resize((100, 60))
iconTxtBtn = ImageTk.PhotoImage(pdfTxtBtn, size=(100, 60))

# создание кнопок
# btnPDF = tk.Button(root, text="Открыть файл PDF", command=open_file)
# btnIMG = tk.Button(root, text="Получить текст IMAGE", command=get_dict_from_IMG)

# кнопка выбора директории для конвертации в рисунок
btnDIR = ttkbootstrap.Button(
    root,
    text="PDF to IMG",
    image=iconPdfBtn,
    bootstyle=PRIMARY,
    padding=(10, 30, 10, 10),
    compound=TOP,
    # anchor="center",
    # pady=20,
    # padx=10,
    # text="Выберите директорию для конвертации PDF в IMG",
    command=generate_IMG_data,
    # compound=tkinter.LEFT,
    width=100,
    # height=80
)

# кнопка извлечения текста из картинки
btnIMGtoTXT = ttkbootstrap.Button(
    root,
    bootstyle=SECONDARY,
    text="IMG to DOC",
    compound=TOP,
    padding=(10, 30, 10, 10),
    image=iconTxtBtn,
    width=100,
    # height=80,
    command=generate_DOC_data
)
# параметры прогресс бара
progress_value = tk.IntVar(value=0)
PROGRESS_BAR_LENGTH = 200

# прогресс бар
progress_bar = ttkbootstrap.Progressbar(
    root,
    style="Custom.Horizontal.TProgressbar",
    orient="horizontal",
    variable=progress_value,
    length=PROGRESS_BAR_LENGTH,
    mode="determinate"
)
# текст к прогресс бару
progress_bar_label = ttkbootstrap.Label(
    text="Статус загрузки",
    font=("Arial")
)

# btnPDF.pack()
# btnIMG.pack()
# btnDIR.pack(side=tkinter.LEFT, ipadx=20, ipady=20, anchor="nw")
# btnIMGtoTXT.pack(side=tkinter.LEFT, ipadx=20, ipady=20, anchor="n")

btnDIR.pack(side=TOP, padx=5, pady=5)
btnIMGtoTXT.pack(side=TOP, padx=5, pady=5)