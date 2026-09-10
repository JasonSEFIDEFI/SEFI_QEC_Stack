# qec/syndrome.py

def geometric_syndrome(phi):

    score = sovereignty_score(phi)

    return {
        "sovereignty_error": score < 0.8,
        "warp_error": phi.warp == "X",
        "metric_error": phi.metric not in ["0", "1", "5"]
    }