import qrcode
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser

root = tk.Tk()
root.title("Aplicacion QR")
root.geometry("400x490")
root.minsize(404,
             560)
root.configure(bg="#FDE047")

def created_text(widget, font_size, row, column, columnspan):  #Componente para los textos
    widget.config(fg="#221E09",
                  bg="#FFFFFF",
                  font=("system-ui",font_size, "bold"))
    widget.grid(row=row,
                column=column,
                columnspan=columnspan,
                padx=25,
                pady=12,
                sticky="nsew")
    return widget

def created_button(text, parent_frame, comand, background, row, column, columnspan):  #Componente para los botones
    buttom = tk.Button(parent_frame)
    buttom.config(text=text,
                  command=comand,
                  fg="#221E09",
                  bg=background,
                  highlightbackground="#221E09",
                  highlightthickness=2,
                  font=("system-ui", 17, "bold"))
    buttom.grid(row=row,
                column=column,
                columnspan=columnspan,
                padx=15,
                pady=12,
                sticky="nsew")
    return buttom

def create_entry(default_text, parent_frame, row):  #Componente para las entradas de datos
    entry = tk.Entry(parent_frame)
    entry.config(fg="#221E09",
                 bg="#FFFFFF",
                 highlightbackground="#221E09",
                 highlightthickness=2,)
    entry.insert(0, default_text)
    entry.grid(row=row,
               column=1,
               padx=25,
               pady=12.5,
               sticky="nsew")
    return entry

def cerrar_cam(cap):  # Solucion a problema de navegacion
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

def mostrar_pagina(page, cap=None):  #Funcion para navegacion entre ventanas
    for widget in root.winfo_children():
        widget.grid_forget()
    if cap:
        cerrar_cam(cap)
    page()

decoded_url = None
def abrir_url():
    if decoded_url:
        webbrowser.open(decoded_url)

def main():
    frame_principal = tk.Frame(root)
    frame_principal.config(bg="#FDE047")

    text_principal = tk.Label(frame_principal, text="Bienvenido a tu aplicacion QR")
    text_principal.config(fg="#221E09",
                          bg="#FDE047",
                          font=("system-ui", 21, "bold"))
    text_principal.grid(row=0,
                        column=0,
                        columnspan=2,
                        padx=10,
                        pady=10,
                        sticky="nsew")

    buttom_generator = created_button("Generador QR", frame_principal, lambda: mostrar_pagina(convertor_qr),"#FFFFFF", 1, 0, 1)

    buttom_reader = created_button("Detector QR", frame_principal, lambda: mostrar_pagina(reader_qr),"#FFFFFF", 1, 1, 1)

    frame_principal.grid()

def convertor_qr():
    frame_convertor = tk.Frame(root)
    frame_convertor.configure(bg="#FFFFFF")

    buttom_back_ = created_button("Retroceder", frame_convertor, lambda: mostrar_pagina(main, cap=None), "#FDE047", 0, 0, 2)

    text_personalization = created_text(tk.Label(frame_convertor, text="Personaliza tu QR"), 17, 1, 0, 2)

    text_personalization_background = created_text(tk.Label(frame_convertor, text="Fondo"), 15, 2, 0, 1)
    Entry_personalization_background = create_entry("Ejemplo: White", frame_convertor, 2)

    text_personalization_color = created_text(tk.Label(frame_convertor, text="Color"), 15, 3, 0, 1)
    Entry_personalization_color = create_entry("Ejemplo: Blue", frame_convertor, 3)

    text_personalization_version = created_text(tk.Label(frame_convertor, text="Estilo"), 15, 4, 0, 1)
    Entry_personalization_version = create_entry("Ejemplo: 1, 2, 3...", frame_convertor, 4)

    text_personalization_size = created_text(tk.Label(frame_convertor, text="Tamaño"), 15, 5, 0, 1)
    Entry_personalization_size = create_entry("Ejemplo: 1, 2, 3...", frame_convertor, 5)

    text_personalization_Border = created_text(tk.Label(frame_convertor, text="Borde"), 15, 6, 0, 1)
    Entry_personalization_border = create_entry("Ejemplo: 1, 2, 3...", frame_convertor, 6)

    text_personalization_name = created_text(tk.Label(frame_convertor, text="Nombre"), 15, 7, 0, 1)
    Entry_personalization_name = create_entry("Ingresar nombre", frame_convertor, 7)

    text_personalization_link = created_text(tk.Label(frame_convertor, text="Direccion web"), 15, 8, 0, 1)
    Entry_personalization_link = create_entry("Ingresar direccion de la web", frame_convertor, 8)

    def insertar_direccion():
        try:
            background_data = Entry_personalization_background.get()
            color_data = Entry_personalization_color.get()
            version_data = Entry_personalization_version.get()
            size_data = Entry_personalization_size.get()
            border_data = Entry_personalization_border.get()
            name_data = Entry_personalization_name.get()
            link_data = Entry_personalization_link.get()

            if not link_data.startswith("http"):
                raise ValueError("La dirección web debe comenzar con 'http' o 'https'.")  #Para validacion de entradas

            qr = qrcode.QRCode(version=int(version_data),
                               box_size=int(size_data),
                               border=int(border_data))
            qr.add_data(link_data)
            qr.make()
            img = qr.make_image(fill_color=color_data,
                                back_color=background_data)
            img.save(name_data)

            # Cuadro de diálogo para poder elegir dónde guardar el archivo
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

            # Guardar la imagen QR en el archivo seleccionado
            if filepath:
                img.save(filepath)
        except ValueError as e:
            print(f"Error: {e}")

    buttom_apply = created_button("Crear QR", frame_convertor, lambda: insertar_direccion,"#FDE047", 9, 0, 2)

    frame_convertor.grid()

def update_camera_frame(label_camera, cap):
    global decoded_url
    ret, frame = cap.read()
    if ret:
        qrCode = cv2.QRCodeDetector()
        ret_qr, decoded_info, points, _ = qrCode.detectAndDecodeMulti(frame)
        if ret_qr:
            for info, point in zip(decoded_info, points):
                if info:  # Si encuentra el codigo qr
                    decoded_url = info
                    color = (0, 255, 0)
                    print(info)
                    button_open_url = tk.Button(label_camera,
                                                text="Abrir URL Escaneado",
                                                command=abrir_url)
                    button_open_url.config(fg="#221E09",
                                           bg="#FDE047",
                                           font=("system-ui", 15, "bold"))
                    button_open_url.grid(row=1,
                                         column=0,
                                         padx=10,
                                         pady=10,
                                         sticky="nsew")
                else:  # Si no encuentra el codigo qr
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [point.astype(int)], True, color, 8)

        width = 380
        height = 450
        frame = cv2.resize(frame, (width, height))

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(img)
        label_camera.imgtk = img_tk
        label_camera.configure(image=img_tk)

        label_camera.after(50, update_camera_frame, label_camera, cap)  # para que se refresque cada 50ms

        def cerrar_cam():  # Para que la camara libere recursos cuando no se usen
            cap.release()
            cv2.destroyAllWindows()

def reader_qr():
    frame_reader = tk.Frame(root)
    frame_reader.configure(bg="#FDE047")

    buttom_back_ = created_button("Retroceder", frame_reader, lambda: mostrar_pagina(main, cap), "#FFFFFF", 0, 0, 2)

    label_camera = tk.Label(frame_reader)
    label_camera.grid(row=1,
                      column=0,
                      padx=10,
                      pady=10,
                      sticky="nsew")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se puede abrir la cámara")
        return

    update_camera_frame(label_camera, cap)

    frame_reader.grid()

main()

root.mainloop()