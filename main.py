import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# Water Mark Image Project
# Steps:
# TODO: Use to trinket to create GUI when user can update a image
# TODO: Use Python library and add text to the image or any symbols and water mark these on the image
# TODO: Draw the water mark all over the image
# TODO: Find a way make the text less visible
# TODO: Find way to use different color
# TODO: The image text, color, and size all should come from the user

# ------------------------------------------------ FUNCTIONS -------------------------------------------------------

# select a file
def image_path():
    """
    Allow the user to select image and replace the current image with the user choice
    """
    global logo_image
    # prevent an empty tkinter window from opening
    tk.Tk().withdraw()
    # Browse for Image file
    file_path = filedialog.askopenfilename(initialdir="/", title="Select image",
                                           filetypes=(("Image files", "*.png*"), ("all files", "*.*")))
    # create new photo from the user selected file
    logo_image = tk.PhotoImage(file=file_path)
    # replace teh current image with users choice
    select_button.configure(image=logo_image)

    # enter file file in the entry box
    entry.delete(0, 'end')
    entry.insert(0, file_path)


def water_mark():
    global logo_image
    img = Image.open(entry.get())
    # determine the size of the image
    img_width, img_height = img.size
    # img = img.rotate(45)

    # water mark the image
    # The first part, "1.0" means that the input should be read from line one,
    # character zero (ie: the very first character).
    # The END part means to read until the end of the text box is reached.
    # The only issue with this is that it actually adds a newline to our input.
    # So, in order to fix it we should change END to end-1c. means delete 1 character
    text = text_entry.get("1.0", 'end-1c')
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('arial.ttf', 18)
    text_width, text_height = draw.textsize(text, font)

    margin = 10
    # calculate the x,y coordinates of the text
    x = img_width - text_width - margin
    y = img_height - text_height - margin

    # the outer loop's left var starts at 0 and increases by img_width
    # the inter loop's top var start at 0 and increases by img_height
    for left in range(0, img_width, text_width):
        for top in range(0, img_height, text_height):
            # Draw the watermark on the image
            draw.text((left, top), text, font=font, fill=(255, 255, 128))

    # creating new image after adding water mark to the mage
    logo_image = ImageTk.PhotoImage(image=img)
    # replacing the current image with the water marked image
    select_button.configure(image=logo_image)

    return img


def save():
    file = entry.get()
    file_name, ext = os.path.splitext(file)

    # call water_mark function to get host of the water_marked img
    updated_img = water_mark()
    # save the img in the same dir with the originalname__watermarked
    updated_img.save(f"{file_name}_watermarked{ext}", format="png")
    files = [("Image files", "*.png*"),
             ("Jpeg files", "*.jpg*"),
             ('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]

    file = filedialog.asksaveasfilename(filetype=files, defaultextension=files)


# ---------------------------------------------- Setup UI ------------------------------------------------
window = tk.Tk()

window.title("Watermark 1000")
window.config(background='#343435', padx=25, pady=25)
# minimize size of the windows
window.minsize(width=800, height=600)
window.resizable(width=True, height=True)

# initial image
logo_image = tk.PhotoImage(file="logo.png")
# new_image = tk.PhotoImage(select_image())


# canvas = tkinter.Canvas(width=600, height=400)
# canvas.pack()


# creating label
select_label = ttk.Label(window, text="Click on the image to select a new image")
select_label.pack(pady=15)
# calling the file_explorer inside select_button
# when user click on the select_button it will open file explore and allow them to select a image
select_button = tk.Button(window, text="SELECT IMAGES", image=logo_image, command=image_path)
select_button.pack()

text_label = ttk.Label(text="Enter Text")
text_label.pack(padx=5)
text_entry = tk.Text(height=2, width=25)
text_entry.pack(pady=20)

update_button = tk.Button(window, text="UPDATE", command=water_mark)
update_button.pack(pady=10)

save_button = tk.Button(window, text="SAVE", command=save)
save_button.pack(pady=10)

entry = ttk.Entry(width=100)
entry.pack(side='bottom', pady=15)


window.mainloop()
