import os
from PIL import Image
import time
from termcolor import colored  # Import colored from the termcolor library

# Check and install required libraries
try:
    import PIL
except ImportError:
    print("Installing Pillow...")
    os.system('pip install Pillow')

try:
    import termcolor
except ImportError:
    print("Installing termcolor...")
    os.system('pip install termcolor')

current_directory = os.getcwd()
subfolders = ['item', 'collection']
start_time = time.time()  # Record the start ti

# Iterate through each subfolder
for subfolder in subfolders:
    folder = os.path.join(current_directory, subfolder)
    png_folder = os.path.join(folder, '')

    # Ensure the png_folder exists
    if not os.path.exists(png_folder):
        os.makedirs(png_folder)

    with open('default.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Ignore lines that start with "//" (comments) or are empty
            if not line.strip().startswith('//') and line.strip():
                parts = line.strip().split('#')

                if len(parts) >= 2:
                    text = parts.pop(0)
                    ids = parts[0]
                    parts = [text, ids]

                    old_name = parts[1]
                    new_name = parts[0]
                    old_path = os.path.join(folder, old_name + '.bmp')
                    new_path = os.path.join(folder, new_name + '.bmp')
                    print(colored(f'Renamed "{old_name}.bmp" to "{new_name}.bmp"', 'light_green'))
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        

                        bmp_image = Image.open(new_path)
                        png_image_path = os.path.join(png_folder, f'{new_name}.png')
                        bmp_image.save(png_image_path)
                        print(colored(f'Converted {new_name}.bmp to {png_image_path}', 'light_yellow'))

    # Remove all converted .png files from the subfolder
    for filename in os.listdir(folder):
        if filename.lower().endswith('.bmp'):
            file_path = os.path.join(folder, filename)
            try:
                os.remove(file_path)
                print(colored(f'Removed {filename} from {subfolder}', 'light_red'))
            except PermissionError:
                print(f'PermissionError: Unable to remove {filename} from {subfolder}. File is in use.')

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time
print(colored(f'Script completed successfully in {elapsed_time:.2f} seconds.', 'light_cyan'))  # Print completion time in cyan

