import os
import pandas as pd
import re

def extract_info_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
        # Extracting the title using regular expression
        title_match = re.search(r'TITLE:\s*(.*?)\s*LINK:', text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = None
        
        # Extracting the link using regular expression
        link_match = re.search(r'LINK:\s*(.*?)\s*', text, re.IGNORECASE)
        if link_match:
            link = link_match.group(1).strip()
        else:
            link = None
        
        # Extracting the context
        context_start = text.find("TITLE:")
        context_end = text.find("\n\n", context_start)
        context = text[context_end:].strip() if context_start != -1 and context_end != -1 else None
        
        return title, link, context

def parse_folder(folder_path):
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            title, link, context = extract_info_from_file(file_path)
            data.append({'Title': title, 'Link': link, 'Context': context})
    return data

# Replace 'folder_path' with the path to your folder containing text files
folder_path = 'data'
parsed_data = parse_folder(folder_path)

# Create DataFrame
df = pd.DataFrame(parsed_data)

# Display DataFrame
print(df)
