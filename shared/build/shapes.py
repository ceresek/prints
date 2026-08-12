import build123d as _bd


class Deltaline:

    def __init__ (self, x : float = 0, y : float = 0):
        self._x = x
        self._y = y

    def x (self, dx):
        _bd.Line (( self._x, self._y ), ( self._x + dx, self._y ))
        self._x += dx
        return self

    def y (self, dy):
        _bd.Line (( self._x, self._y ), ( self._x, self._y + dy ))
        self._y += dy
        return self

    def xy (self, dx, dy):
        _bd.Line (( self._x, self._y ), ( self._x + dx, self._y + dy ))
        self._x += dx
        self._y += dy
        return self


class Tube (_bd.BasePartObject):

    def __init__ (self, outer_radius: float, inner_radius: float, height: float, *, align = (_bd.Align.CENTER, _bd.Align.CENTER, _bd.Align.CENTER), mode = _bd.Mode.ADD):
        assert height > 0
        assert inner_radius > 0
        assert outer_radius > inner_radius

        with _bd.BuildPart () as part:
            with _bd.BuildSketch ():
                _bd.Circle (outer_radius)
                _bd.Circle (inner_radius, mode = _bd.Mode.SUBTRACT)
            _bd.extrude (amount = height / 2, both = True)

        super ().__init__ (part = part.part, align = align, mode = mode)
