import os 
import requests
import os
import ast
from dotenv import load_dotenv
from config_first import generate_access_token, GRAPH_API_ENDPOINT


def get_message_details(message_id, headers):
    response = requests.get(GRAPH_API_ENDPOINT + '/me/messages/{0}'.format(message_id), headers=headers)
    if response.status_code != 200:
        raise Exception(response.json())
    return response.json()


def read_emails_and_save_attachments():
    try:
        # Generate access token
        access_token = generate_access_token()

        headers = {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

        params = {
            'top': 999,  # Max is 1000 messages per request
            'select': 'id,subject,hasAttachments', ## also have attachments
            'filter': 'isRead eq false',  ## Only reading Unseen emails
            # 'filter': 'isRead eq false and hasAttachments eq false' ## unRead Emails with attachments only
            'count': 'true'
        }
        #💡 More about Params Read : https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http

        response = requests.get(GRAPH_API_ENDPOINT + '/me/mailFolders/inbox/messages', headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(response.json())
        
        response_json = response.json()
        emails = response_json['value']
        data_list = []
        
        if emails:
            print(f"You have {len(emails)} new Email\s")
            for email in emails:
                email_id = email['id']
                message_details = get_message_details(email_id, headers)
                
                # Mark the email as "read" (seen)
                patch_data = {
                    "isRead": True
                }

                requests.patch(GRAPH_API_ENDPOINT + f'/me/messages/{email_id}', headers=headers,
                                                json=patch_data)

                ## If emails have attachments, example : download them              
                if email['hasAttachments']:
                    response = requests.get(GRAPH_API_ENDPOINT + '/me/messages/{0}/attachments'.format(email_id), headers=headers)
                    print(f"Found attachment")

                    # attachment_items = response.json()['value']
                    
                    # for attachment in attachment_items:
                    #     file_name = attachment['name']
                    #     attachment_id = attachment['id']
                    #     attachment_content = requests.get(GRAPH_API_ENDPOINT + '/me/messages/{0}/attachments/{1}/$value'.format(email_id, attachment_id), headers=headers)
                        
                    #     save_folder = 'unseen_attachments'
                    #     os.makedirs('unseen_attachments', exist_ok=True) 

                    #     filepath = os.path.join(save_folder, file_name)
                        
                    #     with open(filepath, 'wb') as _f:
                    #         _f.write(attachment_content.content)
                        
                        ## DB actions from  Mail information, example Write to DB etc.
                        # data = {
                        #     'mail': message_details['from']['emailAddress']['address'],
                        #     'name': message_details['from']['emailAddress']['name'],
                        #     'mail_subject': message_details['subject'],
                        #     'mail_date': message_details['receivedDateTime'][:-10],
                        #     'filename': file_name,
                        #     'filepath': filepath
                        # }
                        # data_list.append(candidate_data)
                
                else:
                    print("No Attachements found.")
        else:
            print("Your Inbox is empty....")
        return data_list

    except Exception as e:
        return []
    
if __name__ == "__main__": 
    read_emails_and_save_attachments()
