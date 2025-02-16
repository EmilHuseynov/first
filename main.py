from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from questions import question_groups
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_question(update, context, group_index=0, question_index=0)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, group_index: int, question_index: int):
    if group_index >= len(question_groups):
        await update.message.reply_text("Поздравляем! Вы прошли все вопросы!")
        return

    group = question_groups[group_index]
    if question_index >= len(group['questions']):
        group_index += 1
        question_index = 0
        if group_index >= len(question_groups):
            await update.message.reply_text("Поздравляем! Вы прошли все вопросы!")
            return
        group = question_groups[group_index]

    question = group['questions'][question_index]
    
    keyboard = []
    for answer in question['answers']:
        keyboard.append([InlineKeyboardButton(answer, 
                       callback_data=f"{group_index}_{question_index}_{answer}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка изображения группы и вопроса
    if question_index == 0:  # Показываем картинку только для первого вопроса в группе
        await update.message.reply_photo(
            photo=group['image'],
            caption=question['text'],
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text=question['text'],
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    group_index, question_index, selected_answer = query.data.split('_')
    group_index = int(group_index)
    question_index = int(question_index)

    correct_answer = question_groups[group_index]['questions'][question_index]['correct_answer']

    if selected_answer == correct_answer:
        await query.message.reply_text("Правильно! 👍")
        await send_question(update, context, group_index, question_index + 1)
    else:
        await query.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
        await send_question(update, context, group_index, question_index)

def main():
    application = Application.builder().token(os.environ['BOT_TOKEN']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", "8443")),
        webhook_url=os.environ['WEBHOOK_URL'],
    )

if __name__ == '__main__':
    main()