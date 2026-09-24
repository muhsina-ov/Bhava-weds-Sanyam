import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def draw_diamond(draw, cx, cy, size, fill):
    points = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(points, fill=fill)

def generate_master_icon(size=512):
    # Create RGBA canvas
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.47)
    
    # 1. Subtle Outer Drop Shadow
    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - r_outer, cy - r_outer + 8, cx + r_outer, cy + r_outer + 8], fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.04))
    img = Image.alpha_composite(img, shadow)
    
    # 2. Base Crimson Royal Velvet Disc with Radial Gradient
    disc = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    disc_pixels = disc.load()
    
    c_center = (235, 183, 196, 255) # Soft blush pink center
    c_mid = (212, 130, 150, 255)    # Dusty rose
    c_edge = (90, 77, 83, 255)      # Soft slate grey edge
    
    for y in range(size):
        for x in range(size):
            dist = math.hypot(x - cx, y - cy)
            if dist <= r_outer:
                t = dist / r_outer
                if t < 0.5:
                    sub_t = t / 0.5
                    r = int(c_center[0] * (1 - sub_t) + c_mid[0] * sub_t)
                    g = int(c_center[1] * (1 - sub_t) + c_mid[1] * sub_t)
                    b = int(c_center[2] * (1 - sub_t) + c_mid[2] * sub_t)
                else:
                    sub_t = (t - 0.5) / 0.5
                    r = int(c_mid[0] * (1 - sub_t) + c_edge[0] * sub_t)
                    g = int(c_mid[1] * (1 - sub_t) + c_edge[1] * sub_t)
                    b = int(c_mid[2] * (1 - sub_t) + c_edge[2] * sub_t)
                disc_pixels[x, y] = (r, g, b, 255)
                
    img = Image.alpha_composite(img, disc)
    
    # 3. Gold Concentric Rings & Beaded Border
    gold_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gold_layer)
    
    # Outer Ring
    r_ring1 = int(size * 0.46)
    g_draw.ellipse([cx - r_ring1, cy - r_ring1, cx + r_ring1, cy + r_ring1], outline=(212, 175, 55, 230), width=int(size * 0.016))
    
    # Inner Fine Ring
    r_ring2 = int(size * 0.42)
    g_draw.ellipse([cx - r_ring2, cy - r_ring2, cx + r_ring2, cy + r_ring2], outline=(243, 229, 171, 160), width=int(size * 0.008))
    
    # Circular Beaded Gold Dots
    num_beads = 32
    r_bead_orbit = int(size * 0.44)
    bead_radius = max(2, int(size * 0.012))
    for i in range(num_beads):
        angle = (2 * math.pi / num_beads) * i
        bx = cx + r_bead_orbit * math.cos(angle)
        by = cy + r_bead_orbit * math.sin(angle)
        g_draw.ellipse([bx - bead_radius, by - bead_radius, bx + bead_radius, by + bead_radius], fill=(243, 229, 171, 230))
        
    # 4 Cardinal Diamonds
    diamond_orbit = int(size * 0.44)
    for angle_deg in [0, 90, 180, 270]:
        rad = math.radians(angle_deg)
        dx = cx + diamond_orbit * math.cos(rad)
        dy = cy + diamond_orbit * math.sin(rad)
        draw_diamond(g_draw, dx, dy, int(size * 0.024), (255, 245, 200, 255))
        
    gold_glow = gold_layer.filter(ImageFilter.GaussianBlur(int(size * 0.015)))
    img = Image.alpha_composite(img, gold_glow)
    img = Image.alpha_composite(img, gold_layer)
    
    # 4. Monogram "B & S" in Center
    font_cinzel = ImageFont.truetype('fonts/temp/Cinzel-Bold.ttf', int(size * 0.28))
    font_amp = ImageFont.truetype('fonts/temp/AlexBrush-Regular.ttf', int(size * 0.32))
    font_sub = ImageFont.truetype('fonts/temp/Montserrat-Bold.ttf', int(size * 0.05))
    
    text_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    
    # Measure 'B', '&', 'S'
    bb_b = font_cinzel.getbbox('B')
    w_b = bb_b[2] - bb_b[0]
    bb_amp = font_amp.getbbox('&')
    w_amp = bb_amp[2] - bb_amp[0]
    bb_s = font_cinzel.getbbox('S')
    w_s = bb_s[2] - bb_s[0]
    
    gap = int(size * 0.02)
    total_w = w_b + w_amp + w_s + (gap * 2)
    start_x = cx - (total_w // 2)
    y_letters = int(cy - (size * 0.17))
    y_amp = int(cy - (size * 0.20))
    
    # Shadows
    t_draw.text((start_x + 4, y_letters + 4), 'B', font=font_cinzel, fill=(0, 0, 0, 220))
    t_draw.text((start_x + w_b + gap + 4, y_amp + 4), '&', font=font_amp, fill=(0, 0, 0, 220))
    t_draw.text((start_x + w_b + gap + w_amp + gap + 4, y_letters + 4), 'S', font=font_cinzel, fill=(0, 0, 0, 220))
    
    # Gold Letter Fills
    t_draw.text((start_x, y_letters), 'B', font=font_cinzel, fill=(255, 248, 220, 255))
    t_draw.text((start_x + w_b + gap, y_amp), '&', font=font_amp, fill=(243, 229, 171, 255))
    t_draw.text((start_x + w_b + gap + w_amp + gap, y_letters), 'S', font=font_cinzel, fill=(255, 248, 220, 255))
    
    # Small Sub-text or Lotus Accent underneath
    sub_txt = "WEDDING"
    bb_sub = font_sub.getbbox(sub_txt)
    w_sub = bb_sub[2] - bb_sub[0]
    y_sub = int(cy + (size * 0.16))
    
    t_draw.text((cx - (w_sub // 2) + 2, y_sub + 2), sub_txt, font=font_sub, fill=(0, 0, 0, 200))
    t_draw.text((cx - (w_sub // 2), y_sub), sub_txt, font=font_sub, fill=(212, 175, 55, 235))
    
    # Small top and bottom gold stars / diamonds
    draw_diamond(t_draw, cx, int(cy - (size * 0.25)), int(size * 0.02), (243, 229, 171, 240))
    draw_diamond(t_draw, cx, int(cy + (size * 0.26)), int(size * 0.016), (243, 229, 171, 240))
    
    img = Image.alpha_composite(img, text_layer)
    return img

def build_favicons():
    master = generate_master_icon(512)
    os.makedirs('images', exist_ok=True)
    
    # 1. 512x512
    master.save('images/android-chrome-512x512.png', 'PNG', optimize=True)
    
    # 2. 192x192
    icon_192 = master.resize((192, 192), Image.Resampling.LANCZOS)
    icon_192.save('images/android-chrome-192x192.png', 'PNG', optimize=True)
    
    # 3. 180x180 (Apple Touch Icon)
    icon_180 = master.resize((180, 180), Image.Resampling.LANCZOS)
    icon_180.save('images/apple-touch-icon.png', 'PNG', optimize=True)
    icon_180.save('images/apple-touch-icon_1.png', 'PNG', optimize=True) # backward compatibility
    
    # 4. 48x48
    icon_48 = master.resize((48, 48), Image.Resampling.LANCZOS)
    icon_48.save('images/favicon-48x48.png', 'PNG', optimize=True)
    icon_48.save('images/favicon-light_1.png', 'PNG', optimize=True) # backward compatibility
    icon_48.save('images/favicon-dark_1.png', 'PNG', optimize=True)
    
    # 5. 32x32
    icon_32 = master.resize((32, 32), Image.Resampling.LANCZOS)
    icon_32.save('images/favicon-32x32.png', 'PNG', optimize=True)
    
    # 6. 16x16
    icon_16 = master.resize((16, 16), Image.Resampling.LANCZOS)
    icon_16.save('images/favicon-16x16.png', 'PNG', optimize=True)
    
    # 7. Multi-resolution favicon.ico in root and images/
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    master.save('favicon.ico', format='ICO', sizes=ico_sizes)
    master.save('images/favicon.ico', format='ICO', sizes=ico_sizes)
    
    print('All favicon PNGs and ICO built successfully!')

if __name__ == '__main__':
    build_favicons()
