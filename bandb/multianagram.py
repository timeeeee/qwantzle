#! /usr/bin/python

# Multi-word anagram solver specifically optimized for the
# Dinosaur Comics puzzle from 2010-03-01:
# http://www.qwantz.com/index.php?comic=1663
#
# Usage:
#     multianagram.py <guess>
# where "guess" is any sequence of words, separated by
# spaces.  The program will attempt to fill out the rest of the
# solution using common words from the Dinosaur Comics
# transcript archive.
#
# You may also include a single number in your guess to have
# the solver only use words that appear at least that many
# times in the transcript archive.  If none is specified, the
# default value is 2.
#
# Example:
#     multianagram.py totally awesome you guys 5
# attempts to build a solution using "totally", "awesome",
# "you", and "guys", plus words that have appeared
# five times or more in the comics.  It will only print solutions
# that have at least three words beginning with the letter "i",
# and it assumes that there are no more than 25 words in the
# solution.
#
# Use it in combination with Joel Bradshaw's interactive solver
# app (http://afifthofnothing.com/anacryptogram.html) to
# come up with good guesses, and then get the computer to
# brute-force the rest!
#
# It's not *really* brute-force; there's a lot of stuff going on here
# to make branch-and-bound work reasonably well.  Still, it's a
# really tough problem unless you use up most of the available
# characters in your initial guess.
#
# This software was written 2010-03-01 by Jadrian Miles and is
# hereby released into the public domain.
#
# Sorry if this code looks weird; I use a variable-width font for
# coding, and I also didn't work very hard on prettying this up
# for public consumption.  Fortunately it's Python so it's still
# pretty decent.

import sys, string, math

def frequencies(s):
	d = {}
	for c in string.lowercase:
		d[c] = 0
	for c in s:
		d[c] = d[c] + 1
	return d

def appendfreqs(d, s):
	newd = d.copy()
	for c in s:
		newd[c] = newd[c] + 1
	return newd

# Return a modified frequency dictionary if the word fits;
# None otherwise
def matchtofreqs(word, freq):
	if len(word) > sum(freq.values()):
		# short-circuit if a fit is impossible
		return None
	for c in word:
		try:
			if freq[c] == 0:
				return None
			freq[c] = freq[c] - 1
		except KeyError:
			return None
	return freq

def importwordlist(freqthresh, d):
	#### import the standard Unix system dictionary
	f = open('/usr/share/dict/words')
	syswords = f.read().split('\n')
	f.close()
	# reject capitalized words
	syswords = [w for w in syswords if w == string.lower(w) and len(w) > 0]
	
	#### import shorter words from the simple word list
	f = open('simplewordlist')
	shortwords = f.read().split('\n')
	f.close()
	shortwords = [w for w in shortwords if w == string.lower(w) and len(w) > 0]
	
	#### import the qwantz.com-specific word list
	f = open('qwantzcorpus')
	pairs = [x.split(' ') for x in f.read().split('\n')]
	f.close()
	# drop erroneous empty word entries
	pairs = [x for x in pairs if len(x) == 2]
	# pick only words that are used often
	qwantzwords = dict([(x[1],int(x[0])) for x in pairs if int(x[0]) >= freqthresh])
	
	#### hard-code some words relevant to the comic
	forcedwords = ['anagram','anagrams','anagramist','anagramists','fundamental','fundamental','science','calculus']
	for w in forcedwords:
		if w not in qwantzwords:
			qwantzwords[w] = 1
	syswords = syswords + forcedwords
	
	#### refine and combine the three lists
	# remove one- and two-letter word fragments from the qwantz list
	words = [x for x in qwantzwords.keys() if len(x) > 2]
	# add in valid one- and two-letter words
	words = words + [x for x in shortwords if len(x) < 3] + ['i']
	# reject words longer than the limit
	words = [w for w in words if len(w) <= 11]
	# use only words that are found in the system dictionary
	words = set(words) & set(syswords)
	# remove some repeat offenders
	shitlist = ['ah','ax','eh','ha','ho','ma','oh','pa', 'huh','hey','yea','yeah','bah', 'duh','tee','tic','aha','thy', 'goo','sir','boo','woo','non', 'lee','hah', 'whoa','tony','ouch','gosh', 'narrator']
	for w in shitlist:
		try:
			words.remove(w)
		except KeyError:
			pass
	# turn the word list from a set back into a list
	words = list(words)
	# Preemptively remove all words from the wordlist that don't fit
	# in the initial dictionary
	words = [w for w in words if matchtofreqs(w, d.copy()) is not None]
	# sort by generally decreasing length and corpus frequency
	words.sort(key = lambda w: -(len(w) * (qwantzwords[w] ** 0.25)))
	#words.sort(key = lambda w: -len(w))
	
	#### compute reverse cumulative frequencies, for pruning
	cumfreqs = [{}] * len(words)
	cumfreqs[-1] = frequencies(words[-1])
	for i in range(len(cumfreqs)-1):
		cumfreqs[-(2+i)] = appendfreqs(cumfreqs[-(1+i)], words[-(2+i)])
	
	#### compute the tail-word-length distribution
	tailwordlengths = [max([len(w) for w in words[i:]]) for i in range(len(words))]
	
	return (words, cumfreqs, tailwordlengths)

