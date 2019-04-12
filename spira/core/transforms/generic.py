from spira.core.transformation import ReverseTransform


class GenericTransform(ReverseTransform):

    def __init__(self, translation=(0,0), rotation=0, reflection=False, magnification=1, **kwargs):
        super().__init__(
            translation=translation,
            rotation=rotation,
            reflection=reflection,
            magnification=magnification,
            **kwargs
        )

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()
        # return str(hash("R" + str(int(self.rotation * 10000)) +
        #                 "T" + str(int(self.translation[0] * 1000)) + "_" + str(int(self.translation[1] * 1000)) +
        #                 "M" + str(int(self.magnification * 1000)) +
        #                 "V" + str(self.v_mirror) +
        #                 "AM" + str(self.absolute_magnification) +
        #                 "AR" + str(self.absolute_rotation)
        #                 ))

    def __str__(self):
        """ Gives a string representing the transform. """
        return "_M=%s-R=%s-RF=%s-MN=%s" % (
            # str(''.join(str(e) for e in self.midpoint)),
            str(self.translation),
            str(self.rotation),
            str(self.reflection),
            str(self.magnification)
        )

