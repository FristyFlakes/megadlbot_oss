from pyrogram import filters, emoji, Client
from pyrogram.types import Message

from mega.database.files import MegaFiles
from mega.database.users import MegaUsers
from ...telegram import Common


@Client.on_message(filters.command("start", prefixes=["/"]))
async def start_message_handler(c: Client, m: Message):
    await MegaUsers().insert_user(m.from_user.id)
    if len(m.command) > 1:
        if m.command[1].split("-")[0] == 'plf':
            file_id = m.command[1].split("-", 1)[1]
            file_details = await MegaFiles().get_file_by_file_id(file_id)

            if file_details is not None:
                file_message = await c.get_messages(
                    chat_id=file_details['chat_id'],
                    message_ids=file_details['msg_id']
                )

                if str(file_details['file_type'].split("/"))[0].lower() == "video":
                    await m.reply_video(
                        video=file_message.video.file_id,
                        file_ref=file_message.video.file_ref
                    )
                elif str(file_details['file_type'].split("/"))[0].lower() == "audio":
                    await m.reply_audio(
                        audio=file_message.audio.file_id,
                        file_ref=file_message.audio.file_ref
                    )
                else:
                    await m.reply_document(
                        document=file_message.document.file_id,
                        file_ref=file_message.document.file_ref
                    )
    else:
        await m.reply_text(
            text=f"<b>Hello, My Name Is 𝗠𝗘𝗚𝗔𝗧𝗥𝗢𝗡 (^。^).\n\nI'm A <u>𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗨𝗥𝗟</u> To <u>𝗙𝗜𝗟𝗘</u> Uploading Bot.\n\nSend Me Any <u>𝗗𝗜𝗥𝗘𝗖𝗧 𝗟𝗜𝗡𝗞</u>, Wait For Me To Respond With <u>𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗</u> Or <u>𝗥𝗘𝗡𝗔𝗠𝗘</u> Before Proceeding To Starting Your Download.\n\n❌ <u>𝗣𝗢𝗥𝗡𝗢𝗚𝗥𝗔𝗣𝗛𝗜𝗖 𝗖𝗢𝗡𝗧𝗘𝗡𝗧𝗦</u> Are Strictly Prohibited & Will Get You Banned Permanently.</b>"
        )


@Client.on_message(group=-1)
async def stop_user_from_doing_anything(_, message: Message):
    allowed_users = Common().allowed_users
    if allowed_users and message.from_user.id not in allowed_users:
        message.stop_propagation()
    else:
        message.continue_propagation()
