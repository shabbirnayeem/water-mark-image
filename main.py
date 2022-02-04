import tkinter
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

    # enter file  in the entry box
    path_entry.delete(0, 'end')
    path_entry.insert(0, file_path)


def multi_mark():
    """
    when this is click the text covers the whole image with multiple text
    """
    global logo_image
    img = Image.open(path_entry.get())
    # determine the size of the image
    img_width, img_height = img.size

    # water mark the image
    # The first part, "1.0" means that the input should be read from line one,
    # character zero (ie: the very first character).
    # The END part means to read until the end of the text box is reached.
    # The only issue with this is that it actually adds a newline to our input.
    # So, in order to fix it we should change END to end-1c. means delete 1 character
    text = text_entry.get("1.0", 'end-1c')
    draw = ImageDraw.Draw(img)

    # font_entry.get(): getting the font from the font text
    # font_size: getting hold hold of the font size from the dropdown
    font = ImageFont.truetype('arial.ttf', font_size.get())
    text_width, text_height = draw.textsize(text, font)

    # the outer loop's left var starts at 0 and increases by img_width
    # the inter loop's top var start at 0 and increases by img_height
    for left in range(0, img_width, text_width):
        for top in range(0, img_height, text_height):
            # Draw the watermark on the image
            draw.text((left, top), text, font=font, fill=(255, 255, 255))

    # creating new image after adding water mark to the mage
    logo_image = ImageTk.PhotoImage(image=img)
    # replacing the current image with the water marked image
    select_button.configure(image=logo_image)

    return img


def one_mark():
    """
    when this is clicked the text is put in the middle of the image
    """
    global logo_image
    img = Image.open(path_entry.get())
    # determine the size of the image
    img_width, img_height = img.size

    # water mark the image
    # The first part, "1.0" means that the input should be read from line one,
    # character zero (ie: the very first character).
    # The END part means to read until the end of the text box is reached.
    # The only issue with this is that it actually adds a newline to our input.
    # So, in order to fix it we should change END to end-1c. means delete 1 character
    text = text_entry.get("1.0", 'end-1c')
    draw = ImageDraw.Draw(img)

    # font_entry.get(): getting the font from the font text
    # font_size: getting hold hold of the font size from the dropdown
    font = ImageFont.truetype('arial.ttf', font_size.get())
    text_width, text_height = draw.textsize(text, font)

    # calculating to put the text in the center of the image
    new_width = (img_width - text_width) / 2
    new_height = (img_height - text_height) / 2
    draw.text((new_width, new_height), text, font=font, fill='red', align='center')

    # creating new image after adding water mark to the mage
    logo_image = ImageTk.PhotoImage(image=img)
    # replacing the current image with the water marked image
    select_button.configure(image=logo_image)

    return img


def button_clicked(button_id):
    # when buttons are click it will enter the button_id in button_num and save() will use this determine which
    # water mark to save
    button_num.delete(0, 'end')
    button_num.insert(0, button_id)


def save():
    file = path_entry.get()
    file_name, ext = os.path.splitext(file)

    button = button_num.get()
    if button == '1':
        updated_img = one_mark()
        # save the img in the same dir with the originalname_watermarked
        updated_img.save(f"{file_name}_watermarked{ext}", format="png")
    elif button == '2':
        updated_img = multi_mark()
        # call water_mark function to get host of the water_marked img
        # updated_img = image_to_save
        # save the img in the same dir with the originalname__watermarked
        updated_img.save(f"{file_name}_watermarked{ext}", format="png")


# ---------------------------------------------- Setup UI ------------------------------------------------
window = tk.Tk()

window.title("Watermark 1000")
window.config(background='#343435', padx=25, pady=25)
# minimize size of the windows
window.minsize(width=800, height=600)
window.resizable(width=True, height=True)

# initial image
logo_image = tk.PhotoImage(file="logo.png")


# creating label
select_label = ttk.Label(window, text="Click on the image to select a new image")
# select_label.pack(pady=15)
select_label.grid(row=0, column=4, pady=15, padx=(150, 0))
# calling the file_explorer inside select_button
# when user click on the select_button it will open file explore and allow them to select a image
select_button = tk.Button(window, text="SELECT IMAGES", image=logo_image, command=image_path)
# select_button.pack()
select_button.grid(row=1, column=2, columnspan=25, rowspan=25)

# Enter text to water mark the image
text_label = ttk.Label(text="Enter Text")
text_label.grid(row=1, column=0, sticky='W')
text_entry = tk.Text(height=2, width=25)
text_entry.grid(row=1, column=1, sticky='W', padx=(0, 15))

# fonts
font_label = ttk.Label(text="Enter Font")
font_label.grid(row=2, column=0, sticky='W')
font_entry = ttk.Entry(width=10)
# font_entry.pack(side=tkinter.RIGHT)
# font_entry.grid(row=2, column=1, sticky='W')

# font size using Dropdown menu
font_list = [num for num in range(101)]
# setting the font data type
font_size = tk.IntVar()
# setting the default font size
font_size.set(11)
# creating the dropdown
drop = ttk.OptionMenu(window, font_size, *font_list)
drop.grid(row=2, column=1, sticky='W')

# when this is clicked the text is put in the middle of the image
one_button = ttk.Button(window, text="◙", command=lambda: [one_mark(), button_clicked(1)])
one_button.grid(row=3, column=0, sticky='W')

# when this is click the text covers the whole image with multiple text
multi_button = ttk.Button(window, text="◙ ◙ ◙\n◙ ◙ ◙", command=lambda: [multi_mark(), button_clicked(2)])
multi_button.grid(row=3, column=1, sticky='W', padx=(10, 0))

# save the image to the download folder
save_button = ttk.Button(window, text="SAVE", command=save)
save_button.grid(row=4, column=0, sticky='W')

# setting the font and font size for the label
style = ttk.Style(window)
style.configure("TLabel", font=('Helvetica', 11),)

# setting the font and font size for the button
style = ttk.Style(window)
style.configure("TButton", font=('Helvetica', 11),)

# Getting the path when the user browse for images
path_entry = ttk.Entry(width=100)

# Getting hold of what button clicked
button_num = ttk.Entry(width=10)

window.mainloop()
