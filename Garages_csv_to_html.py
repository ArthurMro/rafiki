
"""
Created on Fri May  8 14:18:41 2020

This document can be of help to support sales team. Often sales team manually put CSV in other format by hand.
Here their taks was to put a list of new garages on a parking website for cars. 
The website neede these garages to be entered in a customer HTML.
Instead of doing by hand, I offered my help to automate the task. Here is the code for it.


@author: arthur.moreau
"""



import pandas as pd
import numpy as np

#Importing the CSV files
data = pd.read_csv(r'C:\Users\list.csv', delimiter=';')
df = pd.DataFrame(data)

#Creating a "full Address column"
df['full_Address']='empty'
df['full_Address'] = df['Address'] +', '+ df['Zipcode'].map(str) +' '+ df['City']
df = df.drop(['Zipcode', 'City'], axis=1)
#Creating a column for the English tariff
df['tariff_en'] = "Opening Hours: Mon - Fri: " + df['Opening_hours_week'].map(str) + ' || Sat - Sun/holidays:' \
    + df['Opening_hours_weekend'].map(str) +'|| Price per hour: '+df['Price_per_hour'].map(str) \
    + '€  ||Max. fee per day: ' + df['Daily_price_cap'].map(str) + '€ '


#Creating a column for the German tariff
df['tariff_de'] = "Öffnungszeiten: Mo - Fr: " + df['Opening_hours_week'].map(str) + ' Uhr || Sa - So/Feiertage: ' \
        + df['Opening_hours_weekend'].map(str) +'|| Stunde: '+df['Price_per_hour'].map(str) \
        + '€ || Tageshöchstsatz: ' + df['Daily_price_cap'].map(str) + '€ ' 

df['tariff_de'].replace(to_replace="Closed", value="Geschlossen")

#Transformation in html
df['html'] = '<cp>\n\t<lat>'+ df['Lat'].map(str) +'</lat>\n\t<lon>'+ df['Long'].map(str) \
        +'</lon>\n\t<name>' + df['Carpark'] + '</name>\n\t<address>'+ df['full_Address'] \
        + '</address>\n\t<tariff>'+ df['tariff_de'] + '</tariff>\n\t<tariff_en>'+ \
        df['tariff_en'] + '</tariff_en>\n\t<tariff_de>'+df['tariff_de']+'</tariff_de>'

#Export, and you are done.
np.savetxt(r'C:\Users\arthur.moreau\Code\html_carparks_germany.txt', df['html'].values, fmt='%s')
print('done')
    
