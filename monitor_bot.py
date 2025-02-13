from telethon import TelegramClient, events
from datetime import datetime

# Your Telegram API credentials
api_id = 28775212  
api_hash = "19cc6537666aa2403b0f5873781cdb5d"  
phone_number = "+917870492073"  # Your Telegram number
target_user = "@EternaMM"  # Target user to monitor
admin_username = "@RootApex"  # Replace with your Telegram username, or use phone number instead

# Initialize the Telegram Client
client = TelegramClient("session_name", api_id, api_hash)

# Track online status
online_time = None
admin_entity = None  # Store the admin user entity

@client.on(events.Raw)
async def track_status(event):
    global online_time, admin_entity
    user = await client.get_entity(target_user)

    # Get the latest status of the user
    user_status = user.status  

    if hasattr(user_status, "was_online") and not hasattr(user_status, "expires"):
        if online_time:
            offline_time = datetime.now()
            duration = offline_time - online_time
            message = (
                f"User Online - {online_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"User Online Till - {duration}\n"
                f"User Offline - {offline_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            # Send the message to the admin (you)
            if admin_entity:
                await client.send_message(admin_entity, message)
            online_time = None  # Reset tracking

    elif hasattr(user_status, "expires"):
        if online_time is None:  # Only log once
            online_time = datetime.now()
            message = f"User Online - {online_time.strftime('%Y-%m-%d %H:%M:%S')}"
            # Send the message to the admin (you)
            if admin_entity:
                await client.send_message(admin_entity, message)

async def main():
    global admin_entity
    await client.start(phone_number)
    # Try fetching the admin entity by username or phone number
    try:
        admin_entity = await client.get_entity(admin_username)  # Using username
    except ValueError:
        # If username fails, use phone number to fetch entity
        admin_entity = await client.get_entity(phone_number)

    # Ensure interaction by sending a message to the admin (you) once
    if admin_entity:
        await client.send_message(admin_entity, "Hello! Bot is now running and monitoring.")

    print("Bot is running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())