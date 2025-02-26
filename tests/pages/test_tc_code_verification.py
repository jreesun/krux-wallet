from . import create_ctx


def test_tc_code_verification(amigo, mocker):
    from krux.pages import (
        DIGITS,
        LETTERS,
        UPPERCASE_LETTERS,
        NUM_SPECIAL_1,
        NUM_SPECIAL_2,
    )
    from krux.pages.tc_code_verification import TCCodeVerification

    cases = [
        # TC Code
        # TC Code Extended hash
        # Should pass True/False
        # Is changing TC Code True/False
        # Return TC Code single hash Hash/False
        (
            "123456",
            b"z\xc0\x99\xac\x01\x1f\xef\x91\xb6\xd5\xbd\xa8\xdc\xfc\x14\xcco-A\x9d\xba\xde\xaf\xe3\xe1{@0t\xb2\x85{",
            True,
            False,
            False,
        ),
        (
            "aBcDeF%@14",
            b"\x98\x99kJ\x03\x98r\xec \x9d\xd6\xbaG\xc2P\xbb9\x00\xe53(\x98\xb9\x1a,\x13-.\x1e\xe6Z\xc8",
            True,
            False,
            False,
        ),
        (
            "aBcDeF%@14",
            b"\x98\x99kJ\x03\x98r\xec \x9d\xd6\xbaG\xc2P\xbb9\x00\xe53(\x98\xb9\x1a,\x13-.\x1e\xe6Z\xc8",
            True,
            True,
            False,
        ),
        (
            "aBcDeF%@14",
            b"\x98\x99kJ\x03\x98r\xec \x9d\xd6\xbaG\xc2P\xbb9\x00\xe53(\x98\xb9\x1a,\x13-.\x1e\xe6Z\xc8",
            True,
            False,
            b'<9y~\xba\xfdqv\xa0\xb5\x0f\xf9v6 lht\xf4\x17\xcfmw"J\xac8bkx\xc3\xfa',
        ),
        (
            "aBcDeF%@14",
            b"\x98\x99kJ\x04\x98r\xec \x9d\xd6\xbaG\xc2P\xbb9\x00\xe53(\x98\xb9\x1a,\x13-.\x1e\xe6Z\xc8",
            False,
            False,
            False,
        ),
    ]
    for case in cases:
        mocker.patch("machine.unique_id", return_value=b"\x01" * 32)
        ctx = create_ctx(mocker, [])
        tc_verifier = TCCodeVerification(ctx)
        tc_verifier.capture_from_keypad = mocker.MagicMock(return_value=case[0])
        mocker.patch("builtins.open", mocker.mock_open(read_data=case[1]))
        if case[4]:
            assert (
                tc_verifier.capture(changing_tc_code=case[3], return_hash=True)
                == case[4]
            )
        elif case[2]:
            assert tc_verifier.capture(changing_tc_code=case[3]) == True
        else:
            assert tc_verifier.capture(changing_tc_code=case[3]) == False
        keypad_label = "Current Tamper Check Code" if case[3] else "Tamper Check Code"
        tc_verifier.capture_from_keypad.assert_called_once_with(
            keypad_label,
            [NUM_SPECIAL_1, LETTERS, UPPERCASE_LETTERS, NUM_SPECIAL_2],
        )
