# NLP - Offense Detection

### Group 07

- Carolina Rosemback - up201800171
- José Eduardo Henriques - up201806372
- Miguel Neves - up201608657

## User Manual

Open DetectOffense.ipynb in Jupyter Notebook.

### Notebook Structure

This notebook is separated in sections.

- **(1)** Dataset import, cleanup and tokenization
- **(2)** Data pre-processing *(choose one)*
  - **(2.1)** Bag of Words
  - **(2.2)** Bag of Words with Bigram
  - **(2.3)** Bag of Words with Trigram
  - **(2.4)** TF-IDF
- **(3)** Balancing of dataset and train/test/dev separation
- **(4)** Classifiers *(choose one)*
  - **(4.1)** Logistic Regression
  - **(4.2)** SVM
  - **(4.3)** Decision Tree
  - **(4.4)** Random Forest
  - **(4.5)** MLP (Neural Network)
- **(5)** User input test
  
### Usage

One must run these sequentially. Aditionally, upon changes on a given section, following sections must be re-run.  

Each classifier is separated in two parts. **(4.X.1)** One where the classifier is applied to the training set and **(4.X.2)** another where it tries to predict the result for the given set (either test or dev sets). For each classifier, one must run (4.X.1) cell **at least once** before being able to run the respective (4.X.2) cells. Aditionally, you can test each classifier on your own sentences in section (5).

If while running (4.5.3) MLP learning curve graphic an error occurs or an interruption is made, the kernel might need to be restarted.