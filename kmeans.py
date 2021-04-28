import numpy as np
import math
import random
import matplotlib.pyplot as plt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dist(self, p):
        return math.sqrt(abs(self.x - p.x)**2 + abs(self.y - p.y)**2)


class Kmeans:

    def __init__(self, n_clusters, max_iter=100, random_restart=1000):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_restart = random_restart

    def get_centroids(self, data):
        return data[random.sample(range(len(data)), self.n_clusters)]

    def compute_centroids(self, data, labels):
        centroids = []
        coords = np.array([[p.x, p.y] for p in data])
        for i in range(self.n_clusters):
            mean = np.mean(coords[labels == i], axis=0)
            centroids.append(Point(mean[0], mean[1]))
        return centroids

    def get_distances_to_centroid(self, centroid, data):
        return [point.get_dist(centroid) for point in data]

    def compute_distances(self, data, centroids):
        distances = np.zeros((len(data), self.n_clusters))
        for k in range(self.n_clusters):
            distances_to_centroid = self.get_distances_to_centroid(
                centroids[k], data)
            distances[:, k] = distances_to_centroid
        return distances

    def find_closest_cluster(self, distances):
        return np.argmin(distances, axis=1)

    def compute_var(self, labels, distances):
        return [np.sum(np.square([distances[labels == i][:, i]])) for i in range(self.n_clusters)]

    def fit(self, X):
        best_var = float('inf')
        for t in range(self.random_restart):
            self.centroids = self.get_centroids(X)
            for i in range(self.max_iter):
                old_centroids = self.centroids
                distances = self.compute_distances(X, old_centroids)
                self.labels = self.find_closest_cluster(distances)
                self.centroids = self.compute_centroids(X, self.labels)
                if np.all(old_centroids == self.centroids):
                    break
            var = self.compute_var(self.labels, distances)
            if np.mean(var) < best_var:
                self.best_centroids = self.centroids
                best_var = np.mean(var)

    def predict(self, data):
        distances = self.compute_distances(data, self.best_centroids)
        return self.find_closest_cluster(distances)

if __name__ == "__main__":
    file = "unbalance.txt"
    n_clusters = 8
    f = open(file, "r")
    points = []

    for x in f:
        line = x.split()
        points.append(Point(float(line[0]), float(line[1])))
    # Plot the data
    plt.scatter([p.x for p in points], [p.y for p in points])
    plt.title('Visualization of raw data')
    plt.show()

    km = Kmeans(n_clusters=8, max_iter=100)
    points = np.array(points)
    km.fit(points)
    centroids = km.centroids

    labels = km.predict(points)
    cls = []
    for i in range(n_clusters):
        clx = [p.x for p in points[labels == i]]
        cly = [p.y for p in points[labels == i]]
        cls.append([clx, cly])
        
    for i in range(n_clusters):
        plt.scatter(cls[i][0], cls[i][1])
    plt.show()