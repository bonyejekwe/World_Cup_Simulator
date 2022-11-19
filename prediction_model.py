
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report


def get_model(match_data, report=False):
    """Get the model trained on data before {year}"""
    X, y = match_data[["team_rank", "opponent_rank", "team_points", "opponent_points"]], match_data["team_won"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=6, stratify=y)

    logreg = LogisticRegression()  # LogisticRegressionCV(cv=5, random_state=0).fit(X, y)
    logreg.fit(X_train, y_train)

    if report:
        scores = cross_val_score(logreg, X_train, y_train, cv=5)
        print(f"Mean Validation accuracy: {scores.mean()}")

        y_pred = logreg.predict(X_test)
        print(f"Test data model accuracy: {logreg.score(X_test, y_test)}")
        print("\n", classification_report(y_test, y_pred))

        #t2 = X_test['team_rank'] < X_test['opponent_rank']  # t2 = -1 * np.sign(X_test['rank_diff'])
        #print("Baseline {predict higher ranked team}:\n", classification_report(y_test, t2))

    match_data = match_data.sort_values(by="date")
    return logreg, match_data
