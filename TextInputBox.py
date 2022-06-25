import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, font, caption, text=""):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = width
        self.font = font
        self.text = text
        self.caption = caption
        self.active = False
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        cap_surf = self.font.render(self.caption, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), (t_surf.get_height() * 2) + 20)
                                    , pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, t_surf.get_height() + 10))
        self.image.blit(cap_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def get_text(self):
        return self.text

    def set_active(self, boolean: bool):
        self.active = boolean

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
                self.color = (255, 0, 0)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = (255, 255, 255)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()
