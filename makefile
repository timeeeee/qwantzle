all: trie solve
	g++ -o solve solve.o trie.o

trie: trie.h trie.cpp
	g++ -c trie.cpp

solve: solve.cpp
	g++ -c solve.cpp

wordlists: make_lists.py qwantzcorpus
	python make_lists.py

clean:
	rm -f solve trie.o solve.o eight_char_words.txt short_words.txt
