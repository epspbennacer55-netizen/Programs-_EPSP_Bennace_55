import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

import arabic_reshaper
from bidi.algorithm import get_display


# تسجيل الخط العربي
pdfmetrics.registerFont(TTFont('Arabic', 'amiri.ttf'))  # تأكد من وجود هذا الملف في نفس المجلد


def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


# def save_statement_as_pdf(name, start_date, end_date, vacation_days, remaining):
#     file_name = "vacation_statement.pdf"
#     c = canvas.Canvas(file_name, pagesize=A4)
#     width, height = A4
#     c.setFont("Arabic", 14)

#     lines = [
#         "الجمهورية الجزائرية الديمقراطية الشعبية - وزارة الصحة",
#         "بيان عطلة",
#         "--------------------------",
#         f"اسم الموظف: {name}",
#         f"تاريخ بداية العطلة: {start_date}",
#         f"تاريخ نهاية العطلة: {end_date}",
#         f"عدد أيام العطلة: {vacation_days}",
#         f"عدد الأيام المتبقية: {remaining} يوم"
#     ]

#     y = height - 50
#     for line in lines:
#         ar_line = reshape_arabic(line)
#         c.drawRightString(width - 40, y, ar_line)  # المحاذاة لليمين
#         y -= 30

#     c.save()
#     return file_name
# # end

from reportlab.lib.colors import HexColor

def save_statement_as_pdf(name, start_date, end_date, vacation_days, remaining):
    file_name = "vacation_statement.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    c.setFont("Arabic", 14)

    # === رسم خلفية رمادية فاتحة خلف العنوان ===
    title_box_width = width - 80
    title_box_height = 40
    title_box_x = 40
    title_box_y = height - 80

    c.setFillColor(HexColor("#f0f0f0"))  # رمادي فاتح
    c.roundRect(title_box_x, title_box_y, title_box_width, title_box_height, 10, fill=True, stroke=False)

    # === إعداد العنوان وتنسيقه ===
    c.setFont("Arabic", 20)
    c.setFillColor(HexColor("#003366"))  # أزرق غامق رسمي
    ar_title = reshape_arabic("بيان عطلة")
    text_width = pdfmetrics.stringWidth(ar_title, "Arabic", 20)
    c.drawString((width - text_width) / 2, title_box_y + 10, ar_title)

    # === المحتوى الأساسي ===
    c.setFont("Arabic", 14)
    c.setFillColor(HexColor("#000000"))  # اللون الأسود للنص

    lines = [
        "الجمهورية الجزائرية الديمقراطية الشعبية - وزارة الصحة",
        "--------------------------",
        f"اسم الموظف: {name}",
        f"تاريخ بداية العطلة: {start_date}",
        f"تاريخ نهاية العطلة: {end_date}",
        f"عدد أيام العطلة: {vacation_days}",
        f"عدد الأيام المتبقية: {remaining} يوم"
    ]

    y = title_box_y - 50
    for line in lines:
        ar_line = reshape_arabic(line)
        c.drawRightString(width - 40, y, ar_line)
        y -= 30

    c.save()
    return file_name

# 

def calculate_vacation():
    name = entry_name.get()
    start_date = entry_start.get()
    end_date = entry_end.get()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            raise ValueError("تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")

        vacation_days = (end - start).days + 1
        remaining = 30 - vacation_days

        statement = f"""
        اسم الموظف: {name}
        تاريخ البداية: {start_date}
        تاريخ النهاية: {end_date}
        عدد أيام العطلة: {vacation_days}
        المتبقي: {remaining} يوم
        """

        messagebox.showinfo("نتيجة العطلة", statement)

        file_path = save_statement_as_pdf(name, start_date, end_date, vacation_days, remaining)

        os.startfile(file_path, "print")

    except ValueError as ve:
        messagebox.showerror("خطأ في الإدخال", str(ve))


# GUI
window = tk.Tk()
window.title("حاسبة عطلة الموظف")
window.geometry("400x300")

tk.Label(window, text="اسم الموظف:").pack(pady=5)
entry_name = tk.Entry(window, width=40)
entry_name.pack()

tk.Label(window, text="تاريخ البداية (YYYY-MM-DD):").pack(pady=5)
entry_start = tk.Entry(window, width=40)
entry_start.pack()

tk.Label(window, text="تاريخ النهاية (YYYY-MM-DD):").pack(pady=5)
entry_end = tk.Entry(window, width=40)
entry_end.pack()

tk.Button(window, text="احسب واطبع", command=calculate_vacation).pack(pady=20)

window.mainloop()
