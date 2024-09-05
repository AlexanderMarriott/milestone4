from .basket import Basket as gbasket


def basket(request):
    return {"basket": gbasket(request)}
