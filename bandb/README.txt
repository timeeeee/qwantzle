Multi-word anagram solver for the Dinosaur Comics puzzle from 2010-03-01:
http://www.qwantz.com/index.php?comic=1663

Written 2010-03-01 by Jadrian Miles (twitter.com/jadrian,
http://cs.brown.edu/~jadrian, or you can always just google my name).

This zip file contains:
	qwantzcorpus --- word frequencies from the Dinosaur Comics archive
	simplewordlist --- the Dale-Chall list of 3000 simple words
	multianagram.py --- a Python script that proposes solutions

The Python script is a command-line program, but it's not hard to use.

Usage:
    multianagram.py <guess>
where "guess" is any sequence of words, separated by spaces.  The program will
attempt to fill out the rest of the solution using common words from the
Dinosaur Comics transcript archive.

Hit ctrl+c (on a Mac, it's still ctrl+c, NOT cmd+c) to stop the program, or you
can let it run until it's looked at every possibility!  At that point it will
write its solutions to a file.

You may also include a single number in your guess to have the solver only use
words that appear at least that many times in the transcript archive.  If none
is specified, the default value is 2.

Example:
    multianagram.py totally awesome you guys 5
attempts to build a solution using "totally", "awesome", "you", and "guys", plus
words that have appeared five times or more in the comics.  It will only print
solutions that have at least three words beginning with the letter "i", and it
assumes that there are no more than 25 words in the solution.

Use it in combination with Joel Bradshaw's interactive solver app
(http://afifthofnothing.com/anacryptogram.html) to come up with good guesses,
and then get the computer to brute-force the rest!

It's not *really* brute-force; there's a lot of stuff going on here to make
branch-and-bound work reasonably well.  Still, it's a really tough problem
unless you use up most of the available characters in your initial guess.
