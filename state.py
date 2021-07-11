from axis_transform import Transform

# Basic functionality for moving through points
class Selectable:
    def __init__(self):
        self.index = 0
        self.points = []

    @property
    def n_points(self):
        return len(self.points)

    def next_point(self):
        self.index += 1
        self.index %= self.n_points

    def prev_point(self):
        self.index += 1
        self.index %= self.n_points

    def set_point(self, x, y):
        self.points[self.index] = (x, y)

    def selected_point(self):
        return self.points[self.index]

    def line(self):
        return self.points

class Axis(Selectable):
    def __init__(self, is_x: bool):
        super().__init__()
        self.points = [
            (100 + (50 if is_x else 0), 100 + (50 if not is_x else 0)),
            (100 + (100 if is_x else 0), 100 + (100 if not is_x else 0))]


class Curve(Selectable):
    """ Curve for data"""
    def __init__(self):
        super().__init__()
        self.points = [(50,50), (150,150)]

    def add_point(self, x, y):
        # find nearest point, then find the nearest of the one/two neighbouring ones, add between them
        index1 = None
        d_sq = 1e100
        for i, (xi, yi) in enumerate(self.points):
            test_d_sq = (x-xi)**2 + (y-yi)**2
            if test_d_sq < d_sq:
                index1 = i
                d_sq = test_d_sq

        if index1 == self.n_points - 1:
            index2 = self.n_points - 2
        elif index1 == 0:
            index2 = 1
        else:
            (x_above, y_above) = self.points[index1 + 1]
            (x_below, y_below) = self.points[index1 - 1]

            d_sq_above = (x - x_above)**2 + (y - y_above)**2
            d_sq_below = (x - x_below)**2 + (y - y_below)**2

            if d_sq_above < d_sq_below:
                index2 = index1 + 1
            else:
                index2 = index1 - 1

        # add the point, swap indices (though we'll only need one)
        if index1 > index2:
            index1, index2 = index2, index1

        left = self.points[:index2]
        right = self.points[index2:]

        self.points = left + [(x, y)] + right
        self.index = index2

    def del_point(self):
        if len(self.points) > 2:
            del self.points[self.index]
            self.index %= self.n_points


class State():
    """ Represents the state of the editor"""
    def __init__(self):

        self.x = Axis(True)
        self.y = Axis(False)

        self.curves = []
        self.curve_index = -1

        self.state = 1

        self.x0 = 0
        self.x1 = 1

        self.y0 = 0
        self.y1 = 1

    @property
    def transform(self):
        return Transform(self.x.points, self.x0, self.x1, self.y.points, self.y0, self.y1)

    def transformed_curve_points(self):
        t = self.transform
        return [t(curve.points) for curve in self.curves]

    def new_curve(self):
        self.curves.append(Curve())
        self.curve_index = len(self.curves) - 1
        self.state = 0

    def del_curve(self):
        if self.state == 0:

            try:
                del self.curves[self.curve_index]
                if len(self.curves) > 0:
                    self.curve_index %= len(self.curves)
                else:
                    self.curve_index = -1

            except Exception as e:
                print(e)

    def next_curve(self):
        if self.state != 0:
            self.state = 0
        else:
            if len(self.curves) > 0:
                self.curve_index += 1
                self.curve_index %= len(self.curves)

    def prev_curve(self):
        if self.state != 0:
            self.state = 0
        else:
            if len(self.curves) > 0:
                self.curve_index += len(self.curves) - 1
                self.curve_index %= len(self.curves)

    def next_point(self):
        if self.state == 0:
            if len(self.curves) > 0:
                self.curves[self.curve_index].next_point()
        elif self.state == 1:
            self.x.next_point()
        elif self.state == 2:
            self.y.next_point()
        else:
            raise ValueError("BAD STATE")

    def prev_point(self):
        if self.state == 0:
            if len(self.curves) > 0:
                self.curves[self.curve_index].prev_point()
        elif self.state == 1:
            self.x.prev_point()
        elif self.state == 2:
            self.y.prev_point()
        else:
            raise ValueError("BAD STATE")

    def set_x(self):
        self.state = 1

    def set_y(self):
        self.state = 2

    def set_curves(self):
        self.state = 0

    def set_point(self, x, y):
        if self.state == 0:
            if len(self.curves) > 0:
                self.curves[self.curve_index].set_point(x, y)

        elif self.state == 1:
            self.x.set_point(x, y)

        elif self.state == 2:
            self.y.set_point(x, y)

        else:
            raise ValueError("BAD STATE")

    def add_point(self, x, y):
        if self.state == 0:
            if len(self.curves) > 0:
                self.curves[self.curve_index].add_point(x, y)

    def del_point(self):
        if self.state == 0:
            if len(self.curves) > 0:
                self.curves[self.curve_index].del_point()

    def drawable_points(self):
        out = []
        out += [(x, y, 255, 0, 0) for x, y in self.x.points]
        out += [(x, y, 0, 0, 255) for x, y in self.y.points]
        for curve in self.curves:
            out += [(x, y, 0, 128, 0) for x, y in curve.points]

        return out

    def text(self):
        return \
            [("%g" % self.x0, (self.x.points[0][0], self.x.points[0][1]), (255, 0, 0)),
             ("%g" % self.x1, (self.x.points[1][0], self.x.points[1][1]), (255, 0, 0)),
             ("%g" % self.y0, (self.y.points[0][0], self.y.points[0][1]), (0, 0, 255)),
             ("%g" % self.y1, (self.y.points[1][0], self.y.points[1][1]), (0, 0, 255))]

    def lines(self):
        out = []
        out.append((self.x.line(), (255,0,0)))
        out.append((self.y.line(), (0,0,255)))

        for curve in self.curves:
            out.append((curve.line(), (0, 128, 0)))

        return out

    def selected_point(self):
        if self.state == 0:
            if len(self.curves) > 0:
                return self.curves[self.curve_index].selected_point()
            else:
                return None

        elif self.state == 1:
            return self.x.selected_point()

        elif self.state == 2:
            return self.y.selected_point()

        else:
            return None