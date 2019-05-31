import random


def get_track(distance):

    track = []
    current = 0
    mid = distance * 4 / 5
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = random.randrange(13,20)
        else:
            a = random.randrange(-10,-5)
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track
