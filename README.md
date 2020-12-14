# EnronQuerying

### process

There are two main components: 
1. preprocessing and loading data onto user's mobile device
2. processing tries at runtime

Preprocessing consists of the following steps:
1. a "lexer" tokenizes all of the emails. These tokens are split by whitespace in the email
2. The lexer serializes and outputs a JSON map of tokens -> emails in which they appear in
3. An initial trie is created from all the tokens in all of the emails.
4. Because this is done in preprocessing, this is ripe for parallelization and merging the tries per sender. I wasn't worried about memory or processing time here, as we could spin up this job once on a cluster and render the following output.
5. The final output of the preprocessor is another JSON map of tokens -> emails in which they appear in, separated by first character into separate directories.

At runtime, the mobile device would do the following as the user searches:
1. Grab the appropriate token -> emails dict based on the first character the user types, and build a trie.
2. Using normal trie traversal techniques, retrieve the appropriate emails that match on the user's query.

There are a *number* of optimizations that could be done here, but I didn't take the time to complete them this weekend.

### optimizations

Client optimizations (highest priority)
* Trie caching
  * perhaps the user makes a mistake and types "cst" instead of "cat". Caching the "c" trie would enable fast sorting without having to make a trie reload
* balance trie caching with memory usage
  * I want to run some comparison tests for how much memory this uses on the full dataset. I could further split the tries by second or third char, instead of just the first. Doing this means that caching smaller tries would lead to fewer cache hits if the user wants to retype something
* "compressing" the trie
  * for every node that doesn't hold any "hits" data, we are wasting space. For tries that have multiple nodes in a row without any hits, we could compress these nodes into a single one.
  * this could slightly speed up traversal, as searching the trie could "batch" steps by checking against a substring instead of single character
  * this would also slightly reduce the amount of memory necessary to store the trie, as it would prune any nodes that are not present as a token.

Preprocessing optimizations
* Process the emails into a logical object structure
  * The preprocessor is tokenizing the full email and disregarding any structure. By parsing out the data into a meaningful structure, we could also do first-pass deduplication of email data. This would drastically cut down on tokenizing and building an initial trie.
  * A misstep here was to assume that there would be a lot of overlap on tokens for emails across the entire dataset. If I was tokenizing just the "written" portions of the emails, that surely would have been the case. However, since the tokens also include unique IDs, the initial preprocessing has been hanging on the '<' trie, due to the fact that includes EVERY unique identifier across emails.
* Don't make a trie in the preprocessing step.
  * The initial tokenizing output and trie serialization is exactly the same. While I coded this, I anticipated creating a full trie in preprocessing, splitting and serializing it, and deserializing the smaller tries at runtime. Little did I realize I was already "serializing the trie" by tokenizing and implementing a way to construct a trie from those tokens.
  * I didn't take the time, but it would be simple to adjust the tokenizing output to merge the token maps from email-user and dissect the maps along the first character of each key.
  * The serialization of the tree is also too naive; it still traverses the full tree but only needs the children. This step would be eliminated by allowing the tokenizing output to split the dicts by initial key char.
  
### user experience improvements

* Queries are currently case-sensitive. They should prioritize matched-case results, but also include case-insensitive results.
* Queries should have some "fuzzy" searching if users misspells something. Perhaps show "cousins" in trie if there are no results for a given query.

### taking this to production
This code could be a prototype, but is certainly missing some pieces that I would add in with more time.

* Unit tests! It would be very helpful to test on mock data and ensure that the serialization / tokenization matches the same trie after deserialization
* Parallelization of preprocessing, which I mentioned before. Running a huge batch of data serially like this is ridiculous
* Benchmarking. There are a number of optimizations that just require tuning of the data and proper measurement of I/O access times and memory usage. I didn't get to do memory analysis, but I have already mentioned memory optimizations in sections above.
