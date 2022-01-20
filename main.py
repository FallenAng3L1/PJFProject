from agoda.agoda import Agoda
import agoda.datacsv as d_csv
import time as t
properties = ["Śniadanie", "winda"]
with Agoda() as bot:
    bot.land_first_page()
    bot.accept_popup()
    bot.select_place('Warszawa')
    bot.select_dates(check_in_date='Sat Mar 05 2022', check_out_date='Sat Mar 26 2022')
    bot.select_guests(3,2,4,2,[5,13])
    bot.search_click()
    while True:
        try:
            bot.scroll_down()
            bot.scroll_properties(properties)
            bot.report_results()

        except Exception:
            bot.scroll_down()
            bot.scroll_properties(properties)
            bot.report_results()

        try:
            bot.next_page()
            t.sleep(5)
        except Exception:
            d_csv.data_printer(properties)
            break
