import pygame


class ToggleButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, font, text):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = (0, 0, 0)
        self.pos = (x, y)
        self.width = width
        self.font = font
        self.text = text
        self.render_text()
        self.active = False

    def render_text(self):
        t1_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t1_surf.get_width() + 10), (t1_surf.get_height() * 3) + 20),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t1_surf, (5, t1_surf.get_height() + 10))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.active and self.rect.collidepoint(event.pos):
                self.active = False
                self.color = (255, 255, 255)
                self.render_text()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.active and self.rect.collidepoint(event.pos):
                self.active = True
                self.color = (128, 128, 128)
                self.render_text()

    def get_pressed(self):
        return self.active
