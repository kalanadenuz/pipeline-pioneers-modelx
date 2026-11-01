"""Fast Gradient Boosted Hydrological Decision Tree Ensemble."""
import numpy as np
import pandas as pd
from typing import List

class DecisionNode:
    def __init__(self, feature: int = None, threshold: float = None, left=None, right=None, value: float = None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    @property
    def is_leaf(self) -> bool:
        return self.value is not None

class FastRegressionTree:
    def __init__(self, max_depth: int = 4, min_samples_split: int = 10):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X: np.ndarray, residuals: np.ndarray, sample_weights: np.ndarray = None):
        self.root = self._build_tree(X, residuals, depth=0, weights=sample_weights)

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int, weights: np.ndarray = None) -> DecisionNode:
        n_samples, n_features = X.shape
        if depth >= self.max_depth or n_samples < self.min_samples_split or np.all(y == y[0]):
            val = float(np.average(y, weights=weights)) if weights is not None else float(np.mean(y))
            return DecisionNode(value=val)

        best_feat, best_thresh, best_gain = None, None, -1.0
        current_variance = np.var(y) * n_samples
        features_to_check = range(n_features)

        for feat in features_to_check:
            col_vals = X[:, feat]
            thresholds = np.percentile(col_vals, [40, 60, 75, 88, 94, 98])
            for thresh in thresholds:
                left_mask = col_vals <= thresh
                right_mask = ~left_mask
                if np.sum(left_mask) < 4 or np.sum(right_mask) < 4:
                    continue
                left_var = np.var(y[left_mask]) * np.sum(left_mask)
                right_var = np.var(y[right_mask]) * np.sum(right_mask)
                gain = current_variance - (left_var + right_var)
                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat
                    best_thresh = thresh

        if best_gain <= 0 or best_feat is None:
            val = float(np.average(y, weights=weights)) if weights is not None else float(np.mean(y))
            return DecisionNode(value=val)

        left_mask = X[:, best_feat] <= best_thresh
        w_left = weights[left_mask] if weights is not None else None
        w_right = weights[~left_mask] if weights is not None else None
        left_node = self._build_tree(X[left_mask], y[left_mask], depth + 1, w_left)
        right_node = self._build_tree(X[~left_mask], y[~left_mask], depth + 1, w_right)
        return DecisionNode(feature=best_feat, threshold=best_thresh, left=left_node, right=right_node)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._predict_row(row, self.root) for row in X])

    def _predict_row(self, row: np.ndarray, node: DecisionNode) -> float:
        if node.is_leaf:
            return node.value
        if row[node.feature] <= node.threshold:
            return self._predict_row(row, node.left)
        return self._predict_row(row, node.right)

class HydroBoostRegressor:
    def __init__(self, n_estimators: int = 25, learning_rate: float = 0.18, max_depth: int = 4, random_state: int = 42):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        self.trees: List[FastRegressionTree] = []
        self.base_pred = 0.0
        self.feature_names_: List[str] = []
        self.feature_importances_: np.ndarray = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        np.random.seed(self.random_state)
        self.feature_names_ = list(X.columns)
        X_mat = X.values
        y_vec = y.values
        n_samples, n_features = X_mat.shape

        sample_weights = 1.0 + 3.0 * (y_vec > 0.35).astype(float) + 6.0 * (y_vec > 0.70).astype(float)
        self.base_pred = float(np.average(y_vec, weights=sample_weights))
        residuals = y_vec - self.base_pred

        self.trees = []
        feat_counts = np.zeros(n_features)
        for _ in range(self.n_estimators):
            tree = FastRegressionTree(max_depth=self.max_depth, min_samples_split=8)
            tree.fit(X_mat, residuals, sample_weights=sample_weights)
            self.trees.append(tree)
            pred_step = tree.predict(X_mat)
            residuals -= self.learning_rate * pred_step
            self._accumulate_importances(tree.root, feat_counts)

        total = np.sum(feat_counts)
        self.feature_importances_ = feat_counts / (total if total > 0 else 1.0)
        return self

    def _accumulate_importances(self, node: DecisionNode, counts: np.ndarray):
        if node is None or node.is_leaf:
            return
        counts[node.feature] += 1
        self._accumulate_importances(node.left, counts)
        self._accumulate_importances(node.right, counts)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        X_mat = X[self.feature_names_].values if isinstance(X, pd.DataFrame) else np.array(X)
        y_pred = np.full(len(X_mat), self.base_pred)
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(X_mat)
        return np.maximum(0.0, y_pred)


        # Subsample feature splits for ensemble diversity


    # Gradient boosting residual updates with shrinkage factor
