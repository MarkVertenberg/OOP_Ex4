
class Scalable:
    """
        Interface that representing scalable object
    """

    def scale(self, x: float, y: float) -> tuple(float, float):
        """
            Scales the object according to width and height.
        """
        raise NotImplementedError

    def get_size(self) -> float:
        """
            Return a float that representing the size of the object.
            For example: for node it is radius.
        """
        raise NotImplementedError

    def __gt__(self, other) -> bool:
        """ Comparing between two scalable objects. """
        return self.get_size() > other.get_size()