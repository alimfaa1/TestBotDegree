from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Bot token
TOKEN = "8126662742:AAHScPgCfw-8wH__SQHNfbG3vslvH3ENzfM"  # استبدلها بتوكن البوت الحقيقي

# درجات وهمية مأخوذة من الطالب الأول
student_data = {
    "اللغة العربية": {"التقييم": 37, "الامتحان": 56, "المجموع": 93},
    "الرياضيات": {"التقييم": 34, "الامتحان": 52, "المجموع": 86},
    "اللغة الإنجليزية": {"التقييم": 36, "الامتحان": 57, "المجموع": 93},
    "متعدد التخصصات": {"التقييم": 40, "الامتحان": 40, "المجموع": 80},
    "التربية الدينية": {"التقييم": 40, "الامتحان": 50, "المجموع": 90},
    "اللغة الإنجليزية مستوى رفيع": {"الامتحان": 23}
}

# تخزين الحالة لكل مستخدم
user_states = {}

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = {"step": "ask_grade"}
    keyboard = [["الصف الأول", "الصف الثاني", "الصف الثالث"]]
    await update.message.reply_text("مرحبًا بك في تجربة بوت النتائج 📊✨")
    await update.message.reply_text(
        "من فضلك اختر الصف الدراسي:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    if chat_id not in user_states:
        user_states[chat_id] = {"step": "ask_grade"}
        await update.message.reply_text("من فضلك اختر الصف الدراسي أولًا.")
        return

    state = user_states[chat_id]

    # خطوة اختيار الصف
    if state["step"] == "ask_grade":
        if text not in ["الصف الأول", "الصف الثاني", "الصف الثالث"]:
            await update.message.reply_text("يرجى اختيار الصف الدراسي من الخيارات المتاحة.")
            return
        state["grade"] = text
        state["step"] = "ask_id"
        await update.message.reply_text("📌 يمكنك تجربة البوت بإدخال الرقم: 123456789\n\nالآن أدخل الرقم القومي الخاص بك:")
        return

    # خطوة إدخال الرقم القومي
    if state["step"] == "ask_id":
        if text != "123456789":
            await update.message.reply_text("❌ الرقم القومي غير صحيح. يرجى المحاولة مرة أخرى.")
            return

        # عرض النتائج باسم "ادوات التعليم الذكية"
        await update.message.reply_text("هتظهر النتائج بالتفصيل زي كدة وطبعاً هتختار رسالة خاصة لتلاميذك وهيكون فيها اسمهم 👋", parse_mode="Markdown")
        for subject, details in student_data.items():
            msg = f"📘 {subject}\n"
            for label, value in details.items():
                msg += f"- {label}: {value}\n"
            await update.message.reply_text(msg)

        # إرسال صورة الميم في النهاية
        try:
            with open("haha.png", "rb") as photo:
                await update.message.reply_photo(photo=photo, caption="🥳🥳🥳🥳")
        except FileNotFoundError:
            await update.message.reply_text("❗ لم يتم العثور على الصورة (haha.png) في مجلد البوت.")

        # إعادة تعيين الحالة
        user_states.pop(chat_id)
        return

# إعداد البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
