from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# Bot token
# =====================
TOKEN = "8126662742:AAHScPgCfw-8wH__SQHNfbG3vslvH3ENzfM"

# =====================
# Demo student data
# =====================
student_data = {
    "اللغة العربية": {"التقييم": 37, "الامتحان": 56, "المجموع": 93},
    "الرياضيات": {"التقييم": 34, "الامتحان": 52, "المجموع": 86},
    "اللغة الإنجليزية": {"التقييم": 36, "الامتحان": 57, "المجموع": 93},
    "متعدد التخصصات": {"التقييم": 40, "الامتحان": 40, "المجموع": 80},
    "التربية الدينية": {"التقييم": 40, "الامتحان": 50, "المجموع": 90},
    "اللغة الإنجليزية مستوى رفيع": {"الامتحان": 23}
}

# =====================
# Support Arabic numbers
# =====================
def normalize_arabic_numbers(text: str):
    translation_table = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return text.translate(translation_table)

# =====================
# User state tracking
# =====================
user_states = {}

# =====================
# Start command
# =====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = {"step": "ask_grade"}

    keyboard = [["الصف الأول", "الصف الثاني", "الصف الثالث"]]

    await update.message.reply_text("🎓 هذه جولة إرشادية للمعلم لمعرفة كيف يستخدم الطالب البوت")
    await update.message.reply_text(
        "🟦 *الخطوة ١: الطالب يختار الصف الدراسي*\n\nاختر الآن أي صف لتجربة الخطوة التالية 👇",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "⬇️ اختر الصف:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# =====================
# Message handler
# =====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = normalize_arabic_numbers(update.message.text.strip())

    if chat_id not in user_states:
        user_states[chat_id] = {"step": "ask_grade"}
        await update.message.reply_text("يرجى اختيار الصف أولًا.")
        return

    state = user_states[chat_id]

    # Step 1: Ask for grade
    if state["step"] == "ask_grade":
        if text not in ["الصف الأول", "الصف الثاني", "الصف الثالث"]:
            await update.message.reply_text("اختر الصف من الأزرار فقط.")
            return
        state["grade"] = text
        state["step"] = "ask_id"
        await update.message.reply_text(
            "🟦 *الخطوة ٢: الطالب يدخل الرقم القومي*\n\n📌 اطلب من الطالب إدخال رقمه القومي.\nللتجربة اكتب: 123456789",
            parse_mode="Markdown"
        )
        return

    # Step 2: Ask for ID
    if state["step"] == "ask_id":
        if text != "123456789":
            await update.message.reply_text("❌ الرقم غير صحيح. جرب: 123456789")
            return

        await update.message.reply_text("✅ هكذا ستظهر النتيجة للطالب 👋", parse_mode="Markdown")

        for subject, details in student_data.items():
            msg = f"📘 {subject}\n"
            for label, value in details.items():
                msg += f"- {label}: {value}\n"
            await update.message.reply_text(msg)

        try:
            with open("haha.png", "rb") as photo:
                await update.message.reply_photo(photo=photo, caption="🥳🥳🥳🥳🥳🥳")
        except FileNotFoundError:
            await update.message.reply_text("❗ لم يتم العثور على صورة (haha.png) في مجلد البوت.")

        # End the flow
        user_states.pop(chat_id, None)
        return

# =====================
# Run the bot
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
