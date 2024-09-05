class basket:

    def __init__(self, request):

        self.session = request.session

        # Check if the session key exists
        basket = self.session.get("sKey")
        # If the session key does not exist, create a new session key
        if "sKey" not in request.session:
            basket = request.session["sKey"] = {}

        self.basket = basket
