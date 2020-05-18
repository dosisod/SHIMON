from SHIMON.kee import Kee

_MSG = "HELLO!"


def test_creating_key_with_bits_sets_up_class() -> None:
    assertSetup(Kee(1024))


def test_importing_key_sets_up_class() -> None:
    assertSetup(Kee.importKey(Kee(1024).private()))


def test_public_key_returns_non_empty_string() -> None:
    assert Kee(1024).pub()


def test_private_key_returns_non_empty_string() -> None:
    assert Kee(1024).private()


def test_signing_returns_ciphertext() -> None:
    assertCipher(Kee(2048).sign(_MSG))


def test_encrypting_returns_ciphertext() -> None:
    assertCipher(Kee(2048).encrypt(_MSG))


def test_decrypting_encrypted_msg() -> None:
    key = Kee(2048)

    plain = key.decrypt(key.encrypt(_MSG))

    assert plain == bytes("HELLO!", "utf-8")


def assertCipher(cipher: bytes) -> None:
    assert cipher != _MSG
    assert cipher
    assert isinstance(cipher, bytes)


def assertSetup(key: Kee) -> None:
    assert key.key
    assert key.signer
    assert key.oaep
