'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

import random
from collections import namedtuple, Counter
from ways import load_map_from_csv


def main(nproblems, output_filename='problems.csv'):
    roads = load_map_from_csv()

    junctions = roads.junctions()

    results = set()
    while len(results) < nproblems:
        start_junction = random.choice(junctions)
        nhops = random.randint(100, 10000)  # allow between 100 and 10000 hops

        curr_junction = start_junction
        for _ in range(nhops):
            neighbors = list(curr_junction.links)
            if len(neighbors) == 0:
                # no neighbors - we reached the target (because we cant move on.)
                break

            random_link = random.choice(neighbors)
            curr_junction = junctions[random_link.target]

        # if somehow we ended up on the same junction - retry
        if start_junction.index == curr_junction.index:
            continue

        results.add((start_junction.index, curr_junction.index))
        print('Finished {0} out of {1}'.format(len(results), nproblems))

    with open(output_filename, 'w') as f:
        f.write(
            '\n'.join('{0},{1}'.format(source, target)
                      for source, target in results)
        )


if __name__ == '__main__':
    main(100, 'problems2.csv')
