import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import csv
import os

# Функция для загрузки данных из CSV файла
def load_data_from_csv(filepath):
    data = []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if len(row) >= 6:  # Проверка наличия нужных столбцов
                    data.append({
                        "interforma": row[2],  # второй столбец
                        "fio": row[3],         # третий столбец
                        "sex": row[4],         # четвертый столбец
                        "dob": row[5],         # пятый столбец
                        "text": row[6]         # шестой столбец
                    })
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    return data

# Функция для отображения данных в listbox
def display_data(listbox, data):
    listbox.delete(0, tk.END)  # Очищаем список перед добавлением новых данных
    for item in data:
        listbox.insert(tk.END, f"{item['interforma']}")

# Функция для отображения информации в полях ввода
def show_contact_details(event):
    selected_contact = listbox.curselection()
    if selected_contact:
        index = selected_contact[0]
        contact = data[index]

        interforma_entry.delete(0, tk.END)
        interforma_entry.insert(0, contact["interforma"])

        fio_entry.delete(0, tk.END)
        fio_entry.insert(0, contact["fio"])

        sex_entry.delete(0, tk.END)
        sex_entry.insert(0, contact["sex"])

        dob_entry.delete(0, tk.END)
        dob_entry.insert(0, contact["dob"])

        text_entry.delete(0, tk.END)
        text_entry.insert(0, contact["text"])

# Функция для отображения информации о программе
def show_about_info():
    about_window = tk.Toplevel(root)
    about_window.title("О программе")
    about_label = ttk.Label(about_window, text="'Контакт+' версия 0.1")
    about_label.pack(padx=20, pady=20)

# Функция для отображения инструкции
def show_instruction():
    instruction_window = tk.Toplevel(root)
    instruction_window.title("Инструкция")
    instruction_label = ttk.Label(instruction_window, text="Инструкция по использованию программы:\n"
                                                           "1. Для добавления контакта заполните поля и нажмите 'Добавить контакт'.\n"
                                                           "2. Для изменения контакта выберите его в списке и нажмите 'Изменить контакт'.\n"
                                                           "3. Для удаления контакта выберите его в списке и нажмите 'Удалить контакт'.\n"
                                                           "4. После того как вами выбран нужный контакт, нажмите кнопку 'Позвонить' для выполнения звонка.")
    instruction_label.pack(padx=20, pady=20)

# Функция для выхода из приложения
def exit_app():
    root.quit()

# Функция для добавления контакта
def add_contact():
    interforma = interforma_entry.get()
    fio = fio_entry.get()
    sex = sex_entry.get()
    dob = dob_entry.get()
    text = text_entry.get()
    if interforma and fio and sex and dob and text:
        data.append({"interforma": interforma, "fio": fio, "sex": sex, "dob": dob, "text": text})
        display_data(listbox, data)

# Функция для удаления контакта
def delete_contact():
    selected_contact = listbox.curselection()
    if selected_contact:
        response = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить этот контакт?")
        if response:
            index = selected_contact[0]
            del data[index]
            display_data(listbox, data)

# Функция для вызова контакта
def call_contact():
    selected_contact = listbox.curselection()
    if selected_contact:
        index = selected_contact[0]
        contact = data[index]
        messagebox.showinfo("Звонок", f"Звоним на номер {contact['interforma']}")

# Функция для поиска контактов
def search_contacts():
    query = search_entry.get().lower()
    filtered_data = [contact for contact in data if query in contact["interforma"].lower() or query in contact["fio"].lower()]
    display_data(listbox, filtered_data)

# Функция для изменения контактов
def edit_contact():
    selected_contact = listbox.curselection()
    if selected_contact:
        index = selected_contact[0]
        interforma = interforma_entry.get()
        fio = fio_entry.get()
        sex = sex_entry.get()
        dob = dob_entry.get()
        text = text_entry.get()
        if interforma and fio and sex and dob and text:
            data[index] = {"interforma": interforma, "fio": fio, "sex": sex, "dob": dob, "text": text}
            display_data(listbox, data)

