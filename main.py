import logging
from bd import create_table

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from states import MAINMENU, KNB, BNC, CNZ
from bulls_and_cows import start_bnc, bnc_game
from cross_abd_zeroes import start_cnz, cnz_game 
from kmn_nshnc_bmg import start_knb, knb_game
from start import start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
) #остается 


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("7940846926:AAGBjqcxvR2xlEzINHTduFGmVJv98wvY3vE")
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("knb", start_knb),
                CommandHandler("bnc", start_bnc),
                CommandHandler("cnz", start_cnz)
            ],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb_game)],
            BNC: [MessageHandler(filters.TEXT & ~filters.COMMAND, bnc_game)],
            CNZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, cnz_game)]

        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    create_table()
    

    application.run_polling()

# Ничьи 
# По файлам все
# клавиатура nfjdsnfj
