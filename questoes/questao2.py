import pandas as pd
from sklearn.datasets import make_moons #usado apenas para gerar os dados da questão

def questao2(n_samples: int = 500, noise: float = 0.06, eps: float = 0.2, min_samples: int = 5, random_state: int = 23) -> pd.DataFrame:
    X, _ = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)
    df = pd.DataFrame(X, columns=['x', 'y'])

    points = df[['x', 'y']].to_numpy()
    n = len(points)
    visited = [False] * n
    labels = [-1] * n
    cluster_id = 0

    neighbors = []
    for i in range(n):
        dist2 = ((points - points[i]) ** 2).sum(axis=1)
        neighbors.append({j for j, d2 in enumerate(dist2) if d2 <= eps ** 2})

    for i in range(n):
        if visited[i]:
            continue
        visited[i] = True
        nbrs = neighbors[i]
        if len(nbrs) < min_samples:
            labels[i] = -1
        else:
            cluster_id += 1
            labels[i] = cluster_id
            seeds = nbrs - {i}
            while seeds:
                j = seeds.pop()
                if not visited[j]:
                    visited[j] = True
                    new_nbrs = neighbors[j]
                    if len(new_nbrs) >= min_samples:
                        seeds |= new_nbrs
                if labels[j] == -1:
                    labels[j] = cluster_id

    df['cluster'] = labels
    return df