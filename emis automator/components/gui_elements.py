import customtkinter as ctk
# import squircled_CTk as SCTk

default_classes: dict[str, type] = {
    # "button": SCTk.SquircleButton,
    # "entry": SCTk.SquircleEntry,
    "label": ctk.CTkLabel,
    "optionmenu": ctk.CTkOptionMenu,
    "textbox": ctk.CTkTextbox,
}




class RGB:
    def __init__(self, r: str, g: str, b: str):
        self.r = int(r, 16)
        self.g = int(g, 16)
        self.b = int(b, 16)

    def invert_single(self, color: int):
        raw = hex(255 - color)[2:]
        return raw.zfill(2)

    def invert(self):
        return self.invert_single(self.r) + self.invert_single(self.g) + self.invert_single(self.b)

    def darken_single(self, color: int):
        raw = hex(color//2)[2:]
        return raw.zfill(2)

    def darken(self):
        return self.darken_single(self.r) + self.darken_single(self.g) + self.darken_single(self.b)

    def lighten_single(self, color: int):
        raw = hex(color + (255 - color)//2)[2:]
        return raw.zfill(2)

    def lighten(self):
        return self.lighten_single(self.r) + self.lighten_single(self.g) + self.lighten_single(self.b)

def invert_color(color: str) -> str:
    color = color.replace("#", "")
    rgb = RGB(color[:2], color[2:4], color[4:])
    return "#" + rgb.invert()

def darken_color(color: str) -> str:
    color = color.replace("#", "")
    rgb = RGB(color[:2], color[2:4], color[4:])
    return "#" + rgb.darken()

def lighten_color(color: str) -> str:
    color = color.replace("#", "")
    rgb = RGB(color[:2], color[2:4], color[4:])
    return "#" + rgb.lighten()

# class _labeled:
#     def __init__(self, *args, **kwargs):
#         if "text" not in kwargs:
#             kwargs["text"] = self.__class__.__name__
#         if "placeholder_text" not in kwargs:
#             kwargs["placeholder_text"] = self.__class__.__name__
        

class Button(ctk.CTkButton):
    saved_configurations: dict[str, dict[str, any]] = {}
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        # if "smoothness" not in kwargs:
        #     kwargs["smoothness"] = 30
        super().__init__(*args, **kwargs)

    def save_configuration(self, configuration_name: str, configuration: dict[str, any] = None):
        if configuration is None:
            configuration: dict(str) = {
                "text": self._text,
                "bg_color": ...
            }
        self.saved_configurations[configuration_name] = configuration

class SmallButton(Button):
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=12)
        if "height" not in kwargs:
            kwargs["height"] = 25
        # if "squircle_n" not in kwargs:
        #     kwargs["squircle_n"] = 2.5
        if "width" not in kwargs:
            kwargs["width"] = len(kwargs["text"]) * kwargs["font"]._size + kwargs["height"] * 0.5
        super().__init__(*args, **kwargs)

class NormalButton(Button):
    def __init__(self, *args, **kwargs):
        # if "squircle_n" not in kwargs:
        #     kwargs["squircle_n"] = 3
        if "height" not in kwargs:
            kwargs["height"] = 50
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=16, weight="bold")
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "width" not in kwargs:
            kwargs["width"] = len(kwargs["text"]) * kwargs["font"]._size + kwargs["height"] * 0.5
        super().__init__(*args, **kwargs)

class BigButton(Button):
    def __init__(self, *args, **kwargs):
        # if "squircle_n" not in kwargs:
        #     kwargs["squircle_n"] = 3
        if "height" not in kwargs:
            kwargs["height"] = 70
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=20, weight="bold")
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "width" not in kwargs:
            kwargs["width"] = len(kwargs["text"]) * kwargs["font"]._size * 0.8 + kwargs["height"] * 0.5 + 10
        super().__init__(*args, **kwargs)


class Entry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        # if "squircle_n" not in kwargs:
        #     kwargs["squircle_n"] = 3
        if "width" not in kwargs:
            kwargs["width"] = 200
        if "height" not in kwargs:
            kwargs["height"] = 30
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=12)
        if "placeholder_text" not in kwargs:
            kwargs["placeholder_text"] = self.__class__.__name__
        super().__init__(*args, **kwargs)


class Label(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        super().__init__(*args, **kwargs)

class SmallLabel(Label):
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=14)
        super().__init__(*args, **kwargs)

class NormalLabel(Label):
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=20)
        super().__init__(*args, **kwargs)

class BigLabel(Label):
    def __init__(self, *args, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.__class__.__name__
        if "font" not in kwargs:
            kwargs["font"] = ctk.CTkFont(size=28, weight="bold")
        super().__init__(*args, **kwargs)


# class OptionMenu(SCTk.SquircleOptionMenu):
#     def __init__(self, *args, **kwargs):
#         if "values" not in kwargs:
#             kwargs["values"] = [self.__class__.__name__]
#         if "squircle_n" not in kwargs:
#             kwargs["squircle_n"] = 3
#         super().__init__(*args, **kwargs)

if __name__ == "not __main__":
    app = ctk.CTk()
    app.geometry("400x300")


    # button = SmallButton(app)
    # button.pack(pady=20)

    # fullsize showcase
    showcase = ctk.CTkCanvas(app, width=app.winfo_screenwidth(), height=app.winfo_screenheight())
    showcase.pack()
    showcase.create_oval(0, 0, 100, 100, fill="#FF0000")
    showcase.create_oval(0, 100, 100, 200, fill=invert_color("#FF0000"))
    showcase.create_oval(0, 200, 100, 300, fill=darken_color("#FF0000"))
    showcase.create_oval(0, 300, 100, 400, fill=lighten_color("#FF0000"))



    app.mainloop()





import customtkinter as ctk
from squircle_engine import SquircleDrawEngine

class SquircleButton(ctk.CTkButton):
    def __init__(self, *args, squircle_n=4, **kwargs):
        super().__init__(*args, **kwargs)
        
        # INJECTION: Replace the default engine with our custom one
        # We pass the existing canvas to our new engine
        self._draw_engine = SquircleDrawEngine(self._canvas, squircle_n=squircle_n)
        
        # Force a redraw so the new engine takes over immediately
        self._draw()

class SquircleEntry(ctk.CTkEntry):
    def __init__(self, *args, squircle_n=4, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Same injection
        self._draw_engine = SquircleDrawEngine(self._canvas, squircle_n=squircle_n)
        
        # Apply the padding logic we discovered earlier
        self._canvas.bind("<Configure>", self._update_dimensions)
        self._draw()

    def _update_dimensions(self, event=None):
        # Keeps text centered safely
        h = self._current_height
        w = self._current_width
        margin = h * 0.35 
        
        for item in self._canvas.find_all():
            if self._canvas.type(item) == "window":
                self._canvas.coords(item, margin, h/2)
                self._canvas.itemconfig(item, width=w - (margin * 2))


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x400")
    
    # 1. Button Test
    btn = SquircleButton(app, text="Engine Swapped!", width=200, height=60, 
                         fg_color="green", border_width=4, border_color="white", squircle_n=3)
    btn.pack(pady=20)

    print(btn._draw_engine)
    
    # 2. Entry Test
    entry = SquircleEntry(app, placeholder_text="Type in a squircle...", width=300, height=50)
    entry.pack(pady=20)

    # 3. Standard CTk Button (Control Group)
    # This proves we haven't broken the rest of the library
    std_btn = ctk.CTkButton(app, text="I am normal")
    std_btn.pack(pady=20)

    app.mainloop()