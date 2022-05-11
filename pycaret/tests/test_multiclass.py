import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import pandas as pd
import pytest

import pycaret.classification
import pycaret.datasets


def test():
    # loading dataset
    data = pycaret.datasets.get_data("iris")
    assert isinstance(data, pd.DataFrame)

    # init setup
    clf1 = pycaret.classification.setup(
        data,
        target="species",
        log_experiment=True,
        silent=True,
        html=False,
        session_id=123,
        n_jobs=1,
    )

    # compare models
    top3 = pycaret.classification.compare_models(errors="raise", n_select=100)[:3]
    assert isinstance(top3, list)

    # tune model
    tuned_top3 = [pycaret.classification.tune_model(i) for i in top3]
    assert isinstance(tuned_top3, list)

    # ensemble model
    bagged_top3 = [pycaret.classification.ensemble_model(i) for i in tuned_top3]
    assert isinstance(bagged_top3, list)

    # blend models
    blender = pycaret.classification.blend_models(top3)

    # stack models
    stacker = pycaret.classification.stack_models(estimator_list=top3)
    predict_holdout = pycaret.classification.predict_model(stacker)

    # plot model
    lr = pycaret.classification.create_model("lr")
    pycaret.classification.plot_model(lr, save=True, scale=5)

    # select best model
    best = pycaret.classification.automl(optimize="MCC")

    # hold out predictions
    predict_holdout = pycaret.classification.predict_model(best)
    assert isinstance(predict_holdout, pd.DataFrame)

    # predictions on new dataset
    predict_holdout = pycaret.classification.predict_model(
        best, data=data.drop("species", axis=1)
    )
    assert isinstance(predict_holdout, pd.DataFrame)

    # calibrate model
    calibrated_best = pycaret.classification.calibrate_model(best)

    # finalize model
    final_best = pycaret.classification.finalize_model(best)

    # save model
    pycaret.classification.save_model(best, "best_model_23122019")

    # load model
    saved_best = pycaret.classification.load_model("best_model_23122019")

    # returns table of models
    all_models = pycaret.classification.models()
    assert isinstance(all_models, pd.DataFrame)

    # get config
    X_train = pycaret.classification.get_config("X_train")
    X_test = pycaret.classification.get_config("X_test")
    y_train = pycaret.classification.get_config("y_train")
    y_test = pycaret.classification.get_config("y_test")
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

    # set config
    pycaret.classification.set_config("seed", 124)
    seed = pycaret.classification.get_config("seed")
    assert seed == 124

    assert 1 == 1


if __name__ == "__main__":
    test()
