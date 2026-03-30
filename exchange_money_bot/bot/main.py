import logging
import re
from typing import Optional

import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from exchange_money_bot.bot.keyboards import (
    MENU_MAIN_CALLBACK,
    main_menu_keyboard,
    with_back_to_main,
)
from exchange_money_bot.bot.sell_flow import build_sell_conversation_handler
from exchange_money_bot.config import settings
from exchange_money_bot.database import async_session_factory, init_db
from exchange_money_bot.services import sell_offers as sell_offers_service
from exchange_money_bot.services import users as user_service

logger = logging.getLogger(__name__)


async def _edit_or_reply(
    message,
    text: str,
    *,
    reply_markup=None,
    parse_mode: Optional[str] = None,
) -> None:
    """Edit the message that carried the callback; fall back to a new reply if edit fails."""
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
    except Exception:
        await message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )


REGISTERED_HOME_TEXT = (
    "خوش برگشتی!\n"
    "آگهی‌های قبلی را از «آگهی‌های من» ببینید یا حذف کنید؛ "
    "برای حذف کل حساب از «حذف داده‌های من» یا /delete استفاده کنید.\n\n"
    "یکی از گزینه‌ها را انتخاب کنید:"
)

CONSENT_TEXT = (
    "برای استفاده از این ربات، آیا مایلید ثبت‌نام کنید؟\n\n"
    "اگر بپذیرید، <b>نام نمایشی</b> و حداقل اطلاعات لازم از حساب تلگرام شما "
    "(برای تمایز حساب در همین سرویس) ذخیره می‌شود؛ این اعداد و مشخصه‌ها در پیام‌های ربات به شما یا دیگران نشان داده نمی‌شود.\n\n"
    "این پروژه <b>رایگان</b> و <b>متن‌باز</b> است و صرفاً برای "
    "<b>تسهیل تبادل ارز بین کاربران</b> طراحی شده است؛ "
    "<b>کاربرد تجاری ندارد</b> و اطلاعات شما برای فروش تبلیغات یا استفادهٔ تجاری "
    "استفاده نمی‌شود.\n\n"
    "آیا موافقید ثبت‌نام شوید؟"
)


def consent_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "بله، ثبت‌نام می‌کنم",
                    callback_data="consent:yes",
                ),
            ],
            [
                InlineKeyboardButton(
                    "خیر",
                    callback_data="consent:no",
                ),
            ],
        ]
    )


def delete_confirm_keyboard() -> InlineKeyboardMarkup:
    return with_back_to_main(
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "بله، حذف شود",
                        callback_data="account:delete_yes",
                    ),
                    InlineKeyboardButton(
                        "انصراف",
                        callback_data="account:delete_no",
                    ),
                ],
            ]
        )
    )


async def apply_home_screen(query) -> None:
    """همان منوی اثرِ /start برای کاربر ثبت‌نام‌شده یا صفحهٔ رضایت برای مهمان."""
    if query.message is None or query.from_user is None:
        return
    tid = query.from_user.id
    async with async_session_factory() as session:
        db_user = await user_service.get_user_by_telegram(session, tid)
    if db_user is not None:
        await _edit_or_reply(
            query.message,
            REGISTERED_HOME_TEXT,
            reply_markup=main_menu_keyboard(),
        )
    else:
        await _edit_or_reply(
            query.message,
            CONSENT_TEXT,
            reply_markup=consent_keyboard(),
            parse_mode="HTML",
        )


async def menu_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.message is None or query.from_user is None:
        return
    await query.answer()
    await apply_home_screen(query)


async def delete_user_data(telegram_id: int) -> bool:
    async with async_session_factory() as session:
        return await user_service.delete_user_by_telegram(session, telegram_id)


