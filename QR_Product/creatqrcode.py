from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
from fpdf import FPDF  # Thêm import thư viện FPDF
import os  # Thêm import thư viện os


# Tạo window app
window = Tk()
window.geometry('600x400')
window.title("Homemap Tech QR Code")
window.resizable(False, False)


# Hàm mở đường dẫn lưu file
def open_path():
    global direct
    files = [('PNG', '*.png'), ('JPEG', '*.jpg'), ('PDF', '*.pdf'),]
    direct = filedialog.asksaveasfilename(
        filetypes=files, defaultextension=files)

    entry_path.delete(0, END)
    entry_path.insert(0, direct)

    if len(direct) == 0:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn nơi lưu file.")
    else:
        pass


# Hàm chọn file logo
def open_logo():
    logo_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg")])
    if logo_path:
        entry_logo.delete(0, END)
        entry_logo.insert(0, logo_path)


# Hàm tạo mã QR với logo
def generate_qr_with_logo():
    data = input_data.get()
    if len(data) == 0:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu hoặc link.")
        return

    if len(direct) == 0:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn nơi lưu file.")
        return

    img = qrcode.make(data)

    logo_path = entry_logo.get()
    if logo_path:
        try:
            logo_img = Image.open(logo_path)
            # Điều chỉnh kích thước logo nếu cần thiết
            logo_img = logo_img.resize((90, 90))

            pos = ((img.size[0] - logo_img.size[0]) // 2,
                   (img.size[1] - logo_img.size[1]) // 2)

            img.paste(logo_img, pos)
        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể chèn logo: " + str(e))
            return

    # Thêm phần tạo file PDF
    if direct.endswith(".pdf"):
        pdf = FPDF()
        pdf.add_page()
        qr_image = "qr_tmp.png"
        img.save(qr_image)
        # Thay (10, 10, 100) bằng vị trí và kích thước ảnh trong PDF
        pdf.image(qr_image, 10, 10, 100)

        if logo_path:
            # Thay (110, 10, 50) bằng vị trí và kích thước logo trong PDF
            pdf.image(logo_path, 110, 10, 50)

        pdf.output(direct)
        pdf.close()

        # Xóa tạm ảnh QR đã tạo
        os.remove(qr_image)

        messagebox.showinfo(
            "Thông báo", "Bạn đã tạo xong mã QR sản phẩm và lưu vào file PDF.")
    else:
        # Nếu không phải là file PDF, chỉ lưu ảnh QR với logo vào đường dẫn đã chọn
        img.save(direct)
        messagebox.showinfo("Thông báo", "Bạn đã tạo xong mã QR sản phẩm.")


# Giao diện thân thiện và chuyên nghiệp hơn
title_label = Label(window, text="Homemap Tech QR Code",
                    font=('Helvetica', 18, 'bold'))
title_label.pack(pady=10)

input_frame = Frame(window)
input_frame.pack(pady=20)

link_label = Label(input_frame, text="Nhập thông tin:", font=('Helvetica', 12))
link_label.grid(row=0, column=0, padx=10, sticky='w')

input_data = Entry(input_frame, width=40, font=('Helvetica', 12))
input_data.grid(row=0, column=1, padx=10, pady=10)

path_label = Label(input_frame, text="Nơi lưu file:", font=('Helvetica', 12))
path_label.grid(row=1, column=0, padx=10, sticky='w')

entry_path = Entry(input_frame, width=40, font=('Helvetica', 12))
entry_path.grid(row=1, column=1, padx=10, pady=10)

btn_browse = Button(input_frame, text="Chọn", font=(
    'Helvetica', 12), command=open_path)
btn_browse.grid(row=1, column=2, padx=10)

logo_frame = Frame(window)
logo_frame.pack(pady=10)

logo_label = Label(logo_frame, text="Logo dự án:", font=('Helvetica', 12))
logo_label.grid(row=0, column=0, padx=10, sticky='w')

entry_logo = Entry(logo_frame, width=40, font=('Helvetica', 12))
entry_logo.grid(row=0, column=1, padx=10, pady=10)

btn_browse_logo = Button(logo_frame, text="Chọn", font=(
    'Helvetica', 12), command=open_logo)
btn_browse_logo.grid(row=0, column=2, padx=10)

btn_create = Button(window, text="Tạo mã QR có logo", font=(
    'Helvetica', 14), command=generate_qr_with_logo)
btn_create.pack(pady=10)

window.mainloop()

# Done!!!!
