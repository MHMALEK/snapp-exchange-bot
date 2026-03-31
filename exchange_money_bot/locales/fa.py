"""Persian (fa) UI strings — edit here or add locales/en.py later."""

STRINGS: dict[str, str] = {
    # Currency labels (used by sell_offers.currency_label_fa)
    "currency.EUR": "یورو",
    "currency.USD": "دلار",
    # Main menu & navigation
    "keyboard.back_main": "بازگشت به منوی اصلی",
    "keyboard.menu_rial": "ریال دارم",
    "keyboard.menu_fx": "ارز دارم",
    "keyboard.menu_list_ads": "مشاهده لیست آگهی ها",
    "keyboard.menu_my_offers": "مدیریت آگهی‌های من (حذف)",
    "keyboard.menu_delete_account": "حذف اکانت",
    # Membership & channel
    "membership.required_html": (
        "<b>عضویت در کانال الزامی است</b>\n\n"
        "برای استفاده از این ربات باید ابتدا عضو کانال شوید. "
        "بعد از عضویت، دوباره /start را بزنید."
    ),
    "membership.sell_gate_html": (
        "<b>عضویت در کانال الزامی است</b>\n\n"
        "برای ثبت آگهی فروش باید ابتدا عضو کانال شوید. سپس دوباره از منو اقدام کنید."
    ),
    "channel.btn_join": "ورود به کانال",
    "channel.btn_open": "مشاهدهٔ کانال",
    "listings.cta_html": (
        "<b>لیست فروشندگان ارز</b>\n\n"
        "آگهی‌های فعال در <b>کانال</b> منتشر می‌شوند. "
        "برای دیدن فروشندگان و زدن دکمهٔ تماس، کانال را باز کنید."
    ),
    "listings.cta_rial_html": (
        "<b>ریال دارم — خرید ارز</b>\n\n"
        "لیست فروشندگان و مبالغ در <b>کانال</b> است. "
        "کانال را باز کنید؛ روی آگهی مورد نظر دکمهٔ «تماس» را بزنید."
    ),
    "listings.channel_link_label": "باز کردن کانال",
    "listings.cta_configure_invite_hint_html": (
        "<i>لینک کانال هنوز برای دکمه تنظیم نشده. "
        "مدیر می‌تواند TELEGRAM_CHANNEL_INVITE_URL را بگذارد یا در TELEGRAM_LISTINGS_CHANNEL_ID از @نام_عمومی کانال استفاده کند.</i>"
    ),
    # Channel listing post (HTML; dynamic parts are escaped before format)
    # Hashtags: currency (#EUR/#USD) + side (#فروش). Plain text for channel search.
    "listing.header_html": "💱 <b>آگهی فروش ارز</b>",
    "listing.amount_line": "💰 مبلغ: <b>{amount}</b> {ccy_fa} ({currency})",
    "listing.seller_line": "👤 فروشنده: {name}",
    "listing.telegram_line": "📱 تلگرام: {telegram_line}",
    "listing.tags_template": "🏷 #{currency} #فروش",
    "listing.no_username": "بدون نام کاربری — از دکمهٔ تماس استفاده کنید",
    "listing.closed_note": "<i>این آگهی برداشته شد.</i>",
    "listing.contact_btn": "تماس — {amount} {ccy_fa}",
    # Home & consent
    "home.registered": (
        "خوش برگشتی!\n"
        "آگهی‌های قبلی را از «آگهی‌های من» ببینید یا حذف کنید؛ "
        "برای حذف کل حساب از «حذف داده‌های من» یا /delete استفاده کنید.\n\n"
        "یکی از گزینه‌ها را انتخاب کنید:"
    ),
    "consent.body_html": (
        "برای استفاده از این ربات، آیا مایلید ثبت‌نام کنید؟\n\n"
        "در صورت موافقت، <b>نام نمایشی</b> و حداقل اطلاعات لازم از حساب تلگرام شما "
        "فقط برای شناسایی حساب در همین سرویس ذخیره می‌شود. "
        "این اطلاعات در پیام‌های ربات به شما یا سایر کاربران نمایش داده نخواهد شد.\n\n"
        "این پروژه <b>رایگان</b> و <b>متن‌باز</b> است و صرفاً برای "
        "تسهیل ارتباط و تبادل بین کاربران طراحی شده است. "
        "اطلاعات شما برای تبلیغات، فروش یا استفادهٔ تجاری به کار نمی‌رود.\n\n"
        "همچنین این ربات فقط یک واسط بین کاربران است و هیچ مسئولیتی در قبال قیمت‌ها، "
        "انجام معامله، صحت اطلاعات کاربران، اعتبار طرفین، وریفای یا هرگونه ضمانت و خسارت احتمالی "
        "نمی‌پذیرد. مسئولیت بررسی نهایی و انجام امن هرگونه تبادل بر عهدهٔ خود کاربران است.\n\n"
        "آیا با ثبت‌نام موافقید؟"
    ),
    "consent.btn_yes": "بله، ثبت‌نام می‌کنم",
    "consent.btn_no": "خیر",
    "consent.declined": "اشکالی ندارد. اگر بعداً نظرتان عوض شد، دوباره /start بزنید.",
    "signup.success": (
        "ثبت‌نام شما با موفقیت انجام شد.\n"
        "آگهی‌ها را از «آگهی‌های من» مدیریت کنید؛ برای حذف کل حساب «حذف داده‌های من» یا /delete.\n\n"
        "حالا یکی از گزینه‌های زیر را انتخاب کنید:"
    ),
    # Errors & prompts
    "error.register_first": "برای استفاده از این گزینه‌ها ابتدا با /start ثبت‌نام کنید.",
    "error.register_first_short": "ابتدا با /start ثبت‌نام کنید.",
    "error.join_channel_first": "ابتدا عضو کانال شوید.",
    "error.register_alert": "ابتدا ثبت‌نام کنید.",
    "error.offer_not_yours": "این آگهی مال شما نیست یا قبلاً حذف شده.",
    "error.offer_save": "ذخیره نشد. دوباره تلاش کنید.",
    "error.data_lost": "خطا در داده‌ها. دوباره از منو شروع کنید.",
    "error.amount_lost": "خطا: مبلغ ذخیره نشد. دوباره از منو «فروش» را بزنید.",
    "error.user_not_found": "کاربر یافت نشد. /start را بزنید.",
    "success.offer_deleted": "آگهی حذف شد.",
    # Account delete
    "account.delete_confirm": "همهٔ اطلاعات ذخیره‌شدهٔ شما در این ربات حذف می‌شود. مطمئن هستید؟",
    "account.delete_btn_yes": "بله، حذف شود",
    "account.delete_btn_cancel": "انصراف",
    "account.delete_cancelled": "حذف انجام نشد.\n\nیکی از گزینه‌ها را انتخاب کنید:",
    "account.deleted": "اطلاعات شما حذف شد. اگر بخواهید دوباره از ربات استفاده کنید، /start بزنید.",
    "account.deleted_short": "اطلاعات شما حذف شد.",
    "account.nothing_stored": "اطلاعاتی از شما ذخیره نشده بود.",
    "account.delete_all_btn": "حذف کامل اطلاعات من از ربات",
    "account.delete_footer": "برای حذف کل حساب و همهٔ آگهی‌ها از دکمهٔ پایین استفاده کنید.",
    # My offers UI
    "offers.title_html": "<b>آگهی‌های فروش من</b>",
    "offers.empty": "هنوز آگهی فعالی ثبت نکرده‌اید.",
    "offers.line_html": "{i}) مبلغ <b>{amount}</b> {ccy} — ثبت: {dt}",
    "offers.delete_btn": "حذف — {amount} {ccy}",
    # Sell flow
    "sell.register_first": "برای فروش ارز ابتدا با /start ثبت‌نام کنید.",
    "sell.amount_prompt": (
        "مبلغی را که می‌خواهید بفروشید وارد کنید.\n\n"
        "فقط با اعداد انگلیسی (0 تا 9)، بدون فاصله، ویرگول یا نقطه.\n"
        "مثال: 100 یا 1000 یا 150\n\n"
        "برای لغو این فرم: /cancel"
    ),
    "sell.amount_invalid": (
        "عدد نامعتبر است. فقط ارقام انگلیسی 0-9، بدون فاصله و بدون نقطه. دوباره بفرستید."
    ),
    "sell.pick_currency": "ارز را انتخاب کنید:",
    "sell.currency_reminder": "لطفاً با یکی از دکمه‌ها، ارز را انتخاب کنید.",
    "sell.btn_eur": "یورو (EUR)",
    "sell.btn_usd": "دلار (USD)",
    "sell.summary": (
        "خلاصهٔ آگهی فروش:\n\n"
        "مبلغ: {amount}\n"
        "ارز: {currency_label}\n"
        "نام نمایشی: {display_name}\n"
        "یوزرنیم تلگرام: {uname}\n\n"
        "اگر درست است «تایید و ثبت» را بزنید؛ وگرنه «انصراف»."
    ),
    "sell.display_fallback": "—",
    "sell.username_none": "ندارد",
    "sell.confirm_reminder": "لطفاً با دکمهٔ «تایید و ثبت» یا «انصراف» پاسخ دهید.",
    "sell.btn_submit": "تایید و ثبت",
    "sell.btn_abort": "انصراف",
    "sell.aborted": "ثبت آگهی لغو شد.\nیکی از گزینه‌های منو را انتخاب کنید:",
    "sell.cancelled_cmd": "فرم فروش لغو شد. از منوی زیر ادامه دهید:",
    "sell.success_intro": "ثبت شما انجام شد.\nمبلغ {amount} {currency_label}.\n{channel_note}",
    "sell.success_channel_on_html": (
        "آگهی شما در <b>کانال</b> هم منتشر شد؛ خریداران از آنجا می‌توانند با شما تماس بگیرند."
    ),
    "sell.success_channel_off": "در صورت فعال‌بودن کانال توسط مدیر، آگهی در کانال هم نمایش داده می‌شود.",
}
