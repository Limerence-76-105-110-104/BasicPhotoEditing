from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

win = Tk()

win.title("Giao diện chỉnh sửa ảnh")
win.geometry("1100x650")

img = ()
img_temp = ()
img_backup = ()
img_original = ()
accept = False
refPt = []
cropping = False
color_button_on = '#0a6806'
color_button_off = '#444444'

#---------------Nút ấn Import ảnh---------------
def open_image():
    global img, img_original, img_backup
    enable_button()

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )

    if file_path:
        img_import = cv.imread(file_path)
        print(img_import.shape[:2])
        if img_import.shape[0] > 320:
            scale_percent = 320 / img_import.shape[0]
            width = int(img_import.shape[1] * scale_percent)
            height = int(img_import.shape[0] * scale_percent)
            dim = (width, height)
            img_import = cv.resize(img_import, dim, interpolation=cv.INTER_AREA)

        elif img_import.shape[1] > 320:
            scale_percent = 320 / img_import.shape[1]
            width = int(img_import.shape[1] * scale_percent)
            height = int(img_import.shape[0] * scale_percent)
            dim = (width, height)
            img_import = cv.resize(img_import, dim, interpolation=cv.INTER_AREA)

        img = img_import
        img_backup = img
        img_original = img_import
        show_image_on_screen(img)

#---------------Nút ấn làm mờ---------------
def blur_img():
    turn_on_button(1)
    destroy_mode()
    blur_mode(True)

#---------------Bộ nút ấn ánh sáng và tương phản---------------
def chage_brightness_n_constras_image():
    turn_on_button(2)
    destroy_mode()
    brightness_n_contrast_mode(True)

#---------------Bộ nút ấn cắt ảnh---------------
def crop_img():
    turn_on_button(3)
    destroy_mode()
    crop_mode(True)

#---------------Bộ nút ấn quay ảnh---------------
def rotate_image():
    turn_on_button(4)
    destroy_mode()
    rotate_mode(True)

def flip_horizontal():
    global img
    img = cv.flip(img, 1)
    show_image_on_screen(img)

def flip_vertical():
    global img
    img = cv.flip(img, -1)
    show_image_on_screen(img)

#---------------Bộ nút ấn quay ảnh---------------
def remove_obj_image():
    turn_on_button(6)
    destroy_mode()
    remove_mode(True)

#---------------Nút ấn lưu ảnh---------------
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG files", "*.jpg"),
                                                        ("PNG files", "*.png"),
                                                        ("All files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, img)
        print(f"Ảnh đã được lưu thành công tại {file_path}")
    else:
        print("Không có file nào được chọn.")

#---------------Hiển thị / Cập nhật hình ảnh---------------
def show_image_on_screen(image):
    if image.shape[0] < 320:
        scale_percent = 320 / image.shape[0]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        image = cv.resize(image, dim, interpolation=cv.INTER_AREA)

    elif image.shape[1] < 320:
        scale_percent = 320 / image.shape[1]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        image = cv.resize(image, dim, interpolation=cv.INTER_AREA)

    cv2image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    img1 = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img1)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.grid(row=0, column=0)

def adjust_image():
    global img
    img = img_temp
    enable_button()

def cancel_mode():
    global img
    img = img_backup
    show_image_on_screen(img)
    enable_button()

#---------------Làm mờ ảnh---------------
def adjust_blur(blur):
    global img, img_temp, img_backup
    disable_button()
    img_backup = img
    if int(blur) % 2 != 0:
        blur_image = cv.blur(img, (int(blur), int(blur)), 0)
        img_temp = blur_image
        show_image_on_screen(blur_image)

def blur_mode(state):
    global frame_blur
    if state:
        frame_blur = Frame(win, borderwidth=10, bg='black')
        label_blur_of_frame = Label(frame_blur, text='Blur Image', bg='black',
                                            fg='white', font=("Arial", 17, "bold"), width=17, height=3)
        label_blur = Label(frame_blur, text='Blur', bg='black', fg='white',
                                 font=("Arial", 13, "bold"), width=10, height=3)
        button_accept = Button(frame_blur, text='Accept', width=10, height=1, borderwidth=2,
                                      command=adjust_image, pady=10, padx=5)
        button_cancel = Button(frame_blur, text='Cancel', width=10, height=1, borderwidth=2,
                                      command=cancel_mode, pady=10, padx=5)
        slider_blur = Scale(frame_blur, from_=0, to=29, orient=HORIZONTAL, command=adjust_blur, resolution=1)
        slider_blur.set(0)

        label_blur.grid(row=1, column=0)
        slider_blur.grid(row=1, column=1)

        button_accept.grid(row=2, column=0, pady=20)
        button_cancel.grid(row=2, column=1, pady=20)

        label_blur_of_frame.grid(row=0, columnspan=2)
        frame_blur.place(x=800, y=25)

    else:
        frame_blur.destroy()

