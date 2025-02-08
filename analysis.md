# Forecast analysis of the domestic argentine commercial flight system

## Introduction

## Descriptive analysis
I have first of all started by visualizing the data, which is done in the vuelos_maps.py file.

We proceed to analyze the data.

We need to overcome the discrepancy between official number of passengers and the actual sum we are getting from the data. 
My first thought is to see whether the amount of flighs is not being taken into account, but it is not the case, since the amount of passengers grows with the amounts of flights per day.

So let's focus in one airport so it is pin point the possible flaws.
Cordoba airport seems to be OK.
I am having a look at all the figures and they now seem to be correct, this will surely pup back up at some point.

I think my mistake came from not realising that 1e7 means multiplied by 10 million, therefore i get the correct figures. My usual type of mistakes that make me waste many days.

## Analysis

I have decided to forecast the number of passangers from Córdoba, incoming and outgoing.
What could possibly go wrong? The range of the series is not complete. I complete it.

We can appreciate a estationary behaviour that persists during the covid pandemic, which is that during weekends demand decreases and the demand tends to increase during November and December.

Autocorrelation and partial autocorrelation


