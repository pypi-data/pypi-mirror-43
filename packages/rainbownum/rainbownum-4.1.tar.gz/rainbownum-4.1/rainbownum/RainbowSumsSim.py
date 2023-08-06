from .RainbowSim import RainbowSim


class RbSumsEq(RainbowSim):
    def __init__(self, n, a, b=0, mod=False):
        super(RbSumsEq, self).__init__(n, a, b, mod)
        self.sums = self.sets
        self.__generate_sums()

    def get_equation(self):
        eq = ""
        for i in self.a:
            eq += str(i) + "x + "
        eq = eq[:-2] + "= " + str(self.b)
        return eq

    def __generate_sums(self):
        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.__recur_gen_sums(self.sums, self.a, self.b, values, 0)

    def __recur_gen_sums(self, sums, a, b, values, loop):
        k = self.k - 1
        if loop == k:
            return
        if self.mod:
            stop_case = self.n - k + loop
        else:
            stop_case = self.n - k + loop + 1
        while values[loop] <= stop_case:
            self.__recur_gen_sums(sums, a, b, values, loop + 1)
            if loop == k - 1:
                sum = 0
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    sum = sum + a[i] * values[i]
                    out[i] = values[i]
                valid = True
                sum1 = (sum - b) / -a[k]
                sum2 = 0
                if self.mod:
                    sum1 = sum1 % self.n
                    sum2 = (sum - b) % self.n
                    sum2 = sum2 / -a[k]
                if sum1 != int(sum1) and sum2 != int(sum2):
                    valid = False
                if sum1 == int(sum1):
                    out[k] = int(sum1)
                elif sum2 == int(sum2):
                    out[k] = int(sum2)
                else:
                    valid = False
                valid = self._set_leq_n(out, valid)
                valid = self._is_distinct(out, valid)
                out = self._decrement_if_not_mod(out, valid)
                self._add_set(out, valid)
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp - 1] + 1
