from pipe import Pipe
import config

class PipeList():
    """
    Control a list of pipe objects and detect collisions with a
    bird object.
    """

    def __init__(self) -> None:
        """
        Initiate a pipe list with a single pipe
        """
        self.l = [Pipe()]


    def update(self):
        """
        update pipe positions, add new pipes when a pipe is at
        half scrteen and remove a pipe the has gone off-screen

        :returns: x and y positions of the first two pipes
        """
        for i in range(len(self.l)-1, -1, -1):
            # Remove pip if it is off screen
            if self.l[i].x <= 0 - config.PIPE_WIDTH:
                self.l.pop(i)
            # Add a pipe if one is halfway
            if (self.l[i].x <= config.WIDTH / 4 and
                self.l[i].x >= (config.WIDTH /4) - (config.PIPE_SPEED / 2)):
                self.l.append(Pipe())
            self.l[i].update()
        return(self.l[0].x, self.l[0].y_top, self.l[0].y_bottom)


    def draw(self, screen) -> None:
        """
        Draw all pipes to the screen.

        :param screen: pygame screen object
        """
        for p in self.l:
            p.draw(screen)


    def check_collision(self, bird) -> bool:
        """
        Detect collision with bird objects for all pipes in
        the pipelist

        :param bird: class Bird
        :returns: boolean
        """
        for p in self.l:
            # Collision detection:
            # Check for x_collision
            x_col = (p.x + config.PIPE_WIDTH >=
                     bird.x + config.CIRCLE_RADIUS >= p.x)
            # Check for collision with both pipes
            y_col_1 = bird.y + config.CIRCLE_RADIUS >= p.y_bottom
            y_col_2 = bird.y - config.CIRCLE_RADIUS <= p.y_top
            if x_col and (y_col_1 or y_col_2):
               return True
        return False
