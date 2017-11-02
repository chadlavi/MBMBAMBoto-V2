* searching is too imprecise based just on episode numbers because of inconsistent data
	- not all episodes have "XXX.mp3" pattern in `item["links"][1]["href"]` (cf. ep 19, which has "Nineteen.mp3"; also many live shows)
	- not all episodes have number in `item["title"]` (cf. "One Guy, One guy, and a chicken place" episode)
	- some episodes have _neither_, especially special episodes like TAZ, Totinos
* maybe try something like: if there's a match in the digits before the .mp3, OR if there's a keyword match in the title
	- allows for numeric or keyword input (keyword will never match on \d+.mp3 but will match on title keywords)
	- does it cover all use cases?
	- certainly less of a headache than transversing lists and using indices to match up episode numbers, though
