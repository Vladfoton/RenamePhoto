import os
import time
import tkinter
from datetime import datetime
from tkinter import filedialog, Tk
from tkinter.messagebox import OK, INFO, showinfo


####___CONSTANTS___####

name_format = '%Y-%m-%d_%H-%M-%S'
list_file_ext = ['.jpg', '.arw', '.png', '.bmp', '.raw', '.gif', '.psd', '.tiff', '.jpeg','.mp4',
            '.JPG', '.ARW', '.PNG', '.BMP', '.RAW', '.GIF', '.PSD', '.TIFF', '.JPEG','.MP4']

start_dir = r'C:\Users\arm012\Pictures'

####_______________####

def rename_files(start_dir: str, nested : bool = True, filecounter :int = 0):
    count = 0
    filelist = os.listdir(path=start_dir)
    for file in filelist:
        path_file = start_dir + "\\" + file
        if os.path.isfile(path_file) and os.path.splitext(path_file)[1] in list_file_ext:
            date_file = time.ctime(os.path.getmtime(start_dir + "\\" + file))
            date_object = datetime.strptime(date_file, '%c')
            new_filename = start_dir + "\\"+date_object.strftime(name_format) + os.path.splitext(path_file)[1]
            try:
                os.rename(path_file, new_filename)
                filecounter += 1
            except FileExistsError:
                while True:
                    try:
                        new_filename = start_dir + "\\" + date_object.strftime(name_format) +'_'+str(count)+ \
                                       os.path.splitext(path_file)[1]
                        os.rename(path_file, new_filename)
                        #count = 0
                        filecounter += 1
                        break
                    except FileExistsError:
                        count+=1

            finally:
                count = 0

        elif os.path.isdir(path_file) and nested:
            filecounter = rename_files(path_file, nested = nested, filecounter = filecounter)
        else:
            pass
    return filecounter
def main_window():

    global start_dir
    def select_folder():
        global start_dir
        start_dir = filedialog.askdirectory()
        path_folder = tkinter.Label(window, text=start_dir)
        path_folder.place(x=20, y=80)
        btn_rename['state'] = 'normal'


    def rename():
        global start_dir
        starttime = time.time()

        count_file = rename_files(start_dir, nested=bool(nested_state.get()))
        showinfo(title='Выполнено!', message= 'Переименовано '+ str(count_file) + ' файлов',detail=f"за {round(time.time() - starttime,4)} сек.", default=OK, icon=INFO)
        # tkinter.Message(text= 'Переименовано '+ str(count_file) + ' файлов')
        window.destroy()


    ###___MAIN_WINDOW___###
    window = Tk()
    window.geometry('550x220')
    window.title('Выберите папку для обработки')
    lbl = tkinter.Label(window, text='Программа переименовывает файлы изображений в папке')
    lbl.place(x=20, y=10)
    lbl1 = tkinter.Label(window, text='Файлы переименовываются в формат YYYY-MM-DD_HH-MM-SS согласно времени съёмки')
    lbl1.place(x=20, y=30)
    lbl2 = tkinter.Label(window, text='Типы обрабатываемых файлов : '+ ", ".join([list_file_ext[i] for i in range(int(len(list_file_ext)/2))]))
    lbl2.place(x=20, y=50)
    btn_select_folder = tkinter.Button(window, text="Выбор папки", command = select_folder)
    btn_select_folder.place(x=400, y=80)

    nested_state = tkinter.BooleanVar()
    nested_state.set(True)
    nested = tkinter.Checkbutton(window, text='Обрабатывать включая вложенные папки', var =  nested_state)
    nested.place(x=20, y=100)

    btn_rename = tkinter.Button(window, text="Переименовать", command=rename)
    btn_rename['state'] = 'disabled'
    btn_rename.place(x=400, y=140)
    window.mainloop()

if __name__ == "__main__":
    main_window()

