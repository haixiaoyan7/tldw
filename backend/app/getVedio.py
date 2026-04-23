import requests
from msal import PublicClientApplication, SerializableTokenCache
import base64   
####################### Azure AD Config #######################

TENANT_ID = "YOUR_TENANT_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
SHAREPOINT_DOMAIN = "graph.microsoft.com" 
SITE_NAME = "YOUR_SITE_NAME"
CACHE_FILE = "token_cache1.json"
SHAREPOINT_API = f"https://{SHAREPOINT_DOMAIN}/sites/{SITE_NAME}/_api"
SCOPES = ["Files.Read"]
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
######################## Token Management #######################
def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        f.write(cache.serialize())

def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            cache = SerializableTokenCache()
            cache.deserialize(f.read())
            return cache
    except FileNotFoundError:
        return SerializableTokenCache()

def get_access_token():
    cache = load_cache()

    app = PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache
    )

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        flow = app.initiate_device_flow(scopes=SCOPES)
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise Exception(f"Token acquisition failed: {result}")

    save_cache(cache)

    access_token = result["access_token"]
    # print("Access Token:", access_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    return headers

def send_request(url):
    headers = get_access_token()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # print(response.json())
        return response
    else:
        print("Request failed:", response.status_code, response.text)
        return response

def download_video(download_url, local_path):
    r = requests.get(download_url, stream=True)
    r.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Video downloaded to {local_path}")

def get_file_info(share_url):
    encoded_url = base64.urlsafe_b64encode(share_url.encode()).decode().rstrip("=")
    share_id = f"u!{encoded_url}"
    graph_url = f"https://graph.microsoft.com/v1.0/shares/{share_id}/driveItem"
    r = send_request(graph_url)
    if r:
        download_url = r.get("@microsoft.graph.downloadUrl")
        file_id = r.get("file").get("hashes").get("quickXorHash")
        return {"download_url":download_url, "file_id": file_id}
    return None
