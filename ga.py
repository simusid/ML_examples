import random
import string

TARGET   = "This is the target sentence that we want to try and match."
L        = len(TARGET)
POP_SIZE = 300   # the number of random sentences
MAX_GEN  = 5000   # max attempts
MUT_RATE = 0.03  # 
CROSS_RATE = 0.3
ELITE_KEEP = 5

ALPHABET = string.printable  # all possible printable ASCII characters

def random_individual():
    """build one random candidate sentence of length L"""
    return ''.join(random.choice(ALPHABET) for _ in range(L))

def fitness(chrom):
    """The more they match, the better the fitness score"""
    return sum(1 for a, b in zip(chrom, TARGET) if a == b)

def tournament(pop, k=3):
    """given all the sentences in pop, randomly pick k of them
    and return the one with the best fit"""
    return max(random.sample(pop, k), key=lambda ind: ind['fit'])

def crossover(p1, p2):
    if random.random() > CROSS_RATE:
        """70% of the time we do this"""
        return p1, p2
    
    """30% of the time we do this"""
    pt = random.randint(1, L-1)

    """use list indexing to swap parts of the two sentences"""
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]

def mutate(chrom):
    lst = list(chrom)
    for i in range(L):
        """decide one char at a time if we will mutate this character"""
        if random.random() < MUT_RATE:
            lst[i] = random.choice(ALPHABET)
    return ''.join(lst)


#### Main program

# build POP_SIZE random candidate sentences with empty fitness
pop = [{'chrom': random_individual(), 'fit'  : None} for _ in range(POP_SIZE)]

# now get the initial fitness for each sentence in pop.
for ind in pop:
    ind['fit'] = fitness(ind['chrom'])

# loop until done or MAX_GEN
for gen in range(1, MAX_GEN+1):
    # fitness is the score, so sort all of them descending
    pop.sort(key=lambda ind: ind['fit'], reverse=True)

    # then take the best one
    best = pop[0]
    print(f"Gen {gen:4d} | best = {best['chrom']} | score = {best['fit']}/{L}")

    # L is length of sentence so if the score is that length we're done
    if best['fit'] == L:
        print("✔︎ Target phrase found!")
        break

    # otherwise keep the best matches 
    # mutate and build new candidate sentence
    # until we have POP_SIZE again
    new_pop = pop[:ELITE_KEEP]
    while len(new_pop) < POP_SIZE:
        p1 = tournament(pop)['chrom']
        p2 = tournament(pop)['chrom']
        c1, c2 = crossover(p1, p2)
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_pop.append({'chrom': c1, 'fit': fitness(c1)})
        if len(new_pop) < POP_SIZE:
            new_pop.append({'chrom': c2, 'fit': fitness(c2)})

    pop = new_pop

 