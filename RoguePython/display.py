from enum import Enum
import os
import sys

import wx



class Font(Enum):

    ATI_8X8 = {'file': os.path.join('fonts', 'cp437-ATI-8x8.png'), 'width': 8, 'height': 8}
    ATI_8X14 = {'file': os.path.join('fonts', 'cp437-ATI-8x14.png'), 'width': 8, 'height': 14}
    ATI_8X16 = {'file': os.path.join('fonts', 'cp437-ATI-8x16.png'), 'width': 8, 'height': 16}
    ATI_10X10 = {'file': os.path.join('fonts', 'cp437-ATI-10x10.png'), 'width': 10, 'height': 10}
    IBMCGA_8X8 = {'file': os.path.join('fonts', 'cp437-IBM-CGA-8x8.png'), 'width': 8, 'height': 8}
    IBMCGA_10X10 = {'file': os.path.join('fonts', 'cp437-IBM-CGA-10x10.png'), 'width': 10, 'height': 10}
    IBMCGA_12X12 = {'file': os.path.join('fonts', 'cp437-IBM-CGA-12x12.png'), 'width': 12, 'height': 12}
    IBMEGA_8X14 = {'file': os.path.join('fonts', 'cp437-IBM-EGA-8x14.png'), 'width': 8, 'height': 14}
    IBMVGA_8X16 = {'file': os.path.join('fonts', 'cp437-IBM-VGA-8x16.png'), 'width': 8, 'height': 16}


class Display():

    def __init__(self, width=80, height=24, font=Font.ATI_8X14, title=''):

        self.app = wx.App()

        self.load_glyphs(font)
        
        self.frame = wx.Frame()
        self.frame.Bind(wx.EVT_PAINT, self.paint)

        self.frame.Create(None, title=title)
        self.frame.SetClientSize(width * self.font_width, height * self.font_height)
        self.frame.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.frame.Centre()

    def load_glyphs(self, font):

        font_file = os.path.join(
            os.path.dirname(sys.modules['RoguePython.display'].__file__),
            font.value['file'])

        glyph_matrix = wx.Bitmap()
        glyph_matrix.LoadFile(font_file)

        self.font_width = glyph_matrix.GetWidth() // 16
        self.font_height = glyph_matrix.GetHeight() // 16

        images = [
            glyph_matrix.GetSubBitmap(
            wx.Rect((i % 16) * self.font_width,
                (i // 16) * self.font_height,
                self.font_width,
                self.font_height)) 
            for i in range(256)
        ]

        self.glyph_masks = [
            (wx.Mask(images[i], wx.BLACK), wx.Mask(images[i], wx.WHITE)) 
            for i in range(256)
        ]

    def paint(self, e):

        dc = wx.AutoBufferedPaintDC(self.frame)

        testImage = wx.Image(self.font_width, self.font_height)
        testImage.SetRGB(wx.Rect(0, 0, self.font_width, self.font_height), 255, 0 , 0)
        testBitmap = testImage.ConvertToBitmap()

        bg = wx.Image(self.font_width, self.font_height, clear = True).ConvertToBitmap()

        for i in range(256):
            testBitmap.SetMask(self.glyph_masks[i][0])
            dc.DrawBitmap(bg, (i % 16) * self.font_width, (i // 16) * self.font_height)
            dc.DrawBitmap(testBitmap, (i % 16) * self.font_width, (i // 16) * self.font_height, useMask = True)

    def start(self):

        self.frame.Show(True)
        self.app.MainLoop()

