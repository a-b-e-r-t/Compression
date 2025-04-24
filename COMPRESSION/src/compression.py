import fitz  
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import io

# ---------------- PDF Compression ----------------
def compress_pdf(input_path, output_path, zoom=0.4, quality=60):
    doc = fitz.open(input_path)
    new_doc = fitz.open()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0] 
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]  

            img = Image.open(io.BytesIO(image_bytes))
            img_byte_arr = io.BytesIO()

            img.save(img_byte_arr, format="JPEG", quality=quality) 
            img_byte_arr.seek(0)

            new_image_pdf = fitz.open("pdf", img_byte_arr.read())

            page.insert_image(page.rect, stream=new_image_pdf.read())

        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    new_doc.save(output_path, garbage=4, deflate=True)  
    new_doc.close()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        set_file(file_path)

def set_file(path):
    file_var.set(path)
    drop_frame.configure(bg="#ffffff", highlightbackground="#4CAF50")
    file_label.config(text="Archivo seleccionado: " + os.path.basename(path), fg="black")

def compress_action():
    input_pdf = file_var.get()
    if not input_pdf:
        messagebox.showwarning("Advertencia", "Por favor, selecciona o arrastra un archivo PDF.")
        return

    dir_name = os.path.dirname(input_pdf)
    file_name = os.path.basename(input_pdf)
    base_name, _ = os.path.splitext(file_name)
    output_pdf = os.path.join(dir_name, f"{base_name}_comprimido.pdf")

    try:
        compress_pdf(input_pdf, output_pdf, zoom=0.4, quality=60) 
        messagebox.showinfo("Éxito", f"PDF comprimido guardado como:\n{output_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo comprimir el PDF:\n{e}")

def on_drop(event):
    file_path = event.data.strip("{}")  
    if file_path.lower().endswith(".pdf"):
        set_file(file_path)
    else:
        messagebox.showwarning("Archivo inválido", "Por favor, arrastra solo archivos PDF.")

root = tk.Tk()
root.title("Compresor de PDF")
root.geometry("480x300")
root.configure(bg="#f5f5f5")  
root.resizable(False, False)

try:
    import tkinterdnd2 as tkdnd
    root = tkdnd.TkinterDnD.Tk()
except:
    pass

file_var = tk.StringVar()

title = tk.Label(root, text="Sistema de compresion PDF GORE", font=("Helvetica", 14, "bold"), bg="#f5f5f5", fg="#333333")
title.pack(pady=15)

drop_frame = tk.LabelFrame(root, text="", width=400, height=100, bg="#ffffff", relief="solid",
                           highlightthickness=2, highlightbackground="#4CAF50", bd=0)
drop_frame.pack(pady=10)
drop_frame.pack_propagate(False)

file_label = tk.Label(drop_frame, text="Subir aquí", bg="#ffffff", fg="gray", font=("Helvetica", 12))
file_label.pack(expand=True)

drop_frame.configure(highlightbackground="#4CAF50", highlightthickness=2)
drop_frame.bind("<Button-1>", lambda e: select_file())

try:
    drop_frame.drop_target_register("*")
    drop_frame.dnd_bind("<<Drop>>", on_drop)
except:
    print("[!] Soporte de arrastrar archivos no disponible (puede faltar tkinterdnd2)")

btn_compress = tk.Button(root, text="Comprimir PDF", command=compress_action,
                         width=20, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="flat")
btn_compress.pack(pady=20)

root.mainloop()
