import os
import math
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def download_fonts():
    os.makedirs('fonts/temp', exist_ok=True)
    font_urls = {
        'Cinzel-Bold.ttf': 'https://fonts.gstatic.com/s/cinzel/v26/8vIU7ww63mVu7gtR-kwKxNvkNOjw-jHgTYo.ttf',
        'CormorantGaramond-BoldItalic.ttf': 'https://fonts.gstatic.com/s/cormorantgaramond/v21/co3umX5slCNuHLi8bLeY9MK7whWMhyjypVO7abI26QOD_hg9GnM.ttf',
        'Montserrat-SemiBold.ttf': 'https://fonts.gstatic.com/s/montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCu170w-.ttf',
        'Montserrat-Bold.ttf': 'https://fonts.gstatic.com/s/montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCuM70w-.ttf',
        'AlexBrush-Regular.ttf': 'https://github.com/google/fonts/raw/main/ofl/alexbrush/AlexBrush-Regular.ttf'
    }
    for name, url in font_urls.items():
        dest = os.path.join('fonts/temp', name)
        if not os.path.exists(dest):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as resp, open(dest, 'wb') as out:
                    out.write(resp.read())
            except Exception as e:
                print(f'Font download info: {e}')

def draw_diamond(draw, cx, cy, size, fill):
    points = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(points, fill=fill)

