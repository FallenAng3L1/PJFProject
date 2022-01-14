import agoda.constants as const
import pandas as pd
def data_printer():
    data = {'Hotel Name': const.hotel_names_all,
            'Price': const.hotel_prices_all,
            'Rating': const.hotel_rating_all}
    df = pd.DataFrame(data)
    df.to_csv('hotels.csv', index=False)