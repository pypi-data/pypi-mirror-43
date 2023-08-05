def co_occurence_matrix(list_of_words, preprocessed_reviews, window_size=5):
  '''
  Function which takes list of words and preprocessed_reviews as the inputs and
  returns the co_occurence_matrix.
  Args:
    list_of_words: A list of words for which the co-occurence matrix is required.
    preprocessed_reviews: A list of all the preprocessed reviews for which the co-occurence matrix is required.
    window_size: Suitable window size for which the co-occurence matrix is required.
  Returns:
    cooc: The calculated co-occurence matrix.
  '''
  import numpy as np
  from tqdm import tqdm
  if not isinstance(list_of_words, list):
    raise TypeError("Please provide a list argument.")
  if not isinstance(preprocessed_reviews, list):
      raise TypeError("Please provide a list argument.")
  if not isinstance(window_size, int):
      raise TypeError("Please provide a integer argument.")
  cooc = np.zeros((len(list_of_words), len(list_of_words)),np.float64)
  list_of_words_dict = {list_of_words[i]:i for i in range(len(list_of_words))}

  for i in tqdm(list_of_words_dict.keys()):
    for j in preprocessed_reviews:
        j = j.split()
        if str(i) not in j:
          continue
        else:
          for x in list_of_words_dict.values():
            if abs(list_of_words_dict[i]-x)<window_size:
              cooc[list_of_words_dict[i],x]+=1
  return cooc     
