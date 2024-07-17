import pygame
class TypeWriter():
    def __init__(self, font, text_col, x, y, width, font_size, sound) -> None:
        self.font = font
        self.text_col = text_col
        self.x = x
        self.y = y
        self.check_x = x
        self.start_x = x
        self.sound = sound
        self.end_x = x+width
        self.width = width
        self.font_size = font_size
        self.list_of_texts = [] # [['h', 'e', 'f', ' ', ','], 'i rock to the core']
        self.last_update = 0
        self.cooldown = 50
        self.current_letter = -1
        self.current_frame = 0 
        self.waiting_to_update = False
        self.strings = ["", "", ""] # [["oneline"], ["secondline"]]
        self.banana_turn = 0
        self.current_string_pos = 0
        self.space_count = 0
    
    def write(self, list_of_texts):
        self.list_of_texts = []
        for text in list_of_texts:
            letters = []
            for letter in text:
                letters.append(letter)
            self.list_of_texts.append(letters)
        self.current_frame = 0
    
    def draw_text(self, texts, display):
        originial_y = self.y
        for text in texts:
            img = self.font.render(text, True, self.text_col)
            display.blit(img, (self.x, originial_y))
            originial_y += 20
        
    def draw_enter(self, x, y, text, display):
        img = self.font.render(text, True, self.text_col)
        display.blit(img, (x, y))
    
    
    def update(self, time, display, enter_loc = [350,80], chuma_object = None):
        if time - self.last_update > self.cooldown:
            self.current_letter += 1
            if self.current_letter >= len(self.list_of_texts[self.current_frame]):
                self.waiting_to_update = True
            if not self.waiting_to_update:
                if self.sound:
                  self.sound.play()
                self.check_x += self.font_size
                self.strings[self.current_string_pos] += self.list_of_texts[self.current_frame][self.current_letter]
                if self.list_of_texts[self.current_frame][self.current_letter] == " ":
                    self.space_count = self.current_letter
                if self.check_x >= self.end_x:
                    #Add a new line
                    if self.current_string_pos >= 1:
                        cache = self.strings[self.current_string_pos][(self.space_count - len(self.strings[self.current_string_pos-1])):len(self.strings[self.current_string_pos])]
                        self.strings[self.current_string_pos] = self.strings[self.current_string_pos][0:(self.space_count - len(self.strings[self.current_string_pos-1]))]
                    else:
                        cache = self.strings[self.current_string_pos][self.space_count + 1:len(self.strings[self.current_string_pos])]
                        self.strings[self.current_string_pos] = self.strings[self.current_string_pos][0:self.space_count]
                    self.current_string_pos += 1
                    self.strings[self.current_string_pos] = cache
                    self.check_x = self.start_x
                self.last_update = time
        self.draw_text(self.strings, display)

        if self.waiting_to_update:
            if chuma_object:
                chuma_object.set_frame(2)
            self.draw_enter(enter_loc[0], enter_loc[1], "Enter", display)
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                self.waiting_to_update = False
                self.current_frame += 1
                self.current_letter = -1
                self.space_count = 0
                self.banana_turn += 1
                self.current_string_pos = 0
                self.strings = ["", "", ""]
                self.check_x = self.start_x
                if chuma_object:
                    chuma_object.reset()
                if self.current_frame > len(self.list_of_texts) - 1:
                    return True
        return False