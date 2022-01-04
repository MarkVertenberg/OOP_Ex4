class ScreenObjectInterface:
    """
        Interface that representing a screen object in pygame framework.
    """

    def draw(self, screen, outline=None) -> None:
        """
            Draws the object on the screen.
            @param screen: pygame display type.
            @param outline: outline of the object, None by default.
        """
        raise NotImplementedError

    def handle_event(self, event) -> None:
        """
            Handles the event.
            @param event: pygame event type
        """

    def is_over(self, pos: tuple) -> bool:
        """
            @param pos: mouse position or a tuple of (x,y) coordinates.
            @return: if the pos is over the object.
        """