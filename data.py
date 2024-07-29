import os


def find_file_with_prefix(folder_path, prefix):
   
    files = os.listdir(folder_path)

    
    for file in files:
        if file.startswith(prefix):
           
            return os.path.join(folder_path, file)

  
    return None


def find_files_with_prefix_list(folder_path, prefix):
    
    files = os.listdir(folder_path)

    
    matching_files = [file for file in files if file.startswith(prefix)]

   
    return [os.path.join(folder_path, file) for file in matching_files]
