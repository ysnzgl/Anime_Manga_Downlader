import requests

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename

download_file("http://myvi.ru/player/embed/html/oTLUx7LMnqrjan78QcZkd9mbPYdo2_73OwkBM8RPhitRN5PjtfO0iOcGYSEgqC98W0");