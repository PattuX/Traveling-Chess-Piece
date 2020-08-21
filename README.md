# Traveling-Chess-Piece

Idea based on Neil Sloane's "Trapped Knight" (https://oeis.org/A316667)

Implementation based on scipython blog: https://scipython.com/blog/the-trapped-knight/

General rules:

* Start with a spiraled, labeled square tiling, like this:

      17--16--15--14--13   .

       |               |   .

      18   5---4---3  12   .

       |   |       |   |   .

      19   6   1---2  11   .

       |   |           |   .

      20   7---8---9--10   .

       |                   .

      21--22--23--24--25--26
      
* define a movement of a piece moving along the board

* move the piece according to the rules such that it always picks the lowest square it can reach but has not visited yet

The initial Trapped Knight of course used a Knight's movement. This script leaves a possibility to extend this to any kind of piece. Add your own pieces in the ```get_moves(iy, ix)``` function by returning all possible (relative) moves given that the piece is on field ```(ix, iy)```.

The pre-implemented pieces ```ROOK```, ```BISHOP``` and ```QUEEN``` can move like the corresponding chess pieces, but the size of their move *must* be equal to the number of digits of the field it is on, plus one. E.g., a Rook on field 77 has to move exactly 3 squares, either up, down, left, or right.
