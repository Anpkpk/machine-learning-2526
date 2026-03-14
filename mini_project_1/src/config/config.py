import os
import torchvision.transforms as T

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SRC_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROJECT_ROOT = os.path.dirname(_SRC_DIR)

DATASET_ROOT = os.path.join(_PROJECT_ROOT, "data", "movielens_1m")
MOVIES_PATH   = os.path.join(DATASET_ROOT, "movies.dat")
RATINGS_PATH     = os.path.join(DATASET_ROOT, "ratings.dat")