import agoda.constants as const
import pandas as pd
def data_printer(properties):
    data = {'Hotel Name': const.hotel_names_all,
            'Price': const.hotel_prices_all,
            'Rating': const.hotel_rating_all}
    df = pd.DataFrame(data)
    for prop in range(len(properties)):
        df[f'{const.hotel_breakfast_all[prop][0]}'] = const.hotel_breakfast_all[prop][1:]
    df.to_csv('hotels.csv', index=False)