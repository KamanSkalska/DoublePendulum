import pygame


class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, font, text_line1="", text_line2=""):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = width
        self.font = font
        self.text_line1 = text_line1
        self.text_line2 = text_line2
        self.render_text()

    def render_text(self):
        t1_surf = self.font.render(self.text_line1, True, self.color, self.backcolor)
        t2_surf = self.font.render(self.text_line2, True, self.color, self.backcolor)
        cap_surf = self.font.render("Instructions:", True, self.color, self.backcolor)

        self.image = pygame.Surface((max(self.width, t1_surf.get_width() + 10), (t1_surf.get_height() * 3) + 20),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(cap_surf, (5, 5))
        self.image.blit(t1_surf, (5, t1_surf.get_height() + 10))
        self.image.blit(t2_surf, (5, t1_surf.get_height() * 2 + 10))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)
