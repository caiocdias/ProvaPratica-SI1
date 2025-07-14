import pandas as pd
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

def questao3(n_samples: int = 500, centers: int = 4, cluster_std: float = 1.5, random_state: int = 23, max_iter: int = 100) -> pd.DataFrame:
    X, _ = make_blobs(n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state)
    df = pd.DataFrame(X, columns=['x', 'y'])

    centroids = df.sample(n=centers, random_state=random_state).reset_index(drop=True)

    for _ in range(max_iter):
        for i, (cx, cy) in centroids.iterrows():
            df[f'dist_{i}'] = (df['x'] - cx)**2 + (df['y'] - cy)**2
        dist_cols = [f'dist_{i}' for i in range(centers)]
        df['cluster'] = df[dist_cols].idxmin(axis=1).str.replace('dist_', '').astype(int)

        new_centroids = df.groupby('cluster')[['x', 'y']].mean().reset_index(drop=True)
        if new_centroids.equals(centroids):
            break
        centroids = new_centroids

    df = df[['x', 'y', 'cluster']]

    plt.figure()
    for i in range(centers):
        subset = df[df['cluster'] == i]
        plt.scatter(subset['x'], subset['y'], label=f'Cluster {i}')

    plt.scatter(centroids['x'], centroids['y'], marker='X', s=200, label='Centroides')
    plt.title('K-Means Clustering - Questão 3')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    return df