from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
from pathlib import Path
import sign_window

# Hàm để lấy đường dẫn tương đối đến thư mục assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Hàm khi nhấn nút "SIGN RECOGNITION"
def sign_recognition():
    sign_window.show_window()

def main():
    window = Tk()
    window.title("App")

    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Tính toán vị trí của cửa sổ
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2

    window.geometry(f"1200x700+{x}+{y}")

    window.configure(bg = "#FFFFFF")

    # Tạo canvas
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Vẽ các hình và nút trên canvas
    canvas.create_rectangle(0.0, 154.0, 303.0, 688.0, fill="#FBFBFB", outline="")
    canvas.create_rectangle(913.0, 154.0, 1182.0, 684.0, fill="#FBFBFB", outline="")
    canvas.create_rectangle(0.0, 0.0, 1200.0, 154.0, fill="#FBFBFB", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(1124.0, 71.0, image=image_image_1)

    button_image_1 = PhotoImage(file=relative_to_assets("button_home.png"))
    button_home = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda : print("hello"),
        relief="flat"
    )
    button_home.place(x=17.0, y=213.0, width=278.0, height=46.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(55.0, 72.0, image=image_image_2)

    button_image_2 = PhotoImage(file=relative_to_assets("button_sign.png"))
    button_sign = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=sign_recognition,
        relief="flat"
    )
    button_sign.place(x=17.0, y=273.0, width=278.0, height=46.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(x=17.0, y=333.0, width=278.0, height=46.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(x=12.0, y=393.0, width=278.0, height=46.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(x=12.0, y=631.0, width=278.0, height=46.0)

    canvas.create_text(
        90.0,
        56.0,
        anchor="nw",
        text="SIGN RECOGNITION",
        fill="#000000",
        font=("Lato Bold", 27 * -1)
    )

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(622.0, 433.0, image=image_image_3)

    canvas.create_text(
        950.0,
        205.0,
        anchor="nw",
        text="Note",
        fill="#000000",
        font=("Lato Bold", 22 * -1)
    )

    canvas.create_text(
        950.0,
        285.0,
        anchor="nw",
        text="This topic is\n used for research\n and educational\n use only.\n It may not\n be used for\n commercial purposes.",
        fill="#000000",
        font=("Light", 20 * -1)
    )

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
    main()
