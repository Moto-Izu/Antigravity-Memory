
import os
import json
import requests
import datetime
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_IDS_ENV = os.getenv('DISCORD_CHANNEL_IDS')
DISCORD_EPOCH = 1420070400000

HEADERS = {
    'authorization': TOKEN,
    'content-type': 'application/json'
}

def date_to_snowflake(date_obj):
    timestamp = date_obj.timestamp() * 1000
    return int(timestamp - DISCORD_EPOCH) << 22

def get_guild_channels(guild_id):
    print(f"Fetching all channels for Guild ID: {guild_id}...")
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    try:
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"Error fetching guild channels: {r.status_code} {r.text}")
            return []
        channels = r.json()
        return [c for c in channels if c['type'] in [0, 5]]
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_messages(channel_id, channel_name, start_snowflake, end_snowflake):
    messages = []
    last_id = None
    
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
            
            if r.status_code in [403, 401]:
                break

            if r.status_code != 200:
                break
                
            batch = r.json()
            if not batch:
                break
                
            for msg in batch:
                msg_id = int(msg['id'])
                
                # Check timeframe
                if msg_id < start_snowflake:
                    return messages
                
                if start_snowflake <= msg_id < end_snowflake:
                    author = msg.get('author', {}).get('username', 'Unknown')
                    content = msg.get('content', '')
                    timestamp = msg.get('timestamp', '')
                    
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
            if int(last_id) < start_snowflake:
                break
            
            time.sleep(0.2)
            
        except Exception:
            break
            
    return messages

def format_report(input_file, output_file, target_date_str):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data file not found.")
        return

    if not data:
        print("No messages to format.")
        # Create empty file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Discord Server Log ({target_date_str})\nNo messages found.")
        return

    total_msgs = len(data)
    channels = set(d['channel'] for d in data)
    users = set(d['author'] for d in data)
    
    msgs_by_channel = {}
    for d in data:
        c = d['channel']
        if c not in msgs_by_channel:
            msgs_by_channel[c] = []
        msgs_by_channel[c].append(d)

    sorted_channels = sorted(msgs_by_channel.items(), key=lambda x: len(x[1]), reverse=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Discord Server Daily Log ({target_date_str})\n")
        f.write(f"**Date:** {target_date_str}\n")
        f.write(f"**Total Messages:** {total_msgs}\n")
        f.write(f"**Active Users:** {len(users)}\n")
        f.write(f"**Active Channels:** {len(channels)}\n\n")
        f.write("## 📝 Executive Summary Request\n")
        f.write("Please analyze the following Discord logs to create a 'Daily News' summary.\n")
        f.write("---\n\n")

        for channel, msgs in sorted_channels:
            f.write(f"## 📺 Channel: #{channel} ({len(msgs)} messages)\n")
            
            # Sort chronologically for reading
            msgs.sort(key=lambda x: x['timestamp'])
            
            for m in msgs:
                ts_str = m['timestamp']
                try:
                    dt = datetime.datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    dt_jst = dt.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
                    time_display = dt_jst.strftime('%H:%M')
                except:
                    time_display = ts_str
                
                content = m['content'].replace('\n', ' ')
                if m.get('attachments'):
                    content += f" [Attached Images: {len(m['attachments'])}]"

                f.write(f"- **{time_display}** {m['author']}: {content}\n")
            f.write("\n")

    print(f"✅ Formatted report saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate Discord Daily Log")
    parser.add_argument("date", nargs="?", help="Target date (YYYY-MM-DD). Defaults to yesterday.")
    args = parser.parse_args()

    # Determine date
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Error: Date must be YYYY-MM-DD")
            return
    else:
        # Default to yesterday
        target_date = datetime.datetime.now() - datetime.timedelta(days=1)

    # Set timezone JST
    JST = datetime.timezone(datetime.timedelta(hours=9))
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=JST)
    next_day = target_date + datetime.timedelta(days=1)
    
    target_date_str = target_date.strftime("%Y-%m-%d")
    
    print(f"Target Date: {target_date_str}")
    
    if not TOKEN:
        print("Error: DISCORD_TOKEN not set in .env")
        return

    # Calculate Snowflakes
    start_snowflake = date_to_snowflake(target_date)
    end_snowflake = date_to_snowflake(next_day)

    # Get Channels
    target_channels = []
    if CHANNEL_IDS_ENV:
        ids = [cid.strip() for cid in CHANNEL_IDS_ENV.split(',') if cid.strip()]
        for i in ids:
            target_channels.append({'id': i, 'name': 'specific-channel'})
    elif GUILD_ID:
        target_channels = get_guild_channels(GUILD_ID)
    else:
        print("Error: Set DISCORD_GUILD_ID or DISCORD_CHANNEL_IDS in .env")
        return

    print(f"Scanning {len(target_channels)} channels...")
    all_messages = []

    try:
        for i, channel in enumerate(target_channels):
            c_id = channel['id']
            c_name = channel.get('name', c_id)
            print(f"[{i+1}/{len(target_channels)}] Checking #{c_name}...", end='\r')
            
            msgs = fetch_messages(c_id, c_name, start_snowflake, end_snowflake)
            if msgs:
                all_messages.extend(msgs)
    except KeyboardInterrupt:
        print("\nInterrupted.")

    print(f"\nFound {len(all_messages)} messages.")
    
    # Save JSON
    json_file = f"discord_export_{target_date_str}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, indent=2, ensure_ascii=False)
    
    # Format TXT
    txt_file = f"discord_news_source_{target_date_str}.txt"
    format_report(json_file, txt_file, target_date_str)

if __name__ == "__main__":
    main()
