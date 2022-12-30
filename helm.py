# one helm may have multiple QE codes associated for example RH3 Richard Hargreaves RS300 and RHF Richard Hargreaves Firefly


class Helm:
    def __init__(self, helm, QEs):
        self.helm = helm
        self.QEs = []
        for qe in QEs:
            if qe.helm == helm:
                self.QEs.append(qe)
