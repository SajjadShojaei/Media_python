import os
import re
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler

# --- تنظیمات ربات ---
BOT_TOKEN = "8392578116:AAE0BSicKgZMWoyDpM2LkQZ0uZsbGyebsbg"  # توکن ربات رو اینجا بذارید

# وضعیت‌های گفتگو (اصلاح شده)
MENU, \
SINGLE_TITLE, SINGLE_SHORT_SUMMARY, SINGLE_IMAGE_URL, SINGLE_IMAGE_ALT, \
SINGLE_IMAGE_DESC, SINGLE_LONG_DESC, SINGLE_WARNING, SINGLE_EMPHASIS, \
SINGLE_VIDEO_URL, SINGLE_ADDITIONAL_LINKS, \
BULK_UPLOAD = range(12)

# قالب HTML یکپارچه (همون قبلی)
UNIFIED_TEMPLATE = """
<p style="text-align: center;"><span style="background-color: #800000; color: #ffffff;">&nbsp; {warning_text} &nbsp; <br /></span></p>
<p style="text-align: center;"><span style="color: #ff0000;"><strong>{emphasis_text}</strong></span></p>
<p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
<p style="text-align: center;"><span style="color: #000080;">
{image_description}
</span></p>
<hr id="system-readmore" />
<p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان:&nbsp;</strong></span>{short_summary}</p>
<p style="text-align: justify;">{long_description}</p>
<p>&nbsp;</p>
<p style="text-align: center;">{download_link}</p>
"""

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).replace(" ", "_")

def generate_html_file(data, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    title = data['title']
    filename = sanitize_filename(title) + ".html"
    filepath = os.path.join(output_dir, filename)

    download_link = '<img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" />'
    if data.get('video_url'):
        download_link = f'<a href="{data["video_url"]}"><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></a>'
    if data.get('additional_links'):
        download_link += f' &nbsp; &nbsp; &nbsp; {data["additional_links"]}'

    html = UNIFIED_TEMPLATE.format(
        warning_text=data.get('warning_text', ''),
        emphasis_text=data.get('emphasis_text', ''),
        image_url=data['image_url'],
        image_alt=data['image_alt'],
        image_description=data['image_description'],
        short_summary=data['short_summary'],
        long_description=data.get('long_description', ''),
        download_link=download_link
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return filepath

# --- منوی اصلی ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["ساخت خبر جدید", "ساخت انبوه از فایل Excel/CSV"],
        ["راهنما", "درباره ربات"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "سلام به ربات سازنده خبر سایت خوش آمدید!\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )
    return MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "ساخت خبر جدید":
        await update.message.reply_text("عنوان خبر را وارد کنید:\n(مثلاً: پلوریبوس – Pluribus)")
        return SINGLE_TITLE
    elif text == "ساخت انبوه از فایل Excel/CSV":
        await update.message.reply_text(
            "فایل Excel یا CSV را ارسال کنید.\n\n"
            "ستون‌های ضروری:\n"
            "• title\n"
            "• short_summary\n"
            "• image_url\n"
            "• image_alt\n"
            "• image_description\n\n"
            "ستون‌های اختیاری:\n"
            "• long_description\n"
            "• warning_text\n"
            "• emphasis_text\n"
            "• video_url\n"
            "• additional_links",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("نمونه فایل CSV", callback_data="sample_csv")]])
        )
        return BULK_UPLOAD
    elif text == "راهنما":
        await update.message.reply_text(
            "این ربات دقیقاً همان قالب سایت شما را تولید می‌کند.\n"
            "فقط اطلاعات را وارد کنید، فایل HTML آماده تحویل می‌گیرد!"
        )
    elif text == "درباره ربات":
        await update.message.reply_text("ربات سازنده خبر سایت\nنسخه 2.0 - آبان ۱۴۰۴\nتوسعه‌دهنده: شما")
    return MENU

# --- ساخت تک خبر ---
async def single_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("خلاصه داستان کوتاه (یک خط):")
    return SINGLE_SHORT_SUMMARY

async def single_short_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['short_summary'] = update.message.text
    await update.message.reply_text("آدرس تصویر پوستر:")
    return SINGLE_IMAGE_URL

async def single_image_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['image_url'] = update.message.text
    await update.message.reply_text("متن Alt تصویر (به انگلیسی):")
    return SINGLE_IMAGE_ALT

async def single_image_alt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['image_alt'] = update.message.text
    await update.message.reply_text("توضیحات زیر تصویر (خط آبی‌رنگ):")
    return SINGLE_IMAGE_DESC

