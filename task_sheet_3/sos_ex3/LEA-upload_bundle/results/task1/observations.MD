First Run Part.c , generate the output then run part1.py 

Task 1 (Part a):
- It looks like after seeing the graph that the system is non linear as well as unstable, but the formation of sawtoot periodically make it look like a function with discounties (like with jumps). kind of an unstable oscillation, 
- interstingly as i increased the num of points i found its like a sinosodial behaviour , and at 50000 points it perfectly sure its a sine wave generator 
Task 1 (Part b):
- The Graph looks like a tent map, inspired from Logistic Map, where it tells us how chotic behvaiour can arise from very simple non-linear dynamic system. The file genertead as csv from blackbox b is done with the help of LLM as i was not aware about how it could be done. 
- As discussed in Evolutionary Robotics, there is a term used attractors in Cobweb plots:chotic Map, it does the same behaviour the printing only starts after large number of Steps(100 Steps), that is commonly used to skip the transient behaviour of the system once its settled or in its steady state (or attractor). The conclusion could be Undersatnding of a system for long term behaviour when inputing largen number of Values.
-So out of curosity, i made a seperate file to test the cobweb.py and i found that is really a choatic Map 
