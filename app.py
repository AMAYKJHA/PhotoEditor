import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from imagemanager import ImageManager

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme("green")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Photo Editor")
        self.geometry("1000x700")
        self._slider_update_after_id = None
        self.file_path = None
        self.compare_image = False
        self.image = None
        self.image_edit = ImageManager()
        self.light_slider_list = []
        self.color_slider_list = []

        self.configure_grid()
        self.image_panel()
        self.tools_panel()
        self.lower_panel()
        self.bind("<Configure>", self.on_resize)

    def configure_grid(self):
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

    def image_panel(self):
        self.imageframe = ctk.CTkFrame(self, border_width=1)
        self.imageframe.grid(column=0, row=0, padx=7, pady=(17,0), sticky='news')
        self.imageframe.rowconfigure(0, weight=1)
        self.imageframe.columnconfigure(0, weight=1)
        self.imagelabel = ctk.CTkLabel(master=self.imageframe, text='')
        self.imagelabel.grid(row=0, column=0, sticky='news')
        self.imageframe.bind("<Configure>", lambda event: self.display_image())

    def tools_panel(self):
        self.tabs = ctk.CTkTabview(master=self, border_width=1)
        self.tabs.grid(row=0, column=1, sticky='news', rowspan=2)
        self.tabs.add('Adjust')
        self.tabs.add('Filter')
        self.tabs.add('Resize')
        self.build_adjust_tab()
        self.build_filter_tab()
        self.build_resize_tab()

    def build_adjust_tab(self):
        adjust_tab = self.tabs.tab('Adjust')
        adjust_tab.rowconfigure((0,1), weight=1)
        light_properties = ['Brightness', 'Contrast', 'Exposure', 'Vignette']
        color_properties = ['Saturation','Sharpness', 'Clarity', 'Temperature']

        light_frame = ctk.CTkFrame(adjust_tab)
        light_frame.grid(row=0, sticky='ew')
        ctk.CTkLabel(light_frame, text='Lighting', font=('Calibri', 20)).grid(row=0, sticky='w')
        self.add_sliders(light_frame, light_properties, self.light_slider_list)

        color_frame = ctk.CTkFrame(adjust_tab)
        color_frame.grid(row=1, sticky='ew')
        ctk.CTkLabel(color_frame, text='Color', font=('Calibri', 20)).grid(row=0, sticky='w')
        self.add_sliders(color_frame, color_properties, self.color_slider_list)

    def add_sliders(self, frame, properties, slider_list):
        for i, prop in enumerate(properties):
            slider = ctk.CTkSlider(frame, from_=-100, to=100, command=self.update_image)
            slider_list.append(slider)
            ctk.CTkLabel(frame, text=prop).grid(row=2*i+1, pady=(10,10))
            slider.grid(row=2*i+2, column=0, sticky='ew')

    def build_filter_tab(self):
        filter_tab = self.tabs.tab('Filter')
        ctk.CTkLabel(filter_tab, text='Filters', font=('Calibri', 20)).grid(row=1, sticky='w')
    
    def build_resize_tab(self):
        filter_tab = self.tabs.tab('Resize')
        ctk.CTkLabel(filter_tab, text='Resize', font=('Calibri', 20)).grid(row=1, sticky='w')

    def lower_panel(self):
        self.upload_btn = ctk.CTkButton(master=self, text="Upload", width=60, command=self.upload_image)
        self.upload_btn.grid(row=1, column=0, sticky='nw', padx=7, pady=5)
        self.filename_label = ctk.CTkLabel(self, text='')
        self.filename_label.grid(row=1, column=0, sticky='n')
        
        self.compare_button = ctk.CTkButton(self, text='Compare', width=60)
        self.compare_button.grid(row=1, column=0, sticky='ne', padx=(5,5), pady=5)
        self.compare_button.bind("<ButtonPress-1>", lambda e: self.compare_btn_clicked(True))
        self.compare_button.bind("<ButtonRelease-1>", lambda e: self.compare_btn_clicked(False))

    def compare_btn_clicked(self, value):
        self.compare_image = value
        if self.compare_image:
            self.compare_button.configure(text='Original')
            self.display_image()
        else:
            self.compare_button.configure(text='Compare')
            self.display_image()
        
    def upload_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if self.file_path:
            self.image_edit.load_image(self.file_path)
            filename = self.file_path.split('/')[-1]
            self.filename_label.configure(text=filename)
            self.display_image()
    
    def update_image(self, _=None):
        if self.file_path:
            self.image_edit.reset_edits()
            self.image_edit.set_brightness(self.light_slider_list[0].get())
            self.image_edit.set_contrast(self.light_slider_list[1].get())
            self.image_edit.set_saturation(self.color_slider_list[0].get())
            self.image_edit.set_sharpness(self.color_slider_list[1].get())
            self.display_image()
    
    def display_image(self):
        if self.file_path is None:
            return
        frame_width = self.imageframe.winfo_width()
        frame_height = self.imageframe.winfo_height()
        if frame_width < 10 or frame_height < 10:
            self.after(100, self.display_image)
            return
        
        img = self.image_edit.get_image(value = 0 if self.compare_image else 1)
        img_ratio = img.width / img.height
        frame_ratio = frame_width / frame_height
        if img_ratio > frame_ratio:
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            new_height = frame_height
            new_width = int(frame_height * img_ratio)
        resized_img = img.resize((new_width, new_height))
        self.image = ImageTk.PhotoImage(resized_img)
        self.imagelabel.configure(image=self.image)

    def on_resize(self, event):
        if self._slider_update_after_id is not None:
            self.after_cancel(self._slider_update_after_id)
        self._slider_update_after_id = self.after(100, self.update_slider_widths)

    def update_slider_widths(self):
        tab_width = self.tabs.winfo_width()
        if tab_width < 10:
            self.after(100, self.update_slider_widths)
            return
        slider_width = int(tab_width * 0.6)
        for slider in self.light_slider_list + self.color_slider_list:
            if slider.winfo_exists():
                slider.configure(width=slider_width)
        self._slider_update_after_id = None


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()