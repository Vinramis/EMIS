# import customtkinter as ctk
# import math

# class SquircleMixin:
#     def _get_squircle_coords(self, width: int, height: int, n: int = 4, *, smoothness: int = 100, padding: int = 1):
#         """
#         Args:
#             n: Power of the squircle, 2 is a circle, bigger n is more square-like. Defaults to 4.
#             smoothness: The smoothness of the squircle. Defaults to 100.
#             padding: Technical padding. Defaults to 1.

#         Returns:
#             A list of points that define the squircle.
#         """
#         w_eff = max(1, width - (padding * 2))
#         h_eff = max(1, height - (padding * 2))
#         points = []
#         a = w_eff / 2
#         b = h_eff / 2

#         for i in range(smoothness):
#             theta = (i / smoothness) * 2 * math.pi
#             cos_t = math.cos(theta)
#             sin_t = math.sin(theta)
#             x = (abs(cos_t) ** (2 / n)) * a * math.copysign(1, cos_t)
#             y = (abs(sin_t) ** (2 / n)) * b * math.copysign(1, sin_t)
#             points.append(x + a + padding)
#             points.append(y + b + padding)

#         return points

#     def _get_stretched_squircle_coords(self, width: int, height: int, n: int = 4, *, smoothness: int = 100, padding: int = 1):
#         """
#         Stretched squircle - is a uniradial sliced squircle with a suitable rectangle put inbetween the slices.

#         Args:
#             n: Power of the squircle, 2 is a circle, bigger n is more square-like. Defaults to 4.
#             smoothness: The smoothness of the squircle. Defaults to 100.
#             padding: Technical padding. Defaults to 1.

#         Returns:
#             A list of points that define the squircle.
#         """
#         w_eff = max(1, width - (padding * 2))
#         h_eff = max(1, height - (padding * 2))
        
#         # Determine the 'radius' based on the smallest dimension
#         r = min(w_eff, h_eff) / 2
        
#         # Calculate the flat bridge length
#         extra_w = max(0, w_eff - h_eff)
#         extra_h = max(0, h_eff - w_eff)
        
#         points = []
        
#         for i in range(smoothness):
#             theta = (i / smoothness) * 2 * math.pi
#             cos_t = math.cos(theta)
#             sin_t = math.sin(theta)
            
#             # Core squircle math
#             x = (abs(cos_t) ** (2 / n)) * r * math.copysign(1, cos_t)
#             y = (abs(sin_t) ** (2 / n)) * r * math.copysign(1, sin_t)
            
#             # Apply offsets based on which quadrant the point is in
#             x_offset = extra_w if cos_t >= 0 else 0
#             y_offset = extra_h if sin_t >= 0 else 0
            
#             points.append(x + r + padding + x_offset)
#             points.append(y + r + padding + y_offset)
            
#         return points


# class SquircleButton(ctk.CTkButton, SquircleMixin):
#     """
#     A CTk-compatible button that draws a squircle instead of a rectangle.
#     """
#     def __init__(self, *args, squircle_n=4, smoothness=100, **kwargs):
#         self.squircle_n = squircle_n
#         self.smoothness = smoothness
#         # Force a radius so CTk doesn't use the 'simple rectangle' optimization
#         kwargs["corner_radius"] = kwargs.get("corner_radius", 15)
#         super().__init__(*args, **kwargs)

#     def _draw(self, no_color_updates=False):
#         super()._draw(no_color_updates)
#         if not self._canvas:
#             return

#         # 1. THE REVEAL: Completely hide CTk's default background rectangle
#         self._canvas.delete("background")

#         w = self._current_width
#         h = self._current_height
#         new_coords = self._get_stretched_squircle_coords(w, h, n=self.squircle_n, smoothness=self.smoothness)

#         # 2. THE HIJACK: Convert all internal parts into squircles
#         # inner_parts = the button fill
#         # border_parts = the button border
#         target_tags = ["inner_parts", "border_parts", "border_parts_inner"]
        
#         target_color = getattr(self, '_current_color', self._fg_color)
#         current_fill = self._apply_appearance_mode(target_color)

