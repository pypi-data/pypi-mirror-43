import operator
from collections import defaultdict
import numpy as np
import sys

cimport cython

from libcpp.string cimport string
from libcpp.vector cimport vector
from libc.stdint cimport uint32_t, uint16_t

from natsort import natsorted

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(False)
def count_reads_on_islands(islands, c_bins_counts):

    cdef:
        int i
        uint32_t number_bins, _island_start, _island_end
        int j = 0
        uint32_t[::1] bins = np.ones(1, dtype=np.uint32)
        uint16_t[::1] counts = np.ones(1, dtype=np.uint16)
        uint32_t[::1] new_counts = np.zeros(1, dtype=np.uint32)


    chromosomes = natsorted(set(islands.keys()))

    vectors = []
    for chromosome in chromosomes:

        j = 0
        _islands = islands[chromosome]
        new_counts = np.zeros(len(_islands), dtype=np.uint32)

        if chromosome not in c_bins_counts:
            vectors.append(new_counts)
            continue

        bins, counts = c_bins_counts[chromosome]
        number_bins = len(bins)

        for i in range(len(_islands)):
            # _island = &_islands.wrapped_vector[i]
            _island_start, _island_end = _islands.iloc[i].Start, _islands.iloc[i].End

            # not overlapping
            while j < number_bins and (bins[j] < _island_start):
                # print("not overlapping:")
                # print("bins[j]", bins[j], "counts[j]", counts[j], "_island_start", _island)
                j += 1

            # overlapping
            while j < number_bins and (bins[j] < _island_end and bins[j] >= _island_start):
                # print("overlapping:")
                # print("bins[j]", bins[j], "counts[j]", counts[j], "_island_start", _island)
                new_counts[i] += counts[j]
                j += 1

        vectors.append(new_counts)

    return np.concatenate(vectors)



    # fdr_ko = np.array(p_values_ko) * len(p_values_ko) / rankdata(p_values_ko)
    # fdr_wt = np.array(p_values_wt) * len(p_values_wt) / rankdata(p_values_wt)
    # fdr_ko[fdr_ko > 1] = 1
    # fdr_wt[fdr_wt > 1] = 1

    # output = sys.stdout
    # count_ko, count_wt = [], []
    # print("#Chromosome	Start	End	KO_Count	WT_Count	KO_FC	WT_FC	FDR_WT	FDR_KO", file=output)
    # fc = args["false_discovery_rate_comparison"]
    # for i, mi in enumerate(merged_islands):
    #     if fdr_wt[i] <= fc or fdr_ko[i] <= fc:
    #         print(mi.Chromosome, mi.Start, mi.End, mi.KO, mi.WT, mi.KOFC, mi.WTFC, fdr_wt[i], fdr_ko[i], file=output, sep="\t")
    #     count_ko.append(mi.KO)
    #     count_wt.append(mi.WT)

    # p = pearsonr(count_ko, count_wt)
    # s = spearmanr(count_ko, count_wt)
    # print("Pearson's correlation is:", p[0], "and the p-value is", p[1], file=sys.stderr)
    # print("Spearman's correlation is:", s[0], "and the p-value is", s[1], file=sys.stderr)