def create_og_banner():
    download_fonts()
    
    W, H = 1200, 630
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    
    # 1. Background Gradient (Velvet royal crimson maroon with smooth radial lighting)
    cx, cy = 600, 285
    max_radius = math.hypot(cx, cy)
    
    bg = Image.new('RGB', (W, H))
    bg_pixels = bg.load()
    
    c_center = (138, 25, 42)   # Glowing ruby crimson center
    c_mid = (66, 8, 17)        # Deep royal wine
    c_edge = (26, 3, 5)        # Midnight velvet edge
    
    for y in range(H):
        for x in range(W):
            dist = math.hypot(x - cx, (y - cy) * 1.30)
            t = min(dist / max_radius, 1.0)
            if t < 0.45:
                sub_t = t / 0.45
                r = int(c_center[0] * (1 - sub_t) + c_mid[0] * sub_t)
                g = int(c_center[1] * (1 - sub_t) + c_mid[1] * sub_t)
                b = int(c_center[2] * (1 - sub_t) + c_mid[2] * sub_t)
            else:
                sub_t = (t - 0.45) / 0.55
                r = int(c_mid[0] * (1 - sub_t) + c_edge[0] * sub_t)
                g = int(c_mid[1] * (1 - sub_t) + c_edge[1] * sub_t)
                b = int(c_mid[2] * (1 - sub_t) + c_edge[2] * sub_t)
            bg_pixels[x, y] = (r, g, b)
            
    img.paste(bg, (0, 0))
    
    # 2. Ambient Golden Glow Aura
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([cx - 480, cy - 260, cx + 480, cy + 260], fill=(212, 175, 55, 40))
    glow_draw.ellipse([cx - 280, cy - 160, cx + 280, cy + 160], fill=(243, 229, 171, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    img = Image.alpha_composite(img, glow)
    
    # 3. Corner Floral Bouquets (Top Left & Top Right)
    if os.path.exists('images/cdn/noroot_3.png') and os.path.exists('images/cdn/noroot_2.png'):
        try:
            fl_l = Image.open('images/cdn/noroot_3.png').convert('RGBA')
            fl_r = Image.open('images/cdn/noroot_2.png').convert('RGBA')
            
            corner_w = 185
            corner_h = int(fl_l.height * (corner_w / fl_l.width))
            fl_l = fl_l.resize((corner_w, corner_h), Image.Resampling.LANCZOS)
            
            corner_rw = 185
            corner_rh = int(fl_r.height * (corner_rw / fl_r.width))
            fl_r = fl_r.resize((corner_rw, corner_rh), Image.Resampling.LANCZOS)
            
            alpha_l = fl_l.split()[3].point(lambda p: int(p * 0.92))
            fl_l.putalpha(alpha_l)
            alpha_r = fl_r.split()[3].point(lambda p: int(p * 0.92))
            fl_r.putalpha(alpha_r)
            
            # Drop shadow
            sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            sh_l = Image.new('RGBA', fl_l.size, (0, 0, 0, 170))
            sh_l.putalpha(alpha_l)
            sh_layer.paste(sh_l, (24, 24), sh_l)
            sh_r = Image.new('RGBA', fl_r.size, (0, 0, 0, 170))
            sh_r.putalpha(alpha_r)
            sh_layer.paste(sh_r, (W - 24 - corner_rw, 24), sh_r)
            sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(9))
            img = Image.alpha_composite(img, sh_layer)
            
            img.paste(fl_l, (22, 22), fl_l)
            img.paste(fl_r, (W - 22 - corner_rw, 22), fl_r)
        except Exception as e:
            print(f'Corner floral error: {e}')
            
    # Bottom Left subtle floral corner accent
    if os.path.exists('images/cdn/left-element_1.png'):
        try:
            btm_fl = Image.open('images/cdn/left-element_1.png').convert('RGBA')
            b_w = 120
            b_h = int(btm_fl.height * (b_w / btm_fl.width))
            btm_fl = btm_fl.resize((b_w, b_h), Image.Resampling.LANCZOS)
            alpha_b = btm_fl.split()[3].point(lambda p: int(p * 0.70))
            btm_fl.putalpha(alpha_b)
            img.paste(btm_fl, (34, H - b_h - 34), btm_fl)
        except Exception as e:
            print(f'Bottom floral error: {e}')
            
    # 4. Gold Borders Frame
    border_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border_layer)
    
    # Outer Frame
    b_draw.rounded_rectangle([22, 22, W - 22, H - 22], radius=16, outline=(212, 175, 55, 215), width=2)
    # Inner Fine Frame
    b_draw.rounded_rectangle([30, 30, W - 30, H - 30], radius=12, outline=(243, 229, 171, 95), width=1)
    
    # Gold Corner Diamonds
    draw_diamond(b_draw, 30, 30, 4, (243, 229, 171, 240))
    draw_diamond(b_draw, W - 30, 30, 4, (243, 229, 171, 240))
    draw_diamond(b_draw, 30, H - 30, 4, (243, 229, 171, 240))
    draw_diamond(b_draw, W - 30, H - 30, 4, (243, 229, 171, 240))
    
    border_shadow = border_layer.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, border_shadow)
    img = Image.alpha_composite(img, border_layer)
    
    # 5. Wax Seal in bottom right
    if os.path.exists('images/cdn/wax_seal_1.png'):
        try:
            seal = Image.open('images/cdn/wax_seal_1.png').convert('RGBA')
            seal_w = 100
            seal_h = int(seal.height * (seal_w / seal.width))
            seal = seal.resize((seal_w, seal_h), Image.Resampling.LANCZOS)
            seal = seal.rotate(-8, resample=Image.Resampling.BICUBIC, expand=True)
            
            seal_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            shadow_mask = seal.split()[3]
            black_seal = Image.new('RGBA', seal.size, (0, 0, 0, 190))
            black_seal.putalpha(shadow_mask)
            seal_shadow.paste(black_seal, (W - seal.width - 48 + 4, H - seal.height - 38 + 6), black_seal)
            seal_shadow = seal_shadow.filter(ImageFilter.GaussianBlur(12))
            img = Image.alpha_composite(img, seal_shadow)
            
            img.paste(seal, (W - seal.width - 48, H - seal.height - 38), seal)
        except Exception as e:
            print(f'Wax seal error: {e}')
            
    # 6. Load Fonts
    font_cinzel_large = ImageFont.truetype('fonts/temp/Cinzel-Bold.ttf', 72)
    font_alex_large = ImageFont.truetype('fonts/temp/AlexBrush-Regular.ttf', 84)
    font_ganesh = ImageFont.truetype('fonts/temp/Cinzel-Bold.ttf', 16)
    font_sub = ImageFont.truetype('fonts/temp/Montserrat-SemiBold.ttf', 12)
    font_tagline = ImageFont.truetype('fonts/temp/CormorantGaramond-BoldItalic.ttf', 24)
    font_badge = ImageFont.truetype('fonts/temp/Montserrat-Bold.ttf', 14)
    font_url = ImageFont.truetype('fonts/temp/Montserrat-SemiBold.ttf', 12)
    
    text_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    
    # 7. Ganesh Top Invocation
    if os.path.exists('images/cdn/noroot_6.png'):
        try:
            flourish = Image.open('images/cdn/noroot_6.png').convert('RGBA')
            f_w = 160
            f_h = int(flourish.height * (f_w / flourish.width))
            flourish = flourish.resize((f_w, f_h), Image.Resampling.LANCZOS)
            img.paste(flourish, (int(cx - f_w / 2), 48), flourish)
        except Exception as e:
            print(f'Flourish top error: {e}')
            
    ganesh_txt = "SHREE  GANESHAYA  NAMAH"
    ganesh_bbox = font_ganesh.getbbox(ganesh_txt)
    g_w = ganesh_bbox[2] - ganesh_bbox[0]
    t_draw.text((cx - g_w / 2 + 2, 82 + 2), ganesh_txt, font=font_ganesh, fill=(0, 0, 0, 220))
    t_draw.text((cx - g_w / 2, 82), ganesh_txt, font=font_ganesh, fill=(243, 229, 171, 255))
    
    sub_txt = "THE ROYAL WEDDING CELEBRATION OF"
    sub_bbox = font_sub.getbbox(sub_txt)
    s_w = sub_bbox[2] - sub_bbox[0]
    t_draw.text((cx - s_w / 2 + 1, 112 + 1), sub_txt, font=font_sub, fill=(0, 0, 0, 200))
    t_draw.text((cx - s_w / 2, 112), sub_txt, font=font_sub, fill=(225, 195, 135, 230))
    
    # 8. Couple Names: "BHAVYA & SANYAM"
    name1 = "BHAVYA"
    name2 = "SANYAM"
    amp = "&"
    
    b1 = font_cinzel_large.getbbox(name1)
    w1 = b1[2] - b1[0]
    b2 = font_cinzel_large.getbbox(name2)
    w2 = b2[2] - b2[0]
    ba = font_alex_large.getbbox(amp)
    wa = ba[2] - ba[0]
    
    spacing = 26
    total_name_w = w1 + wa + w2 + (spacing * 2)
    start_x = cx - (total_name_w / 2)
    
    y_names = 156
    y_amp = 146
    
    # Drop shadow
    t_draw.text((start_x + 3, y_names + 3), name1, font=font_cinzel_large, fill=(0, 0, 0, 240))
    t_draw.text((start_x + w1 + spacing + 3, y_amp + 3), amp, font=font_alex_large, fill=(0, 0, 0, 240))
    t_draw.text((start_x + w1 + wa + (spacing * 2) + 3, y_names + 3), name2, font=font_cinzel_large, fill=(0, 0, 0, 240))
    
    # Shimmer Golden Fill
    t_draw.text((start_x, y_names), name1, font=font_cinzel_large, fill=(255, 248, 222, 255))
    t_draw.text((start_x + w1 + spacing, y_amp), amp, font=font_alex_large, fill=(243, 229, 171, 255))
    t_draw.text((start_x + w1 + wa + (spacing * 2), y_names), name2, font=font_cinzel_large, fill=(255, 248, 222, 255))
    
    # 9. Center Filigree Divider
    if os.path.exists('images/cdn/noroot_6.png'):
        try:
            flourish2 = Image.open('images/cdn/noroot_6.png').convert('RGBA')
            f2_w = 260
            f2_h = int(flourish2.height * (f2_w / flourish2.width))
            flourish2 = flourish2.resize((f2_w, f2_h), Image.Resampling.LANCZOS)
            img.paste(flourish2, (int(cx - f2_w / 2), 268), flourish2)
        except Exception as e:
            print(f'Flourish center error: {e}')
            
    # 10. Sacred Tagline
    tag_txt = "Two Souls  •  Seven Sacred Vows  •  One Eternal Journey"
    tag_bbox = font_tagline.getbbox(tag_txt)
    tag_w = tag_bbox[2] - tag_bbox[0]
    t_draw.text((cx - tag_w / 2 + 2, 318 + 2), tag_txt, font=font_tagline, fill=(0, 0, 0, 220))
    t_draw.text((cx - tag_w / 2, 318), tag_txt, font=font_tagline, fill=(255, 244, 212, 255))
    
    # 11. Details Badges
    b1_txt = "THURSDAY, 26 NOV 2026"
    b2_txt = "RIVAYA BY ZION"
    
    tb1_bbox = font_badge.getbbox(b1_txt)
    tb1_w = tb1_bbox[2] - tb1_bbox[0]
    tb2_bbox = font_badge.getbbox(b2_txt)
    tb2_w = tb2_bbox[2] - tb2_bbox[0]
    
    pad_h = 24
    box1_w = tb1_w + (pad_h * 2) + 16
    box2_w = tb2_w + (pad_h * 2) + 16
    box_h = 44
    
    b_gap = 28
    total_badge_w = box1_w + box2_w + b_gap
    bx_start = cx - (total_badge_w / 2)
    by = 405
    
    badge_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(badge_layer)
    
    # Badge 1 Box (Date)
    bg_draw.rounded_rectangle([bx_start, by, bx_start + box1_w, by + box_h], radius=22, fill=(84, 15, 28, 225), outline=(212, 175, 55, 190), width=2)
    draw_diamond(bg_draw, bx_start + 18, by + (box_h / 2), 4, (243, 229, 171, 240))
    bg_draw.text((bx_start + 30, by + 12), b1_txt, font=font_badge, fill=(255, 255, 255, 255))
    
    # Center divider diamond
    center_div_x = bx_start + box1_w + (b_gap / 2)
    draw_diamond(bg_draw, center_div_x, by + (box_h / 2), 5, (212, 175, 55, 220))
    
    # Badge 2 Box (Venue)
    b2_x = bx_start + box1_w + b_gap
    bg_draw.rounded_rectangle([b2_x, by, b2_x + box2_w, by + box_h], radius=22, fill=(84, 15, 28, 225), outline=(212, 175, 55, 190), width=2)
    draw_diamond(bg_draw, b2_x + 18, by + (box_h / 2), 4, (243, 229, 171, 240))
    bg_draw.text((b2_x + 30, by + 12), b2_txt, font=font_badge, fill=(255, 255, 255, 255))
    
    # 12. Bottom Sub-text Note
    url_txt = "JOIN OUR ROYAL WEDDING CELEBRATION  •  NOVEMBER 2026"
    u_bbox = font_url.getbbox(url_txt)
    u_w = u_bbox[2] - u_bbox[0]
    t_draw.text((cx - u_w / 2 + 1, 528 + 1), url_txt, font=font_url, fill=(0, 0, 0, 180))
    t_draw.text((cx - u_w / 2, 528), url_txt, font=font_url, fill=(212, 175, 55, 220))
    
    # Merge layers
    img = Image.alpha_composite(img, badge_layer)
    img = Image.alpha_composite(img, text_layer)
    
    # 13. Golden Sparkles
    sparkles_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sp_draw = ImageDraw.Draw(sparkles_layer)
    sparkle_coords = [
        (160, 140, 4), (1040, 140, 5), (220, 290, 3), (980, 290, 4),
        (330, 100, 3), (870, 95, 3), (430, 250, 3), (770, 250, 3),
        (280, 440, 4), (920, 440, 4), (600, 490, 3), (140, 470, 3), (1060, 470, 4)
    ]
    for sx, sy, sr in sparkle_coords:
        sp_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 243, 209, 210))
        sp_draw.line([(sx - sr * 2, sy), (sx + sr * 2, sy)], fill=(255, 243, 209, 140), width=1)
        sp_draw.line([(sx, sy - sr * 2), (sx, sy + sr * 2)], fill=(255, 243, 209, 140), width=1)
        
    sparkles_layer = sparkles_layer.filter(ImageFilter.GaussianBlur(0.8))
    img = Image.alpha_composite(img, sparkles_layer)
    
    # Save outputs
    png_path = 'images/og-image.png'
    img.save(png_path, 'PNG', optimize=True)
    print(f'Saved {png_path}: {os.path.getsize(png_path)} bytes')
    
    jpg_path = 'images/og-image.jpg'
    rgb_final = img.convert('RGB')
    rgb_final.save(jpg_path, 'JPEG', quality=92, optimize=True)
    print(f'Saved {jpg_path}: {os.path.getsize(jpg_path)} bytes')
    
    rgb_final.save('images/og-graph.jpg', 'JPEG', quality=92, optimize=True)
    print(f'Saved images/og-graph.jpg: {os.path.getsize("images/og-graph.jpg")} bytes')

if __name__ == '__main__':
    create_og_banner()
