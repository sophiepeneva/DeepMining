import random
import numpy as np


class Politician:
    def __init__(self, party, votes):
        self.party = party
        self.votes = votes


def split_data(data, k=10):
    random.shuffle(data['republican'])
    random.shuffle(data['democrat'])
    return {
        'republican': np.array_split(data['republican'], k),
        'democrat': np.array_split(data['democrat'], k)
    }
    return np.array_split(data, k)


def get_probabilities(distances, k_nearest_indices, train_data):
    probabilities = {
        'republican': 0,
        'democrat': 0
    }
    for index in k_nearest_indices:
        probabilities[train_data[index].party] += 1 / distances[index]
    return probabilities


def get_label_from_probabilities(probabilities):
    return max(probabilities, key=probabilities.get)


def get_vote_count(data):
    vote_count = {
        'republican': [],
        'democrat': [],
        'all': []
    }
    for i in data:
        for j, vote in enumerate(i.votes):
            if(len(vote_count[i.party]) <= j):
                vote_count[i.party].append({})
            if(len(vote_count['all']) <= j):
                vote_count['all'].append({})
            vote_count[i.party][j][vote] = 1 if vote not in vote_count[i.party][j] else vote_count[i.party][j][vote] + 1
            vote_count['all'][j][vote] = 1 if vote not in vote_count['all'][j] else vote_count['all'][j][vote] + 1
    return vote_count


def get_class_probabilities(data):
    vote_count = get_vote_count(data)
    reps = sum(p.party == "republican" for p in data)
    dems = sum(p.party == "democrat" for p in data)
    probs = {}
    for key in vote_count:
        curr_probs = [{option: (votes[option] / sum(votes.values()))
                       for option in votes} for votes in vote_count[key]]
        probs[key] = curr_probs
    return probs, reps/(reps+dems), dems/(reps+dems)


def beyes(probs, votes, reps, dems):
    rep = 1
    dem = 1
    all = 1
    for i, vote in enumerate(votes):
        rep *= 0 if vote not in probs['republican'][i] else probs['republican'][i][vote]
        dem *= 0 if vote not in probs['democrat'][i] else probs['democrat'][i][vote]
        all *= 0 if vote not in probs['all'][i] else probs['all'][i][vote]
    return {
        'republican': (rep*reps)/all,
        'democrat': (dem*dems)/all
    }


def predict_labels(train_data, test_data):
    probs, reps, dems = get_class_probabilities(train_data)
    predictions = []
    for politician in test_data:
        res = beyes(probs, politician.votes, reps, dems)
        predictions.append(get_label_from_probabilities(res))

    return predictions


if __name__ == "__main__":
    f = open("house-votes-84.data", "r")
    politicians = {
        'republican': [],
        'democrat': []
    }

    for x in f:
        line = x.rstrip("\n").split(",")
        politicians[line[0]].append(Politician(line[0], line[1:]))

    split_data = split_data(politicians)
    avg = 0
    for test_index in range(10):
        test_data = [*split_data['democrat'][test_index],
                     *split_data['republican'][test_index]]
        train_data = []
        for i in range(10):
            if i != test_index:
                train_data = [*train_data, *split_data['republican']
                              [i], *split_data['democrat'][i]]
        predictions = predict_labels(train_data, test_data)
        correct = 0
        for i, j in enumerate(predictions):
            if(j == test_data[i].party):
                correct += 1
        acc = correct/len(predictions)*100
        print('Current accuracy : {:f}'.format(acc))
        avg += acc
    print('Average accuracy : {:f}'.format(avg/10))