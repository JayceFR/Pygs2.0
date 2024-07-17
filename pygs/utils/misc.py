import pygame
import moderngl
import numpy as np
from PIL import Image

# Initialize Pygame
pygame.init()

# Initial resolution
current_resolution = (800, 600)

# Initialize the display
pygame.display.set_mode(current_resolution, pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption('Change Resolution Example')

# Initialize ModernGL context
ctx = moderngl.create_context()

# Shader sources
vertex_shader_source = '''
    #version 330
    in vec2 in_vert;
    in vec2 in_text;
    out vec2 v_text;
    void main() {
        gl_Position = vec4(in_vert, 0.0, 1.0);
        v_text = in_text;
    }
'''

fragment_shader_source = '''
    #version 330
    uniform sampler2D Texture;
    in vec2 v_text;
    out vec4 f_color;
    void main() {
        f_color = texture(Texture, v_text);
    }
'''

# Compile shaders and create program
program = ctx.program(
    vertex_shader=vertex_shader_source,
    fragment_shader=fragment_shader_source,
)

# Vertex data
vertices = np.array([
    # Positions  # Texture coords
    -1.0,  1.0,  0.0, 1.0,
    -1.0, -1.0,  0.0, 0.0,
     1.0, -1.0,  1.0, 0.0,
     1.0,  1.0,  1.0, 1.0,
], dtype='f4')

# Create a buffer and load the vertex data into it
vbo = ctx.buffer(vertices)

# Create a vertex array object
vao = ctx.simple_vertex_array(program, vbo, 'in_vert', 'in_text')

# Function to change resolution
def change_resolution(new_resolution):
    global current_resolution, display_screen, ui_display, screen_texture
    current_resolution = new_resolution
    pygame.display.set_mode(current_resolution, pygame.OPENGL | pygame.DOUBLEBUF)
    half_resolution = (new_resolution[0] // 2, new_resolution[1] // 2)
    display_screen = pygame.Surface(half_resolution)
    ui_display = pygame.Surface(new_resolution)
    screen_texture = ctx.texture(half_resolution, 3)

# Menu options for resolutions
resolutions = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1920, 1080)
]

# Font for menu text
font = pygame.font.Font(None, 36)

def draw_menu(selected_index):
    ui_display.fill((0, 0, 0))
    for index, resolution in enumerate(resolutions):
        color = (255, 255, 255) if index == selected_index else (100, 100, 100)
        text = font.render(f'{resolution[0]}x{resolution[1]}', True, color)
        ui_display.blit(text, (50, 50 + index * 40))
    pygame.display.get_surface().blit(ui_display, (0, 0))
    pygame.display.flip()

def main():
    global display_screen, ui_display, screen_texture

    # Initial surfaces
    half_resolution = (current_resolution[0] // 2, current_resolution[1] // 2)
    display_screen = pygame.Surface(half_resolution)
    ui_display = pygame.Surface(current_resolution)
    screen_texture = ctx.texture(half_resolution, 3)

    running = True
    in_menu = True
    selected_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if in_menu:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(resolutions)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(resolutions)
                    elif event.key == pygame.K_RETURN:
                        change_resolution(resolutions[selected_index])
                        in_menu = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        in_menu = True

        if in_menu:
            draw_menu(selected_index)
        else:
            # Render to display_screen (example rendering, replace with your actual rendering logic)
            display_screen.fill((0, 0, 0))  # Example fill, replace with actual rendering
            
            # Convert display_screen to a texture
            display_data = pygame.image.tostring(display_screen, 'RGB')
            screen_texture.write(display_data)
            
            # Clear the screen
            ctx.clear(0.0, 0.0, 0.0, 0.0)
            
            # Use the texture
            screen_texture.use()
            
            # Render the textured quad
            vao.render(moderngl.TRIANGLE_FAN)
            
            # Swap the buffers
            pygame.display.flip()

        pygame.time.wait(100)  # Small delay to limit the loop speed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