# Создаем главное окно
root = tk.Tk()
root.title("'Контакт+' версия 0.1")
root.geometry("800x700")  # Размер окна увеличен на 10%

# Изменение значка программы
root.iconbitmap("C:/Users/asd/Desktop/politeh/proga/сдать/app/your_icon.ico")

# Загружаем изображение фона
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Создаем Canvas для отображения фона
canvas = tk.Canvas(root, width=864, height=648)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Создаем фрейм для размещения элементов на фоне
frame = ttk.Frame(canvas, padding="10")
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Рассчитаем новые размеры
listbox_height = 23
listbox_width = int(40 * 0.9)  # Уменьшение размера списка на 20%
button_width = int(20 * 1.5)  # Увеличение на 50%
entry_width = 40

# Создаем метку для списка
label_listbox = ttk.Label(frame, text="Имя\\Номер")
label_listbox.place(x=10, y=10)

# Создаем список
listbox = tk.Listbox(frame, height=listbox_height + 2, width=listbox_width + 8)  # Увеличение высоты списка на 10%
listbox.place(x=10, y=40)
listbox.bind("<<ListboxSelect>>", show_contact_details)

# Поля для ввода данных
ttk.Label(frame, text="Номер телефона:").place(x=310, y=10)
interforma_entry = ttk.Entry(frame, width=entry_width)
interforma_entry.place(x=310, y=30)

ttk.Label(frame, text="ФИО:").place(x=310, y=60)
fio_entry = ttk.Entry(frame, width=entry_width)
fio_entry.place(x=310, y=80)

ttk.Label(frame, text="Пол:").place(x=310, y=110)
sex_entry = ttk.Entry(frame, width=entry_width)
sex_entry.place(x=310, y=130)

ttk.Label(frame, text="Дата рождения:").place(x=310, y=160)
dob_entry = ttk.Entry(frame, width=entry_width)
dob_entry.place(x=310, y=180)

ttk.Label(frame, text="Комментарий:").place(x=310, y=210)
text_entry = ttk.Entry(frame, width=entry_width + 20)
text_entry.place(x=310, y=230, height=50)  # Увеличиваем высоту поля для комментария

# Кнопки
add_button = ttk.Button(frame, text="Добавить контакт", width=button_width, command=add_contact)
add_button.place(x=10, y=480)

edit_button = ttk.Button(frame, text="Изменить контакт", width=button_width, command=edit_contact)
edit_button.place(x=10, y=520)

delete_button = ttk.Button(frame, text="Удалить контакт", width=button_width, command=delete_contact)
delete_button.place(x=10, y=560)

call_button = ttk.Button(frame, text="Позвонить", width=button_width, command=call_contact)
call_button.place(x=10, y=600)

# Строка поиска и кнопка поиска
search_label = ttk.Label(frame, text="Поиск:")
search_label.place(x=290, y=480)
search_entry = ttk.Entry(frame, width=entry_width)
search_entry.place(x=340, y=480)
search_button = ttk.Button(frame, text="Поиск", width=button_width - 19, command=search_contacts)
search_button.place(x=590, y=478)

# Полный путь к файлу CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_filepath = os.path.join(script_dir, 'data123.csv')

# Загрузка данных из CSV файла при запуске
if os.path.exists(csv_filepath):
    data = load_data_from_csv(csv_filepath)
    display_data(listbox, data)
else:
    messagebox.showerror("Ошибка", f"Файл не найден: {csv_filepath}")

# Создаем контекстное меню
menu_bar = tk.Menu(root)
app_menu = tk.Menu(menu_bar, tearoff=0)
app_menu.add_command(label="О программе", command=show_about_info)
app_menu.add_command(label="Инструкция", command=show_instruction)
app_menu.add_command(label="Выход", command=exit_app)
menu_bar.add_cascade(label="Файл", menu=app_menu)

root.config(menu=menu_bar)

# Запуск главного цикла приложения
root.mainloop()
