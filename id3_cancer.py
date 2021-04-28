import math
import numpy as np
from collections import deque
import random 

class Node:
    def __init__(self, value=None, children={}, next = None):
        self.value = value
        self.next = None
        self.children = children

def split_data(values, lables, k=10):
    data = {label : [i for i in range(len(lables)) if lables[i] == label] for label in set(lables)}
    split_indices = {}
    for key in data: 
        random.shuffle(data[key])
        split_indices[key] = np.array_split(data[key], k)
    stacked = np.column_stack(list(split_indices.values()))
    s = [np.concatenate(i) for i in stacked]
    split_values = [[values[j] for j in s[i]] for i in range(k)]
    split_lables = [[lables[j] for j in s[i]] for i in range(k)]
    return split_values, split_lables

class DecisionTreeClassfier:

    def __init__(self, attribute_names, results, attribute_values):
        self.attribute_names = attribute_names
        self.results = results
        self.attribute_values = attribute_values
        indices = [x for x in range(len(results))]
        self.entropy = self.get_entropy(indices)
        self.root = Node()

    def get_entropy(self, indices):
        results = [self.results[i] for i in indices]
        result_types_count = [results.count(x) for x in self.results]
        entropy = sum([-count / len(indices) * math.log(count /
                                                        len(indices), 2) if count else 0 for count in result_types_count])
        return entropy

    def get_information_gain(self, indices, attribute_id):
        info_gain = self.get_entropy(indices)
        x_features = [self.attribute_values[x][attribute_id] for x in indices]
        feature_vals = list(set(x_features))
        feature_vals_count = [x_features.count(x) for x in feature_vals]
        feature_vals_id = [
            [indices[i]
            for i, x in enumerate(x_features)
            if x == y]
            for y in feature_vals
        ]

        info_gain = info_gain - sum([val_counts / len(indices) * self.get_entropy(val_ids)
                                     for val_counts, val_ids in zip(feature_vals_count, feature_vals_id)])

        return info_gain

    def get_attribute_max_information_gain(self, indices, attribute_ids):
        entropy_per_attribute = [self.get_information_gain(indices, attr_id) for attr_id in attribute_ids]
        max_id = attribute_ids[entropy_per_attribute.index(max(entropy_per_attribute))]
        return self.attribute_names[max_id], max_id

    def id3(self):
        indices = [x for x in range(len(self.attribute_values))]
        attribute_ids = [x for x in range(len(self.attribute_names))]
        self.root = self.id3_recv(indices, attribute_ids, self.root)

    def id3_recv(self, indices, attribute_ids, node):
        current_results = [self.results[x] for x in indices]
        if len(set(current_results)) == 1:
            node.value = self.results[indices[0]]
            return node
        if len(attribute_ids) == 0:
            node.value = max(set(current_results), key=current_results.count)  # compute mode
            return node
        best_attribute_name, best_attribute_id = self.get_attribute_max_information_gain(indices, attribute_ids)
        node.value = best_attribute_name
        attribute_values = list(set([self.attribute_values[x][best_attribute_id] for x in indices]))
        for value in attribute_values:
            child = Node()
            node.children[value] = child
            child_indices = [x for x in indices if self.attribute_values[x][best_attribute_id] == value]
            if not child_indices:
                child.value = max(set(current_results), key=current_results.count)
                print('')
            else:
                if attribute_ids and (best_attribute_id in attribute_ids):
                    to_remove = attribute_ids.index(best_attribute_id)
                    attribute_ids.pop(to_remove)
                child = self.id3_recv(child_indices, attribute_ids, child)
        return node

    def predict(self, test_values):
        predictions = []
        for value in test_values:
            node = self.root
            while node and node.value in self.attribute_names:
                idx = self.attribute_names.index(node.value)
                x = value[idx]
                if x not in node.children:
                    node = None
                    break
                node = node.children[x]
            if node:
                predictions.append(node.value)
            else:
                predictions.append('?')
        return predictions


if __name__ == "__main__":
    f = open("breast-cancer.data", "r")

    attributes = ['class', 'age', 'menopause', 'tumor-size',
                  'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad']

    attribute_values = [set() for i in range(9)]
    X = []
    Y = []
    for x in f:
        line = x.rstrip("\n").split(",")
        Y.append(line[len(line) - 1].upper())
        X.append(line[:len(line) - 1])

    split_values, split_lables = split_data(np.array(X), np.array(Y))
    avg = 0
    for test_index in range(10):
        test_values = split_values[test_index]
        test_lables = split_lables[test_index]
        train_values = []
        train_lables = []
        for i in range(10):
            if i != test_index:
                train_values = [*train_values, *split_values[i]]
                train_lables = [*train_lables, *split_lables[i]]
        tree = DecisionTreeClassfier(attributes, train_lables, train_values)
        tree.id3()
        predictions = tree.predict(test_values)
        correct = 0
        for i, j in enumerate(predictions):
            if(j == test_lables[i]):
                correct += 1
        acc = correct/len(predictions)*100
        print('Current accuracy : {:f}'.format(acc))
        avg += acc
    print('Average accuracy : {:f}'.format(avg/10))
