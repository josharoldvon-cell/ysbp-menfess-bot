import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

users = {}
waiting_menfess = set()


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📨 Kirim Menfess", callback_data="send")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile"),
         InlineKeyboardButton("📋 Rules", callback_data="rules")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📣 <b>YSBP MENFESS</b>\n\n"
        "Bot menfess anonim.\n"
        "Kirim pesanmu dan sampaikan apa yang ingin kamu katakan."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "send":
        waiting_menfess.add(query.from_user.id)

        await query.message.reply_text(
            "💌 <b>Kirim menfess kamu di sini!</b>\n\n"
            "Contoh:\n\n"
            "From :\n"
            "To :\n\n"
            "Message :\n"
            "Song :\n\n"
            "Kirim dalam <b>satu pesan</b> ya.",
            parse_mode="HTML"
        )

    elif query.data == "profile":
        await query.message.reply_text(
            f"👤 <b>Profile</b>\n\n"
            f"User ID: <code>{query.from_user.id}</code>",
            parse_mode="HTML"
        )

    elif query.data == "rules":
        await query.message.reply_text(
            "📋 <b>RULES</b>\n\n"
            "• Jangan mengandung SARA.\n"
            "• Jangan menghina atau mengancam.\n"
            "• Jangan kirim spam.\n"
            "• Gunakan bahasa yang sopan.\n"
            "• Menfess yang melanggar aturan dapat ditolak.",
            parse_mode="HTML"
        )


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in waiting_menfess:
        return

    message = update.message

    try:
        if message.text:
            content = message.text

            post = (
                "💌 <b>YSBP MENFESS</b>\n\n"
                f"{content}\n\n"
                "━━━━━━━━━━━━━━\n"
                "📩 Anonymous Menfess"
            )

            await context.bot.send_message(
                chat_id=CHANNEL,
                text=post,
                parse_mode="HTML"
            )

        else:
            await message.reply_text(
                "Untuk sementara kirim menfess dalam bentuk teks dulu ya."
            )
            return

        waiting_menfess.remove(user_id)

        await message.reply_text(
            "✅ <b>Message successfully sent!</b>\n\n"
            "Menfess kamu sudah dikirim secara anonim.",
            parse_mode="HTML",
            reply_markup=menu()
        )

    except Exception as e:
        await message.reply_text(
            "❌ Menfess gagal dikirim.\n"
            "Pastikan bot sudah menjadi admin di channel tujuan."
        )
        print(e)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)
    )

    print("YSBP Menfess Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
