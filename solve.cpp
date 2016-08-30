#include <iostream>
#include <fstream>
#include <vector>
#include <string>


int solve(std::vector<std::string> wordlist, int** dict_counts, int* anagram_counts);
int solve(std::vector<std::string> wordlist, int** dict_counts, int* anagram_counts, std::vector<std::string> solution_so_far, int start);


// Put letter counts from a word into an array
void count_letters(std::string word, int* counts);

// This will allow us to easily grab an index for a letter- a->0, z->25
int letter_indices[256];


int main(int argc, char* argv[]) {
  if (argc < 3) {
    std::cout << "Usage-  solve wordlist anagram <word2> <word3>...\n";
    return 1;
  }

  // Put together the anagram as a single string
  std::string anagram = "";
  for (int i = 2; i < argc; i++) {
    anagram += argv[i];
    anagram += " ";
  }
  anagram.erase(anagram.size() - 1);

  std::ifstream infile;
  infile.open(argv[1]);
  if (!infile.is_open()) {
    std::cout << "Could not open file \"" << argv[1] << "\"\n";
    return 1;
  }

  std::vector<std::string> wordlist;
  std::string line;
  while (getline(infile, line)) {
    if (line.size() > 0) wordlist.push_back(line);
  }
  int word_count = wordlist.size();
  infile.close();

  // Set up letter indexing
  for (int i = 0; i < 256; i++) {
    if (i >= 'a' && i <= 'z') {
      letter_indices[i] = i - 'a';
    } else if (i >= 'A' && i <= 'Z') {
      letter_indices[i] = i - 'A';
    } else {
      letter_indices[i] = -1;
    }
  }
  
  // Make letter counts for each word
  int** letter_counts = new int* [word_count];
  for (int index = 0; index < word_count; index++) {
    letter_counts[index] = new int [26];
    count_letters(wordlist[index], letter_counts[index]);
  }
  
  int anagram_counts [26];
  count_letters(anagram, anagram_counts);
  std::cerr << anagram << ": ";
  for (int i = 0; i < 26; i++) {
    std::cerr << anagram_counts[i] << " ";
  }
  std::cerr << std::endl;
   
  std::cerr << solve(wordlist, letter_counts, anagram_counts) << std::endl;

  // Delete dictionary letter counts
  for (int index = 0; index < word_count; index ++) {
    delete[] letter_counts[index];
  }
  delete[] letter_counts;

  return 0;
}

int solve(std::vector<std::string> wordlist, int** dict_counts, int* anagram_counts, std::vector<std::string> solution_so_far, int start) {
  // Base case: Are all anagram_counts 0? If so, this is one, print it!
  bool all_zero = true;
  for (int i = 0; i < 26; i++) {
    if (anagram_counts[i] > 0) {
      all_zero = false;
      break;
    }
  }
  
  if (all_zero) {
    for (std::vector<std::string>::iterator iter = solution_so_far.begin(); iter != solution_so_far.end(); iter++) {
      std::cout << (*iter) << " ";
    }
    std::cout << std::endl;
    return 1;
  } else {
    // There are still letters left. Try all words from start to end.
    int solution_count = 0;
    for (int index = start; index < wordlist.size(); index++) {
      // Can we use this word?
      bool can_use_word = true;
      for (int i = 0; i < 26; i++) {
	if (dict_counts[index][i] > anagram_counts[i]) {
	  can_use_word = false;
	  break;
	}
      }

      if (can_use_word) {
	// push it onto the "word stack." this means: add to solution_so_far, and subtract letter counts.
	// We will have to undo all this after the recursive call!
	solution_so_far.push_back(wordlist[index]);
	for (int i = 0; i < 26; i++) {
	  anagram_counts[i] -= dict_counts[index][i];
	}
	solution_count += solve(wordlist, dict_counts, anagram_counts, solution_so_far, index);
	solution_so_far.pop_back();
	for (int i = 0; i < 26; i++) {
	  anagram_counts[i] += dict_counts[index][i];
	}
      }
    }
    return solution_count;
  }
}


int solve(std::vector<std::string> wordlist, int** dict_counts, int* anagram_counts) {
  std::vector<std::string> solution_so_far;
  return solve(wordlist, dict_counts, anagram_counts, solution_so_far, 0);
}


void count_letters(std::string word, int* counts) {
  for (int i = 0; i < 26; i++) {
    counts[i] = 0;
  }
  for (std::string::iterator it = word.begin(); it != word.end(); it++) {
    int index = letter_indices[*it];
    if (index != -1) {
      counts[index]++;
    }
  }
}
