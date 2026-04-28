# Made by IST Technology    
# Telegram: @ISToffical
#GitHub: AlMatCod
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ===================== Настройки =====================
TELEGRAM_TOKEN = "tg api"
API_KEY = "api"

# ===================== Функция запроса к LLM =====================
def ask_med_ai(prompt: str) -> str:
    full_prompt = (
        "Ты медицинский помощник. Пользователь описывает симптомы, например: "
        "'болит голова', 'температура', 'кашель'. "
        "Ты отвечаешь понятно и безопасно, даешь советы что сделать дома, "
        "но не ставишь диагноз и не заменяешь врача. "
        f"Пользователь пишет: '{prompt}'"
    )

    r = requests.post(
        "https://apifreellm.com/api/v1/chat",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"message": full_prompt}
    )
    data = r.json()
    if data.get("success"):
        return data["response"]
    else:
        return "Не могу ответить, попробуй сформулировать по-другому."

# ===================== Обработчики =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Medi, твой медицинский помощник. Опиши свои симптомы, и я дам советы, как действовать."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Подождите, Medi думает...")
    answer = ask_med_ai(user_text)
    await update.message.reply_text(answer)

# ===================== Запуск бота =====================
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Medi бот запущен...")
app.run_polling()
