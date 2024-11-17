import logging
from bd import create_table

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from states import MAINMENU, KNB, BNC, CNZ, RATE
from bulls_and_cows import start_bnc, bnc_game
from cross_abd_zeroes import start_cnz, cnz_game
from kmn_nshnc_bmg import start_knb, knb_game
from start import start, rate, rate_answer

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)  # остается


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    flag = 0 #Колхоз && костыль || База && единорог-мув

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("knb", start_knb),
                CommandHandler("bnc", start_bnc),
                CommandHandler("cnz", start_cnz),
                CommandHandler("rate", rate),
            ],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb_game)],
            BNC: [MessageHandler(filters.TEXT & ~filters.COMMAND, bnc_game)],
            CNZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, cnz_game)],
            RATE: [CallbackQueryHandler(rate_answer)]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    create_table()

    application.run_polling()    
