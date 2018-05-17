from PIL import Image, ImageDraw
class filters():
    def __init__(self,Path_im):
        self.Path_im = Path_im
        self.image = Image.open(Path_im)  # Открываем изображение.
        self.draw = ImageDraw.Draw(self.image)  # Создаем инструмент для рисования.
        self.width = self.image.size[0]  # Определяем ширину.
        self.height = self.image.size[1]  # Определяем высоту.
        self.pix = self.image.load()  # Выгружаем значения пикселей.

    def ImageEditbw(self):
        for i in range(self.width):
            for j in range(self.height):
                r = self.pix[i, j][0]
                g = self.pix[i, j][1]
                b = self.pix[i, j][2]
                S = (r + g + b) // 3
                self.draw.point((i, j), (S, S, S))
        self.image.save(self.Path_im)

    def Sepia(self):
        for i in range(self.width):
            for j in range(self.height):
                r = self.pix[i, j][0]
                g = self.pix[i, j][1]
                b = self.pix[i, j][2]
                S = (r + g + b) // 3
                r = S + 30 * 2
                g  = S + 30
                b = S
                if (r > 255):
                    r = 255
                if (g > 255):
                    g = 255
                if (b > 255):
                    b = 255
                self.draw.point((i, j), (r, g, b))
        self.image.save(self.Path_im)

    def Negative(self):
        for i in range(self.width):
            for j in range(self.height):
                r = self.pix[i, j][0]
                g = self.pix[i, j][1]
                b = self.pix[i, j][2]
                self.draw.point((i, j), (255 - r, 255 - g, 255 - b))
        self.image.save(self.Path_im)

    def BlackWhite(self):
        factor = 100
        for i in range(self.width):
            for j in range(self.height):
                r = self.pix[i, j][0]
                g = self.pix[i, j][1]
                b = self.pix[i, j][2]
                S = r + g + b
                if (S > (((255 + factor) // 2) * 3)):
                    r, g, b = 255, 255, 255
                else:
                    r, g, b = 0, 0, 0
                self.draw.point((i, j), (r, g, b))
        self.image.save(self.Path_im)





