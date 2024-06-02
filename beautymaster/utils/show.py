form PIL improt Image

def show_func(match_results):
    for match_result in match_results:
        image = match_result["image"]

        image.show()

