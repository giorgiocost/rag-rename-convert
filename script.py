import os
from PIL import Image

folder = r'C:\Users\ge-gi\OneDrive\Área de Trabalho\workspace\api-node\rag-rename-convert\item'
png_folder = os.path.join(folder, 'png')

# Ensure the png_folder exists
if not os.path.exists(png_folder):
    os.makedirs(png_folder)

with open('default.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # Ignore lines that start with "//" (comments) or are empty
        if not line.strip().startswith('//') and line.strip():
            parts = line.strip().split('#')
            
            if len(parts) >= 2:  # Make sure there are at least two elements in parts
                text = parts.pop(0)
                ids = parts[0]
                parts = [text, ids]

                old_name = parts[1]
                new_name = parts[0]
                print(f'Renamed "{old_name}.bmp" to "{new_name}.bmp"')
                old_path = os.path.join(folder, old_name + '.bmp')
                new_path = os.path.join(folder, new_name + '.bmp')
                
           
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f'Renamed "{old_name}.bmp" to "{new_name}.bmp"')
                    
                    bmp_image = Image.open(new_path)
                    png_image_path = os.path.join(png_folder, f'{new_name}.png')
                    bmp_image.save(png_image_path)
                    print(f'Converted {new_name}.bmp to {png_image_path}')
