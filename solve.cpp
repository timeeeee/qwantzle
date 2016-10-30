#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

#include "trie.h"

// Put letter counts from a word into an array
void count_letters(std::string word, int* counts);

// Get a 26-int array of letter counts from an anagram string
void get_letter_counts(std::string anagram, int counts[]);

// Does a word fit in the given letter counts?
bool fits_counts(std::string word, int counts[]);

// Subtract a word from a letter-count array, mutating array
void subtract_word(std::string word, int counts[]);

// Print all solutions of an anagram. Return solution count
int solve(Trie* trie, int letter_counts[]);
int solve(Trie* trie, int letter_counts[], std::string partial_solution);
int solve(Trie* trie, int letter_counts[], std::string partial_solution, std::string this_word, std::string least_word);

// This will allow us to easily grab an index for a letter- a->0, z->25
int letter_indices[256];

std::string alphabet = "abcdefghijklmnopqrstuvwxyz";

std::string anagram = "ttttttttttttooooooooooeeeeeeeeaaaaaaallllllnnnnnnuuuuuuiiiiisssssdddddhhhhhyyyyyIIIrrrfffbbwwkcmvg";


int main() {
  // Create eight-char wordlist 
  std::ifstream infile;
  infile.open("eight_char_words.txt");
  std::vector<std::string> eight_char_wordlist;
  std::string line;
  while (getline(infile, line)) {
    if (line.size() > 0) eight_char_wordlist.push_back(line);
  }
  int eight_char_word_count = eight_char_wordlist.size();
  infile.close();

  std::cerr << "constructed eight-char wordlist with " << eight_char_word_count << " words.\n";

  // Create <8 char wordlist
  infile.open("short_words.txt");
  std::vector<std::string> short_wordlist;
  while (getline(infile, line)) {
    if (line.size() > 0) short_wordlist.push_back(line);
  }
  int short_word_count = short_wordlist.size();
  infile.close();

  std::cerr << "constructed < eight-char wordlist with " << short_word_count << " words.\n";

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
  
  // Get letter counts for the anagram
  int anagram_counts [26];
  count_letters(anagram, anagram_counts);
  subtract_word("fundamental", anagram_counts);
  subtract_word("I", anagram_counts);
  subtract_word("I", anagram_counts);
  subtract_word("I", anagram_counts);

  /*
   * For each eight letter word:
   *     Subtract it from the letter counts.
   *     Generate a trie with all shorter words that fit the counts still.
   *     Call solve function with this trie and letter count array.
   */
  int solution_count = 0;
  for (int long_index = 0; long_index < eight_char_word_count; long_index ++) {
    std::string long_word = eight_char_wordlist[long_index];
    int counts[26];
    for (int x = 0; x < 26; x++) counts[x] = anagram_counts[x];
    subtract_word(long_word, counts);

    // Build trie with words that fit the counts still
    Trie trie;
    for (int short_index = 0; short_index < short_word_count; short_index ++) {
      std::string short_word = short_wordlist[short_index];
      if (fits_counts(short_word, counts)) trie.insert(short_word);
    }
    std::cerr << long_word << ": built trie with " << trie.get_size() << " words.\n";

    std::string partial_solution = "fundamental I I I " + long_word + " ";
    int this_word_solution_count = solve(&trie, counts, partial_solution);
    std::cerr << long_word << ": " << this_word_solution_count << " solutions.\n";
    solution_count += this_word_solution_count;
  }

  std::cerr << solution_count << " solutions total.\n";

  return 0;
}


int solve(Trie* trie, int letter_counts[]) {
  return solve(trie, letter_counts, "", "", "");
}

int solve(Trie* trie, int letter_counts[], std::string partial_solution) {
  return solve(trie, letter_counts, partial_solution, "", "");
}


/*
 * Recursively guess new letters to add to the solution. Use both a trie of
 * valid words, and an array of letter counts to determine if a letter is
 * available.
 * 
 * Trie* trie: a pointer to the node we are currently located at in a trie.
 *
 * int letter_counts[]: 26-int array with how many of each letter we have left.
 *
 * string partial_solution: The solution so far (we'll append new letters and
 *     spaces to this when guessing them and pass them when recursing)
 *
 * string this_word: The word that is currently being build, so far.
 *
 * string least_word: We want the words in our solution to be in alphabetical
 *     order, so when guessing characters, we'll make sure not to choose
 *     anything that would come earlier in the alphabet than the first
 *     character of least_word. When we're not concerned about this requirement
 *     (first word, previous letters guarantee the word is later
 *     alphabetically, longer word than the previous one) this will be an empty
 *     string.
 */

int solve(Trie* trie, int letter_counts[], std::string partial_solution, std::string this_word, std::string least_word) {
  // Log some debugging info
// std::cerr << "Starting from partial solution '" << partial_solution << std::endl;
// std::cerr << "', this word so far is '" << this_word << "'. Start from '";
// std::cerr << least_word << "'. Counts are:\n";
// for (int i = 0; i < 26; i++) {
//   std::cerr << letter_counts[i] << " ";
// }
// std::cerr << std::endl;

  // Base case: All letters used.
  bool all_zero = true;
  for (int i = 0; i < 26; i++) {
    if (letter_counts[i] > 0) {
      all_zero = false;
      break;
    }
  }

  // If we're out of letters, print this if it's a solution.
  if (all_zero) {
    if (trie->word_ends_here) {
      std::cout << partial_solution << std::endl;
      return 1;
    } else {
      return 0;
    }
  }

  int solution_count = 0;

  // We still have some characters to use. Try each valid next character.
  int least_char = 0;
  std::string next_least_word = "";
  if (!least_word.empty()) {
    least_char = letter_indices[least_word[0]];
    next_least_word = least_word.substr(1);
  }
  
  for (int i = least_char; i < 26; i++) {
    Trie* next_trie = trie->next_chars[i];
    if (next_trie && letter_counts[i] > 0) {
      letter_counts[i]--;  // We'll have to undo this after recursing
      char new_char = alphabet[i];
      solution_count += solve(next_trie, letter_counts, partial_solution + new_char, this_word + new_char, next_least_word);

      // A little cleanup
      letter_counts[i]++;  // Restore letter counts
    }
    next_least_word = "";  // After start_char, we've guaranteed this word is later alphabetically
  }

  // Also maybe we can start a new word here
  if (trie->word_ends_here) {
    solution_count += solve(trie->root, letter_counts, partial_solution + " ", "", this_word);
  }

  return solution_count;
}


void count_letters(std::string word, int counts[]) {
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


bool fits_counts(std::string word, int counts[]) {
  int word_letter_counts[26];
  count_letters(word, word_letter_counts);
  for (int i = 0; i < 26; i++) {
    if (word_letter_counts[i] > counts[i]) return false;
  }
  return true;
}


void subtract_word(std::string word, int counts[]) {
  for (int i = 0; i < word.size(); i++) {
    char letter = word[i];
    int index = letter_indices[letter];
    counts[index]--;
  }
}
