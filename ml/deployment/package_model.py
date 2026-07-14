from __future__ import annotations

import shutil
import tarfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHURN_ARTIFACT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "artifacts"
    / "churn"
)

MODEL_PATH = (
    CHURN_ARTIFACT_DIR
    / "churn_model.joblib"
)

INFERENCE_PATH = (
    PROJECT_ROOT
    / "ml"
    / "deployment"
    / "inference.py"
)

PACKAGE_DIR = (
    CHURN_ARTIFACT_DIR
    / "package"
)

CODE_DIR = PACKAGE_DIR / "code"

OUTPUT_PATH = (
    CHURN_ARTIFACT_DIR
    / "model.tar.gz"
)


def package_model() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing churn model: {MODEL_PATH}"
        )

    if not INFERENCE_PATH.exists():
        raise FileNotFoundError(
            f"Missing inference script: {INFERENCE_PATH}"
        )

    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)

    CODE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        MODEL_PATH,
        PACKAGE_DIR / "churn_model.joblib",
    )

    shutil.copy2(
        INFERENCE_PATH,
        CODE_DIR / "inference.py",
    )

    with tarfile.open(
        OUTPUT_PATH,
        "w:gz",
    ) as archive:
        archive.add(
            PACKAGE_DIR / "churn_model.joblib",
            arcname="churn_model.joblib",
        )

        archive.add(
            CODE_DIR,
            arcname="code",
        )

    shutil.rmtree(PACKAGE_DIR)

    print(f"Created model package: {OUTPUT_PATH}")


if __name__ == "__main__":
    package_model()