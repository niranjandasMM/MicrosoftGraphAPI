import os
import requests
from config_first import generate_access_token, GRAPH_API_ENDPOINT

save_location = os.getcwd() ## By default it saves all files to current Working Directory.

file_names = ['Chat_app_AC_setup.pdf','patent_example.txt']  # Replace with the actual names of the files on OneDrive you want

access_token = generate_access_token()
headers = {
	'Authorization': 'Bearer ' + access_token['access_token']
}

# Step 1. Iterate through file names
for file_name in file_names:
    # Step 2. Get file information
    response_file_info = requests.get(
        GRAPH_API_ENDPOINT + f'/me/drive/root:/{file_name}',  # Replace with the actual path, by default searches in root path in onedrive
        headers=headers
    )
    
    # Check if the file exists
    if response_file_info.status_code == 200:
        # Step 3. Downloading OneDrive file
        file_id = response_file_info.json().get('id')
        response_file_content = requests.get(GRAPH_API_ENDPOINT + f'/me/drive/items/{file_id}/content', headers=headers)
        with open(os.path.join(save_location, file_name), 'wb') as _f:
            _f.write(response_file_content.content)
        print(f'{file_name} downloaded successfully.')
    else:
        print(f'File not found: {file_name}')