async def single_image_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['image_description'] = update.message.text
    await update.message.reply_text("توضیحات طولانی (بازیگران، درباره اثر و ...) - اختیاری، برای رد کردن /skip بزنید:")
    return SINGLE_LONG_DESC

async def single_long_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/skip":
        context.user_data['long_description'] = ""
    else:
        context.user_data['long_description'] = text
    await update.message.reply_text("متن هشدار (مثل سریال ایرانی) - اختیاری، /skip برای رد:")
    return SINGLE_WARNING

async def single_warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/skip":
        context.user_data['warning_text'] = ""
    else:
        context.user_data['warning_text'] = text
    await update.message.reply_text("متن تاکیدی قرمز (مثل قسمت آخر اضافه شد) - اختیاری، /skip:")
    return SINGLE_EMPHASIS

async def single_emphasis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/skip":
        context.user_data['emphasis_text'] = ""
    else:
        context.user_data['emphasis_text'] = text
    await update.message.reply_text("لینک مستقیم فایل (اگر موجود است) - اختیاری، /skip:")
    return SINGLE_VIDEO_URL

async def single_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/skip":
        context.user_data['video_url'] = ""
    else:
        context.user_data['video_url'] = text
    await update.message.reply_text("لینک‌های اضافی (مثل خرید قانونی) - اختیاری، /skip:")
    return SINGLE_ADDITIONAL_LINKS

async def single_additional_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text != "/skip":
        context.user_data['additional_links'] = text

    # ساخت فایل
    file_path = generate_html_file(context.user_data)
    await update.message.reply_text("در حال ساخت فایل...")
    with open(file_path, 'rb') as f:
        await update.message.reply_document(f, caption=f"خبر «{context.user_data['title']}» با موفقیت ساخته شد!")
    
    await update.message.reply_text("خبر با موفقیت ساخته شد! می‌خوای یکی دیگه بسازی؟", reply_markup=ReplyKeyboardMarkup([["ساخت خبر جدید"], ["منوی اصلی"]], resize_keyboard=True))
    context.user_data.clear()
    return MENU

# --- ساخت انبوه ---
async def bulk_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("لطفاً یک فایل Excel یا CSV ارسال کنید.")
        return BULK_UPLOAD

    file = await update.message.document.get_file()
    file_path = f"temp_{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        await update.message.reply_text(f"فایل دریافت شد! {len(df)} خبر پیدا شد.\nدر حال ساخت فایل‌ها...")
        
        zip_path = "خبرهای_ساخته_شده.zip"
        import zipfile
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for _, row in df.iterrows():
                data = row.to_dict()
                data = {k: str(v) if pd.notna(v) else "" for k, v in data.items()}
                html_path = generate_html_file(data)
                zipf.write(html_path, os.path.basename(html_path))
        
        with open(zip_path, 'rb') as f:
            await update.message.reply_document(f, caption=f"همه {len(df)} خبر با موفقیت ساخته و زیپ شدند!")
        
        os.remove(file_path)
        os.remove(zip_path)
        for f in os.listdir("output"):
            os.remove(os.path.join("output", f))
        
    except Exception as e:
        await update.message.reply_text(f"خطا در پردازش فایل:\n{str(e)}")

    return MENU

async def sample_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sample = """title,short_summary,image_url,image_alt,image_description,long_description,warning_text,emphasis_text,video_url,additional_links
پلوریبوس – Pluribus,سریال پلوریبوس در البوکرکی...,images/52/Serial/EN/Pluribus-2025.jpg,Pluribus 2025,نام: پلوریبوس | ژانر: فانتزی...,توضیحات کامل بازیگران و...,,قسمت آخر اضافه شد,https://mediaftp...,<a href="https://shop..."><img ... /></a>"""
    await query.message.reply_text(f"نمونه CSV:\n\n`{sample}`\n\nاین رو کپی کن و در اکسل یا نوت‌پد ذخیره کن.", parse_mode='Markdown')

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            SINGLE_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_title)],
            SINGLE_SHORT_SUMMARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_short_summary)],
            SINGLE_IMAGE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_image_url)],
            SINGLE_IMAGE_ALT: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_image_alt)],
            SINGLE_IMAGE_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_image_desc)],
            SINGLE_LONG_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_long_desc)],
            SINGLE_WARNING: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_warning)],
            SINGLE_EMPHASIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_emphasis)],
            SINGLE_VIDEO_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_video_url)],
            SINGLE_ADDITIONAL_LINKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, single_additional_links)],
            BULK_UPLOAD: [MessageHandler(filters.Document.ALL, bulk_upload)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(sample_csv, pattern="sample_csv"))

    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()