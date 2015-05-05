# results.py
from numpy import mean, median
import numpy as np
import pylab as P

from matplotlib import pyplot as plt
# Run 1
results = [93068.54664182669, 96956.21962247501, 115530.27792057063, 113677.60900095104, 128101.07503799514, 79400.80611624727, 126697.82934691012, 79148.76357812904, 113084.37800264961, 107214.21376622164, 115979.6952448421, 95779.17352352111, 109356.82231648799, 105304.45137359305, 107817.82386046402, 106527.42989206145, 97181.79527636612, 109396.36604207235, 111506.71048629403, 124469.89963156625, 89229.74373680087, 75761.946110991, 113961.30447468463, 93599.15118975367, 142499.54089023545,
           126461.86206707006, 97714.23302599201, 95545.33676026016, 102016.94375536258, 122417.54206125208, 160421.65462840427, 99601.4110299792, 93039.08935027078, 102487.97149382831, 119054.97183716623, 117060.95692869616, 94456.42406270606, 130466.89531286233, 111165.40074076841, 107833.08858488697, 97245.77159610798, 116610.53436281119, 133387.62182085885, 100062.36066022303, 90915.45912829235, 85439.20543542314, 115237.3920326482, 80155.55679129387, 109372.62381515963, 105322.94421768899]
firstyear = 2006
lastyear = 2010
num_stocks = 20
trials = 50
spfirst = 1268.80
splast = 1257.64
print 'RUN 1'
print min(results)
print max(results)
print median(results)
print mean(results)

print 'S&P 500 Return: %.2f%%' % (((splast - spfirst) / 100000) * 100)
print 'Average Return: %.2f%%' % (((mean(results) - 100000) / 100000) * 100)
print 'Max Return: %.2f%%' % (((max(results) - 100000) / 100000) * 100)
print 'Min Return: %.2f%%' % (((min(results) - 100000) / 100000) * 100)


plt.hist(results, bins=20)
plt.show()

# Run 1
results = [195854.99232056213, 162667.65951077835, 145297.282749024, 170348.74817332477, 146004.47361515183, 146979.73148131787, 133995.43485382985, 146793.55473451046, 144793.2081338067, 146691.2639578249, 142917.88084915275, 153243.83837070267, 139505.6245087778, 128680.04868658526, 167010.46039782924, 130249.50014056414, 134256.87638248102, 149206.96382018202, 133773.97704462495, 125191.36064008505, 136712.8631657153, 137604.1403769268, 158332.57709063505, 145259.57792818, 148432.38475453318,
           136557.75166235166, 163800.24724063673, 135591.94991682566, 163200.73810091158, 158935.2643360668, 169077.78682643897, 121004.43126835037, 210905.16581927732, 122482.2508041557, 189758.51061636565, 204745.0152773241, 134052.60648145236, 163821.22200533957, 179983.72202526184, 130569.33004092309, 161251.7030935801, 148753.97865572118, 154767.53525387758, 126868.61195400824, 144900.42660522021, 150181.4103094148, 138449.06166608178, 166875.70882066584, 115515.77881870847, 118443.92851657966]
firstyear = 2010
lastyear = 2015
num_stocks = 20
trials = 50
print 'RUN 2'
print min(results)
print max(results)
print median(results)
print mean(results)

spfirst = 1132.99
splast = 2106.85
print 'S&P 500 Return: %.2f%%' % (((splast - spfirst) / 100000) * 100)
print 'Average Return: %.2f%%' % (((mean(results) - 100000) / 100000) * 100)
print 'Max Return: %.2f%%' % (((max(results) - 100000) / 100000) * 100)
print 'Min Return: %.2f%%' % (((min(results) - 100000) / 100000) * 100)


plt.hist(results, bins=20)
plt.show()