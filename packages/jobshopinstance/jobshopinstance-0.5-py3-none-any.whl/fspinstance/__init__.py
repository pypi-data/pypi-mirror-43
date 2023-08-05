import math
import os
import datetime

# Global variables for the class
_Taillard = "taillard"
_Gaussian = "gaussian"
_JobCorrelated = "job-correlated"
_MachineCorrelated = "machine-correlated"
_MixedCorrelated = "mixed-correlated"
_M = 2147483647
_A = 16807
_B = 127773
_C = 2836
_outputDirectory = "output/instances"
_now = datetime.datetime.now()
_todayFolder = f"{_now.year}{_now.month}{_now.day}"

_GBL_DurationLB=1
_GBL_DurationUB=99
_GBL_RandNumSeed=0


class FSProblemGenerator:
    """Generate instances of JSSP"""
    def __init__(self, problem_type, nb_jobs, nb_machines, random_seed):
        self.Times = [[0]*nb_machines for _ in range(nb_jobs)]
        self.Machines = [[0]*nb_machines for _ in range(nb_jobs)]
        self.random_seed = [random_seed]
        global _GBL_RandNumSeed
        _GBL_RandNumSeed = random_seed
        self.unif_zero_one()

        # TODO: modify values according to problem_type
        # for i in range(0, nb_jobs):
        #     for j in range(0, nb_machines):
        #         self.Times[i][j] = self.unif(self.time_seed, 1, 99)

        if problem_type == _Gaussian:
            self.Times = self.generateGaussianFlow(nb_jobs, nb_machines, self.Times)
        elif problem_type == _Taillard:
            self.Times = self.generateTaillardFlow(nb_jobs, nb_machines, self.Times)

        for i in range(0, nb_jobs):
            for j in range(0, nb_machines):
                self.Machines[i][j] = j+1

        for i in range(0, nb_jobs):
            for j in range(0, nb_machines):
                k2 = self.unif(self.random_seed, j, nb_machines-1)
                # Swap of variables
                self.Machines[i][j], self.Machines[i][k2] = self.Machines[i][k2], self.Machines[i][j]

    def save(self):
        """
        Save file with the params of the object.
        :return:
        """
        content = f"{self.random_seed[0]}\n" \
                        f"{len(self.Times)},{len(self.Times[0])},{len(self.Machines[0])}\n"

        content += self.fillContentByMatrix(self.Times)
        content += f"MACHINES\r\n"
        content += self.fillContentByMatrix(self.Machines)

        self.saveFile(content, f"{len(self.Times)}{len(self.Times)}-{self.random_seed[0]}")


    def fillContentByMatrix(self, matrixOfElements):
        """
            Fill the string in the argument with the values in the matrix
            :param self:
            :param matrixOfElements:
            :param content:
            :return:
        """
        content: str = ""
        for i in range(0, len(matrixOfElements)):
            for j in range(0, len(matrixOfElements[0])):
                content += f"{matrixOfElements[i][j]} "
            content += "\r\n"
        return content

    def unif_zero_one(self):
        global _GBL_RandNumSeed
        value01 = 0
        k = _GBL_RandNumSeed // _B
        _GBL_RandNumSeed = (_A * (_GBL_RandNumSeed % _B)) - (k * _C)

        if _GBL_RandNumSeed < 0:
            _GBL_RandNumSeed = _GBL_RandNumSeed + _M
        value01 = _GBL_RandNumSeed / float(_M)

        assert((value01>=0.0) and (value01<1.0))

        return value01

    def unif(self, seed, low, high):
        """
            :param seed: Array of ints
            :param low: lower-bound
            :param high: upper-bound
            :return:
        """
        value01 = 0
        k = seed[0] // _B
        seed[0] = (_A * (seed[0] % _B)) - (k * _C)

        if seed[0] < 0:
            seed[0] = seed[0] + _M
        value01 = seed[0] / float(_M)

        return int(low + math.floor(value01 * (high - low + 1)))

    def unif_supplied(self, low, high):
        assert(low<=high)

        value01 = self.unif_zero_one()
        result = low + int(math.floor(value01 * (high - low + 1)))
        assert(result>=low and result<=high)

        return result

    def saveFile(self, content, fileName):
        """
        Save the given content with the specified fileName parameter
        :param content:
        :param fileName:
        :return:
        """
        if not os.path.exists(_outputDirectory):
            os.makedirs(_outputDirectory)

        if not os.path.exists(f"{_outputDirectory}/{_todayFolder}"):
            os.makedirs(f"{_outputDirectory}/{_todayFolder}")

        file = open(f"./{_outputDirectory}/{_todayFolder}/{fileName}.txt","w+")
        file.write(content)
        file.close()

    def generateTaillardFlow(self, nb_jobs, nb_machines, times_matrix):
        for i in range(nb_jobs):
            for j in range(nb_machines):
                times_matrix[i][j] = self.unif_supplied(_GBL_DurationLB, _GBL_DurationUB)

        return times_matrix

    def generateGaussianFlow(self, nb_jobs, nb_machines, times_matrix):
        gaussian_mean = ((_GBL_DurationUB-_GBL_DurationLB)/2)+_GBL_DurationLB
        gaussian_sigma = (_GBL_DurationUB-_GBL_DurationLB)/6

        for i in range(nb_jobs):
            for j in range(nb_machines):
                times_matrix[i][j] = self.round_int(self.normal(gaussian_mean, gaussian_sigma))

        return times_matrix

    def normal(self, mean, std_dev):
        i_set = 0
        fac=0
        r=0
        v1=0
        v2=0
        g_set = 0

        if (i_set == 0):
            while True:
                v1 = 2.0 * self.unif_zero_one()-1.0
                v2 = 2.0 * self.unif_zero_one()-1.0
                r = v1*v1 + v2*v2
                if r <= 1:
                    break

            fac = math.sqrt(-2*math.log2(r)/r)
            g_set = v1*fac
            i_set = 1
            a = (v2*fac)*std_dev+mean
            return a
        else:
            i_set = 0
            a = g_set*std_dev+mean
            return a

    def round_int(self, value):
        nb_int = int(value)
        nb_dec = float(str(value)[1:])

        return nb_int+1 if nb_dec >= 0.5 else nb_int


# gaussian 15 15 1234
def createFspInstance(problem_type, nb_jobs, nb_machines, random_seed):
    temp = FSProblemGenerator(problem_type, nb_jobs, nb_machines, random_seed)
    temp.save()


def createFspInstances(list):
    for i in list:
        temp = FSProblemGenerator(i[0], i[1], i[2], i[3])
        temp.save()