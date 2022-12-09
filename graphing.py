import random
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import core.engine as engine
import core.variables as variables
import core.stats as statistiques


#Clé= nom de la stat , valeur en valeur
data = {'longueur minimum' : 5,
        'longueur maximum': 9,
        'longueur moyenne': 6.916666666666667}

tab2_layout = [
    [sg.Table(values=data.items(),
              headings=['Statistique', 'Valeur'],
              auto_size_columns=True,
              justification='center',
              alternating_row_color='green',
              num_rows=len(data)),
     ]
         ]
# show plot
windowtbl = sg.Window('Histogram and Table', tab2_layout)
while True:
    event, values = windowtbl.read()
    if event == sg.WIN_CLOSED:
        break
windowtbl.close()


stat2={'nb minuscules':  192,
       'nb majuscules':  1,
       'nb numeriques':  57,
       'nb symboles':  1}
explode=[0.1]
explode=explode*len(stat2)
#sample freq
stat3={}
for i in range(255):
    c=chr(i)
    stat3[c]=random.random()*50

# Create a figure and a subplot
fig = plt.figure()
gs = gridspec.GridSpec(nrows=2, ncols=2)

# Plot a table and two histograms

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])


# Create the table
ax1.table(cellText=[[key, value] for key, value in data.items()],
                 colLabels=['Measurement', 'Value'],
                 colWidths=[0.5, 0.5],
                 loc='center')
ax1.axis('off')
ax2.pie(stat2.values(),labels=stat2.keys(),autopct='%1.1f%%',shadow=True,explode=explode, startangle=90)
ax3.bar(stat3.keys(),stat3.values())
#titles
ax1.set_title('Métriques')
ax2.set_title('Répartition des caractères')
ax3.set_title('Frequence présence ASCII')
# Show the figure
fig.tight_layout()
plt.show()


fig.suptitle('Statistiques', fontsize=14, fontweight='bold')
fig.show()


