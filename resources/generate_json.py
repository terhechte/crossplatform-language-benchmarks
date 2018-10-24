import random
import pprint
import json

media = []

def make_name():
    names = ["Carey", "Alisha", "Therese", "Tressa", "Vance", "May", "Yuonne", "Holli", "Lyndon", "Emilee", "Darius", "Frederic", "Stewart", "Camellia", "Adalberto", "Shaneka", "Hattie", "Marianne", "Tess", "Leonore", "Colby", "Debbie", "Noe", "Lael", "Dulcie", "Joslyn", "Slyvia", "Marilee", "Liliana", "Les", "Ray", "Lakenya", "Marisha", "Luanna", "Mickie", "Loan", "Veronica", "Echo", "Desiree", "Lenora", "Malik"]
    return random.choice(names)

def make_user():
    return {"username": make_name()}

def make_like():
    return {"username": make_name()}

def make_desc():
    comments = ["Lorem ipsum dolor sit amet, Mikaela Rivard consectetur adipiscing elit.", "Ut blandit viverra diam luctus luctus. In Sharan Olney tellus", "nunc, dapibus id gravida vel, lacinia venenatis augue. Nunc Delfina", "Hyler sagittis rhoncus hendrerit. Sed vel augue nisi, vel sagittis", "sem. Lakiesha Driskell Aenean ante diam, rutrum ut eleifend in,", "convallis sed est. Lavonna Brandis Pellentesque eu ante quis metus", "dictum feugiat. Ut blandit volutpat Kandis Ammerman ante in commodo.", "Duis quam lorem, lacinia nec tempus non, Sondra Swigart tristique", "sed turpis. In id est mi. Class aptent taciti Ruby", "Mcgovern sociosqu ad litora torquent per conubia nostra, per inceptos", "himenaeos. Macy Barak Nunc ipsum libero, tempor et interdum quis,", "molestie commodo mauris. Annita Flemings Fusce tempor, felis vel pellentesque", "luctus, enim lacus sagittis arcu, Clement Cassity at mollis tellus", "mauris in dui. Nunc vel leo velit. Tobie Shive Aliquam", "sit amet erat sit amet elit consequat tempor. Etiam Odessa", "Jenny a metus nunc."]
    return "".join([random.choice(comments) for x in range(0, random.randint(1, 20))])

def make_comment():
    return {"author": make_user(), "text": make_desc(), "likes": [make_like() for x in range(0, random.randint(3, 70))]}

def make_media():
    return {
        "author": make_user(),
        "likes": [make_like() for x in range(0, random.randint(1, 70))],
        "comments": [make_comment() for x in range(0, random.randint(1, 50))],
        "images": {"small": "http://appventure.me/small.png",
                   "medium": "http://appventure.me/medium.png"},
        "description": "".join([make_desc() for x in range(0, random.randint(1, 15))])
    }

if __name__ == "__main__":
    output = [make_media() for x in range(0, 600)]
    print json.dumps(output)
