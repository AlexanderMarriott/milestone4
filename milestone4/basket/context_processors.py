from .basket import basket as gbasket


def basket(request):
    return {"basket": gbasket(request)}
