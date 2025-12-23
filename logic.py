import numpy as np
from PIL import Image, ImageOps
import os
import logging

logging.basicConfig(level=logging.INFO)

def process_image_to_bitmap(image_path, max_size=500, mode='text'):
    """
    Converts input to a clean 1-bit (Black/White) grid.
    """
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        # Resize maintaining aspect ratio
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        if mode == 'text':
            # Text Mode: Thresholding (Best for documents)
            img = img.convert('L')
            # Force pixels to 0 (Black) or 255 (White)
            img = img.point(lambda x: 255 if x > 128 else 0, '1')
        else: 
            # Photo Mode: Dithering (Best for pictures)
            img = img.convert('1') 

        return np.array(img, dtype=np.uint8)

def generate_shares(image_path, output_folder, mode='text'):
    try:
        secret_grid = process_image_to_bitmap(image_path, mode=mode)
        height, width = secret_grid.shape

        # 1. Share A: Random Noise (0 or 1)
        share_a = np.random.randint(0, 2, size=(height, width), dtype=np.uint8)
        
        # 2. Share B Calculation
        # Standard Visual Crypto Rule:
        # Secret=Black (0) -> Shares are Opposite (0,1 or 1,0)
        # Secret=White (1) -> Shares are Same (0,0 or 1,1)
        share_b = share_a.copy()
        mask_black_text = (secret_grid == 0) 
        share_b[mask_black_text] = 1 - share_a[mask_black_text]

        # 3. Save as Robust PNGs
        os.makedirs(output_folder, exist_ok=True)
        
        # We save as '1' mode (1-bit pixels) to prevent any browser compression
        Image.fromarray(share_a * 255).convert('1').save(os.path.join(output_folder, "share1.png"), "PNG")
        Image.fromarray(share_b * 255).convert('1').save(os.path.join(output_folder, "share2.png"), "PNG")
        return True
    except Exception as e:
        logging.error(f"Encrypt Error: {e}")
        return False

def decrypt_shares_digitally(share1_path, share2_path, output_path):
    try:
        # 1. Load Shares
        # Force convert to '1' (Binary) immediately to remove any JPEG/Resize artifacts
        s1_img = Image.open(share1_path).convert('1')
        s2_img = Image.open(share2_path).convert('1')
        
        # 2. SAFE ALIGNMENT (Crucial Fix)
        # Instead of resizing (which creates fuzzy pixels), we CROP to the common size.
        # This handles cases where the browser added 1px border.
        min_w = min(s1_img.width, s2_img.width)
        min_h = min(s1_img.height, s2_img.height)
        
        s1_img = s1_img.crop((0, 0, min_w, min_h))
        s2_img = s2_img.crop((0, 0, min_w, min_h))

        # Convert to arrays (0=Black, 1=White)
        s1 = np.array(s1_img, dtype=np.uint8)
        s2 = np.array(s2_img, dtype=np.uint8)

        # 3. ROBUST DECRYPTION (Visual Overlay Simulation)
        # We simulate "stacking" the transparencies.
        # If either pixel is Black (0), the result is Black. 
        # Result is White ONLY if both are White.
        # Math: Result = s1 & s2  (Bitwise AND)
        
        stacked_grid = np.bitwise_and(s1, s2)
        
        # 4. Convert to Image
        # 0 -> Black, 1 -> White (255)
        result = Image.fromarray(stacked_grid * 255)

        # 5. CONTRAST CLEANUP
        # The result of stacking is usually "Dark Gray" vs "Black".
        # We perform a "Stretch" to make the gray parts White again.
        # This removes the "messy noise" from the background.
        result = result.convert('L') # Convert to Grayscale for filtering
        
        # Any pixel that is NOT pure black, make it White.
        # This clears up the "static" in the white areas.
        result = result.point(lambda x: 255 if x > 0 else 0, '1')

        result.save(output_path, "PNG")
        return True
    except Exception as e:
        logging.error(f"Decrypt Error: {e}")
        return False