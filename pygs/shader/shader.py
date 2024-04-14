import moderngl
from array import array
class Shader():
    def __init__(self, shader, vertex_loc, fragment_loc) -> None:
        self.shader = shader
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            #Position (x,y), uv coords (x,y)
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        file = open(vertex_loc, "r")
        vertex_shader = file.read()
        file.close()

        file = open(fragment_loc, "r")
        frag_shader = file.read()
        file.close()

        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def draw(self, *args):
        if self.shader:
            key_list = args[0].keys()
            for key in key_list:
                args[0][key] = self.surf_to_texture(args[0].get(key))
            for x, key in enumerate(key_list):
                args[0].get(key).use(location=x)
                self.program[key] = x
            key_list = args[1].keys()
            for key in key_list:
                self.program[key] = args[1].get(key)
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
            key_list = args[0].keys()
            for key in key_list:
                args[0].get(key).release()
    
    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

