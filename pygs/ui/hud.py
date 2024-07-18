import pygame
class Hud():
    def __init__(self, obj) -> None:
        pygame.init()
        self.joysticks = {}
        self.obj = obj
        self.return_dict = {"l_click": False, "ongrid": True, "r_click": False, "run" : True, "left" : False, "right" : False, "up" : False, "down": False, "jump": False, "x_axis" : 0.0}

    def events(self, key_controls):
        # self.return_dict = {"run" : True, "left" : False, "right" : False, "jump": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.return_dict["run"] = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    joystick = self.joysticks[event.instance_id]
                    self.return_dict["jump"] = True
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.player.jump()
                    # if joystick.rumble(0, 0.7, 500):
                    #     print(f"Rumble effect played on joystick {event.instance_id}")
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.return_dict["jump"] = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.return_dict["x_axis"] = event.value
            if event.type == pygame.JOYDEVICEADDED:
                print(event)
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(str(joy.get_instance_id()) + " Connected ")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.return_dict["l_click"] = True
                    if self.obj.__class__.__name__ == "Game":
                        #check for changes in display res
                        if self.obj.settings.curr_hover_pos != -1:
                            self.obj.settings.update_res(self.obj.settings.resolutions[self.obj.settings.curr_hover_pos][1])
                    if self.obj.__class__.__name__ == "Editor":
                        if not pygame.rect.Rect(0,0,100,600).collidepoint(self.obj.mouse_pos) and not self.obj.ongrid:
                            self.obj.toggle_offgrid()
                if event.button == 3:   
                    self.return_dict["r_click"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.return_dict["l_click"] = False
                if event.button == 3:
                    self.return_dict["r_click"] = False

            #Keyboard controls
            
            if event.type == pygame.KEYDOWN:
                if event.key in key_controls["right"]:
                    self.return_dict["right"] = True
                if event.key in key_controls["left"]:
                    self.return_dict["left"] = True
                if event.key in key_controls["jump"]:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.player.jump()
                        print(pygame.display.get_window_size())
                    self.return_dict["jump"] = True
                if event.key in key_controls["dash"]:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.player.dash()
                if event.key in key_controls["up"]:
                    self.return_dict["up"] = True
                if event.key in key_controls["down"]:
                    self.return_dict["down"] = True
                if event.key == pygame.K_LSHIFT:
                    self.return_dict['ongrid'] = not self.return_dict['ongrid']
                if event.key in key_controls["settings"]:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.settings_window = not self.obj.settings_window
                if event.key == pygame.K_o:
                    if self.obj.__class__.__name__ == "Editor":
                        self.obj.tilemap.save('map.json')
            if event.type == pygame.KEYUP:
                if event.key in key_controls["right"]:
                    self.return_dict["right"] = False
                if event.key in key_controls["left"]:
                    self.return_dict["left"] = False
                if event.key == key_controls["jump"]:
                    self.return_dict["jump"] = False
                if event.key in key_controls["up"]:
                    self.return_dict["up"] = False
                if event.key in key_controls["down"]:
                    self.return_dict["down"] = False
    
    def get_controls(self):
        return self.return_dict