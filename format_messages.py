import json
import datetime

INPUT_FILE = 'discord_export_2025-12-29.json'
OUTPUT_FILE = 'discord_news_source_2025-12-29.txt'

def format_for_notebooklm():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data file not found. Run fetch_discord_messages.py first.")
        return

    if not data:
        print("No messages to format.")
        return

    # Statistics
    total_msgs = len(data)
    channels = set(d['channel'] for d in data)
    users = set(d['author'] for d in data)
    
    # Group by channel
    msgs_by_channel = {}
    for d in data:
        c = d['channel']
        if c not in msgs_by_channel:
            msgs_by_channel[c] = []
        msgs_by_channel[c].append(d)

    # Sort channels by activity (message count)
    sorted_channels = sorted(msgs_by_channel.items(), key=lambda x: len(x[1]), reverse=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Header for AI Context
        f.write("# Discord Server Daily Log (2025-12-29)\n")
        f.write(f"**Date:** 2025-12-29\n")
        f.write(f"**Total Messages:** {total_msgs}\n")
        f.write(f"**Active Users:** {len(users)}\n")
        f.write(f"**Active Channels:** {len(channels)}\n\n")
        f.write("## 📝 Executive Summary Request\n")
        f.write("Please analyze the following Discord logs to create a 'Daily News' summary.\n")
        f.write("Focus on:\n")
        f.write("1. Major announcements or releases.\n")
        f.write("2. Interesting technical discussions or discoveries.\n")
        f.write("3. Fun community moments or trending topics.\n")
        f.write("Ignore system messages or trivial greetings unless they led to a discussion.\n\n")
        f.write("---\n\n")

        # Channel Logs
        for channel, msgs in sorted_channels:
            f.write(f"## 📺 Channel: #{channel} ({len(msgs)} messages)\n")
            
            for m in msgs:
                # Format: [Time] User: Content
                # Parse timestamp for simpler display (HH:MM)
                ts_str = m['timestamp']
                try:
                    dt = datetime.datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    # Convert to JST for display
                    dt_jst = dt.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
                    time_display = dt_jst.strftime('%H:%M')
                except:
                    time_display = ts_str
                
                content = m['content'].replace('\n', ' ')
                # Handle attachments label
                if m.get('attachments'):
                    content += f" [Attached Images: {len(m['attachments'])}]"

                f.write(f"- **{time_display}** {m['author']}: {content}\n")
            
            f.write("\n")

    print(f"✅ Formatted data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    format_for_notebooklm()
