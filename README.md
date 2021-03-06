# Game of Life by petya0927
Simple Game of Life simulation in Pyhton 3., based on the work of John Horton Conway. It is a cellular automaton, means each cell on the screen is generated by the state of other cells. We can create a lot of generated structures. More on [Conway's Game of Life - Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## User manual

Dependencies:
- Python ^3. If you don't have it installed, you can download and install it from https://www.python.org/
- Pygame ^2. Follow the instructions Pygame's GitHub page: https://github.com/pygame/pygame

Once you installed everything and started the game_of_life.pyw script, you can place squares in the grid where every black cell is alive, every white cell is dead. By hitting the ```space``` key, you can start the simulation, where every frame is generated based on the rules below. You can restart the game and the simulation by hitting the ```r``` key any time. 

### Rules:
1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

### Basic keybindings:

- ```space``` : switch mode between Editing and Playing. Default is Editing.
- ```r``` : delete every alive cell, and restart the game.
- ```m``` : show more cells on the screen
- ```l``` : show less cells on the screen
- ```g``` : toggle grid display 

## Versions:
- v1: Computes the next step by iterating through the cells and check if the cell is alive or dead. With that information, creates a new matrix based on the rules of the game. Problems: iterating through the array for each frame takes a *long* time; stores the cells in an array (that could be *really* large); the new step computation is not smart (means for every generation it checks *all* the alive and dead cells).

- v2: Faster than v1. Computes the next step by filtering the alive cells and iterates through them. Checks the alive cells and their neighbours. (The logic behind is that every dead cell becomes only if there're enough alive cells around, so we don't need to check cells that are not surrounded by a living cell.) Problems: it still stores the cells in an array and not only the alive cells; 

- v3: It stores only the alive cells and directly render those on the specific coordinates. It uses the same algorythm as the v2 for every alive cell, but the simulation has no borders, because we do not use a specificly shaped array, but create the coordinates of the next living cells from the prevoius ones. Unfortunately, as the simulation goes on, it becames slower. Problems: sometimes it checks a dead cell multiple times.
