# Install

* requires python 3.x
* for better performances use python 3.11+

```
pip install -r requirements.txt
```
# Download the sample passwords database : 

La base rockyou.txt est téléchargeable à l'aide du lien suivant : [rockyou.txt](https://drive.proton.me/urls/9Z15W7J2T4#Ok8g4totrkfM)

# Use : 

## Use the GUI :

`python mainGUI.py`

## Use the program in console mode : 

`python main.py -h`

```
python main.py -h
usage: main.py [-h] [--sample SAMPLE] [--cores CORES] [--strategy {lines,block,multiprocess}] [--paquet PAQUET]
               [--stats STATS [STATS ...]]

Compute statistics on passwords text database.

options:
  -h, --help            show this help message and exit
  --sample SAMPLE       file name
  --cores CORES         number of cores to use (multiprocessing only)
  --strategy {lines,block,multiprocess}
  --paquet PAQUET       read block or lines at once
  --stats STATS [STATS ...]
                        specify stats to compute : length, frequency, characters

```




