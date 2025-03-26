import earthaccess
import os

# Option 1: Try the requested authentication method first
try:
    auth = earthaccess.login(persist=True)
    print("Authentication successful!")
except Exception as e:
    print(f"Direct authentication failed: {e}")
    
    # Option 2: Try account strategy
    try:
        auth = earthaccess.login(strategy='account', persist=True)
        print("Account authentication successful!")
    except Exception as e:
        print(f"Account authentication failed: {e}")
        
        # Option 3: Try netrc authentication
        try:
            auth = earthaccess.login(strategy='netrc')
            print("Netrc authentication successful!")
        except Exception as e:
            print(f"Netrc authentication failed: {e}")
            print("Please set up a .netrc file in your home directory with:")
            print("machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD")


# Define search parameters
merra2_product = "M2I3NVAER"
temporal_range = ("2020-03-01", "2020-03-05")
north_america_bbox = (-140, 20, -50, 60)  # North America [W, S, E, N]

print(f"Searching for MERRA-2 aerosol data...")
results = earthaccess.search_data(
    short_name=merra2_product,
    temporal=temporal_range,
    bounding_box=north_america_bbox
)

print(f"Found {len(results)} results")
# Extract download URLs from search results
def extract_urls_from_granules(granules):
    urls = []
    for granule in granules:
        try:
            if hasattr(granule, 'render_dict') and 'umm' in granule.render_dict:
                umm = granule.render_dict['umm']
                if 'RelatedUrls' in umm and isinstance(umm['RelatedUrls'], list):
                    for url_obj in umm['RelatedUrls']:
                        if isinstance(url_obj, dict) and 'Type' in url_obj and url_obj['Type'] == 'GET DATA':
                            if 'URL' in url_obj:
                                urls.append(url_obj['URL'])
        except Exception as e:
            print(f"Error extracting URL: {e}")
    return urls

download_urls = extract_urls_from_granules(results)
print(f"Extracted {len(download_urls)} download URLs")

import requests
import os

# Create download directory
download_dir = './merra2_data_3d'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Download function with session-based authentication
def download_files(urls, dest_dir, auth_obj):
    downloaded_files = []
    
    # Try to get a session from auth
    try:
        session = None
        if hasattr(auth_obj, 'get_session') and callable(getattr(auth_obj, 'get_session')):
            session = auth_obj.get_session()
        else:
            # Create a new session
            session = requests.Session()
            
        # Download each file
        for url in urls:
            filename = os.path.basename(url)
            file_path = os.path.join(dest_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(file_path):
                print(f"File already exists: {filename}")
                downloaded_files.append(file_path)
                continue
                
            print(f"Downloading {filename}...")
            response = session.get(url, stream=True)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded {filename}")
                downloaded_files.append(file_path)
            else:
                print(f"Download failed with status code: {response.status_code}")
                
    except Exception as e:
        print(f"Error during download: {e}")
        
    return downloaded_files

# Download the data
downloaded_files = download_files(download_urls, download_dir, auth)