#---------------Độ sáng và tương phản---------------
def adjust_brightness(brightness):
    global img, img_temp, img_backup
    disable_button()
    img_backup = img
    brightness_image = cv2.convertScaleAbs(img, alpha=1, beta=float(brightness))
    img_temp = brightness_image
    show_image_on_screen(brightness_image)

def adjust_contrast(contrast):
    global img, img_temp, img_backup
    disable_button()
    img_backup = img
    contrast_image = cv2.convertScaleAbs(img, alpha=float(contrast), beta=0)
    img_temp = contrast_image
    show_image_on_screen(contrast_image)

def brightness_n_contrast_mode(state):
    global frame_brightness_n_contrast
    if state:
        frame_brightness_n_contrast = Frame(win, borderwidth=10, bg='black')
        label_brightness_n_contrast = Label(frame_brightness_n_contrast, text='Brightness\nand\nContrast', bg='black',
                                            fg='white', font=("Arial", 17, "bold"), width=17, height=3)
        label_brightness = Label(frame_brightness_n_contrast, text='Brightness', bg='black', fg='white',
                                 font=("Arial", 13, "bold"), width=10, height=3)
        label_contrast = Label(frame_brightness_n_contrast, text='Contrast', bg='black', fg='white',
                                 font=("Arial", 13, "bold"), width=10, height=3)
        button_accept = Button(frame_brightness_n_contrast, text='Accept', width=10, height=1, borderwidth=2,
                                      command=adjust_image, pady=10, padx=5)
        button_cancel = Button(frame_brightness_n_contrast, text='Cancel', width=10, height=1, borderwidth=2,
                                      command=cancel_mode, pady=10, padx=5)
        slider_brightness = Scale(frame_brightness_n_contrast, from_=-50, to=100, orient=HORIZONTAL, command=adjust_brightness, width=10)
        slider_brightness.set(0)
        slider_contrast = Scale(frame_brightness_n_contrast, from_=0.0, to=5.0, orient=HORIZONTAL, resolution=0.1, command=adjust_contrast)
        slider_contrast.set(1.0)
        label_brightness.grid(row=1, column=0)
        slider_brightness.grid(row=1, column=1)
        label_contrast.grid(row=2, column=0)
        slider_contrast.grid(row=2, column=1)
        button_accept.grid(row=3, column=0, pady=20)
        button_cancel.grid(row=3, column=1, pady=20)
        label_brightness_n_contrast.grid(row=0, columnspan=2)
        frame_brightness_n_contrast.place(x=800, y=25)

    else:
        frame_brightness_n_contrast.destroy()

