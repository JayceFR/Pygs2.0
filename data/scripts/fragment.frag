#version 330 

uniform sampler2D tex;
uniform sampler2D ui_tex;
uniform float time;

uniform sampler2D noise_tex1;
uniform sampler2D noise_tex2;
uniform float itime;

uniform vec2 cam_scroll;

in vec2 uvs;
out vec4 f_color;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

uniform vec2 scroll = vec2(0.05, -0.05);
uniform vec2 scroll2 = vec2(0.05, 0.05);
uniform vec2 scroll3 = vec2(0.05, -0.15);
uniform vec2 scroll4 = vec2(0.15, 0.05);

float seamlessNoise(vec2 uv, float tileSize, sampler2D noise) {
    vec2 st = uv * tileSize;
    vec2 i_st = floor(st);
    vec2 f_st = fract(st);

    vec4 a = texture(noise, (i_st + vec2(0.5, 0.5)) / tileSize);
    vec4 b = texture(noise, (i_st + vec2(1.5, 0.5)) / tileSize);
    vec4 c = texture(noise, (i_st + vec2(0.5, 1.5)) / tileSize);
    vec4 d = texture(noise, (i_st + vec2(1.5, 1.5)) / tileSize);

    // Smoothly interpolate between the noise values
    vec2 smooth_uv = smoothstep(0.0, 1.0, f_st);
    float value = mix(mix(a.r, b.r, smooth_uv.x), mix(c.r, d.r, smooth_uv.x), smooth_uv.y);

    return value;
}

void foreground(){
    vec4 tex_color = texture(tex, uvs);
    vec2 px_uvs = vec2(floor(uvs.x * 500) / 500, floor(uvs.y * 300) / 300);
    vec2 px_uvs2 = vec2((floor(uvs.x * 500) + cam_scroll.x * 1.3)/500, (floor(uvs.y * 300) + cam_scroll.y * 1)/300);
    vec2 px_uvs3 = vec2((floor(uvs.x * 500) + cam_scroll.x * 1)/500, (floor(uvs.y * 300) + cam_scroll.y * 1)/300);
    f_color = tex_color;
    float depth = seamlessNoise(px_uvs2  + scroll * itime * 2.6 , 16.0, noise_tex1) * seamlessNoise(px_uvs2  + scroll2 * itime * 0.3, 15.0, noise_tex2) ;
    float depth2 = seamlessNoise(px_uvs3  + scroll3 * sin(itime) * 0.6 * cos(itime) * 0.6 , 16.0, noise_tex1) * seamlessNoise(px_uvs3  + scroll4 * cos(itime) * 0.6, 16.0, noise_tex1) ;
    vec3 fog_color = vec3(0.15,0.14,0.35);
    vec3 fog_color2 = vec3(0.1, 0.1, 0.3);
    float fogFactor = exp(-0.3 + depth);
    if (depth < 0.5){
        f_color = vec4(mix(fog_color, f_color.rgb, fogFactor), 1.0);
        f_color = vec4(mix(fog_color2, f_color.rgb, fogFactor), 1.0);
    }
    float darkness = 0.7;
    vec4 dark = vec4(0.0, 0.0, 0.0, 1.0);
    f_color = darkness * dark + (1 - darkness) * f_color;
    vec4 ui_color = texture(ui_tex, px_uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    }
}



void main(){
    foreground();
}