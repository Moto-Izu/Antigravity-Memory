import os
import json
import requests
import datetime
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_IDS_ENV = os.getenv('DISCORD_CHANNEL_IDS')

if not TOKEN:
    print("Error: Please set DISCORD_TOKEN in .env file")
    exit(1)

HEADERS = {
    'authorization': TOKEN,
    'content-type': 'application/json'
}

# Target Date: 2025-12-29 (JST)
JST = datetime.timezone(datetime.timedelta(hours=9))
TARGET_DATE = datetime.datetime(2025, 12, 29, 0, 0, 0, tzinfo=JST)
NEXT_DAY = TARGET_DATE + datetime.timedelta(days=1)

# Discord Snowflake Epoch
DISCORD_EPOCH = 1420070400000

def date_to_snowflake(date_obj):
    timestamp = date_obj.timestamp() * 1000
    return int(timestamp - DISCORD_EPOCH) << 22

START_SNOWFLAKE = date_to_snowflake(TARGET_DATE)
END_SNOWFLAKE = date_to_snowflake(NEXT_DAY)

print(f"DEBUG: Target Range (JST): {TARGET_DATE} to {NEXT_DAY}")

def get_guild_channels(guild_id):
    print(f"Fetching all channels for Guild ID: {guild_id}...")
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error fetching guild channels: {r.status_code} {r.text}")
        return []
    
    channels = r.json()
    # Filter for Text Channels (type 0) and Announcement Channels (type 5)
    # Also capable of reading threads if we wanted, but sticking to root channels for now.
    text_channels = [c for c in channels if c['type'] in [0, 5]] 
    print(f"  Found {len(text_channels)} text channels in guild.")
    return text_channels

def fetch_messages(channel_id, channel_name):
    messages = []
    last_id = None
    
    # print(f"  Scanning #{channel_name} ({channel_id})...") 
    
    while True:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        if last_id:
            url += f"&before={last_id}"
            
        try:
            r = requests.get(url, headers=HEADERS)
            
            if r.status_code == 429:
                retry_after = r.json().get('retry_after', 1)
                time.sleep(retry_after)
                continue
            
            if r.status_code == 403: # Permission denied
                # print(f"    Skipping #{channel_name}: No permission")
                break

            if r.status_code != 200:
                # print(f"    Error fetching #{channel_name}: {r.status_code}")
                break
                
            batch = r.json()
            if not batch:
                break
                
            for msg in batch:
                msg_id = int(msg['id'])
                
                if msg_id < START_SNOWFLAKE:
                    return messages
                
                if START_SNOWFLAKE <= msg_id < END_SNOWFLAKE:
                    author = msg.get('author', {}).get('username', 'Unknown')
                    content = msg.get('content', '')
                    timestamp = msg.get('timestamp', '')
                    
                    # Attachments (Images)
                    attachments = []
                    if 'attachments' in msg:
                        for att in msg['attachments']:
                            attachments.append(att.get('url'))

                    formatted_msg = {
                        'id': str(msg_id),
                        'channel': channel_name,
                        'timestamp': timestamp,
                        'author': author,
                        'content': content,
                        'attachments': attachments
                    }
                    messages.append(formatted_msg)
            
            last_id = batch[-1]['id']
            if int(last_id) < START_SNOWFLAKE:
                break
            
            time.sleep(0.2)
            
        except Exception:
            break
            
    return messages

# Main execution logic
target_channels = []

if CHANNEL_IDS_ENV:
    # Use specific channels if provided
    ids = [cid.strip() for cid in CHANNEL_IDS_ENV.split(',') if cid.strip()]
    for i in ids:
        target_channels.append({'id': i, 'name': 'specific-channel'})
elif GUILD_ID:
    # Fetch all channels from guild
    target_channels = get_guild_channels(GUILD_ID)
else:
    print("Error: Please set DISCORD_GUILD_ID or DISCORD_CHANNEL_IDS in .env")
    exit(1)

all_messages = []
print(f"Starting scan of {len(target_channels)} channels...")

try:
    for i, channel in enumerate(target_channels):
        c_id = channel['id']
        c_name = channel.get('name', c_id)
        
        # Progress indicator
        print(f"[{i+1}/{len(target_channels)}] Checking #{c_name}...", end='\r')
        
        msgs = fetch_messages(c_id, c_name)
        if msgs:
            print(f"\n  ✅ Found {len(msgs)} messages in #{c_name}")
            all_messages.extend(msgs)

except KeyboardInterrupt:
    print("\n\n⚠️ Scan interrupted by user! Saving collected messages so far...")
except Exception as e:
    print(f"\n\n⚠️ Unexpected error: {e}. Saving collected messages so far...")

print("\nScan complete (or interrupted).")

# Sort matches
all_messages.sort(key=lambda x: x['timestamp'])

output_file = 'discord_export_2025-12-29.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_messages, f, indent=2, ensure_ascii=False)

print(f"Done! Exported {len(all_messages)} messages to {output_file}")