#---------------Cắt ảnh---------------
def click_and_crop(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        temp_image = img.copy()
        cv2.rectangle(temp_image, refPt[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("image", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

def crop_image():
    global img, refPt, img_temp
    img_backup = img
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click_and_crop)
    key = cv2.waitKey(0) & 0xFF
    if key == ord(' ') and len(refPt) == 2:
        img_crop = img_backup[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        img_temp = img_crop
        show_image_on_screen(img_crop)
    cv.destroyAllWindows()

def crop_mode(state):
    global frame_crop
    if state:
        frame_crop = Frame(win, borderwidth=10, bg='black')
        label_crop_of_frame = Label(frame_crop, text='Crop Image', bg='black', fg='white',
                                      font=("Arial", 19, "bold"), width=17, height=1)
        button_crop_image = Button(frame_crop, text='Crop', width=10, height=1, borderwidth=2,
                                    command=crop_image, pady=10, padx=5)
        button_accept_crop = Button(frame_crop, text='Accept', width=10, height=1, borderwidth=2,
                                    command=adjust_image, pady=10, padx=5)
        button_cancel_crop = Button(frame_crop, text='Cancel', width=10, height=1, borderwidth=2,
                                    command=cancel_mode, pady=10, padx=5)
        label_crop_of_frame.grid(row=0, columnspan=2)
        button_crop_image.grid(row=1, columnspan=2, padx=20, pady=20)
        button_accept_crop.grid(row=2, column=0)
        button_cancel_crop.grid(row=2, column=1)
        frame_crop.place(x=800, y=25)

    else:
        frame_crop.destroy()

#---------------Xoay ảnh---------------
def adjust_angle(angle):
    global img, img_temp, img_backup, rotate_state
    disable_button()
    img_backup = img
    height, width = img.shape[:2]
    print(height, width)
    rotPoint = (width//2, height//2)
    rotMat = cv.getRotationMatrix2D(rotPoint, int(angle), 1.0)
    dimentions = (width, height)
    img_rotate = cv.warpAffine(img, rotMat, dimentions)
    img_temp = img_rotate
    show_image_on_screen(img_rotate)

def rotate_mode(state):
    global frame_rotate
    if state:
        frame_rotate = Frame(win, borderwidth=10, bg='black')
        label_rotate_of_frame = Label(frame_rotate, text='Rotate Image', bg='black', fg='white', font=("Arial", 19, "bold"), width=17,
                             height=1)
        label_rotate = Label(frame_rotate, text='Rotate', bg='black', fg='white', font=("Arial", 13, "bold"), width=10,
                             height=1)
        button_flip_horizontal = Button(frame_rotate, text='Flip_horizon', width=10, height=1, borderwidth=2,
                                        command=flip_horizontal, pady=10, padx=5)
        button_flip_vertical = Button(frame_rotate, text='Flip_horizon', width=10, height=1, borderwidth=2,
                                      command=flip_vertical, pady=10, padx=5)
        button_accept_rotate = Button(frame_rotate, text='Accept', width=10, height=1, borderwidth=2,
                                      command=adjust_image, pady=10, padx=5)
        button_cancel_rotate = Button(frame_rotate, text='Cancel', width=10, height=1, borderwidth=2,
                                      command=cancel_mode, pady=10, padx=5)
        slider = Scale(frame_rotate, from_=-180, to=180, orient=HORIZONTAL, command=adjust_angle)
        slider.set(0)  # Đặt giá trị mặc định
        label_rotate_of_frame.grid(row = 0, columnspan = 2)
        label_rotate.grid(row = 1, column = 0)
        slider.grid(row = 1, column = 1, pady=20)
        button_accept_rotate.grid(row=2, column=0, pady=20)
        button_cancel_rotate.grid(row=2, column=1, pady=20)
        button_flip_horizontal.grid(row = 3, column = 0)
        button_flip_vertical.grid(row = 3, column = 1)
        frame_rotate.place(x=800, y=25)

    else:
        frame_rotate.destroy()

#---------------Xóa vật thể trên nền---------------
def remove_object():
    global img, img_temp, img_backup
    img_backup = img
    r = cv2.selectROI("Image", img, fromCenter=False, showCrosshair=True)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (int(r[0]), int(r[1])), (int(r[0] + r[2]), int(r[1] + r[3])), 255, -1)
    img_remove = cv.inpaint(img_backup, mask, 3, cv2.INPAINT_TELEA)
    img_temp = img_remove
    show_image_on_screen(img_remove)
    cv.destroyAllWindows()

def remove_mode(state):
    global frame_remove
    if state:
        frame_remove = Frame(win, borderwidth=10, bg='black')
        label_remove_of_frame = Label(frame_remove, text='Remove Object', bg='black', fg='white',
                                      font=("Arial", 19, "bold"), width=17, height=1)
        button_remove_image = Button(frame_remove, text='Remove', width=10, height=1, borderwidth=2,
                                   command=remove_object, pady=10, padx=5)
        button_accept_remove = Button(frame_remove, text='Accept', width=10, height=1, borderwidth=2,
                                      command=adjust_image, pady=10, padx=5)
        button_cancel_remove = Button(frame_remove, text='Cancel', width=10, height=1, borderwidth=2,
                                      command=cancel_mode, pady=10, padx=5)
        label_remove_of_frame.grid(row=0, columnspan=2)
        button_remove_image.grid(row=1, columnspan=2, padx=20, pady=20)
        button_accept_remove.grid(row=2, column=0)
        button_cancel_remove.grid(row=2, column=1)
        frame_remove.place(x=800, y=25)
    else:
        frame_remove.destroy()

#---------------Reset về ảnh gốc--------------
def reset_all():
    global img
    turn_on_button(7)
    img = img_original
    show_image_on_screen(img)

#---------------Xóa bộ chỉnh sửa---------------
def destroy_mode():
    blur_mode(False)
    brightness_n_contrast_mode(False)
    rotate_mode(False)
    crop_mode(False)
    remove_mode(False)

#--------------Màu On/Off của nút ấn---------------
def turn_on_button(mode):
    button_import.configure(bg=color_button_off)
    button_blur.configure(bg=color_button_off)
    button_brightness.configure(bg=color_button_off)
    button_crop.configure(bg=color_button_off)
    button_rotate.configure(bg=color_button_off)
    button_save.configure(bg=color_button_off)
    button_reset_all.configure(bg=color_button_off)
    button_remove_bg.configure(bg=color_button_off)

    if mode == 1:
        button_blur.configure(bg=color_button_on)

    elif mode == 2:
        button_brightness.configure(bg=color_button_on)

    elif mode == 3:
        button_crop.configure(bg=color_button_on)

    elif mode == 4:
        button_rotate.configure(bg=color_button_on)

    elif mode == 5:
        button_save.configure(bg=color_button_on)

    elif mode == 6:
        button_remove_bg.configure(bg=color_button_on)

    elif mode == 7:
        button_reset_all.configure(bg=color_button_on)

def enable_button():
    button_import.configure(state='normal')
    button_blur.configure(state='normal')
    button_brightness.configure(state='normal')
    button_rotate.configure(state='normal')
    button_crop.configure(state='normal')
    button_save.configure(state='normal')
    button_remove_bg.configure(state='normal')
    button_reset_all.configure(state='normal')

def disable_button():
    button_import.configure(state='disabled')
    button_blur.configure(state='disabled')
    button_brightness.configure(state='disabled')
    button_rotate.configure(state='disabled')
    button_crop.configure(state='disabled')
    button_remove_bg.configure(state='disabled')
    button_save.configure(state='disabled')

#---------------Giao diện---------------
button_import = Button(win, width=13, height=3, text='Import', fg='white', font=("Arial", 13, "bold"), command=open_image)
button_import.place(x = 20, y = 25)

button_blur = Button(win, width=13, height=3, text='Blur', fg='white', font=("Arial", 13, "bold"), state='disabled', command=blur_img)
button_blur.place(x = 20, y = 125)

button_brightness = Button(win, width=13, height=3, text='Brightness\nand\nContrast', fg='white', font=("Arial", 13, "bold"), state='disabled', command=chage_brightness_n_constras_image)
button_brightness.place(x = 20, y = 225)

button_crop = Button(win, width=13, height=3, text='Crop', fg='white', font=("Arial", 13, "bold"), state='disabled', command=crop_img)
button_crop.place(x = 20, y = 325)

button_rotate = Button(win, width=13, height=3, text='Rotate', fg='white', font=("Arial", 13, "bold"), state='disabled', command=rotate_image)
button_rotate.place(x = 20, y = 425)

button_save = Button(win, width=13, height=3, text='Save', fg='white', font=("Arial", 13, "bold"), state='disabled', command=save_image)
button_save.place(x = 310, y = 525)

button_remove_bg = Button(win, width=13, height=3, text='Remove\rBackground', fg='white', font=("Arial", 13, "bold"), state='disabled', command=remove_obj_image)
button_remove_bg.place(x = 20, y = 525)

button_reset_all = Button(win, width=13, height=3, text='Reset', fg='white', font=("Arial", 13, "bold"), state='disabled', command=reset_all)
button_reset_all.place(x = 600, y = 525)

button_exit = Button(win, width=13, height=3, text='Exit', fg='white', bg='#D60000', font=("Arial", 13, "bold"), command=win.destroy)
button_exit.place(x = 900, y = 525)

frame_blur = Frame(win, borderwidth=10, width=200)
frame_brightness_n_contrast = Frame(win, borderwidth=10, width=200)
frame_crop = Frame(win, borderwidth=10, width=200)
frame_rotate = Frame(win, borderwidth=10, width=200)
frame_remove = Frame(win, borderwidth=10, width=200)

frame_video = Frame(win, width=640, height=480, bg='black')
label = Label(frame_video)

frame_video.place(x = 200, y = 25)

turn_on_button(0)

win.mainloop()
