=======
History
=======

0.1.0 (2019-03-13)
------------------

* First release on PyPI.


0.2.0 (2019-03-20)
------------------
* Completed the Tweet class that allows the user to make usable instances of a
  tweet model. Includes initialization of all the Tweet attributes indicated in
  the Twitter documentation (default to None, unless the user provides a value)
  and overriding of __getitem__ to provide a dictionary-like access to the
  information.


0.3.0 (2019-03-20)
------------------
* Added method "get_tweets_from_csv()", which gets a CSV file as an argument
  and returns a list containing as many Tweet objects as lines (minus the
  header) in the CSV file. The header of the CSV is used to know which 
  attributes should be set.
* The method will raise an error and exit if any item in the header does not
  match with the specification of the Tweet object (for example, the header
  word "media.sizes.thumb.h" would be valid, but "user.lightsaber.color" would
  not.
* At this point, the method took 1.75s aprox to read and return the contents of
  a 5.7 MB as a list of 'Tweet's. This could be troublesome with very large
  collections in a future if the progression of time was proportional with the 
  file size (estimation would be 25 minutes for a 5 GB file)
