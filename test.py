import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Image Display Example")

    # Tạo đối tượng PhotoImage
    image = tk.PhotoImage(file="images/queen.png")

    # Tạo Label để hiển thị hình ảnh
    image_label = tk.Label(root, image=image, width=100, height=100)
    image_label.grid(row=0, column=0, padx=0, pady=0)  # Đặt Label vào cửa sổ
    image_label2 = tk.Label(root, image=image)
    image_label2.grid(row=0, column=1, padx=0, pady=0)  # Đặt Label vào cửa sổ

    root.mainloop()

if __name__ == "__main__":
    main()
