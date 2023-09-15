from huggingface_hub import snapshot_download
import os 

REPO_ID  ='MBZUAI/LaMini-Flan-T5-248M'
os.makedirs('model/',exist_ok=True)
snapshot_download(repo_id=REPO_ID,local_dir = 'model/')
