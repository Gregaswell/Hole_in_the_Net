# Hole_in_the_Net
Hello there!	

I am new to game development, it could possibly change. In any case I coded my first game without any engines (as you probably notice), in Python.



GAME DESCRIPTION
(also available on https://gregoryvs.itch.io/holeinthenet)

  You wake with a start hearing that disturbing buzz round your ears. You are trying to fall back asleep but that gnat doesn't let you do that. Then you get more and more angry, yes, there's a hole in your bug screen.
  
  Slap the brownish gnat (of course, clicking on it), only that one. Be careful, slapping aside you will attract other gnats' attention. Avoid contacting the drugged grey blood-suckers, otherwise they can bite you. (Touching the net reduces the time and your points as well.) The game may go on even if you can't slap that annoying gnat in time.

  :) Let's get a fine score! Trust me, you will rewarded at the final stage. (Yes, there is a final stage! It will end sometime.)

  Gnats can easily make me angry. Hah. This in itself seemed to be a good reason for making the game. I hope you'll enjoy it.
  Thanks @Haman for his icon (https://www.cleanpng.com/users/@haman.html).



PROJECT USEFULNESS

  This game is a few minutes' relaxing manner for all age-groups. But it possibly could serve the improvement of eye-hand coordination, concentration and fine motor skills.


DEV SPECIFICATIONS

  Game does not use any game engines at all. It is coded in Python 3.8 and consists of two files, the .py script and an .ico file. For .exe version you can check (https://gregoryvs.itch.io/holeinthenet), then download the .zip file. Game also creates a .py file (hs_holeinthenet.py) which will store the high-score data.
  Unfortunately some antivirus softwares (Avast, maybe AVG) could mark the .exe file as infected despite of the fact it is also provided with a digital signature. The reason could be its building method (I used pyinstaller).

  All the functions are in one file, that's why the code seems too long. Basically while the gnat which one must be flapped is flying, the code is generating for it a new target, every time it is arriving closely to the last target. There are two methods for the gnat to reach its target: moving straightly or drawing an arc. After generating a new target it is chosen how to move there (by .scale method).
  
  The easier way will be the straight one, determining a function according to the equation of a line.
  
  The arc-path will be created in a more complex way based on the equation of a circle. First the program defines the inclination of the beeline, then it knows which coordinate will be increased (x or y) to avoid unexpected jump and velocity. Next step is to choice the side of the arc's dilation (left or right). The basic principle is the figure of a circumscribed triangle. Variables center_x,center_y will be the coordinates of the central vertex between the arrival and departure vertices. We have to get the maximum dilation (max_distance, min_distance can be near 0), which can only be the distance between the central vertex and a bounding point (based on a circle's equation). According to the inclination max_distance can become smaller, therefore the distance between the line segment and the device-screen's edges must be measured. Finally the middle_distance gets a value in the above defined range.
  
  The equation of the circle's chord (as a line) can be determined reversing the method based on distance from a point to a line: (y2-y1)x+(x1-x2)y+y1(x2-x1)-x1(y2-y1)=0. A perpendicular bisector must go through the segment midpoint: A*x+B*y=A*x0+B*y0, from here the equation of the bisector can be determined: Ax+By-Ax0-By0=0. Based on the solving of the equations system the third vertex of the triangle can be defined now. There will be two solutions from which the proper one can be selected knowing the inclination and direction.
  
  Having the triangle an other perpendicular bisector most be determined. The solution of the equation-system defines the intersection of the lines, the center of the circle. The square of radius can be determined now, so at this time we have all the necessary variables to construct the function based on the circle's equation.
The 'drugged' gnats will move differently. There moving must be more predictable to make the game not too difficult to play. Program perceives when the gnats arrive to an edge of the device-screen. Then it makes a choice for the direction of the drugged gnats from three possibilities (with .move method).

Enjoy it!
