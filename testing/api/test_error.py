from SHIMON.api.error import http_codes


def test_sane_http_codes() -> None:
    for num, name in http_codes.items():
        assert 100 <= num <= 500
        assert name