# Return True if we shouldn't append word i to the sentence, given the
# remaining character frequencies d
def quitEarly(prefix, i, d):
	# never use the same word three times
	if len(prefix) > 2 and words[i] == prefix[-1] and words[i] == prefix[-2]:
		return True
	# bail if the shortest possible sentence we can generate is too long
	if (sum(d.values()) / tailwordlengths[i]) + len(prefix) > 25:
		#print "Quit because of the small-words criterion"
		return True
	# bail if the remaining words in the list can't possibly cover the characters we need to use up
	for c in string.lowercase:
		if d[c] > cumfreqs[i][c]:
			return True
	return False

# Recursive function to return a list of sentences made only of words
# with index >= i that exactly match the frequency dictionary d
def sentences(prefix, i, d):
	if quitEarly(prefix, i, d):
		#print 'Quit early!'
		return None
	try:
		newDict = matchtofreqs(words[i], d.copy())
	except IndexError:
		# i was out of bounds
		return None
	if newDict is None:
		# word i doesn't fit in the frequency dictionary
		return None
	#print 'Match with %i' % i
	if max(newDict.values()) == 0:
		# we exhausted the dictionary and we're done
		#print 'Full match with %i' % i
		if len([w for w in prefix + [words[i]] if w[0] == 'i']) < 3:
			# at least three words must begin with "i"
			return None
		print ' '.join([w for w in prefix + [words[i]]])
		return [[i]]
	retval = []
	for j in range(len(words) - i):
		#print 'Branch from %i to %i' % (i, i + j)
		suffixes = sentences(prefix + [words[i]], i + j, newDict)
		if suffixes is not None:
			for s in suffixes:
				retval = retval + [[i] + s]
	if retval:
		return retval
	else:
		return None

if __name__ == "__main__":
	guess = [string.lower(x) for x in sys.argv[1:]]
	freqthresh = 2
	numbers = [int(w) for w in guess if w.isdigit()]
	if len(numbers) > 0:
		freqthresh = numbers[-1]
	guess = [w for w in guess if not w.isdigit()]
	
	#### Create the dictionary of letter frequencies to match
	
	code=(12*'t')+(10*'o')+(8*'ie')+(7*'a')+(6*'lnu')+(5*'sdhy')+(3*'rf')+'bbwwkcmvg'
	code = ''.join(sorted(code))
	masterdict = frequencies(code)
	try:
		guessdict = frequencies(''.join(guess))
	except KeyError, e:
		print 'Your guess included a weird character: %s' % e
		sys.exit(1)
	
	for c in string.lowercase:
		masterdict[c] = masterdict[c] - guessdict[c]
		if masterdict[c] < 0:
			print 'Your guess used too many "%s"s!' % c
			sys.exit(1)
	
	print '%i remaining letters:' % sum(masterdict.values())
	print '(by frequency): %s' % ''.join([k * v for (k, v) in sorted(masterdict.items(), key = lambda x: -x[1])])
	print '(in abc order): %s' % ''.join([k * v for (k, v) in sorted(masterdict.items(), key = lambda x: x[0])])
	
	#### Create the word list and pre-computed measures on it
	try:
		(words, cumfreqs, tailwordlengths) = importwordlist(freqthresh, masterdict)
		
		print 'Searching %i words (written to file "words.txt"), %i of which are <4 chars long...' % (len(words), len([w for w in words if len(w) < 4]))
		f = open('words.txt', 'w')
		f.write('\n'.join(words) + '\n')
		f.close()
		
		minidx = 0
		maxidx = None
		if maxidx is None:
			maxidx = len(words)
		
		allmatches = []
		for i in range(maxidx - minidx):
			s = sentences(guess, minidx + i, masterdict.copy())
	except KeyboardInterrupt:
			print ''
			sys.exit(0)
	
	print '\n\n========= %i matches (written to matches.txt) =========' % len(s)
	f = open('matches.txt', 'w')
	f.write('\n'.join([' '.join(prefix + [words[i] for i in x]) for x in allmatches]))
	f.close()
