import os
import re
import sys

import wx

from .color import Color
from .font import Font


class Display():

    def __init__(self, width=80, height=24, font=Font.ATI_8X14, title=''):

        self.app = wx.App()

        self.default_bg_color = Color.BLACK
        self.default_fg_color = Color.WHITE

        self.grid_width = width
        self.grid_height = height

        self.color_regex = re.compile(r'%([bc])\{([^}]*)\}')

        self.load_glyphs(font)

        self.client_size = (width * self.font_width, height * self.font_height)

        # Windows Version
        buffer_image = wx.Image(self.client_size[0], self.client_size[1])
        buffer_image.SetRGB(
            wx.Rect(0, 0, self.client_size[0], self.client_size[1]),
            0,
            0,
            0
        )
        self.buffer_bitmap = buffer_image.ConvertToBitmap()

        # Mac Version
        # self.buffer_bitmap = wx.Bitmap.FromRGBA(
        #     self.client_size[0], 
        #     self.client_size[1]
        # )

        self.display_grid = [
            [
                {
                    'x': x,
                    'y': y,
                    'character': ' ', 
                    'fg_color': Color.WHITE, 
                    'bg_color': Color.BLACK
                } for y in range(height)
            ] for x in range(width)
        ]

        self.updates = []
        
        self.frame = wx.Frame()
        self.frame.Bind(wx.EVT_PAINT, self.paint)

        self.frame.Create(None, title=title)
        self.frame.SetClientSize(self.client_size)

        # Mac Version
        # self.frame.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.frame.Centre()

    def check_bounds(self, x, y):
        if x < 0 or x >= self.grid_width:
            raise ValueError(
                'The value of x must be within [0, ' 
                + str(self.grid_width - 1)
                + ']'
            )

        if y < 0 or y >= self.grid_height:
            raise ValueError(
                'The value of y must be within [0, '
                + str(self.grid_height - 1)
                + ']'
            )

    def color_string_length(self, text):
        length = len(text)

        for m in self.color_regex.finditer(text):
            length -= m.end() - m.start()

        return length

    def get_glyph(self, character, fg_color, bg_color):

        index = ord(character)

        key = str(fg_color) + character + str(bg_color)

        if not key in self.glyph_dictionary:
            mask = wx.Mask(self.glyph_images[index], Color.BLACK.value)

            fg_image = wx.Image(self.font_width, self.font_height)
            fg_image.SetRGB(
                wx.Rect(0, 0, self.font_width, self.font_height),
                fg_color.value.Red(),
                fg_color.value.Green(),
                fg_color.value.Blue()
            )

            fg_bitmap = fg_image.ConvertToBitmap()
            fg_bitmap.SetMask(mask)

            bitmap = wx.Bitmap(self.font_width, self.font_height)

            dc = wx.MemoryDC(bitmap)
            dc.SetBackground(wx.Brush(bg_color.value))
            dc.Clear()

            dc.DrawBitmap(fg_bitmap, 0, 0, useMask=True)
            dc.SelectObject(wx.NullBitmap)

            self.glyph_dictionary[key] = bitmap

        return self.glyph_dictionary[key]

    def load_glyphs(self, font):

        font_file = os.path.join(
            os.path.dirname(sys.modules['RoguePython.display'].__file__),
            font.value['file'])

        glyph_matrix = wx.Bitmap()
        glyph_matrix.LoadFile(font_file)

        self.glyph_dictionary = dict()

        self.font_width = glyph_matrix.GetWidth() // 16
        self.font_height = glyph_matrix.GetHeight() // 16

        self.glyph_images = []

        for i in range(256):
            area = wx.Rect(
                (i % 16) * self.font_width,
                (i // 16) * self.font_height,
                self.font_width,
                self.font_height
            )

            image = glyph_matrix.GetSubBitmap(area)

            self.glyph_images.append(image)

    def paint(self, e):

        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer_bitmap)

        for i in range(len(self.updates)):
            glyph = self.get_glyph(
                self.updates[i]['character'], 
                self.updates[i]['fg_color'], 
                self.updates[i]['bg_color']
            )

            dc.DrawBitmap(
                glyph, 
                self.updates[i]['x'] * self.font_width, 
                self.updates[i]['y'] * self.font_height
            )

        dc.SelectObject(wx.NullBitmap)

        self.updates.clear()

        # Mac Version
        # paint_dc = wx.AutoBufferedPaintDC(self.frame)

        # Windows Version
        paint_dc = wx.PaintDC(self.frame)
        paint_dc.DrawBitmap(self.buffer_bitmap, 0, 0)

    def process_color_string(self, text):
        
        current_fg = self.default_fg_color
        current_bg = self.default_bg_color
        text_index = 0
        stubs = []

        for m in self.color_regex.finditer(text):
            text_stub = text[text_index:m.start()]
            stubs.append(
                {
                    'text': text_stub, 
                    'fg': current_fg, 
                    'bg': current_bg
                }
            )

            if m.group(1) == 'b':
                if len(m.group(2)) == 0:
                    current_bg = self.default_bg_color
                else:
                    current_bg = Color[m.group(2)]
            else:
                if len(m.group(2)) == 0:
                    current_fg = self.default_fg_color
                else:
                    current_fg = Color[m.group(2)]

            text_index = m.end()

        text_stub = text[text_index:]
        stubs.append(
            {
                'text': text_stub,
                'fg': current_fg,
                'bg': current_bg
            }
        )

        return stubs

    def put_character(self, character, x, y, fg_color=-1, bg_color=-1):

        self.check_bounds(x, y)

        if fg_color == -1:
            fg_color = self.default_fg_color

        if bg_color == -1:
            bg_color = self.default_bg_color

        update = {
            'x': x,
            'y': y,
            'character': character,
            'fg_color': fg_color,
            'bg_color': bg_color
        }

        if self.display_grid[x][y] != update:
            self.updates.append(update)
            self.display_grid[x][y] = update

    def put_text(self, text, x, y, width=-1, height=-1):

        if width == -1:
            width = self.grid_width - x

        if height == -1:
            height = self.grid_height - y

        dx = 0
        dy = 0

        text_data = self.process_color_string(text)

        for i in range(len(text_data)):
            data = text_data[i]
            words = data['text'].split(' ')

            for j in range(len(words)):
                if dx + len(words[j]) + (0 if j == 0 else 1) > width:
                    dx = 0
                    dy += 1
                    if dy == height:
                        return

                if j > 0 and dx > 0:
                    self.put_character(
                        ' ', 
                        dx + x, 
                        dy + y, 
                        data['fg'], 
                        data['bg']
                    )

                    dx += 1

                if len(words[j]) > 0:
                    for k in range(len(words[j])):
                        self.put_character(
                            words[j][k],
                            dx + x,
                            dy + y,
                            data['fg'],
                            data['bg']
                        )

                        dx += 1

    def put_text_centered(self, text, y, x=0, width=-1):

        if width == -1:
            width = self.grid_width - x

        length = self.color_string_length(text)
        dx = (width - length) // 2

        if dx < 0:
            dx = 0

        self.put_text(text, dx + x, y, length, 1)

    def start(self):

        self.frame.Show(True)
        self.app.MainLoop()

