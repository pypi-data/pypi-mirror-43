# Pyewacket

Pyewacket is a lightweight drop-in replacement for the Python random module. 
Pyewacket is based on the RNG Storm Engine, configured for speed.

While Storm is a high quality engine, Pyewacket is not appropriate for cryptography of any kind. 
Pyewacket is meant for games, data science, A.I. and experimental programming, not security.


*Recommended Installation:* `$ pip install Pyewacket`


## Development Log
##### Pyewacket v0.0.1b2
- Basic Functionality
    - random()
    - uniform()
    - randbelow()
    - randint()
    - randrange()
    - choice()
    - choices()
    - shuffle()
    
##### Pyewacket v0.0.1b1
- Initial Design & Planning


## Pywacket Distribution and Performance Test Suite
```
Output Distribution: Random.random()
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 156ns
Raw Samples: 0.5344283340507532, 0.10364106503325066, 0.2130604609406146, 0.2677112766435301, 0.2390854401964766
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00020361509808208833
 Median: (0.49750478052375935, 0.4975582987602688)
 Maximum: 0.9998820855841124
 Mean: 0.499876867961783
 Std Deviation: 0.2898208283739117
Post-processor Distribution using <lambda> method:
 0: 10.1%
 1: 9.85%
 2: 10.09%
 3: 10.2%
 4: 9.98%
 5: 9.93%
 6: 9.6%
 7: 9.81%
 8: 10.31%
 9: 10.13%

Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 0.5158324288090468, 0.4180722617596217, 0.474422233562453, 0.20638082367997831, 0.21890875236294952
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.435690071859404e-05
 Median: (0.49397789564323163, 0.49400754850815315)
 Maximum: 0.9997703971676334
 Mean: 0.4981130757231045
 Std Deviation: 0.28920596803634385
Post-processor Distribution using <lambda> method:
 0: 10.05%
 1: 10.16%
 2: 10.17%
 3: 10.15%
 4: 9.92%
 5: 9.85%
 6: 9.94%
 7: 9.92%
 8: 9.81%
 9: 10.03%

Output Distribution: Random.uniform(0.0, 1.0)
Approximate Single Execution Time: Min: 281ns, Mid: 281ns, Max: 500ns
Raw Samples: 0.9049028390666327, 0.957389423567991, 0.22674586351187542, 0.1243812680992259, 0.7019126973190616
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00014223954175596187
 Median: (0.5059413378985098, 0.5059539301242587)
 Maximum: 0.9999327119550295
 Mean: 0.5063174763221022
 Std Deviation: 0.28914935710764633
Post-processor Distribution using <lambda> method:
 0: 9.58%
 1: 9.63%
 2: 9.99%
 3: 10.23%
 4: 10.05%
 5: 9.92%
 6: 9.87%
 7: 9.81%
 8: 10.42%
 9: 10.5%

Output Distribution: uniform(0.0, 1.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 0.4820354446596393, 0.8642457334986571, 0.2758470841813183, 0.41409995610868716, 0.9049164133507527
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 8.218968230960192e-06
 Median: (0.49908904289231376, 0.4991087069733439)
 Maximum: 0.9999565206623128
 Mean: 0.5000729661676843
 Std Deviation: 0.2886329361924544
Post-processor Distribution using <lambda> method:
 0: 9.74%
 1: 10.36%
 2: 10.0%
 3: 9.83%
 4: 10.2%
 5: 9.91%
 6: 9.81%
 7: 10.36%
 8: 9.69%
 9: 10.1%

Output Distribution: Random.randint(1, 10)
Approximate Single Execution Time: Min: 1468ns, Mid: 1562ns, Max: 3000ns
Raw Samples: 7, 4, 3, 8, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4206
 Std Deviation: 2.8531578454353164
Sample Distribution:
 1: 10.4%
 2: 10.05%
 3: 10.2%
 4: 10.12%
 5: 10.25%
 6: 10.51%
 7: 9.78%
 8: 9.86%
 9: 9.47%
 10: 9.36%

Output Distribution: randint(1, 10)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 1625ns
Raw Samples: 3, 2, 7, 4, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.4937
 Std Deviation: 2.8682020445388483
Sample Distribution:
 1: 10.1%
 2: 10.02%
 3: 9.88%
 4: 9.86%
 5: 9.95%
 6: 10.58%
 7: 9.5%
 8: 10.29%
 9: 10.1%
 10: 9.72%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 906ns, Mid: 968ns, Max: 1187ns
Raw Samples: 1, 8, 2, 2, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4829
 Std Deviation: 2.874566733160032
Sample Distribution:
 0: 10.01%
 1: 10.18%
 2: 10.1%
 3: 9.74%
 4: 10.49%
 5: 9.81%
 6: 10.23%
 7: 9.42%
 8: 9.82%
 9: 10.2%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 343ns
Raw Samples: 3, 0, 5, 3, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4809
 Std Deviation: 2.877509895086311
Sample Distribution:
 0: 10.1%
 1: 10.15%
 2: 10.15%
 3: 10.1%
 4: 9.57%
 5: 10.29%
 6: 9.9%
 7: 9.53%
 8: 10.39%
 9: 9.82%

Output Distribution: Random.randrange(1, 10, 2)
Approximate Single Execution Time: Min: 2000ns, Mid: 3109ns, Max: 9125ns
Raw Samples: 9, 5, 9, 3, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.9884
 Std Deviation: 2.801401475158907
Sample Distribution:
 1: 19.51%
 3: 20.43%
 5: 20.61%
 7: 20.03%
 9: 19.42%

Output Distribution: randrange(1, 10, 2)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 187ns
Raw Samples: 1, 9, 7, 9, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.0598
 Std Deviation: 2.8319650355532744
Sample Distribution:
 1: 19.61%
 3: 19.41%
 5: 19.91%
 7: 20.52%
 9: 20.55%

Timer only: py_random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 8375ns, Mid: 8577ns, Max: 10500ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 437ns, Mid: 468ns, Max: 500ns

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 3687ns, Mid: 3781ns, Max: 4343ns
Raw Samples: [1, 0, 3], [4, 6, 8], [9, 4, 6], [7, 1, 1], [0, 1, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0243
 Std Deviation: 2.4522868676172673
Sample Distribution:
 0: 18.08%
 1: 16.07%
 2: 14.01%
 3: 13.02%
 4: 11.48%
 5: 9.35%
 6: 6.8%
 7: 5.67%
 8: 3.56%
 9: 1.96%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 2375ns, Mid: 4781ns, Max: 7593ns
Raw Samples: [7, 2, 1], [0, 0, 6], [4, 2, 0], [4, 5, 3], [1, 8, 1]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9865
 Std Deviation: 2.4566076695565804
Sample Distribution:
 0: 18.51%
 1: 16.5%
 2: 14.21%
 3: 12.77%
 4: 11.17%
 5: 8.65%
 6: 7.31%
 7: 5.3%
 8: 3.69%
 9: 1.89%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 3125ns, Mid: 3312ns, Max: 5250ns
Raw Samples: [9, 3, 0], [0, 3, 2], [7, 0, 6], [2, 1, 3], [0, 7, 1]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0015
 Std Deviation: 2.4557485254158267
Sample Distribution:
 0: 18.05%
 1: 16.6%
 2: 14.74%
 3: 12.37%
 4: 10.97%
 5: 8.87%
 6: 7.61%
 7: 5.24%
 8: 3.56%
 9: 1.99%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 1750ns, Mid: 1843ns, Max: 5062ns
Raw Samples: [1, 0, 3], [2, 4, 0], [4, 1, 6], [0, 4, 0], [7, 0, 2]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0147
 Std Deviation: 2.461928110039345
Sample Distribution:
 0: 18.26%
 1: 16.64%
 2: 13.68%
 3: 13.0%
 4: 10.7%
 5: 9.0%
 6: 7.61%
 7: 5.56%
 8: 3.86%
 9: 1.69%


```
