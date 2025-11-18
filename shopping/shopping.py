import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    headers = []
    with open(filename, newline = '') as file:
        shopping_data = csv.reader(file)
        headers = next(shopping_data)
        
        for row in shopping_data:
            evidence.append(interpret_evidence_row(row[0:17]))
            labels.append(interpret_labels(row[17]))
    """for row in range(0, 20):
        print(f"{evidence[row]} {labels[row]}")
    print(headers)"""
    return (evidence, labels)

def interpret_evidence_row(row):
    evidence = []
    #evidence[0] = 0
    for element in range(0,6):
        if element % 2 == 0: 
            evidence.append(int(row[element]))
        else:
            evidence.append(float(row[element]))
    for element in range(6,10):
        evidence.append(float(row[element]))
    evidence.append(interpret_month(row[10]))
    for element in range(11, 15):
        evidence.append(int(row[element]))
    returning_visitor = lambda a: 1 if a == 'Returning_Visitor' else 0
    evidence.append(returning_visitor(row[15]))
    weekend = lambda a: 1 if a == 'TRUE' else 0
    evidence.append(weekend(row[16]))
    return evidence  
def interpret_month(word):
    months = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr':4, 'May':5, 'June':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    return months[word] -1
def interpret_labels(word):
    if word == 'FALSE':
        return 0
    else:
        return 1  
    
def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    return neigh.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sens = 0
    spec = 0
    pos_count = 0
    neg_count = 0
    for number in range(0,len(labels)):
        if labels[number] == 1:
            pos_count += 1
            if labels[number] == predictions[number]:
              sens += 1
        elif labels[number] == 0:
            neg_count += 1
            if labels[number] == predictions[number]:
              spec += 1
    return (sens/pos_count, spec/neg_count)


if __name__ == "__main__":
    main()
