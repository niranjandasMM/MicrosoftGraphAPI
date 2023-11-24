import os 
import requests
from config_first import generate_access_token, GRAPH_API_ENDPOINT


def upload_file_to_onedrive(file_path):
    try:
        
        access_token = generate_access_token()
        headers = {
            'Authorization': 'Bearer ' + access_token['access_token'],
        }
        
        file_name = os.path.basename(file_path)
        
        with open(file_path, 'rb') as upload:
            media_content = upload.read()
        
        response = requests.put(
            GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name}:/content',
            headers=headers,
            data=media_content
        )

        if response.status_code == 200 or response.status_code == 201:
            
            item_id = response.json().get('id')

            file_metadata_response = requests.get(
                GRAPH_API_ENDPOINT + f'/me/drive/items/{item_id}',
                headers=headers
            )

            if file_metadata_response.status_code == 200:
                file_metadata = file_metadata_response.json()
                sharing_link = file_metadata.get('webUrl')
                return sharing_link
            else:
                print("some Error happened")
        else:
            print("Response failed")

    except Exception as e:
        return e


if __name__ == "__main__": 
    upload_file_to_onedrive(file_path="Your_file_you_want_to_upload.txt")
