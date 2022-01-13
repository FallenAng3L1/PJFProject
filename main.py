from agoda.agoda import Agoda

with Agoda() as bot:
    bot.land_first_page()
    bot.accept_popup()
    bot.select_place('Warszawa')
    bot.select_dates(check_in_date='Wed Jan 12 2022', check_out_date='Tue Feb 01 2022')
    bot.select_guests(3,2,4,2)
    bot.search_click()
    bot.scroll_down()
    bot.report_results()