#         for tag in target_tags:
#             items = self._canvas.find_withtag(tag)
#             for item in items:
#                 # We replace the item type to allow for 200+ points
#                 self._canvas.delete(item)
#                 self._canvas.create_polygon(
#                     new_coords,
#                     fill=current_fill if "inner" in tag else "",
#                     outline=self._apply_appearance_mode(self._border_color) if self._border_width > 0 else "",
#                     width=self._border_width,
#                     tag=tag,
#                     smooth=True
#                 )

#         # 3. TEXT SAFETY: Ensure the text doesn't have its own box background
#         if self._canvas.find_withtag("text"):
#             # Set the text background to empty/transparent
#             self._canvas.itemconfig("text", fill=self._apply_appearance_mode(self._text_color))
#             self._canvas.tag_raise("text")


# class SquircleEntry(ctk.CTkEntry, SquircleMixin):
#     def __init__(self, *args, squircle_n=4, **kwargs):
#         self.squircle_n = squircle_n
#         kwargs["corner_radius"] = kwargs.get("corner_radius", 15)
#         super().__init__(*args, **kwargs)

#     def _draw(self, no_color_updates=False):
#         super()._draw(no_color_updates)
#         if not self._canvas:
#             return

#         self._canvas.delete("background")

#         w = self._current_width
#         h = self._current_height
#         new_coords = self._get_stretched_squircle_coords(w, h, n=self.squircle_n)

#         # 1. Identity Theft: Transform the background and border
#         target_tags = ["inner_parts", "border_parts"]
#         current_fill = self._apply_appearance_mode(self._fg_color)
#         border_fill = self._apply_appearance_mode(self._border_color)

#         for tag in target_tags:
#             items = self._canvas.find_withtag(tag)
#             for item in items:
#                 self._canvas.delete(item)
#                 self._canvas.create_polygon(
#                     new_coords,
#                     fill=current_fill if tag == "inner_parts" else "",
#                     outline=border_fill if self._border_width > 0 else "",
#                     width=self._border_width,
#                     tag=tag,
#                     smooth=True
#                 )

#         # 2. THE ADAPTIVE MARGIN MATH
#         # We calculate the horizontal safe-zone based on height.
#         # Formula: margin = height * 0.35 (adjust 0.35 to your taste)
#         dynamic_margin = h * 0.5
        
#         for item in self._canvas.find_all():
#             if self._canvas.type(item) == "window":
#                 # Position the internal entry widget
#                 self._canvas.coords(item, dynamic_margin, h/2) 
#                 # Constrain its width so it doesn't clip the right curve
#                 self._canvas.itemconfig(item, width=w - (dynamic_margin * 2))
#                 self._canvas.tag_raise(item)

#         if self._canvas.find_withtag("placeholder_text"):
#             self._canvas.itemconfig("placeholder_text", fill=self._apply_appearance_mode(self._text_color))
#             self._canvas.tag_raise("placeholder_text")

#         # 3. TEXT SAFETY: Ensure the text doesn't have its own box background
#         if self._canvas.find_withtag("text"):
#             # Set the text background to empty/transparent
#             self._canvas.itemconfig("text", fill=self._apply_appearance_mode(self._text_color))
#             self._canvas.tag_raise("text")


# # --- Test Area ---
# if __name__ == "__main__":
#     app = ctk.CTk()
#     app.configure(fg_color="#000001", font=("Arial", 16))

#     app.geometry("400x300")
    

#     size = 500
#     normal_button = ctk.CTkButton(
#         app, 
#         text="Not the beautiful\nsquircled button",
#         font=ctk.CTkFont(family="Arial", size=int(size/10)),
#         width=size,
#         height=size/2,
#         border_width=size/200,
#         corner_radius=size/4.5,
#         border_color="red",
#     )
#     normal_button.pack(expand=True)

#     sq_btn = SquircleButton(
#         app, 
#         text="The beautiful\nsquircled button",
#         font=ctk.CTkFont(family="Arial", size=int(size/10)),
#         squircle_n=3,
#         width=size,
#         height=size/2,
#         border_width=size/200,
#         border_color="red",
#     )
#     sq_btn.pack(expand=True)

#     entry = SquircleEntry(
#         app, 
#         placeholder_text="I have room to breathe...",
#         squircle_n=4,
#         width=size,
#         height=size/8,
#         border_width=size/200,
#         border_color="red",
#         font=("Arial", size/20),
#     )
#     entry.pack(expand=True)


#     app.mainloop()
