#!/usr/bin/env python3
"""Generate web-optimized derivatives into website/images/site/.

Source files in website/images/ are the originals from Ontario Tech
communications; nothing here modifies them. Re-run after swapping a source:
    python3 -I website/build-images.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'images')
OUT = os.path.join(SRC, 'site')
LEARN = os.path.join(SRC, 'learning_images')
LOGOS = os.path.join(SRC, 'logos')

# out name -> (source, target width, target height or None, quality)
PHOTOS = {
    'hero.jpg':            ('190930_18/190930-18-banner.jpg',       1920, 600, 80),
    'band-physics.jpg':    ('physics_4/physics-4-banner.jpg',       1920, 440, 80),
    'about.jpg':           ('181220_32/181220-32-web.jpg',          1280, 854, 80),
    'teaching.jpg':        ('181220_9/181220-9-web.jpg',            1280, 854, 80),
    'formats.jpg':         ('190930_34/190930-34-web.jpg',          1280, 854, 80),
    'theme-ai.jpg':        ('190930_83/190930-83-web.jpg',           900, 600, 80),
    'theme-engagement.jpg':('171027_2_32/171027_2-32-web.jpg',       900, 600, 80),
    'theme-technology.jpg':('physicslab_5/physicslab-5-web.jpg',     900, 600, 80),
}

LOGO_FILES = {
    'logo-science.png': (
        'logos_ontario_tech_signatures_ontario_tech_science_colour/'
        'ontariotech_science_rgb_300ppi.png', 620),
    'logo-ontariotech-reverse.png': (
        'logos_ontario_tech_university_primary_logo_reverse_colour_dark_background/'
        'ontariotechuniversity_primary_colour_rgb_dk_bkgnd_300ppi.png', 760),
}


def cover(im, w, h):
    """Resize and centre-crop to exactly w x h."""
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    nw, nh = im.size
    left, top = (nw - w) // 2, (nh - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (rel, w, h, q) in PHOTOS.items():
        src = os.path.join(LEARN, rel)
        im = Image.open(src).convert('RGB')
        cover(im, w, h).save(os.path.join(OUT, name), 'JPEG',
                             quality=q, optimize=True, progressive=True)
        print(f'{name:24} {w}x{h}  <- {rel}')
    for name, (rel, w) in LOGO_FILES.items():
        im = Image.open(os.path.join(LOGOS, rel)).convert('RGBA')
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, name), 'PNG', optimize=True)
        print(f'{name:24} {w}x{h}  <- logo')


if __name__ == '__main__':
    main()
