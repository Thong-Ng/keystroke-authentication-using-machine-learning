import numpy as np
from sklearn.decomposition import PCA

# Create sample dataset
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

# Create PCA object
pca = PCA(n_components=2)  # Specify the number of components to keep

# Perform PCA
transformed_data = pca.fit_transform(data)

# Print transformed data
print(transformed_data)
