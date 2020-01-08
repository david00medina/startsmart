from scipy.spatial.distance import directed_hausdorff
from shapely.geometry import Polygon


class GeometricTools:
    @staticmethod
    def directed_hausdorff(u, v):
        return directed_hausdorff(u, v)

    @staticmethod
    def is_polygon_intersecting(points_1, points_2):
        polygon_1 = Polygon(points_1)
        polygon_2 = Polygon(points_2)
        return polygon_1.intersects(polygon_2)