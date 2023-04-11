class GameExc(Exception):
    pass

class OffBoardExc(GameExc):
    def __str__(self):
        return "Выбранные координаты вне координатной плоскости."


class DotAlreadyHitExc(GameExc):
    def __str__(self):
        return "Вы уже стреляли по этим координатам, либо уничтожили корабль поблизости."


class ShipIncorrectPlacementExc(GameExc):
    def __str__(self):
        return "Корабль нелья расположить по этим координатам."
