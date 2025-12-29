from eye_tracking import track_eyes
import os
import cv2
import zipfile
import shutil

def display_menu():
    print("""
    [0] Crop Input Pictures to Desired Aspect Ratio
    [1] Zip Output Pictures
    [2] Delete Input Pictures
    [3] Delete Output Pictures
    [4] Exit
          """)
    return input("Select an option: ")

def handle_selection(selection):
    if selection == '0':
        aspect_ratio = input("Enter desired aspect ratio (width:height), e.g., 4:5: ")
        aspect_width, aspect_height = map(int, aspect_ratio.split(':'))
        input_root = "input_pictures"
        output_root = "output_pictures"

        n = 1
        for root, dirs, files in os.walk(input_root):
            for file in files:
                if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue

                print(f"Processing image {n}: {file}")

                input_path = os.path.join(root, file)
                image = cv2.imread(input_path)

                if image is None:
                    print(f"Failed to load image: {input_path}")
                    continue

                fixed_image = track_eyes(image, aspect_width, aspect_height)

                # Preserve folder structure in output
                rel_path = os.path.relpath(root, input_root)
                output_dir = os.path.join(output_root, rel_path)
                os.makedirs(output_dir, exist_ok=True)

                output_path = os.path.join(
                    output_dir,
                    f"{aspect_width}x{aspect_height}_{file}"
                )

                cv2.imwrite(output_path, fixed_image)

                n += 1

    elif selection == '1': 
        output_root = "output_pictures"

        # zip top-level folder(s) separately
        for item in os.listdir(output_root):
            item_path = os.path.join(output_root, item)

            if os.path.isdir(item_path):
                zip_name = f"{item}.zip"
                print(f"Creating {zip_name}")

                with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(item_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, item_path)
                            print(f"  Adding {arcname}")
                            zipf.write(full_path, arcname)

        # zip images directly inside output_pictures/
        loose_zip_name = "output_pictures.zip"
        print(f"Creating {loose_zip_name}")

        with zipfile.ZipFile(loose_zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in os.listdir(output_root):
                if item == "text.txt":
                    continue
                item_path = os.path.join(output_root, item)

                if os.path.isfile(item_path) and item.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"  Adding {item}")
                    zipf.write(item_path, arcname=item)

    elif selection == '2':
        warning_confirmed = warning(selection)
        if not warning_confirmed:
            return True

        input_dir = "input_pictures"

        for item in os.listdir(input_dir):
            if item == "text.txt":
                continue
            item_path = os.path.join(input_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    print(f"Deleted file: {item}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Deleted folder: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")

    elif selection == '3':
        warning_confirmed = warning(selection)
        if not warning_confirmed:
            return True
        
        output_dir = "output_pictures"
        
        for item in os.listdir(output_dir):
            if item == "text.txt":
                continue
            item_path = os.path.join(output_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    print(f"Deleted file: {item}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Deleted folder: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")

    elif selection == '4':
        print("Exiting the program.")
    else:
        print("Invalid selection. Please try again.")
    return True

def warning(selection):
    if selection == '2':
        print("Warning: This will delete all files in input_pictures folder except .txt files. Proceed? (y/n)")
        confirm = input().lower()
        if confirm == 'y':
            return True
        elif confirm == 'n':
            print("Aborting deletion process.")
            return False
        else:
            print("Invalid input. Aborting deletion process.")
            return False
    if selection == '3':
        print("Warning: This will delete all files in output_pictures folder. Proceed? (y/n)")
        confirm = input().lower()
        if confirm == 'y':
            return True
        elif confirm == 'n':
            print("Aborting deletion process.")
            return False
        else:
            print("Invalid input. Aborting deletion process.")
            return False
