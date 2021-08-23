from timeit import default_timer as t


# Donne le prochain entier candidat
# Qui s'écrit sous la forme 6k +/- 1
# On ignore 2, 3 et leurs multiples
def primeCandidateGenerator():
	k, r = 1, -1
	while True:
		yield 6*k + r
		k += (r + 1) >> 1
		r = -r

# Lucas–Lehmer Test
# Verifie rapidement si le nombre 2**p - 1 est premier
def lucasLehmerTest(p):
	mersennePrime = (1 << p) - 1
	mersenneSequence = 4
	for i in range(p-2):
		mersenneSequence = (mersenneSequence*mersenneSequence - 2) #% mersennePrime #> Optimisation du modulo
		mersenneSequence = (mersenneSequence & mersennePrime) + (mersenneSequence >> p)
		mersenneSequence = (mersenneSequence & mersennePrime) + (mersenneSequence >> p)

	return mersenneSequence == 0 or mersenneSequence == mersennePrime

# Paramètres du temps
# tmax: temps de la simulation en secondes
ts = t0 = t(); tmax = 5
# Maximum du nombre premier
limit = 1e6

# Crible d'eratosthène pour chercher les premiers < 1e6
# p[0] <- le nombre premier
# p[1] <- le carré du premier
# p[2] <- le plus grand multiple de p qui est supérieur ou égal à n
primes = [] 
for n in primeCandidateGenerator():
	isPrime = True
	for p in primes:
		# si p² > n alors tout les premiers >= p ne divisent pas n
		if p[1] > n: break
		# on cherche le plus petit multiple de p qui est >= n
		while p[2] < n:
			p[2] += p[0]

		# si n est ce multiple, alors il est pas premier
		if p[2] == n:
			isPrime = False
			break

	if isPrime:
		primes.append([n, n*n, n*n])

	# Aucun espoir de tester 2**10**6 - 1
	if n >= limit:
		break

# Liste des premiers qu'on a trouvé
primes = [2, 3] + [p[0] for p in primes]

# Le plus grand entier premier
pmax = max(primes)
p0 = pmax

# On utilise ce qui reste pour chercher parmi les premiers de Mersenne avec LLT
trem = tmax - (t() - t0)
diff = 0
for p in primes:
	t0 = t()
	pmax, p0 = (max(pmax, (1 << p) - 1), p) if lucasLehmerTest(p) else (pmax, p0)
	diff = t() - t0
	
	# Contrôler le temps
	if trem - 2.1*diff < 0:
		break

	trem -= diff

print("M =", pmax)
print("p =", p0)
print("t =", t() - ts)
