# Machine Learning Fundamentals

Machine learning enables computers to learn from data without explicit programming.

## Types of Machine Learning

### Supervised Learning

Learning from **labeled data** to make predictions.

#### Classification

Predicting discrete categories:

- **Binary Classification**: Yes/No, True/False
- Multi-class Classification: Multiple categories
- Multi-label Classification: Multiple labels per instance

**Popular Algorithms:**
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)
- Neural Networks

#### Regression

Predicting continuous values:

- Linear Regression
- Polynomial Regression
- Ridge and Lasso Regression

### Unsupervised Learning

Finding patterns in **unlabeled data**.

#### Clustering

Grouping similar data points:

- **K-Means**: Partition-based clustering
- **Hierarchical Clustering**: Tree-like structure
- DBSCAN: Density-based clustering
- Gaussian Mixture Models

#### Dimensionality Reduction

Reducing the number of features:

- **PCA** (Principal Component Analysis)
- t-SNE: Visualization
- Autoencoders

### Reinforcement Learning

Learning through **rewards and penalties**.

- Agent interacts with environment
- Learns optimal policy
- Applications: Game AI, Robotics, Self-driving cars

**Key Concepts:**
- State and Action
- Reward Signal
- Q-Learning
- Deep Q-Networks (DQN)

## Model Training Process

1. **Data Collection**: Gather relevant data
2. **Data Preprocessing**: Clean and transform
3. **Feature Engineering**: Create meaningful features
4. **Model Selection**: Choose appropriate algorithm
5. **Training**: Fit model to data
6. **Evaluation**: Assess performance
7. **Tuning**: Optimize hyperparameters

## Evaluation Metrics

### Classification Metrics

- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- ROC-AUC: Area under the curve

### Regression Metrics

- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **MAE** (Mean Absolute Error)
- R² Score

## Overfitting and Underfitting

### Overfitting

Model learns training data **too well**, including noise.

**Solutions:**
- More training data
- Regularization (L1, L2)
- Dropout
- Early stopping
- Cross-validation

### Underfitting

Model is **too simple** to capture patterns.

**Solutions:**
- More complex model
- More features
- Less regularization

## Feature Engineering

Creating new features to improve model performance:

- **Scaling**: Normalization, Standardization
- **Encoding**: One-hot encoding, Label encoding
- **Transformation**: Log, Square root
- **Interaction Features**: Combining features

## Popular Libraries

- **scikit-learn**: Traditional ML algorithms
- **TensorFlow**: Deep learning framework
- **PyTorch**: Research-focused deep learning
- **XGBoost**: Gradient boosting
- **LightGBM**: Fast gradient boosting
