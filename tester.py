class Meter(object):
    """Descriptor for a meter."""

    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    """Descriptor for a foot."""

    def __get__(self, instance, owner):
        print(instance)
        print(owner)
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808


class Distance(object):
    """Class to represent distance holding two descriptors for feet and
    meters."""
    meter = Meter()
    foot = Foot()

class Holder(object):
    def __init__(self, value: Distance = None):
        self.value = value

    def printthing(self):
        print(__name__)
        print(self.value)

    def valueset(self, value):
        self.value.foot = value

    def valueget(self):
        return self.value.foot

def makeobject(makethis):
    print(__name__)
    return makethis()


holder = Holder()
holder.value = makeobject(Distance)
holder.printthing()
holder.valueset(87)
holder.valueget()
print(holder.value.foot)
