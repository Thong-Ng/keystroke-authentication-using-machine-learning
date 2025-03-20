from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import RandomForest


# Create a Random Forest classifier with a specific max_depth value
min_samples_split  = 3  # Adjust this value as needed
rf_model = RandomForestClassifier(n_estimators=100, min_samples_split =min_samples_split , random_state=42)

# Fit the model on your training data
rf_model.fit(preprocess.X_train, preprocess.y_train)

# Evaluate the model's performance on validation or test data
accuracy = rf_model.score(preprocess.X_test, preprocess.y_test)
print(f"Validation Accuracy with max_depth={min_samples_split }: {accuracy:.4f}")

