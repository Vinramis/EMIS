
import os
import time

def extract_files(folder_path: str, case_insensitivity: bool, infix: list[str] | str):
    """
    Finds files in the specified folder by infixes in the filename, returns a list of filenames.
    """
    try:
        all_files = os.listdir(folder_path)
        matched_files = []
        if isinstance(infix, str):
            infix = [infix]
        
        # Note: logic modified slightly to be more robust and clearer than original
        # original logic removed matched items from all_files while iterating or checked containment
        
        files_to_check = list(all_files) # Copy to avoid modification issues if we were removing
        
        processed_files = set()

        for inf in infix:
            search_inf = inf.lower() if case_insensitivity else inf
            
            for file in files_to_check:
                if file in processed_files:
                    continue
                
                search_file = file.lower() if case_insensitivity else file
                
                if search_inf in search_file:
                    matched_files.append(file)
                    processed_files.add(file)
                    
    except Exception as e:
        print(f"[ERROR] Error extracting files: {e}")
        exit(0)
    
    # print("extract_files worked correctly.")
    return matched_files

def find_file_by_prefix(directory: str, prefix: str):
    """
    Finds the first file in the directory starting with the given prefix.
    """
    try:
        for filename in os.listdir(directory):
            if filename.lower().startswith(prefix.lower().strip()):
                return os.path.join(directory, filename)
    except FileNotFoundError:
        print(f"[ERROR] Directory '{directory}' does not exist.")
        return None
    except Exception as e:
        print(f"[ERROR] Error searching in directory '{directory}': {e}")
        return None
    return None

def organize_files(topics_folder: str, homework_folder: str) -> tuple[str, str]:
    """
    Organizes files into TOPICS and HOMEWORK subfolders if they are currently in the same folder.
    Returns the new paths for TOPICS_FOLDER and HOMEWORK_FOLDER.
    """
    # Check if they point to the same directory
    # Normalize paths to be sure
    if os.path.abspath(topics_folder) == os.path.abspath(homework_folder):
        print("Separating topic and homework files...")
        topic_keywords = ["кл", "лек", "урок"]
        homework_keywords = ["дз", "дом"]

        all_folder = topics_folder
        
        topic_files = extract_files(all_folder, True, topic_keywords)
        homework_files = extract_files(all_folder, True, homework_keywords)
        
        # Check for unassigned files (optional, but good for user info)
        all_files_in_dir = os.listdir(all_folder)
        assigned_files = set(topic_files + homework_files)
        unassigned = [f for f in all_files_in_dir if f not in assigned_files and os.path.isfile(os.path.join(all_folder, f))]

        if unassigned:
            print(f"[INFO] Unassigned files in '{all_folder}': {unassigned}")
            print("(?) Separating remaining files manually or add keywords.")
            print(f"\n(?) --- Keywords used ---")
            print(f"(?) Classwork: {topic_keywords}")
            print(f"(?) Homework: {homework_keywords}\n")
            time.sleep(2) # Short wait

        # Define new subdirectories
        new_topics_folder = os.path.join(os.path.dirname(all_folder), "КЛ")
        new_homework_folder = os.path.join(os.path.dirname(all_folder), "ДЗ")
        
        os.makedirs(new_topics_folder, exist_ok=True)
        os.makedirs(new_homework_folder, exist_ok=True)

        # Move files
        for file in topic_files:
            try:
                os.rename(os.path.join(all_folder, file), os.path.join(new_topics_folder, file))
            except FileNotFoundError:
                pass # Already moved?
        
        for file in homework_files:
            try:
                os.rename(os.path.join(all_folder, file), os.path.join(new_homework_folder, file))
            except FileNotFoundError:
                pass

        # Clean up original folder if empty
        if not os.listdir(all_folder):
            try:
                os.rmdir(all_folder)
                print(f"[INFO] Files successfully separated into '{new_topics_folder}' and '{new_homework_folder}'.")
            except OSError:
                pass
        
        return new_topics_folder, new_homework_folder
    
    return topics_folder, homework_folder
