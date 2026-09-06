from core.identity_types import Phi
from qec.collapse import predict_collapse
from stack import build_identity, decode, encode, sefi_qec_pipeline
from transport.channel_models import (
    break_sovereignty,
    corrupt_authorship,
    corrupt_metric,
    corrupt_origin,
    flip_warp,
    no_noise,
)


def test_build_identity_creates_phi():
    observables = {
        "origin": "1",
        "authorship": "2",
        "sovereignty": "3",
        "warp": "4",
        "metric": "5",
    }

    phi = build_identity(observables)

    assert isinstance(phi, Phi)
    assert phi.origin == "1"
    assert phi.authorship == "2"
    assert phi.sovereignty == "3"
    assert phi.warp == "4"
    assert phi.metric == "5"


def test_codec_round_trip_preserves_phi():
    phi = Phi("1", "2", "3", "4", "5")

    encoded = encode(phi)
    decoded = decode(encoded)

    assert decoded.origin == "1"
    assert decoded.authorship == "2"
    assert decoded.sovereignty == "3"
    assert decoded.warp == "4"
    assert decoded.metric == "5"


def test_sefi_qec_pipeline_returns_result_mapping():
    observables = {
        "origin": "1",
        "authorship": "2",
        "sovereignty": "3",
        "warp": "0",
        "metric": "5",
    }

    result = sefi_qec_pipeline(observables, no_noise)

    assert set(result) >= {
        "Phi_original",
        "Phi_propagated",
        "Phi_rx",
        "Phi_corr",
        "bitstring_tx",
        "fidelity",
        "curvature_energy",
        "collapse",
        "consistency",
    }
    assert result["Phi_original"].origin == "1"
    assert result["bitstring_tx"] == result["bitstring_tx"]


def test_predict_collapse_threshold_logic():
    assert predict_collapse(0.9, 20) is False
    assert predict_collapse(0.2, 20) is True
    assert predict_collapse(0.6, 2) is False


def test_channel_models_noop_and_single_bit_flip():
    original = encode(Phi("1", "2", "3", "4", "5"))

    assert no_noise(original) == original
    assert flip_warp(original) != original
    assert flip_warp(original).split("|")[3] == "X"


def test_channel_models_corruption_regressions():
    original = encode(Phi("1", "2", "3", "4", "5"))

    assert corrupt_origin(original) != original
    assert corrupt_authorship(original) != original
    assert corrupt_metric(original) != original
    assert break_sovereignty(original) != original

    decoded_origin = decode(corrupt_origin(original))
    decoded_metric = decode(corrupt_metric(original))
    decoded_sovereignty = decode(break_sovereignty(original))

    assert decoded_origin.origin in {"0", "99"}
    assert decoded_metric.metric in {"0", "X"}
    assert decoded_sovereignty.sovereignty in {"0", "99"}


def test_decode_handles_non_pipe_bitstrings_gracefully():
    bitstring = "00010010001101000101"
    decoded = decode(bitstring)

    assert set(decoded.__dict__) == {"origin", "authorship", "sovereignty", "warp", "metric"}
    assert decoded.origin == "1"
    assert decoded.authorship == "2"
    assert decoded.sovereignty == "3"
    assert decoded.warp == "4"
    assert decoded.metric == "5"


def test_decode_handles_malformed_bit_lengths_gracefully():
    bitstrings = [
        "0001|0010|0011|01",
        "0001001000110100",
        "0001|0010|0011|0100|010",
        "|",
    ]

    for bitstring in bitstrings:
        decoded = decode(bitstring)
        assert set(decoded.__dict__) == {"origin", "authorship", "sovereignty", "warp", "metric"}
        assert all(value.isdigit() for value in decoded.__dict__.values())
        assert int(decoded.origin) >= 0
        assert int(decoded.authorship) >= 0
        assert int(decoded.sovereignty) >= 0
        assert int(decoded.warp) >= 0
        assert int(decoded.metric) >= 0


def test_decode_handles_invalid_field_values_gracefully():
    invalid_bitstrings = [
        "9999|9999|9999|9999|9999",
        "1111|abcd|0110|1010|0011",
        "zzzz|zzzz|zzzz|zzzz|zzzz",
        "0001|0010|0011|0100|X",
    ]

    for bitstring in invalid_bitstrings:
        decoded = decode(bitstring)
        assert set(decoded.__dict__) == {"origin", "authorship", "sovereignty", "warp", "metric"}
        assert all(value.isdigit() for value in decoded.__dict__.values())
        assert int(decoded.origin) <= 9
        assert int(decoded.authorship) <= 9
        assert int(decoded.sovereignty) <= 9
        assert int(decoded.warp) <= 9
        assert int(decoded.metric) <= 9


def test_pipeline_handles_channel_corruption_and_keeps_result_shape():
    observables = {
        "origin": "1",
        "authorship": "2",
        "sovereignty": "3",
        "warp": "0",
        "metric": "5",
    }

    for corruptor in (corrupt_origin, corrupt_metric, flip_warp, break_sovereignty):
        result = sefi_qec_pipeline(observables, corruptor)

        assert set(result) >= {
            "Phi_original",
            "Phi_propagated",
            "Phi_rx",
            "Phi_corr",
            "bitstring_tx",
            "fidelity",
            "curvature_energy",
            "collapse",
            "consistency",
        }
        assert isinstance(result["fidelity"], float)
        assert isinstance(result["consistency"], int)
