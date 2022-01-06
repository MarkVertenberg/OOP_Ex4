# Ex4: The Pokemon game

# Introduction:
In this project we had to realize the "Pokemon game".

![image](https://user-images.githubusercontent.com/93255163/148103741-6767c48e-07fc-445c-8319-b2eeab5fbffc.png)

- # About the game:

* The game consists of 16 stages [0-15].
* At each stage a different number of Pokemon and agents.
* The main goal at each stage is to catch as many Pokemon as possible by the agents. When the game scene actually a strongly weighted (directed) graph.
* Every Pokemon has a "weight". The same "weight" is summed up after the capture of the Pokemon.
* The goal of the game is to accumulate the maximum number of points ("score") in the smallest number of steps and in the shortest time (each game has a fixed time - usually 30-120 seconds).
* At the end of each game we will get the score and the number of steps performed.

- # Motivation:
This project is a concluding assignment of the Object Oriented Programming (OOP) course. This is an opportunity to practically experience the material being studied, to design the general algorithm then to implement the version of a working algorithm, Work as a group on "Github" , to do tests (unitest), and of course do a graphical user interface (GUI) and experiment with "Pygame".

 * **Algorithm goals:** 
 
    - The algorithm should be as efficient as possible.
    - At each stage we need to consider the number of agents and the number of Pokemon to make a pre-planning of the moves we want to make.
    - It is important to consider not only the shortest distance of the agents from these Pokemon but also the "weight" of the Pokemon, so that in the shortest time we will gain a bigger score and make fewer moves.


 * **GUI goals:** 
 
    - The GUI should be clear.
    - Should be scalable with a resizable window.
    - Should show the overall points.
    - Should show the moves counter.
    - Should show the time to end in seconds.
    - Should have a “stop” button to gracefully stop the game at any time point.


# Algorithm:


# UML:

![Untitled Diagram drawio (6)](https://user-images.githubusercontent.com/93255163/148453646-cd74b33b-83e1-4ad5-8df7-b540a600bab4.png)


# Report results:
**The results can be seen in the attached WIKI file.**  
Link: https://github.com/MarkVertenberg/OOP_Ex4/wiki/Report-results


# How to play?
**Guidance and explanation can be found on the attached WIKI file.**    
Link: https://github.com/MarkVertenberg/OOP_Ex4/wiki/How-to-play%3F


# Helpful Links:

- OXFORD COLLEGE | Directed and Edge-Weighted Graphs: 
In this site you can find information about Directed and Edge-Weighted Graphs , and the best data structure for it.   
    Link: http://math.oxford.emory.edu/site/cs171/directedAndEdgeWeightedGraphs/

- Explanation of Dijkstra’s algorithm for finding the shortest path between one vertex in a graph and another.  
This video helped us to implement our Dijkstra class.     
    Link: https://www.youtube.com/watch?v=pVfj6mxhdMw

- Explanation on performing Depth–first search (DFS) to check if A directed graph is strongly connected.   
    Link: https://www.techiedelight.com/check-given-graph-strongly-connected-not/
    
- Dijkstra's Shortest Path Algorithm - A Detailed and Visual Introduction.   
  Link: https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/
   
# Credits:
1. Mark vertenberg.
2. Mishell dubovitski.
3. Alina zakhozha.