async def build_my_offers_ui(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    async with async_session_factory() as session:
        offers = await sell_offers_service.list_offers_for_user(session, user_id)
    lines = ["<b>آگهی‌های فروش من</b>", ""]
    rows: list[list[InlineKeyboardButton]] = []
    if not offers:
        lines.append("هنوز آگهی فعالی ثبت نکرده‌اید.")
    else:
        for i, o in enumerate(offers, start=1):
            ccy = sell_offers_service.currency_label_fa(o.currency)
            dt = o.created_at.strftime("%Y-%m-%d %H:%M") if o.created_at is not None else "—"
            lines.append(f"{i}) مبلغ <b>{o.amount}</b> {ccy} — ثبت: {dt}")
            rows.append(
                [
                    InlineKeyboardButton(
                        f"حذف — {o.amount} {ccy}",
                        callback_data=f"offer:del:{o.id}",
                    )
                ]
            )
    lines.extend(
        [
            "",
            "برای حذف کل حساب و همهٔ آگهی‌ها از دکمهٔ پایین استفاده کنید.",
        ]
    )
    rows.append(
        [
            InlineKeyboardButton(
                "حذف کامل اطلاعات من از ربات",
                callback_data="account:delete",
            )
        ]
    )
    return "\n".join(lines), with_back_to_main(InlineKeyboardMarkup(rows))


async def account_manage_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.message is None or query.from_user is None:
        return
    await query.answer()
    tid = query.from_user.id
    async with async_session_factory() as session:
        db_user = await user_service.get_user_by_telegram(session, tid)
    if db_user is None:
        await _edit_or_reply(
            query.message,
            "ابتدا با /start ثبت‌نام کنید.",
            reply_markup=with_back_to_main(InlineKeyboardMarkup([])),
        )
        return
    text, keyboard = await build_my_offers_ui(db_user.id)
    await _edit_or_reply(
        query.message,
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def offer_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.message is None or query.data is None or query.from_user is None:
        return
    m = re.fullmatch(r"offer:del:(\d+)", query.data)
    if not m:
        return
    offer_id = int(m.group(1))
    tid = query.from_user.id
    async with async_session_factory() as session:
        db_user = await user_service.get_user_by_telegram(session, tid)
        if db_user is None:
            await query.answer("ابتدا ثبت‌نام کنید.", show_alert=True)
            return
        deleted = await sell_offers_service.delete_offer_owned(session, offer_id, db_user.id)
        if not deleted:
            await query.answer("این آگهی مال شما نیست یا قبلاً حذف شده.", show_alert=True)
            return
    await query.answer("آگهی حذف شد.")
    text, keyboard = await build_my_offers_ui(db_user.id)
    await _edit_or_reply(
        query.message,
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def notify_api_after_upsert(telegram_id: int) -> None:
    if not settings.api_base_url:
        return
    url = f"{settings.api_base_url.rstrip('/')}/users/by-telegram/{telegram_id}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.get(url)
    except Exception:
        logger.exception("Optional API ping after /start failed")


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.message is None:
        return
    u = update.effective_user
    async with async_session_factory() as session:
        existing = await user_service.get_user_by_telegram(session, u.id)

    if existing is not None:
        await update.message.reply_text(
            REGISTERED_HOME_TEXT,
            reply_markup=main_menu_keyboard(),
        )
        return

    await update.message.reply_text(
        CONSENT_TEXT,
        reply_markup=consent_keyboard(),
        parse_mode="HTML",
    )


async def consent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.data is None or query.message is None:
        return
    if query.from_user is None:
        return

    await query.answer()

    if query.data == "consent:no":
        await _edit_or_reply(
            query.message,
            "اشکالی ندارد. اگر بعداً نظرتان عوض شد، دوباره /start بزنید.",
            reply_markup=with_back_to_main(InlineKeyboardMarkup([])),
        )
        return

    if query.data != "consent:yes":
        return

    u = query.from_user
    async with async_session_factory() as session:
        await user_service.upsert_user(
            session,
            telegram_id=u.id,
            username=u.username,
            first_name=u.first_name,
        )
    await notify_api_after_upsert(u.id)
    text = (
        "ثبت‌نام شما با موفقیت انجام شد.\n"
        "آگهی‌ها را از «آگهی‌های من» مدیریت کنید؛ برای حذف کل حساب «حذف داده‌های من» یا /delete.\n\n"
        "حالا یکی از گزینه‌های زیر را انتخاب کنید:"
    )
    await _edit_or_reply(query.message, text, reply_markup=main_menu_keyboard())


async def start_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.data is None or query.message is None or query.from_user is None:
        return
    await query.answer()
    async with async_session_factory() as session:
        registered = await user_service.get_user_by_telegram(session, query.from_user.id)
    if registered is None:
        await _edit_or_reply(
            query.message,
            "برای استفاده از این گزینه‌ها ابتدا با /start ثبت‌نام کنید.",
            reply_markup=with_back_to_main(InlineKeyboardMarkup([])),
        )
        return
    if query.data == "start:2":
        await _edit_or_reply(
            query.message,
            settings.start_button_2_reply,
            reply_markup=main_menu_keyboard(),
        )
    else:
        return


async def account_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.data is None or query.message is None or query.from_user is None:
        return

    if query.data == "account:delete":
        await query.answer()
        await _edit_or_reply(
            query.message,
            "همهٔ اطلاعات ذخیره‌شدهٔ شما در این ربات حذف می‌شود. مطمئن هستید؟",
            reply_markup=delete_confirm_keyboard(),
        )
        return

    await query.answer()

    if query.data == "account:delete_no":
        await _edit_or_reply(
            query.message,
            "حذف انجام نشد.\n\nیکی از گزینه‌ها را انتخاب کنید:",
            reply_markup=main_menu_keyboard(),
        )
        return

    if query.data != "account:delete_yes":
        return

    tid = query.from_user.id
    ok = await delete_user_data(tid)
    back_only = with_back_to_main(InlineKeyboardMarkup([]))
    if ok:
        await _edit_or_reply(
            query.message,
            "اطلاعات شما حذف شد. اگر بخواهید دوباره از ربات استفاده کنید، /start بزنید.",
            reply_markup=back_only,
        )
    else:
        await _edit_or_reply(
            query.message,
            "اطلاعاتی از شما ذخیره نشده بود.",
            reply_markup=back_only,
        )


async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.message is None:
        return
    tid = update.effective_user.id
    ok = await delete_user_data(tid)
    if ok:
        await update.message.reply_text("اطلاعات شما حذف شد.")
    else:
        await update.message.reply_text("اطلاعاتی از شما ذخیره نشده بود.")


async def on_post_init(application: Application) -> None:
    await init_db()


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    if not settings.telegram_bot_token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set (see .env.example)")

    application = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .post_init(on_post_init)
        .build()
    )
    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("delete", delete_cmd))
    application.add_handler(CallbackQueryHandler(consent_callback, pattern=r"^consent:(yes|no)$"))
    application.add_handler(CallbackQueryHandler(account_manage_callback, pattern=r"^account:manage$"))
    application.add_handler(CallbackQueryHandler(offer_delete_callback, pattern=r"^offer:del:\d+$"))
    application.add_handler(
        CallbackQueryHandler(
            account_delete_callback,
            pattern=r"^account:(delete|delete_yes|delete_no)$",
        )
    )
    application.add_handler(build_sell_conversation_handler())
    application.add_handler(
        CallbackQueryHandler(menu_main_callback, pattern=rf"^{MENU_MAIN_CALLBACK}$")
    )
    application.add_handler(CallbackQueryHandler(start_menu_callback, pattern=r"^start:2$"))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
