import pytest
from .shared_mocks import MockFile, mock_open

WSH_MULTISIG = "wsh(sortedmulti(2,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*,[8cb36b38/48h/1h/0h/2h]tpubDESTVwqbbaSoN2mPq7tcWkPBpRBkaEADrUzUhRTVnNef6oVn6w2PHL4zoUjUAJSPLJQRBetkgX4sDRcoaCyFHxqHGyWyaiV8REKDkh7zQac/<0;1>/*,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*))#jpxgnm0a"
WSH_MINISCRIPT = "wsh(or_d(pk([73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*),and_v(v:pkh([02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*),older(65535))))#466dtswe"
TR_MINISCRIPT = "tr([73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*,and_v(v:pk([02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*),older(6)))#rfuhsd9c"
TR_EXP_MULTI_MINISCRIPT = "tr(tpubD6NzVbkrYhZ4YYQjuKXFp85eRGCk4oA94MXbbHJW6zNAibMfkwZh7JQNVHEhpcQYaRCUs3b5PhvKPKESGoAJptiLvF8Rm1jhoFsryyFuR1P/<0;1>/*,{and_v(v:multi_a(2,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<2;3>/*,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<2;3>/*,[8cb36b38/48h/1h/0h/2h]tpubDESTVwqbbaSoN2mPq7tcWkPBpRBkaEADrUzUhRTVnNef6oVn6w2PHL4zoUjUAJSPLJQRBetkgX4sDRcoaCyFHxqHGyWyaiV8REKDkh7zQac/<0;1>/*),older(6)),multi_a(2,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*)})#6ga85u82"


@pytest.fixture
def tdata(mocker):
    from collections import namedtuple
    from ur.ur import UR
    from urtypes.crypto.psbt import PSBT
    from krux.bbqr import encode_bbqr

    TEST_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    TEST_MNEMONIC_BIP85_I0 = "prosper short ramp prepare exchange stove life snack client enough purpose fold"

    # Legacy Singlesig
    P2PKH_PSBT = b'psbt\xff\x01\x00\xa4\x02\x00\x00\x00\x03\xae\xe25\xaf(\x9a\xc9\xee\xc23\xca"\x15\xbf?\xf4\xc1\xcaxAP\xd6\x0f[\x94kA\x87\x8b\x15\x04,\x00\x00\x00\x00\x00\xfd\xff\xff\xffT\xc9\x91i\xc4ZIg Z!\xd6)\xbf+z\x161\xc4uoS \xf0\x9d\x96\xcf#\xdc\xdbc\xa0\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x04\x1eVt\x8d\x80H\x1f\x89k\x07T(\xca\xaf\x91\x1e"\x1a2\xef\xa5_\\s\xf9\x8b\xc2J\xa0\xc8\x11\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x01\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hlZ\x0f+\x00O\x01\x045\x87\xcf\x03\x06\xb07\xf6\x80\x00\x00\x00k"\xc5\x12;\xa1\n\xde\xafK\xfc\xbbE\xd1\xa0-\x82\x8f%\xbf\x86F\x95z\x98\xd0b\x87\xc4\xe2\xb8P\x02\x8bB\xcdGv7l\x82y\x1bIAU\x15\x1fV\xc2\xd7\xb4q\xe0\xc7\xa5&\xa7\xce`\xdd\x87.8g\x10s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x01\x00~\x02\x00\x00\x00\x02\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x02\x00\x00\x00\x00\xfd\xff\xff\xff\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01@\x07\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xacZ\x0f+\x00\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00U\x02\x00\x00\x00\x01\x873 i\xd7\x11\xa7\xcd*`\xd5\x84\x1c8\n,U\xe8\xa2\n\xdd\xdaV\xa2\x9c\x00\x84e\xef\xf6[\xa2\x01\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00U\x02\x00\x00\x00\x01\x05j\xc0\xa7"\x1f\xe5\x82x\xc9\xa7h\xd0\x1a!\xe6\xb6GJ\x01\x9a\xf6\xe7?\x08\xc8R\xe6\x86|\xad\xa5\x00\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    P2PKH_PSBT_B43 = "GG*F8Q17IWZRLD2-18VY*1TXTGM*I+$R6ZULQ0*57H0JP/$S*/1MU2DNKKAF2TQ9DRXY:RGZ78NURNB7C8TK6LY29E7BIE9G7.99+L1U.2/PW68CG$AUH-2.S2YIFN9UQT4XMR5M1$TT5W+YR3U+XG:5RG/F+V5+4J9AFUW.ZE:YFX+/SE8T0MVUG5GR--W:9:7.ZRXCXM+$0JI:VPIF5GRR4K.LYVYRHR6C532UV++/AXRKCDNXT8CO-UZ+C4:XA/5SWA/Q.1G*.QAINY88NQ4JI-/7V+AW/Y9DFHU/L8FHLI0NRJI2C5$R1P2NS37$-K9-C-2-*5JJP.0:GD:B4D9.336TSMF*09EV4H+N-ZZXFV57+Z*GO-QTKZZ4R$9LCG+N97G-VOG:UCSKQTH.Y7O/RHS3LBM*/I+CFV2QODT7SJA*9N47MGX*Z/X4ZY2OY2-0TH7JKSU$ZTTB32Y4L0BKQCF*41$KFA1PEO2*/4+3$YV9/$DN*OZIO9Q:/HI7$94Q::8C9AG9U-/3UFQVJ94BZY*8DMT5QDBY4207KE12IKKWWYHN7+1.T*QVQYHQ2.Y-+VSM21FIB9CG4.63.I-OLBT-/M28*O-6+*DQV9HB-J/HEXIE.7$0H.UPJPRNIE.8TEYQCDYDPE9Q0E0D+HYP8YMJF2ODHGAT/E15-X:J.4J9P3Z-2R4:L2-S6CX7LF+I3A35M.BYF/XQLAJX92G1A-R0FF036U4Y2BKSI*/LAXWO9Q4KQBGJRLF:WZOE-:L76F2LJ5/-25TK7H$PMZON1AK735JQ0U9YZTLE$WMT.APZ65T8FR$NC9ZBXI46$B5-IG0$D8I-LF:TZCBJ81/0:V4$4*QX84ZP$Q/4120FZS:98YODBIL5W+EZ-+AXSPEW9/L+8Q0SGV*AX:8PSOAX+17:O+4V*7RA8YHD3OO-$57XMH7QH5TGCVBJHLZWQDI0*2VP6-5XNSK187-Y1C747124EI4B/XO3Z+-126R.5RA1.74WBV2DF:ECPVXEOXHPPAMP3ARKRH.IZQ.CQP9IKZN6+Z70WY+X:QSFHQFQJ-OZTM5F**E+KL4W:RE7OCI4ZC8SOEF89T5AA1O8XZGYZ*Q5AJSF2NQHE3H8DF-1S$GWHKFQX5JX0YWUV$"
    P2PKH_PSBT_B58 = "23c6ymBTk6EPbwvP3j8ozTBrkZ8TSBgW19wbakNqZTW8m7ac1XmyY8j9F7PezXGAa28kf8hdq2wF75LZhJWUNaCEwKMomEaRqcQwAfVXkTF9CzhGFtTv8XdhY7Xe8j1Phj9zJFCQ8MJ2d9Eb8kmRGmA6BcPHArVe9c5UrxQrUoXw3nJeLyGELYm6sd2bcu3gotYTejiJW2r3YcYxwnpKN32G9PsAeZ6oULLWG4rH7tKCUMWZkrPiQKdviZkpXJj3KybK21RsZCyvJnqWtCMKZBjE55TXkfWM3EC9TAStk2n85o72v2chGwJojXDdET4ZWpZgX9Qzfh9C24nsbedTGq1zNECwpbdvz43VUjz7LUtzNcfHhYipk6hD69he4dwFM4ACE2prm7b7wwmqonN7JMt59v1oZpDRphXbRxxPNvdao2kryGfrzhrk4H1UJWPouoUA7QaNW3wYENFHafw6cLyuQAETZ8RCYN2gujxw5QNZLSGB4HiKvPY1aQK6rvnE9DsiTzhEs5Rbrsd3H9BfRxoerAbUN4zxYPmgosrTNwnpDUtHvr2n6c1qGBJTu4o3wLHfm6VpyWiLrK9eissxhqAAuB2CnmdKhQq5t1RLDykYVbhJPCKzwchWr75jmAPKJRzAfZ7GUXx49YqdKcDtkJiRxHRUChh5ww2zYo8TpjHMAbHELosS7GsLhnzzPsyDnVPFaxWYwV6R7pFfZHXgMjp8zE6yEnHXoFvfNVegGFC9hnJgHm3VWw6k1cGKnh78kpW9pXih4GhV2KN6DueSonRtY6gVqVMp8jbtoXohr1vHuBag1VMvntfnFJDorjb1dtwRfbZ6bVNmY1C1efiwmF433hyEEbXPS477F2teZ2Guhj7EuEF785WxENndw27Knh4Z5DjStX9i7busoyFnE2vtZgEhrioa5cipTvaMins89yxSVNMJXf1aq6HCkqhE6p3seBPodq26KoJZNAB9qx4KhQpobGiM2y1bdpxourumW8cWJAWEJS1bFfJUSAH8b7u4y3DvxMYMpK3AjE1CqGtLECiyuikMwekuHtXTJX"
    P2PKH_PSBT_B64 = "cHNidP8BAKQCAAAAA67iNa8omsnuwjPKIhW/P/TBynhBUNYPW5RrQYeLFQQsAAAAAAD9////VMmRacRaSWcgWiHWKb8rehYxxHVvUyDwnZbPI9zbY6AAAAAAAP3///8EHlZ0jYBIH4lrB1Qoyq+RHiIaMu+lX1xz+YvCSqDIEQAAAAAA/f///wHoAwAAAAAAABYAFK7NHtw+/2WqIJ0CFec9cJBdwWhsWg8rAE8BBDWHzwMGsDf2gAAAAGsixRI7oQrer0v8u0XRoC2CjyW/hkaVepjQYofE4rhQAotCzUd2N2yCeRtJQVUVH1bC17Rx4MelJqfOYN2HLjhnEHPF2gosAACAAQAAgAAAAIAAAQB+AgAAAAKam+HKKRBcl3Q8D9HuecDmDSKKYcjsv3T558/6ARkMewIAAAAA/f///5qb4copEFyXdDwP0e55wOYNIophyOy/dPnnz/oBGQx7AQAAAAD9////AUAHAAAAAAAAGXapFDotQUWk8JhSOz6BJ/Hah8/FW455iKxaDysAAQMEAQAAACIGAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WGHPF2gosAACAAQAAgAAAAIAAAAAAAAAAAAABAFUCAAAAAYczIGnXEafNKmDVhBw4CixV6KIK3dpWopwAhGXv9luiAQAAAAD/////AQAAAAAAAAAAGXapFDotQUWk8JhSOz6BJ/Hah8/FW455iKwAAAAAAQMEAQAAACIGAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WGHPF2gosAACAAQAAgAAAAIAAAAAAAAAAAAABAFUCAAAAAQVqwKciH+WCeMmnaNAaIea2R0oBmvbnPwjIUuaGfK2lAAAAAAD/////AQAAAAAAAAAAGXapFDotQUWk8JhSOz6BJ/Hah8/FW455iKwAAAAAAQMEAQAAACIGAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WGHPF2gosAACAAQAAgAAAAIAAAAAAAAAAAAAA"
    P2PKH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2PKH_PSBT).to_cbor())

    SIGNED_P2PKH_PSBT = b'psbt\xff\x01\x00\xa4\x02\x00\x00\x00\x03\xae\xe25\xaf(\x9a\xc9\xee\xc23\xca"\x15\xbf?\xf4\xc1\xcaxAP\xd6\x0f[\x94kA\x87\x8b\x15\x04,\x00\x00\x00\x00\x00\xfd\xff\xff\xffT\xc9\x91i\xc4ZIg Z!\xd6)\xbf+z\x161\xc4uoS \xf0\x9d\x96\xcf#\xdc\xdbc\xa0\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x04\x1eVt\x8d\x80H\x1f\x89k\x07T(\xca\xaf\x91\x1e"\x1a2\xef\xa5_\\s\xf9\x8b\xc2J\xa0\xc8\x11\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x01\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hlZ\x0f+\x00\x00\x01\x00~\x02\x00\x00\x00\x02\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x02\x00\x00\x00\x00\xfd\xff\xff\xff\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01@\x07\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xacZ\x0f+\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 \x14\x1e\xa4X\xff>l\x9d\xd8Dg\xda\xaf\x1b\xba9B\x94@eb\xbc\xb3\\\xe4\xa5O:N\xc8\x9c\xeb\x02 /\xa3%\xb6Qw\x8e\x1c\xda\xca\r\xa0\xb1,,ZCL\xa320u\xd5\xc7gT\'+\x82\x80\x00\xe5\x01\x00\x01\x00U\x02\x00\x00\x00\x01\x873 i\xd7\x11\xa7\xcd*`\xd5\x84\x1c8\n,U\xe8\xa2\n\xdd\xdaV\xa2\x9c\x00\x84e\xef\xf6[\xa2\x01\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 a\xf4`\xa5W\xbd\xc5+\xa4\xaej\xfd\xf5,\x16\x98l\xd2\xd3X\x1aB\xee\xed\x13\xee\xd5\r\xf0J\xc9\x8d\x02 R\xa8\xfe\xa2]\xe6Y \xf3Q\xb1\xd5^G\xeaEpr\xcf,-\x90\xe5,\x18\xd4\x92\x84\xe5y\x8c\x02\x01\x00\x01\x00U\x02\x00\x00\x00\x01\x05j\xc0\xa7"\x1f\xe5\x82x\xc9\xa7h\xd0\x1a!\xe6\xb6GJ\x01\x9a\xf6\xe7?\x08\xc8R\xe6\x86|\xad\xa5\x00\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 /\xf9wQJ\x85J\xd6\xc0\xa7fY9S\x1ae\x7f\xedq\xc0\xc0\x98\x89\x80\x9a~\xe2\xf04\x90n\xb5\x02 (\x9bx\x99\xe0\xef\xc2\x0b\x01\r\xe1J\x93\xfc]Q\xed&Q\xce}\xb5\x91a\xc06\xdd\x1a\xaf\xd4\xb8\xaf\x01\x00\x00'
    SIGNED_P2PKH_PSBT_B43 = "BR$75LAJ*NO3F5WJXNJ1A:EL:+BDHMS4-Z5WYFOJ1854D.:B/CIMW*I35ZX6X:M:H:D-2RC51JGDI7G12DA4SLF$WS3/07UG8I7RNOKDFSE43J0+7R0J6..CAI5-OY-ATI:*L055QSOAOY9XZ2WQNNK9+55T9N-EX0/UV1WJ+32C5D1LRF9$MX:9B3RCO5NYRSGC..28STID/8F188UUUD2A:3$IP:UQBYV5-UU:4N8P1*YF2AU+H2YRH9W2OA5OS1YO6Z.DY/AFOWMN*IBZ6:7T1ZTT2/Z6ZE3BMDQ5QTPKZ76BBR0.YL$53WG*WT+742I0DEXIFSU8UCJJ4XOI25$N*THS4B.7J$B4YM:XWK$-DMI0-31FI9N.KS0$J2R4+597*/GTCHD*CUM.O102D7UC7MH7QI86NHAYPSO*UV-E4JL7CNKGLGLK4ZRJ-KYVDA$VBER.AV*ZKEG7/VUC8P2V5G7HG64+3YOCSU/K049/OFRB$$.2:Z77OHECAUSM99TXT1S/KAR-V8FBX4UHYU-7MWCSL68K61FLU1-TIUUNM616M/7HNN8J..06V63EQI*ACVR*Q2HQL:8LW3E/ID:EU$PUEG/E09FVJQ2IVI0WH:Q$Q$.X8OSH58YNUB3Y5DIJQ-IKW*69VT5/TQ6L20ZLDIEP4UBUQW8FJBD/+O9J:T/80HNI9KUC18JM59.WZQ8*DAT46-2*--08GZV8ZQC8$-QZHKUQ.+T.Y1A65VRK6I1YJDFULKFV4GW+/+0CC..ELCA3GGBP4XXZ7L1GJH7-25QWSF95F8W3A$39BJ7LCZGM/0:NO983:KGUBBQ:C5F:V7MA4QKOZYKFD4WH**YMMCQ2Y4GURTQ3+-6KBM1X6$/POH75K9LG:IKCS+E/.QF2R*D6:I.$E7VJN2:02DMP9$QL.PK5NCRBM*JL/J-+TY5ZU6OO07*X-6TO/K.5IQR+.5V7Z-INJ93SMRDR0FS+$6UV-E4N5TZEV38EREOX9C3:35VNHB722-$D2X-TP9ZA7T+K9$M0+/X*Q0.C-NCBAFLW+FWUSUU*B9V*TJRHF$U5YA3YNH*LP176A8EY-O5U.E-MMJK5X*4XP*RLXIKQG-/I3G7R+QET:FD8HJYRS:54LW5MPNLCPJBP3JVUAK+BEP7W8T-8CBS50U$R44-91.KZ0PEE"
    SIGNED_P2PKH_PSBT_B58 = "6XT9mnsYS6MLhfs4uWirQJGRNWXt7Qrs2f94yDPQ3y9c7ZmRhzpuGCvKnZLfFgDepYGRtqF4sDyfwykXMjppJZy4zxgkatKvZaoB8M9cp4jEYeWjTeqxTNXKVjDCHVRhswofDYqtEowhUsg76HhHzL1sZ4RitQJ1oQoqojkphmX1jjHL4AzJzkgoSCpMLvKh2TAVmqfhuv4Vid9gLiVBu5X1jHVdwUqQ8qnmcoP6ypGaVVoYWWaDhf9vrWi2tUhP4fNPWTVfj4txdC4a6yui28fdPW8UWu9f4h85tekokRpUWCHzJUhuXpahtiTbFsLhaw1PhpAbN5M3PEbs53poHiNFbG6rjLveyiDnyeW6vTGEecGcAgktvVzv2f5cBc9VwcfLUDqYN4bwdUpbzeuuHC3JeNwx2Q1pEspqZDhm94R3a6jw3g35CzaHZ5cMDfMKp7LFsbh4AgKD2HhvWMLk2EpSRc31Avet6j8ARCUXHRNRE9eay3NKy9AhE2zdQnEg42PVK5Sjs7PpT6QcvifdfaNAZ852eBQSTUk9X3oLXG43RaA2eNXmu92ydAfdWr9SyQ5WHKDhZq1xzcGnB4eaz1qJ1TpbWhkTnsEqsw3h6aqL2MWEpKjopKLn88gFSKN4nBUTz2ZvXdPqyZMuFVqnZ79LY1JaM77pyrdyc8G68VFhyMWADd4ABEeLdFq2a8yrTGkdq1V1ef3KWLJCKFV3WHEXcwQkKyS2t8XFgpKMJ1gGu5tQ8BYEzboUjP6EJs5dVZmcjNgwyh1MYpSHorm4AUyfGAoSiNjwWjjfM2F8z4JEWxLdfk4ufoG25gbrzbKrhQJjFNr3TeqZJBfVpEgsn8QjmaV7RBzrk7Whx3K51hx6HZe9JkUG9z5abmBA7FZQMACx8FRLRaZBxc7GiEf3hiT4Sv7fyUmTagViamSXbzvpHGqyaVnN7PD62yfxSzkFWwjVfPG78ufotrQ7fxJ4gfAcz7DgpH8xBe1GhPLuDZP1kDHi3JcoJ6CF8w9w3q4pkZVCtwB7AqTwimMXztLhdULWGDjBc3PVXmzfziCbc2CzJHzfzbxVqSAi8UA5WJzNXaiZhFTXV"
    SIGNED_P2PKH_PSBT_B64 = "cHNidP8BAKQCAAAAA67iNa8omsnuwjPKIhW/P/TBynhBUNYPW5RrQYeLFQQsAAAAAAD9////VMmRacRaSWcgWiHWKb8rehYxxHVvUyDwnZbPI9zbY6AAAAAAAP3///8EHlZ0jYBIH4lrB1Qoyq+RHiIaMu+lX1xz+YvCSqDIEQAAAAAA/f///wHoAwAAAAAAABYAFK7NHtw+/2WqIJ0CFec9cJBdwWhsWg8rAAABAH4CAAAAApqb4copEFyXdDwP0e55wOYNIophyOy/dPnnz/oBGQx7AgAAAAD9////mpvhyikQXJd0PA/R7nnA5g0iimHI7L90+efP+gEZDHsBAAAAAP3///8BQAcAAAAAAAAZdqkUOi1BRaTwmFI7PoEn8dqHz8VbjnmIrFoPKwAiAgKnRROVc1Np8uzfyCnA93TojvEwPf5bLwTbqrMKU1391kcwRAIgFB6kWP8+bJ3YRGfarxu6OUKUQGVivLNc5KVPOk7InOsCIC+jJbZRd44c2soNoLEsLFpDTKMyMHXVx2dUJyuCgADlAQABAFUCAAAAAYczIGnXEafNKmDVhBw4CixV6KIK3dpWopwAhGXv9luiAQAAAAD/////AQAAAAAAAAAAGXapFDotQUWk8JhSOz6BJ/Hah8/FW455iKwAAAAAIgICp0UTlXNTafLs38gpwPd06I7xMD3+Wy8E26qzClNd/dZHMEQCIGH0YKVXvcUrpK5q/fUsFphs0tNYGkLu7RPu1Q3wSsmNAiBSqP6iXeZZIPNRsdVeR+pFcHLPLC2Q5SwY1JKE5XmMAgEAAQBVAgAAAAEFasCnIh/lgnjJp2jQGiHmtkdKAZr25z8IyFLmhnytpQAAAAAA/////wEAAAAAAAAAABl2qRQ6LUFFpPCYUjs+gSfx2ofPxVuOeYisAAAAACICAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WRzBEAiAv+XdRSoVK1sCnZlk5Uxplf+1xwMCYiYCafuLwNJButQIgKJt4meDvwgsBDeFKk/xdUe0mUc59tZFhwDbdGq/UuK8BAAA="
    SIGNED_P2PKH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(SIGNED_P2PKH_PSBT).to_cbor())
    SIGNED_P2PKH_PSBT_SD = b'psbt\xff\x01\x00\xa4\x02\x00\x00\x00\x03\xae\xe25\xaf(\x9a\xc9\xee\xc23\xca"\x15\xbf?\xf4\xc1\xcaxAP\xd6\x0f[\x94kA\x87\x8b\x15\x04,\x00\x00\x00\x00\x00\xfd\xff\xff\xffT\xc9\x91i\xc4ZIg Z!\xd6)\xbf+z\x161\xc4uoS \xf0\x9d\x96\xcf#\xdc\xdbc\xa0\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x04\x1eVt\x8d\x80H\x1f\x89k\x07T(\xca\xaf\x91\x1e"\x1a2\xef\xa5_\\s\xf9\x8b\xc2J\xa0\xc8\x11\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x01\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hlZ\x0f+\x00O\x01\x045\x87\xcf\x03\x06\xb07\xf6\x80\x00\x00\x00k"\xc5\x12;\xa1\n\xde\xafK\xfc\xbbE\xd1\xa0-\x82\x8f%\xbf\x86F\x95z\x98\xd0b\x87\xc4\xe2\xb8P\x02\x8bB\xcdGv7l\x82y\x1bIAU\x15\x1fV\xc2\xd7\xb4q\xe0\xc7\xa5&\xa7\xce`\xdd\x87.8g\x10s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x01\x00~\x02\x00\x00\x00\x02\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x02\x00\x00\x00\x00\xfd\xff\xff\xff\x9a\x9b\xe1\xca)\x10\\\x97t<\x0f\xd1\xeey\xc0\xe6\r"\x8aa\xc8\xec\xbft\xf9\xe7\xcf\xfa\x01\x19\x0c{\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01@\x07\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xacZ\x0f+\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 \x14\x1e\xa4X\xff>l\x9d\xd8Dg\xda\xaf\x1b\xba9B\x94@eb\xbc\xb3\\\xe4\xa5O:N\xc8\x9c\xeb\x02 /\xa3%\xb6Qw\x8e\x1c\xda\xca\r\xa0\xb1,,ZCL\xa320u\xd5\xc7gT\'+\x82\x80\x00\xe5\x01\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00U\x02\x00\x00\x00\x01\x873 i\xd7\x11\xa7\xcd*`\xd5\x84\x1c8\n,U\xe8\xa2\n\xdd\xdaV\xa2\x9c\x00\x84e\xef\xf6[\xa2\x01\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 a\xf4`\xa5W\xbd\xc5+\xa4\xaej\xfd\xf5,\x16\x98l\xd2\xd3X\x1aB\xee\xed\x13\xee\xd5\r\xf0J\xc9\x8d\x02 R\xa8\xfe\xa2]\xe6Y \xf3Q\xb1\xd5^G\xeaEpr\xcf,-\x90\xe5,\x18\xd4\x92\x84\xe5y\x8c\x02\x01\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00U\x02\x00\x00\x00\x01\x05j\xc0\xa7"\x1f\xe5\x82x\xc9\xa7h\xd0\x1a!\xe6\xb6GJ\x01\x9a\xf6\xe7?\x08\xc8R\xe6\x86|\xad\xa5\x00\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x19v\xa9\x14:-AE\xa4\xf0\x98R;>\x81\'\xf1\xda\x87\xcf\xc5[\x8ey\x88\xac\x00\x00\x00\x00"\x02\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6G0D\x02 /\xf9wQJ\x85J\xd6\xc0\xa7fY9S\x1ae\x7f\xedq\xc0\xc0\x98\x89\x80\x9a~\xe2\xf04\x90n\xb5\x02 (\x9bx\x99\xe0\xef\xc2\x0b\x01\r\xe1J\x93\xfc]Q\xed&Q\xce}\xb5\x91a\xc06\xdd\x1a\xaf\xd4\xb8\xaf\x01\x01\x03\x04\x01\x00\x00\x00"\x06\x02\xa7E\x13\x95sSi\xf2\xec\xdf\xc8)\xc0\xf7t\xe8\x8e\xf10=\xfe[/\x04\xdb\xaa\xb3\nS]\xfd\xd6\x18s\xc5\xda\n,\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    SIGNED_P2PKH_PSBT_B64_SD = "cHNidP8BAKQCAAAAA67iNa8omsnuwjPKIhW/P/TBynhBUNYPW5RrQYeLFQQsAAAAAAD9////VMmRacRaSWcgWiHWKb8rehYxxHVvUyDwnZbPI9zbY6AAAAAAAP3///8EHlZ0jYBIH4lrB1Qoyq+RHiIaMu+lX1xz+YvCSqDIEQAAAAAA/f///wHoAwAAAAAAABYAFK7NHtw+/2WqIJ0CFec9cJBdwWhsWg8rAE8BBDWHzwMGsDf2gAAAAGsixRI7oQrer0v8u0XRoC2CjyW/hkaVepjQYofE4rhQAotCzUd2N2yCeRtJQVUVH1bC17Rx4MelJqfOYN2HLjhnEHPF2gosAACAAQAAgAAAAIAAAQB+AgAAAAKam+HKKRBcl3Q8D9HuecDmDSKKYcjsv3T558/6ARkMewIAAAAA/f///5qb4copEFyXdDwP0e55wOYNIophyOy/dPnnz/oBGQx7AQAAAAD9////AUAHAAAAAAAAGXapFDotQUWk8JhSOz6BJ/Hah8/FW455iKxaDysAIgICp0UTlXNTafLs38gpwPd06I7xMD3+Wy8E26qzClNd/dZHMEQCIBQepFj/Pmyd2ERn2q8bujlClEBlYryzXOSlTzpOyJzrAiAvoyW2UXeOHNrKDaCxLCxaQ0yjMjB11cdnVCcrgoAA5QEBAwQBAAAAIgYCp0UTlXNTafLs38gpwPd06I7xMD3+Wy8E26qzClNd/dYYc8XaCiwAAIABAACAAAAAgAAAAAAAAAAAAAEAVQIAAAABhzMgadcRp80qYNWEHDgKLFXoogrd2lainACEZe/2W6IBAAAAAP////8BAAAAAAAAAAAZdqkUOi1BRaTwmFI7PoEn8dqHz8VbjnmIrAAAAAAiAgKnRROVc1Np8uzfyCnA93TojvEwPf5bLwTbqrMKU1391kcwRAIgYfRgpVe9xSukrmr99SwWmGzS01gaQu7tE+7VDfBKyY0CIFKo/qJd5lkg81Gx1V5H6kVwcs8sLZDlLBjUkoTleYwCAQEDBAEAAAAiBgKnRROVc1Np8uzfyCnA93TojvEwPf5bLwTbqrMKU1391hhzxdoKLAAAgAEAAIAAAACAAAAAAAAAAAAAAQBVAgAAAAEFasCnIh/lgnjJp2jQGiHmtkdKAZr25z8IyFLmhnytpQAAAAAA/////wEAAAAAAAAAABl2qRQ6LUFFpPCYUjs+gSfx2ofPxVuOeYisAAAAACICAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WRzBEAiAv+XdRSoVK1sCnZlk5Uxplf+1xwMCYiYCafuLwNJButQIgKJt4meDvwgsBDeFKk/xdUe0mUc59tZFhwDbdGq/UuK8BAQMEAQAAACIGAqdFE5VzU2ny7N/IKcD3dOiO8TA9/lsvBNuqswpTXf3WGHPF2gosAACAAQAAgAAAAIAAAAAAAAAAAAAA"

    # Native Segwit Singlesig
    P2WPKH_PSBT = b'psbt\xff\x01\x00q\x02\x00\x00\x00\x01\xcf<X\xc3)\x82\xae P\x88\xd9\xbdI\xeb\x9b\x02\xac\xdfM=\xaev\xa5\x16\xc6\xb3\x06\xb1]\xe3\xa1N\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02|?]\x05\x00\x00\x00\x00\x16\x00\x14/4\xaa\x1c\xf0\nS\xb0U\xa2\x91\xa0:}E\xf0\xa6\x98\x8bR\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01\x1f\x00\xe1\xf5\x05\x00\x00\x00\x00\x16\x00\x14\xd0\xc4\xa3\xef\t\xe9\x97\xb6\xe9\x9e9~Q\x8f\xe3\xe4\x1a\x11\x8c\xa1"\x06\x02\xe7\xab%7\xb5\xd4\x9e\x97\x03\t\xaa\xe0n\x9eI\xf3l\xe1\xc9\xfe\xbb\xd4N\xc8\xe0\xd1\xcc\xa0\xb4\xf9\xc3\x19\x18s\xc5\xda\nT\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x02\x03]I\xec\xcdT\xd0\t\x9eCgbw\xc7\xa6\xd4b]a\x1d\xa8\x8a]\xf4\x9b\xf9Qzw\x91\xa7w\xa5\x18s\xc5\xda\nT\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    P2WPKH_PSBT_B43 = "1N0HGUN:R2Q*R86JDWEOBMHAETS.D$7T+SEGWXJO3JPKXA+O3JNN$$VLXOA4R/O+2+T$0BL68OC3*:/B4SOZWX3MY9B1R0AXW5-KVBGEJJWUNUTMA5-XE+IX*M5$/.++VV9F/RHZC9:E9JT$NLGK39-VJKFHLA*C90GDVYE01C17+N*JBV0RQLT8D*1*BVK+K2K/$8.VYDK3JPC2X634YJKT57OJNX61X$4J39$.4*TZK55UAA0ALQC0PLZC61AYGB$J:SKX63U23TBU.C9NB.9C0N$RKANBNTQTYPVL1ZG6SHLT093GQFJILC0QMUYEY9F-K8.-3:JMZ4ESOL8AO+CD*7U06IVD3U6Y.$HH5PU/NPL037224KA-1A09MM76ZJ.:HY4TS-Y/8MZC6P/D6*DQF6A9"
    P2WPKH_PSBT_B58 = "UUucvki6KWyS35DhetbWPw1DiaccbHKywScF96E8VUwEnN1gss947UasRfkNxtrkzCeHziHyMCuoiQ2mSYsbYXuV3YwYBZwFh1c6xtBAEK1aDgPwMgqf74xTzf3m4KH4iUU5nHTqroDpoRZR59meafTCUBChZ5NJ8MoUdKE6avyYdSm5kUb4npmFpMpJ9S3qd2RedHMoQFRiXK3jwdH81emAEsFYSW3Kb7caPcWjkza4S4EEWWbaggofGFmxE5gNNg4A4LNC2ZUGLsALZffNvg3yh3qg6rFxhkiyzWc44kx9Khp6Evm1j4Njh8kjifkngLTPFtX3uWNLAB1XrvpPMx6kkkhr7RnFVrA4JsDp5BwVGAXBoSBLTqweFevZ5"
    P2WPKH_PSBT_B64 = "cHNidP8BAHECAAAAAc88WMMpgq4gUIjZvUnrmwKs3009rnalFsazBrFd46FOAAAAAAD9////Anw/XQUAAAAAFgAULzSqHPAKU7BVopGgOn1F8KaYi1KAlpgAAAAAABYAFOZq/v/Dg45x8KJ7B+OwDt5q6OFgAAAAAAABAR8A4fUFAAAAABYAFNDEo+8J6Ze26Z45flGP4+QaEYyhIgYC56slN7XUnpcDCargbp5J82zhyf671E7I4NHMoLT5wxkYc8XaClQAAIABAACAAAAAgAAAAAAAAAAAACICA11J7M1U0AmeQ2did8em1GJdYR2oil30m/lReneRp3elGHPF2gpUAACAAQAAgAAAAIABAAAAAAAAAAAA"
    P2WPKH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2WPKH_PSBT).to_cbor())
    P2WPKH_PSBT_BBQR_PSBT = P2WPKH_PSBT  # BBQr is decoded to binary before being passed to the PSBT constructor

    SIGNED_P2WPKH_PSBT = b'psbt\xff\x01\x00q\x02\x00\x00\x00\x01\xcf<X\xc3)\x82\xae P\x88\xd9\xbdI\xeb\x9b\x02\xac\xdfM=\xaev\xa5\x16\xc6\xb3\x06\xb1]\xe3\xa1N\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02|?]\x05\x00\x00\x00\x00\x16\x00\x14/4\xaa\x1c\xf0\nS\xb0U\xa2\x91\xa0:}E\xf0\xa6\x98\x8bR\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01\x1f\x00\xe1\xf5\x05\x00\x00\x00\x00\x16\x00\x14\xd0\xc4\xa3\xef\t\xe9\x97\xb6\xe9\x9e9~Q\x8f\xe3\xe4\x1a\x11\x8c\xa1"\x02\x02\xe7\xab%7\xb5\xd4\x9e\x97\x03\t\xaa\xe0n\x9eI\xf3l\xe1\xc9\xfe\xbb\xd4N\xc8\xe0\xd1\xcc\xa0\xb4\xf9\xc3\x19G0D\x02 >e\xff;L\xd4\x7f\x12\x1f\xa7\xc9\x82(F\x18\xdb\x801G\xb0V\xd3\x93\x94\xd4\xecB\x0e\xfd\xfck\xa1\x02 l\xbd\xd8\x8a\xc5\x18l?.\xfd$%1\xedy\x17uvQ\xac&#t\xf3\xd3\x1d\x85\xd6\x16\xcdj\x81\x01\x00\x00\x00'
    SIGNED_P2WPKH_PSBT_B43 = "ZF1XCF+Z*C015XRRLXYR*QCNLC+GG904*T:WKMSDWEXX2VS57*S7X9FJGRN/0Q0$-OBHIJ8/B.C-BG*2ITD2B9C5VJ0AVI5GAH7LMHJ3.EY3KL*/6I*ERF8GTDFTN5KA6Z-NUJ0UV/2NBXH43OSU3T98BSCAIZ.:HWRXU/L.HMUDEJEO$3.C/80-LULS/CM0DV*$3*EM/736NIXS-0+:E-A4TDYZRGW9W181MRBNJ6A*O$VO/VT+SAX+TVO4DH.$Q$MKU6OFVP94EX8LXOK6F69TJI8T.38.BLI.55W3/928OSS-1SK022VB+Q0WZ3F33NB*EE:$*YD+*1BK.SU1EV3M2C4UG.PA.T--YRP8BB/QH:V-9F4B/XUZYCDUDAYG/CR4VT15"
    SIGNED_P2WPKH_PSBT_B58 = "2HkajtjMgNpiuo5QQYDP4zEc3vrWa1f7qgwNkMySr8EJbPoEtguwAQ2qkgA7k7NzAvLjA3FA4C9ejVxLx8vSemVQxcda4LjDyrbpinuPeSakKBjvR1XrCa5jxU29xfiaYjLTKDPPAPHCdTJy4r7Zcc9kqaTk9NxoqMhdUiNqxfyuBoDeCwMemE2UE4D5GrDMMuhJvJ2vyJkK6w9a1P7cE6gwL4CVx7LrLtwRGbUUiQ3tkr8ve57kWjyTLT1FALNVVyNfDb4kJccqZ6Nv1riwPaRRUpr2yaBkTogG4nAK31ywpiAwqxZpswjUF6gpbnLJUQDsowNjYeW9NEA83S2oL3FshKWsfcB1vhKT5DvCQZzo"
    SIGNED_P2WPKH_PSBT_B64 = "cHNidP8BAHECAAAAAc88WMMpgq4gUIjZvUnrmwKs3009rnalFsazBrFd46FOAAAAAAD9////Anw/XQUAAAAAFgAULzSqHPAKU7BVopGgOn1F8KaYi1KAlpgAAAAAABYAFOZq/v/Dg45x8KJ7B+OwDt5q6OFgAAAAAAABAR8A4fUFAAAAABYAFNDEo+8J6Ze26Z45flGP4+QaEYyhIgIC56slN7XUnpcDCargbp5J82zhyf671E7I4NHMoLT5wxlHMEQCID5l/ztM1H8SH6fJgihGGNuAMUewVtOTlNTsQg79/GuhAiBsvdiKxRhsPy79JCUx7XkXdXZRrCYjdPPTHYXWFs1qgQEAAAA="
    SIGNED_P2WPKH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(SIGNED_P2WPKH_PSBT).to_cbor())
    SIGNED_P2WPKH_PSBT_BBQR_PSBT = encode_bbqr(SIGNED_P2WPKH_PSBT, "Z", "P")
    SIGNED_P2WPKH_PSBT_SD = b'psbt\xff\x01\x00q\x02\x00\x00\x00\x01\xcf<X\xc3)\x82\xae P\x88\xd9\xbdI\xeb\x9b\x02\xac\xdfM=\xaev\xa5\x16\xc6\xb3\x06\xb1]\xe3\xa1N\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02|?]\x05\x00\x00\x00\x00\x16\x00\x14/4\xaa\x1c\xf0\nS\xb0U\xa2\x91\xa0:}E\xf0\xa6\x98\x8bR\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01\x1f\x00\xe1\xf5\x05\x00\x00\x00\x00\x16\x00\x14\xd0\xc4\xa3\xef\t\xe9\x97\xb6\xe9\x9e9~Q\x8f\xe3\xe4\x1a\x11\x8c\xa1"\x02\x02\xe7\xab%7\xb5\xd4\x9e\x97\x03\t\xaa\xe0n\x9eI\xf3l\xe1\xc9\xfe\xbb\xd4N\xc8\xe0\xd1\xcc\xa0\xb4\xf9\xc3\x19G0D\x02 >e\xff;L\xd4\x7f\x12\x1f\xa7\xc9\x82(F\x18\xdb\x801G\xb0V\xd3\x93\x94\xd4\xecB\x0e\xfd\xfck\xa1\x02 l\xbd\xd8\x8a\xc5\x18l?.\xfd$%1\xedy\x17uvQ\xac&#t\xf3\xd3\x1d\x85\xd6\x16\xcdj\x81\x01"\x06\x02\xe7\xab%7\xb5\xd4\x9e\x97\x03\t\xaa\xe0n\x9eI\xf3l\xe1\xc9\xfe\xbb\xd4N\xc8\xe0\xd1\xcc\xa0\xb4\xf9\xc3\x19\x18s\xc5\xda\nT\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x02\x03]I\xec\xcdT\xd0\t\x9eCgbw\xc7\xa6\xd4b]a\x1d\xa8\x8a]\xf4\x9b\xf9Qzw\x91\xa7w\xa5\x18s\xc5\xda\nT\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    SIGNED_P2WPKH_PSBT_B64_SD = "cHNidP8BAHECAAAAAc88WMMpgq4gUIjZvUnrmwKs3009rnalFsazBrFd46FOAAAAAAD9////Anw/XQUAAAAAFgAULzSqHPAKU7BVopGgOn1F8KaYi1KAlpgAAAAAABYAFOZq/v/Dg45x8KJ7B+OwDt5q6OFgAAAAAAABAR8A4fUFAAAAABYAFNDEo+8J6Ze26Z45flGP4+QaEYyhIgIC56slN7XUnpcDCargbp5J82zhyf671E7I4NHMoLT5wxlHMEQCID5l/ztM1H8SH6fJgihGGNuAMUewVtOTlNTsQg79/GuhAiBsvdiKxRhsPy79JCUx7XkXdXZRrCYjdPPTHYXWFs1qgQEiBgLnqyU3tdSelwMJquBunknzbOHJ/rvUTsjg0cygtPnDGRhzxdoKVAAAgAEAAIAAAACAAAAAAAAAAAAAIgIDXUnszVTQCZ5DZ2J3x6bUYl1hHaiKXfSb+VF6d5Gnd6UYc8XaClQAAIABAACAAAAAgAEAAAAAAAAAAAA="

    # Nested Segwit Singlesig
    P2SH_P2WPKH_PSBT = b'psbt\xff\x01\x00r\x02\x00\x00\x00\x01v\xefk\xf2\xbd\xd0@\xf3\xc1\xd8:\xcc\xb9t9\xf1\xab\xb1\xa5V\xad\x1d\x0fR\x96\x81\xff\xa7\xe8\xca\x94\x8a\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02\x9c=]\x05\x00\x00\x00\x00\x17\xa9\x14%\x1d\xd1\x14W\xa2Y\xc3\xbaG\xe5\xcc\xa3q\x7f\xe4!N\x02\x98\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x143l\xaa\x13\xe0\x8b\x96\x08\n2\xb5\xd8\x18\xd5\x9bJ\xb3\xb3gB\x87\x01\x04\x16\x00\x148\x97\x1fs\x93\x0fl\x14\x1d\x97z\xc4\xfdJr|\x85I5\xb3"\x06\x03\xa1\xaf\x80J\xc1\x08\xa8\xa5\x17\x82\x19\x8c-\x03K(\xbf\x90\xc8\x80?ZS\xf7bv\xfai\xa4\xea\xe7\x7f\x18s\xc5\xda\n1\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x16\x00\x14p\xbe\xb1\xe0JP\t@\xe9\xf3\xab\xaaf\xe1\xa4\x9a\xc5[\x8f5"\x02\x02\xa2\xfc\x89\x96\xc5&"H\xb5\xda\xef\xc5\xa4\xd0\xcd\xcd\x00\xc10G\xd0\xcb\x13\x02\x816\xeac\r\x87Z\x87\x18s\xc5\xda\n1\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    P2SH_P2WPKH_PSBT_B43 = "ISOGTD+S3R8H0DQLFI44D9XVW+NU6FLJ-.-6DZON$.R31OG$AFCWZGO40V:6HQ.DT2C3.CPVM-F+V+GB$A9G:.K3B:KCWPOU8.LZ4SO1D-W/:PCK5Y1.B$HQGWWR1BN8:9J-HXGFVVL1D3R+MTLP/10MGI6AN$1*5ITO3105-C1QBR+LAR5D7VM/1P*KBYJH6P4LH9GCU5DE2*8MP3*YT2K.KDV32OAMNKHV/VGLX9XJ0*B6850S794RVAWR*LEY40SCBLQ.*OR7T$RZ9581/GKU4KYV48LDPURZMDKBEZXRG2SDL4UYGF330F$4*1JCUL5TS+:*X*+E6D::-0L1L63IAMW:*IVLP$YQUV922+G$OJY.INJRHY/A$0.UFB.VD21PM8ED92HKS5TXCAPFS9LT199UMOMBNKM$HE*7*VOJQ*J7JY1PLG188K8IB97211B+AH$4$GDJ750S--S.H45Y4HA4N$PK5S03HS4K"
    P2SH_P2WPKH_PSBT_B58 = "W7hsNtPR1YU4YQRATn9QwVubQ3s4aLKhoSpCJQtZuiqGxTQPhu1FB4bqZdtL2MpygirLgext5jZpLSRKGQEhcuiUjg5wvnyP5EP7w1RxkE4Zc5mxDKyEhRH7k3wcSA8TTahF7Rg7r2cWry4c7LySnwoAGtYP1VRwcgMfbYXroHrrKqgdfaKLmMD1M5bCYpU6fMCzcEK5hXQSFaupmhTyAPHiGAczMSmnsoaeZ4cCNpZzexK6FkYES1XTBkroLD68tYejJTjkEpASRVTwS1LUJHEUVmAgASWQ1r3x9yGQaSamXqvedoZ3dNuUsmVJNdGNjKFJRsQugzxEHEj2PWJCpYCUo4Ms79wRkSYjeaQaEEHnBLnkbhPdL6rUu5oGCpzkkgewTcH5hSPA8GefzSgLo3CrGQgY5K3GvPTH5aP6VvMWpUBHGiPqddjQzqeAePxKHi6T"
    P2SH_P2WPKH_PSBT_B64 = "cHNidP8BAHICAAAAAXbva/K90EDzwdg6zLl0OfGrsaVWrR0PUpaB/6foypSKAQAAAAD9////Apw9XQUAAAAAF6kUJR3RFFeiWcO6R+XMo3F/5CFOApiHgJaYAAAAAAAWABTmav7/w4OOcfCiewfjsA7eaujhYAAAAAAAAQEgAOH1BQAAAAAXqRQzbKoT4IuWCAoytdgY1ZtKs7NnQocBBBYAFDiXH3OTD2wUHZd6xP1KcnyFSTWzIgYDoa+ASsEIqKUXghmMLQNLKL+QyIA/WlP3Ynb6aaTq538Yc8XaCjEAAIABAACAAAAAgAAAAAAAAAAAAAEAFgAUcL6x4EpQCUDp86uqZuGkmsVbjzUiAgKi/ImWxSYiSLXa78Wk0M3NAMEwR9DLEwKBNupjDYdahxhzxdoKMQAAgAEAAIAAAACAAQAAAAAAAAAAAA=="
    P2SH_P2WPKH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2SH_P2WPKH_PSBT).to_cbor())

    SIGNED_P2SH_P2WPKH_PSBT = b'psbt\xff\x01\x00r\x02\x00\x00\x00\x01v\xefk\xf2\xbd\xd0@\xf3\xc1\xd8:\xcc\xb9t9\xf1\xab\xb1\xa5V\xad\x1d\x0fR\x96\x81\xff\xa7\xe8\xca\x94\x8a\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02\x9c=]\x05\x00\x00\x00\x00\x17\xa9\x14%\x1d\xd1\x14W\xa2Y\xc3\xbaG\xe5\xcc\xa3q\x7f\xe4!N\x02\x98\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x143l\xaa\x13\xe0\x8b\x96\x08\n2\xb5\xd8\x18\xd5\x9bJ\xb3\xb3gB\x87"\x02\x03\xa1\xaf\x80J\xc1\x08\xa8\xa5\x17\x82\x19\x8c-\x03K(\xbf\x90\xc8\x80?ZS\xf7bv\xfai\xa4\xea\xe7\x7fG0D\x02 u\x0c\xf8\xe6\x03\x15l\xab\xaa7a`\x1f\xcb\xc5\xd92TC\x97\xbd\xed\xfeS\xeeC\xf4\x1d\xddc\x1cx\x02 4{\xe5K\xe5\xf2F\x04\xd5\x05V\xe8}K\x00\xcc\x93)\x90\x1f\r\x02,\xee?\xd8\xed\xd2\xb8\x97\xcaS\x01\x01\x04\x16\x00\x148\x97\x1fs\x93\x0fl\x14\x1d\x97z\xc4\xfdJr|\x85I5\xb3\x00\x00\x00'
    SIGNED_P2SH_P2WPKH_PSBT_B43 = "H2ZW15J2ZL-VL/WIC5AQ67IT6:2*PR$1PNPWZ67EY3.D*MU1XLGL2:M$73JM9*$9Q6EJCOAWF:258LFQ$D209+HXGLHAW1P7F0GS3/9*+TM4.972T18+WAVDG0FBTR7KD*GY.UQ*2$$O:7L015ZB$TIRBR0X0JW7FTWZJOFA2BXZ-+F2DCNJ6CGT0:5GR5BJE8XE/G*Y3S0$11D4*F.C8OGM-M*UQDY-2X0+NF6X106N2$9FZSA-*6WIW+ET$79KLN8AVDGO*6Z+ON4J43Z5S*A$UZEH5VNKO.ZQKD+VC/BJANEHK+OLCBD5H1GSQUMOHJ6VO//5Q1515V6YKJ4FLMG8OU-2M-S.+GS+T10EI6EP*GCYGQPD9389V01Q52.$A+3O-YCO55.Q*BOXPW2CF.VEPR:.HWZ**QA5NITVI3:MQWKL"
    SIGNED_P2SH_P2WPKH_PSBT_B58 = "mbNU9ochR3r2kucYTPNx2gt6qUqhQ2BCrRrQkjve3E7b4YoV1fG7Nno8bcE4Rtq5jiXfYNV1LYeRYPwek67KsJdfTL1y2pxK6Kis2hA2GF7s3eJkUzXdTBPGpmMW39bAnU2315fnDjfanJxRJsj9iefvwteXmCR2mY1vFZwDJ9E66mmtjXQjQ57bD33WoAbZqJjYucy5u8d1HmSAwBaMqfzYYNyjNkAKDCD1Jd3CZfcwo5jB1qLeq3i3hu4XGB8puf4fJ9B3uGjMAaL5Po32Wrw5RaAPBJ39hXJBskvsEKC6gcHEP92oXsTTDHQWrsAnLMs1fkjEBsvjHsWsff6PebdDCLdzRGoJavc5TUTyaydbitxWfUQT99ZCuoKQkxhGqVC65euWJCFSSR67"
    SIGNED_P2SH_P2WPKH_PSBT_B64 = "cHNidP8BAHICAAAAAXbva/K90EDzwdg6zLl0OfGrsaVWrR0PUpaB/6foypSKAQAAAAD9////Apw9XQUAAAAAF6kUJR3RFFeiWcO6R+XMo3F/5CFOApiHgJaYAAAAAAAWABTmav7/w4OOcfCiewfjsA7eaujhYAAAAAAAAQEgAOH1BQAAAAAXqRQzbKoT4IuWCAoytdgY1ZtKs7NnQociAgOhr4BKwQiopReCGYwtA0sov5DIgD9aU/didvpppOrnf0cwRAIgdQz45gMVbKuqN2FgH8vF2TJUQ5e97f5T7kP0Hd1jHHgCIDR75Uvl8kYE1QVW6H1LAMyTKZAfDQIs7j/Y7dK4l8pTAQEEFgAUOJcfc5MPbBQdl3rE/UpyfIVJNbMAAAA="
    SIGNED_P2SH_P2WPKH_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(SIGNED_P2SH_P2WPKH_PSBT).to_cbor()
    )
    SIGNED_P2SH_P2WPKH_PSBT_SD = b'psbt\xff\x01\x00r\x02\x00\x00\x00\x01v\xefk\xf2\xbd\xd0@\xf3\xc1\xd8:\xcc\xb9t9\xf1\xab\xb1\xa5V\xad\x1d\x0fR\x96\x81\xff\xa7\xe8\xca\x94\x8a\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02\x9c=]\x05\x00\x00\x00\x00\x17\xa9\x14%\x1d\xd1\x14W\xa2Y\xc3\xbaG\xe5\xcc\xa3q\x7f\xe4!N\x02\x98\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x143l\xaa\x13\xe0\x8b\x96\x08\n2\xb5\xd8\x18\xd5\x9bJ\xb3\xb3gB\x87"\x02\x03\xa1\xaf\x80J\xc1\x08\xa8\xa5\x17\x82\x19\x8c-\x03K(\xbf\x90\xc8\x80?ZS\xf7bv\xfai\xa4\xea\xe7\x7fG0D\x02 u\x0c\xf8\xe6\x03\x15l\xab\xaa7a`\x1f\xcb\xc5\xd92TC\x97\xbd\xed\xfeS\xeeC\xf4\x1d\xddc\x1cx\x02 4{\xe5K\xe5\xf2F\x04\xd5\x05V\xe8}K\x00\xcc\x93)\x90\x1f\r\x02,\xee?\xd8\xed\xd2\xb8\x97\xcaS\x01\x01\x04\x16\x00\x148\x97\x1fs\x93\x0fl\x14\x1d\x97z\xc4\xfdJr|\x85I5\xb3"\x06\x03\xa1\xaf\x80J\xc1\x08\xa8\xa5\x17\x82\x19\x8c-\x03K(\xbf\x90\xc8\x80?ZS\xf7bv\xfai\xa4\xea\xe7\x7f\x18s\xc5\xda\n1\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x16\x00\x14p\xbe\xb1\xe0JP\t@\xe9\xf3\xab\xaaf\xe1\xa4\x9a\xc5[\x8f5"\x02\x02\xa2\xfc\x89\x96\xc5&"H\xb5\xda\xef\xc5\xa4\xd0\xcd\xcd\x00\xc10G\xd0\xcb\x13\x02\x816\xeac\r\x87Z\x87\x18s\xc5\xda\n1\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    SIGNED_P2SH_P2WPKH_PSBT_B64_SD = "cHNidP8BAHICAAAAAXbva/K90EDzwdg6zLl0OfGrsaVWrR0PUpaB/6foypSKAQAAAAD9////Apw9XQUAAAAAF6kUJR3RFFeiWcO6R+XMo3F/5CFOApiHgJaYAAAAAAAWABTmav7/w4OOcfCiewfjsA7eaujhYAAAAAAAAQEgAOH1BQAAAAAXqRQzbKoT4IuWCAoytdgY1ZtKs7NnQociAgOhr4BKwQiopReCGYwtA0sov5DIgD9aU/didvpppOrnf0cwRAIgdQz45gMVbKuqN2FgH8vF2TJUQ5e97f5T7kP0Hd1jHHgCIDR75Uvl8kYE1QVW6H1LAMyTKZAfDQIs7j/Y7dK4l8pTAQEEFgAUOJcfc5MPbBQdl3rE/UpyfIVJNbMiBgOhr4BKwQiopReCGYwtA0sov5DIgD9aU/didvpppOrnfxhzxdoKMQAAgAEAAIAAAACAAAAAAAAAAAAAAQAWABRwvrHgSlAJQOnzq6pm4aSaxVuPNSICAqL8iZbFJiJItdrvxaTQzc0AwTBH0MsTAoE26mMNh1qHGHPF2goxAACAAQAAgAAAAIABAAAAAAAAAAAA"

    # Taproot Singlesig
    P2TR_PSBT = b"psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\xf9\xfe\xa6\x15\x16\xa0\x07\xe4v2WHAq\x8d\xc0\xda\\\x1a\xf6\xd9\x173\x7f\x06\x8eT\xda\xbeI\xbe?\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03:\x1e\x00\x00\x00\x00\x00\x00\"Q u\xe6_\x88=\xe5\x87'1\xd9\x8e\xa8o_\x08b\xf0\x929\xd0\xe9\xb0\x0fI\xf5\x92\x06\x9c\x18M\x02\xa2\xe8\x03\x00\x00\x00\x00\x00\x00\"Q \x9d-\x9bm\xe6\x0c\xdc\xddY\x07\xc1\xc0\x961I\x1b\xddCN\xee\xaa\x8a\xaf;;\xf1\x9dc\xd5>@\x99\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hl\x83\xbf+\x00O\x01\x045\x87\xcf\x03\xe0\x17\xd1\xbb\x80\x00\x00\x00\x01\x83\\\x0bQ!\x83v\xc6\x14UB\x8a\x9fG\xbf\xcc\xe1\xf6\xce\x83\x97\xea\xd7\xb0\x03\x87\xe9\xd9\xeaV\x83\x02\xcf\xbdq\x001\x1e\x0e\x85\x84L78r\x83\x149N\xb80*kPp\xd6\x92\xe4\x1b\x14\xba\x81\x80\x90\x10s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x01\x01+\x7f'\x00\x00\x00\x00\x00\x00\"Q \x06\xac\x82\xfc6\xdb\xb6\rHy\x1d\x81\xc3\xc1\xeb9\x7f\xa9s\xe4V\xc8\xc6\xfbT\xc1\x04!\x1f\x04{\x1a\x01\x03\x04\x00\x00\x00\x00!\x16E\xc6\xb1\xe44\x82<\xe9\xe6\xb4H\xfb\xc1\xe4\x05' 8:\r!(\x82\xbc\xbavSMwR\x8a\xad\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\x00\x00\x00\x01\x17 E\xc6\xb1\xe44\x82<\xe9\xe6\xb4H\xfb\xc1\xe4\x05' 8:\r!(\x82\xbc\xbavSMwR\x8a\xad\x00!\x07 \xeb\x90P\x06\x8b\x01;\xde= M\xb5\x9a\xc5\xdb*\x1cx\xa8\xaa%\x07?\xbf.z\xd4\x9d\x05\x15\xc6\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x01\x05  \xeb\x90P\x06\x8b\x01;\xde= M\xb5\x9a\xc5\xdb*\x1cx\xa8\xaa%\x07?\xbf.z\xd4\x9d\x05\x15\xc6\x00!\x07\xdc\xab\x8eB3\xd9\x14\xf2\x98\x08\x9e]\x8d;'a\x8a\x07\xf5!?\x89\x9a+\xbd\xbax\xfd\xb9\x02\xc5\xcf\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\n\x00\x00\x00\x01\x05 \xdc\xab\x8eB3\xd9\x14\xf2\x98\x08\x9e]\x8d;'a\x8a\x07\xf5!?\x89\x9a+\xbd\xbax\xfd\xb9\x02\xc5\xcf\x00\x00"
    P2TR_PSBT_B43 = "$MYCB*Z8$F$U43$$$AYNPYV7P2O$0N:NND-4/R6WA3K5UCTN2W2UH1W+-OO$GDVLG22/ZLRV1Q8.E8J7N420ZF-M4JE.DG07WFA+62X4.4ZA-OVEWYBN:QE73QV1QF+4N7281Z2I5S1N6Y9644OHRR*SE9ZV14W2K$43KBK:SHCYT$B0YG1-J6YXZKKN4676SPPD4DGPLT3L.8E117P1-7E4YOJWP2IPW81BC3TQ3YX2OP8MONZD+O8DV95:K93RLFWQSYIDM2YKLVSKZ*+K:WWO6-3H4:.J97WXTVTUL3/+8HAKSL9+8BPQHJK-MQ5SALS79II3T:P*C6D*1ZYSDDAZ82F0W*WRR91/:YOFKC9EFMQ1CSK2HN-HCLBXVRKS4/G:6MJ61OP$08QL0X:YAJGL*IL:D*/56V1/ZFDEM*3*F-NVZNQAIEFMF08Z2MM0I$S2B61W$EY++.6X**AH0CWY9DWE4D2U*E3AECQE2Y5R1ZHTOG1MKTZ3GHTBD7F02K-DPZL+ABUVMIELQWT:M+5.FT9-RAY3OS05+/J-S*BIOI0Q6YT$UQ-RI/.429T2/:66YNAHKCVH3J7AGS46TAHCI$JSJ9*NPE2XZWW+1L30SDVFNULC4T75VP:XBBXP9I750LGP1:8ZDP0YF*BKWQZ93-U2Q0EJSJ9WB3A0ZJGLNQ57BXMVSRPDDSI+7D9B8ZKBG7X+:U84V5DMYSW3W/*I*/*UB8MJQV0+2BSQTARB$DND/9N9.+T-6O8D*74K5M+LXP*-4I:P79JX-RJH2-MKW:X5DSO13Y0AASMVOAS/28/F9Q4$B*VL.$RW0ZO.UH5T7ODJS47.MA$AK3RQ/3L4O+KWU5E:SJ..:*X:GU*HCV9-HX7$2T-/9ZAY7J3W.7W+1Y-$IM6-"
    P2TR_PSBT_B58 = "2C2dk2DpdViMV7XztuFHDKYpnMmQYUHxBC97tosVRCndABjAHMnx5Vjw2Hugev5DyrLPXfM58fxKHCcGdReZxLRr4ZDaXRy7SCssavWr9NgP7aPqbGnDZJirLEgau5p12f1FmEwoSMD9ZnrjoFwPZF5AhYr3R7ixUn7Kf7LDW63sdPV45a5z6CeUQvDELrxxyKVG4qej4GEH5DgED8PWFNQ4nq8cKU2TJL8oNZrMMSGSopG1YzEvoFf7fUzpZR6dC2hgBnEBGZWTccnAoA418aauwZU2dBqWYire6nhXsKZF4cVKweMFt8ZGFT3YRjM5uqc4i2ii4a9XrFJQd7DTLqsNHY2fUSfNSfuTdBSy7zh4eiDEU44XJcnBp1QJzb63nrAJnZjRnz6NcmRY2YrRgDq4LgRAyPCYs7UpGa1JgCK3hupDH8bPCbbtECqBXQ8nuZtNk3H6weCR4vuri2r9mMWhXY5thnyhcTjAwi51Cir3iHnjKcGPepL15U6BnNjfTAoQ6wKX3nN2pZDhn5RwyDpv7qPnouhLds7dKEn64HJqqBTVrDjTuWHNCBUMj6TcXTuPdSYH8CeL8YMfcMjhbRPHh1aSyhgLWuwBqL1eSW7wTAGLfJXoHcCJsMheMDma9MEMeP4UEAeEhNVQ5QEFFTCRH8MkMev4Fo6q4L39yhT1C5LAKkRMSnkJwKuUSAxqW4YiYH68dFjsW1MFwfXngDpcxS1QVBzhpW95Bb32VCLWHQzbCx3XcEMi5Q77MVW6aVyMHzYUNadH4Wbhn4QxQM11gPW2LQNyqwZjuxEesFJ8sqX2pCRHX6J5mBJKzyT9pyhvvQkxMu"
    P2TR_PSBT_B64 = "cHNidP8BAKgCAAAAAfn+phUWoAfkdjJXSEFxjcDaXBr22RczfwaOVNq+Sb4/AAAAAAD9////AzoeAAAAAAAAIlEgdeZfiD3lhycx2Y6ob18IYvCSOdDpsA9J9ZIGnBhNAqLoAwAAAAAAACJRIJ0tm23mDNzdWQfBwJYxSRvdQ07uqoqvOzvxnWPVPkCZ6AMAAAAAAAAWABSuzR7cPv9lqiCdAhXnPXCQXcFobIO/KwBPAQQ1h88D4BfRu4AAAAABg1wLUSGDdsYUVUKKn0e/zOH2zoOX6tewA4fp2epWgwLPvXEAMR4OhYRMNzhygxQ5TrgwKmtQcNaS5BsUuoGAkBBzxdoKVgAAgAEAAIAAAACAAAEBK38nAAAAAAAAIlEgBqyC/Dbbtg1IeR2Bw8HrOX+pc+RWyMb7VMEEIR8EexoBAwQAAAAAIRZFxrHkNII86ea0SPvB5AUnIDg6DSEogry6dlNNd1KKrRkAc8XaClYAAIABAACAAAAAgAAAAAAJAAAAARcgRcax5DSCPOnmtEj7weQFJyA4Og0hKIK8unZTTXdSiq0AIQcg65BQBosBO949IE21msXbKhx4qKolBz+/LnrUnQUVxhkAc8XaClYAAIABAACAAAAAgAEAAAABAAAAAQUgIOuQUAaLATvePSBNtZrF2yoceKiqJQc/vy561J0FFcYAIQfcq45CM9kU8pgInl2NOydhigf1IT+Jmiu9unj9uQLFzxkAc8XaClYAAIABAACAAAAAgAAAAAAKAAAAAQUg3KuOQjPZFPKYCJ5djTsnYYoH9SE/iZorvbp4/bkCxc8AAA=="
    P2TR_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2TR_PSBT).to_cbor())

    SIGNED_P2TR_PSBT = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\xf9\xfe\xa6\x15\x16\xa0\x07\xe4v2WHAq\x8d\xc0\xda\\\x1a\xf6\xd9\x173\x7f\x06\x8eT\xda\xbeI\xbe?\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03:\x1e\x00\x00\x00\x00\x00\x00"Q u\xe6_\x88=\xe5\x87\'1\xd9\x8e\xa8o_\x08b\xf0\x929\xd0\xe9\xb0\x0fI\xf5\x92\x06\x9c\x18M\x02\xa2\xe8\x03\x00\x00\x00\x00\x00\x00"Q \x9d-\x9bm\xe6\x0c\xdc\xddY\x07\xc1\xc0\x961I\x1b\xddCN\xee\xaa\x8a\xaf;;\xf1\x9dc\xd5>@\x99\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hl\x83\xbf+\x00\x00\x01\x01+\x7f\'\x00\x00\x00\x00\x00\x00"Q \x06\xac\x82\xfc6\xdb\xb6\rHy\x1d\x81\xc3\xc1\xeb9\x7f\xa9s\xe4V\xc8\xc6\xfbT\xc1\x04!\x1f\x04{\x1a\x01\x08B\x01@(\xb0\x7f\x8d\x19\x9a\xa5\xa3\xae_ ti\x10G\x95\xc3)\x18\x1e\xca=Lq^\x9ah\xe7\xb58=\x87\x80\xd8\x1a\xbd\x0bb\x06@}\xd2\x0c?\xd9G\xac\xe9!%{\xe0E\x8bY\xca\xedH\xebh`\xbc\xbb\x13\x01\x13@(\xb0\x7f\x8d\x19\x9a\xa5\xa3\xae_ ti\x10G\x95\xc3)\x18\x1e\xca=Lq^\x9ah\xe7\xb58=\x87\x80\xd8\x1a\xbd\x0bb\x06@}\xd2\x0c?\xd9G\xac\xe9!%{\xe0E\x8bY\xca\xedH\xebh`\xbc\xbb\x13\x00\x00\x00\x00'
    SIGNED_P2TR_PSBT_B43 = "$JBJ$DT-D-U/1AEWDTQ*PH4J+H:1+I467L27$UINP.QOHP:ZYLDCPD8/LI+DN/A.X7-PC4UCX-K$/OQO-G-H.CGX.+9:5JKUVI:PVG+C37HW*MVZDUS$J-CLTWQ6WQ.A0MGXBUZF:X:276$9AZTBLV82BDNXAV1XQ6..R3I+.LV4OLAXU0MO:KY3KB.:-2PFJOYQ/*95CD:5HPWA/HJ2OW1ZPNB*S39+EAP+60B73/9W9KU.A:DTLVNCOCV1/BBLE9O14Z5ACDF0N$PHZ-B:IEJHV17V91KA/WPGFPSZNSIB/-WNYY./+5VQV.DUAIILF88LFSGJ/E36.B6WJ1$I/FWPOI/L*3.8F2B1TNQS-24N8QJAF**+S13/RFDR9ZZ3/N4CP7S9Y9HKJ-$/B43SC*+BRP44+DUH+$79DJB1-9AY7N/SZPZSHJP6+KYW+4/GIWNVRW$DUE08UMY-7/FH3*ZPPAL2PWR$1+R996Y.E9H:PIB*SJQY.JOEQL/X+2Q5V91UL*/WNCH$$DY*GK.I9XN"
    SIGNED_P2TR_PSBT_B58 = "9eehoGbwQ78EoHBL2mrxCSrMophCYTK9PxBW3WqL69ZFwj5F1ESdYXt9GdSKA3xxCgfDKhQt9PqBtSkNoKRFgnm6WyTASro6r5za7Nd2JtywPgYe1JdErssp47WvjrbkBBYV5jvWrzPTJhFrpyis8LLyKExp1XY4VwfSTrcFXfDEM7QoRDehks7s7w7CbLHg8zJEDqRjCdcZpzbVunb3FR7ypZHv41S8VKvhiGHFq1nW99F3dErPYbEs8Pc7gVwhJ6XuhmkpHArZp8pyFd3pQJhyBYQwqUR4QU41buYuFQ465SyMuCLyXhcevALrcjJRJVJsCpsEEZgqTk5z2oqsNPXNVHweNjeHBUdN9uJBgtQ6v5mVWRdsYUfmwFeQqyvDEaioqAnNNSpSe2ByNfcv8ftSfzocbNHLahUqTbjSvxThW84LpEwMUitaUQoguJweVscdRRitkx1kCmsaMC5JwrRH13zHVoFnJqPEUHZwqYTzAJCf"
    SIGNED_P2TR_PSBT_B64 = "cHNidP8BAKgCAAAAAfn+phUWoAfkdjJXSEFxjcDaXBr22RczfwaOVNq+Sb4/AAAAAAD9////AzoeAAAAAAAAIlEgdeZfiD3lhycx2Y6ob18IYvCSOdDpsA9J9ZIGnBhNAqLoAwAAAAAAACJRIJ0tm23mDNzdWQfBwJYxSRvdQ07uqoqvOzvxnWPVPkCZ6AMAAAAAAAAWABSuzR7cPv9lqiCdAhXnPXCQXcFobIO/KwAAAQErfycAAAAAAAAiUSAGrIL8Ntu2DUh5HYHDwes5f6lz5FbIxvtUwQQhHwR7GgEIQgFAKLB/jRmapaOuXyB0aRBHlcMpGB7KPUxxXppo57U4PYeA2Bq9C2IGQH3SDD/ZR6zpISV74EWLWcrtSOtoYLy7EwETQCiwf40ZmqWjrl8gdGkQR5XDKRgeyj1McV6aaOe1OD2HgNgavQtiBkB90gw/2Ues6SEle+BFi1nK7UjraGC8uxMAAAAA"
    SIGNED_P2TR_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(SIGNED_P2TR_PSBT).to_cbor())
    SIGNED_P2TR_PSBT_SD = b"psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\xf9\xfe\xa6\x15\x16\xa0\x07\xe4v2WHAq\x8d\xc0\xda\\\x1a\xf6\xd9\x173\x7f\x06\x8eT\xda\xbeI\xbe?\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03:\x1e\x00\x00\x00\x00\x00\x00\"Q u\xe6_\x88=\xe5\x87'1\xd9\x8e\xa8o_\x08b\xf0\x929\xd0\xe9\xb0\x0fI\xf5\x92\x06\x9c\x18M\x02\xa2\xe8\x03\x00\x00\x00\x00\x00\x00\"Q \x9d-\x9bm\xe6\x0c\xdc\xddY\x07\xc1\xc0\x961I\x1b\xddCN\xee\xaa\x8a\xaf;;\xf1\x9dc\xd5>@\x99\xe8\x03\x00\x00\x00\x00\x00\x00\x16\x00\x14\xae\xcd\x1e\xdc>\xffe\xaa \x9d\x02\x15\xe7=p\x90]\xc1hl\x83\xbf+\x00O\x01\x045\x87\xcf\x03\xe0\x17\xd1\xbb\x80\x00\x00\x00\x01\x83\\\x0bQ!\x83v\xc6\x14UB\x8a\x9fG\xbf\xcc\xe1\xf6\xce\x83\x97\xea\xd7\xb0\x03\x87\xe9\xd9\xeaV\x83\x02\xcf\xbdq\x001\x1e\x0e\x85\x84L78r\x83\x149N\xb80*kPp\xd6\x92\xe4\x1b\x14\xba\x81\x80\x90\x10s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x01\x01+\x7f'\x00\x00\x00\x00\x00\x00\"Q \x06\xac\x82\xfc6\xdb\xb6\rHy\x1d\x81\xc3\xc1\xeb9\x7f\xa9s\xe4V\xc8\xc6\xfbT\xc1\x04!\x1f\x04{\x1a\x01\x03\x04\x00\x00\x00\x00\x01\x08B\x01@(\xb0\x7f\x8d\x19\x9a\xa5\xa3\xae_ ti\x10G\x95\xc3)\x18\x1e\xca=Lq^\x9ah\xe7\xb58=\x87\x80\xd8\x1a\xbd\x0bb\x06@}\xd2\x0c?\xd9G\xac\xe9!%{\xe0E\x8bY\xca\xedH\xebh`\xbc\xbb\x13\x01\x13@(\xb0\x7f\x8d\x19\x9a\xa5\xa3\xae_ ti\x10G\x95\xc3)\x18\x1e\xca=Lq^\x9ah\xe7\xb58=\x87\x80\xd8\x1a\xbd\x0bb\x06@}\xd2\x0c?\xd9G\xac\xe9!%{\xe0E\x8bY\xca\xedH\xebh`\xbc\xbb\x13!\x16E\xc6\xb1\xe44\x82<\xe9\xe6\xb4H\xfb\xc1\xe4\x05' 8:\r!(\x82\xbc\xbavSMwR\x8a\xad\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\t\x00\x00\x00\x01\x17 E\xc6\xb1\xe44\x82<\xe9\xe6\xb4H\xfb\xc1\xe4\x05' 8:\r!(\x82\xbc\xbavSMwR\x8a\xad\x00\x01\x05  \xeb\x90P\x06\x8b\x01;\xde= M\xb5\x9a\xc5\xdb*\x1cx\xa8\xaa%\x07?\xbf.z\xd4\x9d\x05\x15\xc6!\x07 \xeb\x90P\x06\x8b\x01;\xde= M\xb5\x9a\xc5\xdb*\x1cx\xa8\xaa%\x07?\xbf.z\xd4\x9d\x05\x15\xc6\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x05 \xdc\xab\x8eB3\xd9\x14\xf2\x98\x08\x9e]\x8d;'a\x8a\x07\xf5!?\x89\x9a+\xbd\xbax\xfd\xb9\x02\xc5\xcf!\x07\xdc\xab\x8eB3\xd9\x14\xf2\x98\x08\x9e]\x8d;'a\x8a\x07\xf5!?\x89\x9a+\xbd\xbax\xfd\xb9\x02\xc5\xcf\x19\x00s\xc5\xda\nV\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\n\x00\x00\x00\x00\x00"
    SIGNED_P2TR_PSBT_B64_SD = "cHNidP8BAKgCAAAAAfn+phUWoAfkdjJXSEFxjcDaXBr22RczfwaOVNq+Sb4/AAAAAAD9////AzoeAAAAAAAAIlEgdeZfiD3lhycx2Y6ob18IYvCSOdDpsA9J9ZIGnBhNAqLoAwAAAAAAACJRIJ0tm23mDNzdWQfBwJYxSRvdQ07uqoqvOzvxnWPVPkCZ6AMAAAAAAAAWABSuzR7cPv9lqiCdAhXnPXCQXcFobIO/KwBPAQQ1h88D4BfRu4AAAAABg1wLUSGDdsYUVUKKn0e/zOH2zoOX6tewA4fp2epWgwLPvXEAMR4OhYRMNzhygxQ5TrgwKmtQcNaS5BsUuoGAkBBzxdoKVgAAgAEAAIAAAACAAAEBK38nAAAAAAAAIlEgBqyC/Dbbtg1IeR2Bw8HrOX+pc+RWyMb7VMEEIR8EexoBAwQAAAAAAQhCAUAosH+NGZqlo65fIHRpEEeVwykYHso9THFemmjntTg9h4DYGr0LYgZAfdIMP9lHrOkhJXvgRYtZyu1I62hgvLsTARNAKLB/jRmapaOuXyB0aRBHlcMpGB7KPUxxXppo57U4PYeA2Bq9C2IGQH3SDD/ZR6zpISV74EWLWcrtSOtoYLy7EyEWRcax5DSCPOnmtEj7weQFJyA4Og0hKIK8unZTTXdSiq0ZAHPF2gpWAACAAQAAgAAAAIAAAAAACQAAAAEXIEXGseQ0gjzp5rRI+8HkBScgODoNISiCvLp2U013UoqtAAEFICDrkFAGiwE73j0gTbWaxdsqHHioqiUHP78uetSdBRXGIQcg65BQBosBO949IE21msXbKhx4qKolBz+/LnrUnQUVxhkAc8XaClYAAIABAACAAAAAgAEAAAABAAAAAAEFINyrjkIz2RTymAieXY07J2GKB/UhP4maK726eP25AsXPIQfcq45CM9kU8pgInl2NOydhigf1IT+Jmiu9unj9uQLFzxkAc8XaClYAAIABAACAAAAAgAAAAAAKAAAAAAA="

    # Native Segwit Multisig
    P2WSH_PSBT = b'psbt\xff\x01\x00\xb2\x02\x00\x00\x00\x02\xadC\x87\x14J\xfae\x07\xe1>\xaeP\xda\x1b\xf1\xb5\x1ag\xb3\x0f\xfb\x8e\x0c[\x8f\x98\xf5\xb3\xb1\xa68Y\x00\x00\x00\x00\x00\xfd\xff\xff\xffig%Y\x0f\xb8\xe4r\xab#N\xeb\xf3\xbf\x04\xd9J\xc0\xba\x94\xf6\xa5\xa4\xf8B\xea\xdb\x9a\xd3c`\xd4\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02@B\x0f\x00\x00\x00\x00\x00"\x00 \xa9\x903\xc3\x86b3>Y\t\xae<=\x03\xbdq\x8d\xb2\x14Y\xfd\xd5P\x1e\xe8\xa0RaMY\xb4\xe2\xd8\xd2!\x01\x00\x00\x00\x00"\x00 \x8d\x02\x85\r\xab\x88^\xc5y\xbbm\xcb\x05\xd6 ;\x05\xf5\x17\x01\x86\xac\xb8\x90}l\xc1\xb4R\x99\xed\xd2\x00\x00\x00\x00O\x01\x045\x87\xcf\x04>b\xdf~\x80\x00\x00\x02A+I\x84\xd5I\xba^\xef\x1c\xa6\xe8\xf3u]\x9a\xe0\x16\xdam\x16ir\xca\x0eQ@6~\xddP\xda\x025\xb8K1\xdc8*|\xfbC\xba:{\x17K\xe9AaA\xe8\x16\xf6r[\xd1%\x12\xb5\xb2\xc4\xa5\xac\x14\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04\x9d\xb1\xd0\x00\x80\x00\x00\x02?\xd8\xd7;\xc7\xb8\x8c\xa4\x93Z\xa57\xbf8\x94\xd5\xe2\x88\x9f\xab4\x1ca\x8fJWo\x8f\x19\x18\xc2u\x02h\xc3\rV\x9d#j}\xccW\x1b+\xb1\xd2\xadO\xa9\xf9\xb3R\xa8\t6\xa2\x89\n\x99\xaa#\xdbx\xec\x14&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04\xba\xc1H9\x80\x00\x00\x02\x1dO\xbe\xbd\xd9g\xe1\xafqL\t\x97\xd3\x8f\xcfg\x0b\\\xe9\xd3\x01\xc0D\x0b\xbc\xc3\xb6\xa2\x0e\xb7r\x1c\x03V\x8e\xa1\xf3`Q\x91n\xd1\xb6\x90\xc3\x9e\x12\xa8\xe7\x06\x03\xb2\x80\xbd0\xce_(\x1f)\x18\xa5Sc\xaa\x14s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 \x89\x801pn\xdd\x9e\xb1"g\x85G\x15Q\xce\xa3_\x17\t\xa9o\x85\x96.2\xa0k\xf6~\xc7\x11$\x01\x05iR!\x02N\x8d\x08\x0c}}\xba\\G\xfe\xb6\xb1\xc8\x12M\xebbA\x17\xe5\x8d\x8d~\xb1J@\x04Oq\xdd\x97\xf2!\x03\x05a\xd4\x82\xad\xb9=\xf1\xef\x13\xe8ep\x1a\xf2$n\xf0\xa3l\xbc\x8c\xa5\x12=\x8e\xecw\xceN8\xc7!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87S\xae"\x06\x02N\x8d\x08\x0c}}\xba\\G\xfe\xb6\xb1\xc8\x12M\xebbA\x17\xe5\x8d\x8d~\xb1J@\x04Oq\xdd\x97\xf2\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03\x05a\xd4\x82\xad\xb9=\xf1\xef\x13\xe8ep\x1a\xf2$n\xf0\xa3l\xbc\x8c\xa5\x12=\x8e\xecw\xceN8\xc7\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 3w\xad03\xd1\x05\x9c\xf1\xd25\xbb\x12%\xfc\xa2\xa4\xbf&\xc9R\xd5?o\xef\xc3:-UD\x8d\xc5\x01\x05iR!\x02"\x821\x12\xe5\xcc\x88K\x91\x16\xcb!B\x0c\xc7\x92\x98$\xcd/\xe8\xb7#[\xf9\x92\xe8\xae\xde\x14l"!\x02\x83\xcdG\xe5Sm\xcby\xe7\x11\x830\xe8\xe4\x80B\x12\xf6\x96\x19\xf1\xd6\xec\x99\r\xc75\xef\xb9\xce\xc5t!\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01S\xae"\x06\x02"\x821\x12\xe5\xcc\x88K\x91\x16\xcb!B\x0c\xc7\x92\x98$\xcd/\xe8\xb7#[\xf9\x92\xe8\xae\xde\x14l"\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x02\x83\xcdG\xe5Sm\xcby\xe7\x11\x830\xe8\xe4\x80B\x12\xf6\x96\x19\xf1\xd6\xec\x99\r\xc75\xef\xb9\xce\xc5t\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01iR!\x02\xad!\xd9\xad(\xab\x99\xac~\xdf\xd9\x1e"!O\x11YS\xab\t\xd1\xd5X\x10\x92\xfbG\xbd\xa5\x92r\xfe!\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v!\x03\xa1\xa8C\xfa-A\xd9;\xd6u)a\x91_nD\x8at\x19$J>\x02\xb8\xf4\xcfb\xbc\xc6\xa7\xa2kS\xae"\x02\x02\xad!\xd9\xad(\xab\x99\xac~\xdf\xd9\x1e"!O\x11YS\xab\t\xd1\xd5X\x10\x92\xfbG\xbd\xa5\x92r\xfe\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xa1\xa8C\xfa-A\xd9;\xd6u)a\x91_nD\x8at\x19$J>\x02\xb8\xf4\xcfb\xbc\xc6\xa7\xa2k\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    P2WSH_PSBT_B43 = "9YO76-S3DRXKI-6JS23**6N$12A3MTF2R66Q0-C-*BD+VB.V3O1EM2VDNMX:*DHL-RMVYZ/.W:9XKN7$4/1M0$$U8+$77KE5:40Z527KZOHA-$MLTL21L3*ON6SCCF:4HMW2K1IS7VUOUF6JW/A+DGMGVF17C0BFK/Y*FDJQWWLX*EEJUR12L3*R0.F6W5674M-+KZUKD+77RB$PGQSTPRX49C25391EP+5/ZJ7$N$F+8*CU24O78HRO0-YO51IO7+A8RZ386S5AK200DG92O6P/QT3W.T$NA7*:GYGTFT+ZC9JWTD-BMVZPBNMT9/EGO.ZHBHAPYHU6MN.U.UZ118L8G4PXR5+*SOXHDQGS$+ZY0HX9X016901VG2$.22I8LNKUGLVRBP.G4Y6DXIAO5B6TPES$F8ALOIDB30SH:29L.*/GSED*V-L0CXWM3SI6YZB59SVDKAJPMCBMDF4:8/Y9FEFIN+5AJ:UQ.J*AC+3N5Y/OOU/HCMOBNRHMN-0QZH8*CQ4-7CSJ7+KU:UX5KFO9XUQG+5U2-2VD6NZCF+N0Y97CP8HR$+N2K98A+0Z8ILV0KI634*/WEI+97-B3E*TW-5F82$N.QRDP/4R9Z6/:0H0$A2DKP2V.RUNDT0E56489TJTX48.1DPCP1KY71RVFFEC:/8:3S6EIS2DETQ2U9.N6TK$6+:H6+UH7KG3ZDW39CLSET-V6MEZSTDL*/A65IK.F3TEJSF++3FOO+-F2SOYFS.V/*SSMCJ7$2Z63SS0K+*O88Y-9+A-IQ04-3VE7PAI$MCR*J6O0$*ZJ9W07:/G+ZVGHJIE:/00UE0*CXLY8COUJIB1ITXR.YNFTLT9B.-IA6KQ7R/56G.54NTU2E657O0KNC0DT$+EGI**JM5F0YNRL01/Y*O:1WQU5J*TTZJGG-HJZA2Q+0F:ML1PY1MXYWNM8ABM4*F33XH6HUZMAW82FRSP302M4NARGWWA2DI8CC1$84B/NFJ5WOJE.5UOUUMUILQJZIK3PA2P-18SQTV*R258MJQ+:++DYHCHI6B5I+J3$OB1AKOLKY4I5XD.3Q2JK*RJ1E1LOU1IV/H7555LHI:RKDV-W995M3-*H4-DBBLDSI9BC*C+U978N2-9K$6+0V/PN-TR.-WIBBBI:3QNPXZ/N4MHI+JI:NIN/80OOG39A9$$G3FE+V71:/Y1VD0UUW.+XTVSO$6SHD:1JXTWYUEAPZUD5/28Z5KW843*BS*2.$WYMG+7YI1.H38BL7YN8/4-34XGFS/L.+V0:RSOAU8NP4ZCAU3Q:GL1/SG5ZU$:*58DIWF8.RNIRG22S18LLNKJXQSY.PH3+66PH0J9*I8S9E70-+*W4ADFYICDA4-0$-MTPE7LO*1*UT/Q6DTUBY0MYTKELTSOGJ0*IFU-N9L3E*8T9/Z:D2JMAI-JJQ7EKP859SIN:+I:Z3G209-DA0$9*H7GBEMOM3V5S/T$LLA/J.U-C5+ZIALSP37NKX2*PWB216D6OITOLQ:3.OAG4U/R45PH$$:K1D/$75QC9SK6S7.O0UJFZK7F*PFY8XJHGP-O.P4E07/M-RKIHQ7L$VFN292+UN8F7KZYP$NF/JY4N+9.RXV1DS**QPYQVY2+U9QR/+1T7-2/YAG9K*T549*:/578Q.AI0/1TQZCCG9FLLL4J$+ETZ0LKF+*3DN84F8GC-P4EYLAF923H9JRXNHXDDPN/NX$O$4SELXX$S8QNZJO$Y7GD/LKH$5:-9J6PMTVT/G3+WS-T*FBFTI3JB/A0OWEPAY:GTOFMBV/M$L1.P$N0S2DL/O4D4SUVJ76S21/:Y$VKF4V+SV-0/UO1GSK:G*H-GGL+ST8MBNG*DUEZHCC-$4J9KRL39V9G00YDA6SW2IF8AKCR9L7YV05RGHEJA0BYZVPYOL:KV/UL+$5ZMHJ9F84Q4YU-XR9THI-/$2W9ZQNR-J-N+WXC+A3FSA$2B4$FQH$71P0T8EBR+WM3W-XT*UG$YKZV3*$HU8Q-XRBXD6Q8K.4$COENY4/V3VL5O7SP.0$5+R5VHO./ULKTKC0G/WG8-5*IXB.4QHRYG90IV48VVNZ2-W*Q0QN7XPJIXK1FNPVQNECX:1$+C.U7*I1.WF.N-UVXNPJZCIOCIFJC1-Z7SWS:3SP7N1OCJK.PB4PVGM*.H6BC8ED4*587E:UD"
    P2WSH_PSBT_B58 = "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"
    P2WSH_PSBT_B64 = "cHNidP8BALICAAAAAq1DhxRK+mUH4T6uUNob8bUaZ7MP+44MW4+Y9bOxpjhZAAAAAAD9////aWclWQ+45HKrI07r878E2UrAupT2paT4QurbmtNjYNQBAAAAAP3///8CQEIPAAAAAAAiACCpkDPDhmIzPlkJrjw9A71xjbIUWf3VUB7ooFJhTVm04tjSIQEAAAAAIgAgjQKFDauIXsV5u23LBdYgOwX1FwGGrLiQfWzBtFKZ7dIAAAAATwEENYfPBD5i336AAAACQStJhNVJul7vHKbo83VdmuAW2m0WaXLKDlFANn7dUNoCNbhLMdw4Knz7Q7o6exdL6UFhQegW9nJb0SUStbLEpawUAgjLdzAAAIABAACAAAAAgAIAAIBPAQQ1h88EnbHQAIAAAAI/2Nc7x7iMpJNapTe/OJTV4oifqzQcYY9KV2+PGRjCdQJoww1WnSNqfcxXGyux0q1PqfmzUqgJNqKJCpmqI9t47BQmu4PEMAAAgAEAAIAAAACAAgAAgE8BBDWHzwS6wUg5gAAAAh1Pvr3ZZ+GvcUwJl9OPz2cLXOnTAcBEC7zDtqIOt3IcA1aOofNgUZFu0baQw54SqOcGA7KAvTDOXygfKRilU2OqFHPF2gowAACAAQAAgAAAAIACAACAAAEBK4CWmAAAAAAAIgAgiYAxcG7dnrEiZ4VHFVHOo18XCalvhZYuMqBr9n7HESQBBWlSIQJOjQgMfX26XEf+trHIEk3rYkEX5Y2NfrFKQARPcd2X8iEDBWHUgq25PfHvE+hlcBryJG7wo2y8jKUSPY7sd85OOMchA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHU64iBgJOjQgMfX26XEf+trHIEk3rYkEX5Y2NfrFKQARPcd2X8hwmu4PEMAAAgAEAAIAAAACAAgAAgAAAAAABAAAAIgYDBWHUgq25PfHvE+hlcBryJG7wo2y8jKUSPY7sd85OOMccAgjLdzAAAIABAACAAAAAgAIAAIAAAAAAAQAAACIGA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHHHPF2gowAACAAQAAgAAAAIACAACAAAAAAAEAAAAAAQErgJaYAAAAAAAiACAzd60wM9EFnPHSNbsSJfyipL8myVLVP2/vwzotVUSNxQEFaVIhAiKCMRLlzIhLkRbLIUIMx5KYJM0v6LcjW/mS6K7eFGwiIQKDzUflU23LeecRgzDo5IBCEvaWGfHW7JkNxzXvuc7FdCEDC5DtLoa61/Kk/pdpu0F9e6nKoRJIB9v7Ni377rZefgFTriIGAiKCMRLlzIhLkRbLIUIMx5KYJM0v6LcjW/mS6K7eFGwiHAIIy3cwAACAAQAAgAAAAIACAACAAAAAAAAAAAAiBgKDzUflU23LeecRgzDo5IBCEvaWGfHW7JkNxzXvuc7FdBwmu4PEMAAAgAEAAIAAAACAAgAAgAAAAAAAAAAAIgYDC5DtLoa61/Kk/pdpu0F9e6nKoRJIB9v7Ni377rZefgEcc8XaCjAAAIABAACAAAAAgAIAAIAAAAAAAAAAAAABAWlSIQKtIdmtKKuZrH7f2R4iIU8RWVOrCdHVWBCS+0e9pZJy/iEDoH074LrWPIA10hyXtBCJDT06GdLkA6+z/PxoJqomPHYhA6GoQ/otQdk71nUpYZFfbkSKdBkkSj4CuPTPYrzGp6JrU64iAgKtIdmtKKuZrH7f2R4iIU8RWVOrCdHVWBCS+0e9pZJy/hwCCMt3MAAAgAEAAIAAAACAAgAAgAEAAAAAAAAAIgIDoH074LrWPIA10hyXtBCJDT06GdLkA6+z/PxoJqomPHYcc8XaCjAAAIABAACAAAAAgAIAAIABAAAAAAAAACICA6GoQ/otQdk71nUpYZFfbkSKdBkkSj4CuPTPYrzGp6JrHCa7g8QwAACAAQAAgAAAAIACAACAAQAAAAAAAAAAAA=="
    P2WSH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2WSH_PSBT).to_cbor())

    SIGNED_P2WSH_PSBT = b'psbt\xff\x01\x00\xb2\x02\x00\x00\x00\x02\xadC\x87\x14J\xfae\x07\xe1>\xaeP\xda\x1b\xf1\xb5\x1ag\xb3\x0f\xfb\x8e\x0c[\x8f\x98\xf5\xb3\xb1\xa68Y\x00\x00\x00\x00\x00\xfd\xff\xff\xffig%Y\x0f\xb8\xe4r\xab#N\xeb\xf3\xbf\x04\xd9J\xc0\xba\x94\xf6\xa5\xa4\xf8B\xea\xdb\x9a\xd3c`\xd4\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02@B\x0f\x00\x00\x00\x00\x00"\x00 \xa9\x903\xc3\x86b3>Y\t\xae<=\x03\xbdq\x8d\xb2\x14Y\xfd\xd5P\x1e\xe8\xa0RaMY\xb4\xe2\xd8\xd2!\x01\x00\x00\x00\x00"\x00 \x8d\x02\x85\r\xab\x88^\xc5y\xbbm\xcb\x05\xd6 ;\x05\xf5\x17\x01\x86\xac\xb8\x90}l\xc1\xb4R\x99\xed\xd2\x00\x00\x00\x00\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 \x89\x801pn\xdd\x9e\xb1"g\x85G\x15Q\xce\xa3_\x17\t\xa9o\x85\x96.2\xa0k\xf6~\xc7\x11$"\x02\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87G0D\x02 h?m\x19\x04C\x89\x95\x8b\xba\xed\xbb\xba8)\t\xae^\xe3`\x16G\xc8\x8bq\x9c\x0e\xbc\xc5\xb1j\xa2\x02 \x05\rP(\xe0\x9cc])q\xe5\xe2S\x9f\xaf+\xe4_\xa9\xc6\xf9\r"%\xf4\xa2\x00;\xa2\xaf2W\x01\x01\x05iR!\x02N\x8d\x08\x0c}}\xba\\G\xfe\xb6\xb1\xc8\x12M\xebbA\x17\xe5\x8d\x8d~\xb1J@\x04Oq\xdd\x97\xf2!\x03\x05a\xd4\x82\xad\xb9=\xf1\xef\x13\xe8ep\x1a\xf2$n\xf0\xa3l\xbc\x8c\xa5\x12=\x8e\xecw\xceN8\xc7!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87S\xae\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 3w\xad03\xd1\x05\x9c\xf1\xd25\xbb\x12%\xfc\xa2\xa4\xbf&\xc9R\xd5?o\xef\xc3:-UD\x8d\xc5"\x02\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01G0D\x02 ~O\x1b\x8c\xbb\x87x\xa3\xbb\xff\x04\xd8\x10Cq\xc8Y\x0f;N6\x97\xd8S\xfeti\x80\xb3\x12\xe0>\x02 l\x93=\x02m\xb4<\x90\xf4%\xf9Z${\xb7\xecO\x19\x15\xa3\xa3S\xf2Q\x81\xdcX\xfb\xd5&\x9e\xc5\x01\x01\x05iR!\x02"\x821\x12\xe5\xcc\x88K\x91\x16\xcb!B\x0c\xc7\x92\x98$\xcd/\xe8\xb7#[\xf9\x92\xe8\xae\xde\x14l"!\x02\x83\xcdG\xe5Sm\xcby\xe7\x11\x830\xe8\xe4\x80B\x12\xf6\x96\x19\xf1\xd6\xec\x99\r\xc75\xef\xb9\xce\xc5t!\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01S\xae\x00\x00\x00'
    SIGNED_P2WSH_PSBT_B43 = "*SPXND+LRIGD5M1*NM-KV3RHL.*VA-BKB4S768T1HCIA:IJ:U+OW:72QTH6YLJ2ZVYJW90CFVID.GA2O1G$TG1K3I4759UGCO/U3Z$030$GR5R*OXST6TO$34/UZ*VJ+Z*A2CQVJ8CSN2Z5FK79JTWD$HDPEWX7C8C220T24FZ-RSZ:GM3Y578HCV*FG1QG-/$Q5H0LMI*I1HD$51K6UP.5N0/FOPFC/MIGLLXJP:YTGR11+1JX90+GDZ5+3$/BD*ISW36V$ZK5-3V5ID0VJ9U*X6PL*QH$SP5YQW/SWFNV80VD5MTEN46$P.7EUD4A1A$.5E7H5+51OZAD-.RY9HU*B8/+-TSQ2C4OA6+M6ZBDALSJ5IY2:XB481FZO.WLXUQND-FAB+XAESK9303ZFYA:6CX9AXG/2US*N+*79Y4U68*P/LNPP1PNCC.I3ATP:EN/MBPXU+P*3MX5HDBOR4HT:8RF.WO6HGFL8T*H-+61R+R6V-CJ*-VVLB83QPH*.G0/3T4FN2029Y96+3XMJPPSLU+Q6YW101MH8A3J2CYB*CFS$$NSL5I3OCN*:3V001Z:8PEG:+:HE54GUB2UM*GRY46/639A*40K$SB*G2P$D7PWJHP6SGNO.Z827V6$+09WZR-2GC4-2D9KSNAGK38WUFEV$1UIDZ/+83HX$IKJDYF3AEWR-L9ZX$/5QHW-1HA26CECX52/FQPAFE7ZRPCH9RA9XA556ASF8YW6I4+*ID/8VYMW.I-LQTMVLYFLTV097P*ZGRYONCULW37MFJ408I$CVCV2M.LJ+SV-49.33.WNDE2X5KCC4IVO8F9BH95UN$Q:SCZSR*M2UK/0BWQUO*YT.IB3UW8YV/8NGGOEZGA4QJ2-ICL5MIZ+4U1-QZFMXS6PEEH5IO5RU$+W.DF$5-AMFMQJV1LRLUAHJ9ZGM:WW*.06UQFBBDUO0:YVVO85FSFXE*/:1UIHQW5DJCY2CX0W94Q:D:T8ES9HZON85YXQZTC9+ASY/B525SCPL44BTZ8R1*15:+6-6FQ112E1$G9L"
    SIGNED_P2WSH_PSBT_B58 = "8zF2eD2uMaxb2DsPbbKRp9Mpm1UH66wJ4uSMZPn5MA1nJwE8S3RAGDWCCvsguUhQDPCPVw5S8GsAJvAc811WwP71guKubiPxppUKqaWUkQN71B18krk1K2NrWCA9ewdJE1d1BopmzNBr5Qg3qZNCsN6EDSCn8uow2r97h2rnokSq4nXfy3KE2v7hBrGvSZw8A96WAJDSEnS1sP7U5wgtiSYdWxEHBfKocVC3G3sayPuMEjzA9QcYWpy1U6S3EW8YWw5kvQW88LKg8b3js9R7w9aWFnQwMdRg3CFSfGkoHegiWSufPejQ65Airoo8WqNvGVacmSZybkmcvu57KRobPuhZCDPbtJ5435eJsarQ9nmRpac6VJNoLrdHvkeWRZ9QEXk654TW7z6NV87it5vPVDNEnFW3c9pAdtZsYXHafw7CMSiWRPEsCoRKzodieHJFfeHiJGT5zqcP3bgmHTszp3GPMdRy3onHeFRCoyftuAEBkwsCyaYFwoSBE6YUgjHT1T4mWCoe7W4ktoDEKXsHawFC6sw6KCPzDbuTZJuaDoWijHeo7FnC97QVvMNHdVgz1ZmCerxQLrkFJsT8x5WYuVoMmcHRpbyRcuCV64YYPgFFfCZs7VVedPsgSNdkQ7qKCqVYnTaNiBpeE5NB4gwcMcCYUJMWXkqCq7t91o9Mi5ozv4R9yPonSUaTH13D6FSPY9RSZbU1F9SMgFXBoB4DdssC36RGpqZ3Fnm77RJB5v1WJAQ95RNXHuSuKB43X1HiiKYKohtFrwd7jCtbUGuUUs9mpd7VqdvVtbSE9jpQxgxJHvF983X43ZxKcE2K8AMr4WyL8s2Pi2Xj644V9zauy2qmLeNusxudGNgPdTsktjEoWCSuFPtxuqcmC8MwXh5cSQqiFkULgFNuGtkUajJQEnfW9jMfjm5y7Va5DhJN4S7MN371DgiusGnsmb5YZGBeycptyDykdsFXYs"
    SIGNED_P2WSH_PSBT_B64 = "cHNidP8BALICAAAAAq1DhxRK+mUH4T6uUNob8bUaZ7MP+44MW4+Y9bOxpjhZAAAAAAD9////aWclWQ+45HKrI07r878E2UrAupT2paT4QurbmtNjYNQBAAAAAP3///8CQEIPAAAAAAAiACCpkDPDhmIzPlkJrjw9A71xjbIUWf3VUB7ooFJhTVm04tjSIQEAAAAAIgAgjQKFDauIXsV5u23LBdYgOwX1FwGGrLiQfWzBtFKZ7dIAAAAAAAEBK4CWmAAAAAAAIgAgiYAxcG7dnrEiZ4VHFVHOo18XCalvhZYuMqBr9n7HESQiAgNolXLiiw/tqdaYHAI32eXe2/7BbecUP2gKAu1dFZ91h0cwRAIgaD9tGQRDiZWLuu27ujgpCa5e42AWR8iLcZwOvMWxaqICIAUNUCjgnGNdKXHl4lOfryvkX6nG+Q0iJfSiADuirzJXAQEFaVIhAk6NCAx9fbpcR/62scgSTetiQRfljY1+sUpABE9x3ZfyIQMFYdSCrbk98e8T6GVwGvIkbvCjbLyMpRI9jux3zk44xyEDaJVy4osP7anWmBwCN9nl3tv+wW3nFD9oCgLtXRWfdYdTrgABASuAlpgAAAAAACIAIDN3rTAz0QWc8dI1uxIl/KKkvybJUtU/b+/DOi1VRI3FIgIDC5DtLoa61/Kk/pdpu0F9e6nKoRJIB9v7Ni377rZefgFHMEQCIH5PG4y7h3iju/8E2BBDcchZDztONpfYU/50aYCzEuA+AiBskz0CbbQ8kPQl+Voke7fsTxkVo6NT8lGB3Fj71SaexQEBBWlSIQIigjES5cyIS5EWyyFCDMeSmCTNL+i3I1v5kuiu3hRsIiECg81H5VNty3nnEYMw6OSAQhL2lhnx1uyZDcc177nOxXQhAwuQ7S6GutfypP6XabtBfXupyqESSAfb+zYt++62Xn4BU64AAAA="
    SIGNED_P2WSH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(SIGNED_P2WSH_PSBT).to_cbor())
    SIGNED_P2WSH_PSBT_SD = b'psbt\xff\x01\x00\xb2\x02\x00\x00\x00\x02\xadC\x87\x14J\xfae\x07\xe1>\xaeP\xda\x1b\xf1\xb5\x1ag\xb3\x0f\xfb\x8e\x0c[\x8f\x98\xf5\xb3\xb1\xa68Y\x00\x00\x00\x00\x00\xfd\xff\xff\xffig%Y\x0f\xb8\xe4r\xab#N\xeb\xf3\xbf\x04\xd9J\xc0\xba\x94\xf6\xa5\xa4\xf8B\xea\xdb\x9a\xd3c`\xd4\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x02@B\x0f\x00\x00\x00\x00\x00"\x00 \xa9\x903\xc3\x86b3>Y\t\xae<=\x03\xbdq\x8d\xb2\x14Y\xfd\xd5P\x1e\xe8\xa0RaMY\xb4\xe2\xd8\xd2!\x01\x00\x00\x00\x00"\x00 \x8d\x02\x85\r\xab\x88^\xc5y\xbbm\xcb\x05\xd6 ;\x05\xf5\x17\x01\x86\xac\xb8\x90}l\xc1\xb4R\x99\xed\xd2\x00\x00\x00\x00O\x01\x045\x87\xcf\x04>b\xdf~\x80\x00\x00\x02A+I\x84\xd5I\xba^\xef\x1c\xa6\xe8\xf3u]\x9a\xe0\x16\xdam\x16ir\xca\x0eQ@6~\xddP\xda\x025\xb8K1\xdc8*|\xfbC\xba:{\x17K\xe9AaA\xe8\x16\xf6r[\xd1%\x12\xb5\xb2\xc4\xa5\xac\x14\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04\x9d\xb1\xd0\x00\x80\x00\x00\x02?\xd8\xd7;\xc7\xb8\x8c\xa4\x93Z\xa57\xbf8\x94\xd5\xe2\x88\x9f\xab4\x1ca\x8fJWo\x8f\x19\x18\xc2u\x02h\xc3\rV\x9d#j}\xccW\x1b+\xb1\xd2\xadO\xa9\xf9\xb3R\xa8\t6\xa2\x89\n\x99\xaa#\xdbx\xec\x14&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04\xba\xc1H9\x80\x00\x00\x02\x1dO\xbe\xbd\xd9g\xe1\xafqL\t\x97\xd3\x8f\xcfg\x0b\\\xe9\xd3\x01\xc0D\x0b\xbc\xc3\xb6\xa2\x0e\xb7r\x1c\x03V\x8e\xa1\xf3`Q\x91n\xd1\xb6\x90\xc3\x9e\x12\xa8\xe7\x06\x03\xb2\x80\xbd0\xce_(\x1f)\x18\xa5Sc\xaa\x14s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 \x89\x801pn\xdd\x9e\xb1"g\x85G\x15Q\xce\xa3_\x17\t\xa9o\x85\x96.2\xa0k\xf6~\xc7\x11$"\x02\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87G0D\x02 h?m\x19\x04C\x89\x95\x8b\xba\xed\xbb\xba8)\t\xae^\xe3`\x16G\xc8\x8bq\x9c\x0e\xbc\xc5\xb1j\xa2\x02 \x05\rP(\xe0\x9cc])q\xe5\xe2S\x9f\xaf+\xe4_\xa9\xc6\xf9\r"%\xf4\xa2\x00;\xa2\xaf2W\x01\x01\x05iR!\x02N\x8d\x08\x0c}}\xba\\G\xfe\xb6\xb1\xc8\x12M\xebbA\x17\xe5\x8d\x8d~\xb1J@\x04Oq\xdd\x97\xf2!\x03\x05a\xd4\x82\xad\xb9=\xf1\xef\x13\xe8ep\x1a\xf2$n\xf0\xa3l\xbc\x8c\xa5\x12=\x8e\xecw\xceN8\xc7!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87S\xae"\x06\x02N\x8d\x08\x0c}}\xba\\G\xfe\xb6\xb1\xc8\x12M\xebbA\x17\xe5\x8d\x8d~\xb1J@\x04Oq\xdd\x97\xf2\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03\x05a\xd4\x82\xad\xb9=\xf1\xef\x13\xe8ep\x1a\xf2$n\xf0\xa3l\xbc\x8c\xa5\x12=\x8e\xecw\xceN8\xc7\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x01+\x80\x96\x98\x00\x00\x00\x00\x00"\x00 3w\xad03\xd1\x05\x9c\xf1\xd25\xbb\x12%\xfc\xa2\xa4\xbf&\xc9R\xd5?o\xef\xc3:-UD\x8d\xc5"\x02\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01G0D\x02 ~O\x1b\x8c\xbb\x87x\xa3\xbb\xff\x04\xd8\x10Cq\xc8Y\x0f;N6\x97\xd8S\xfeti\x80\xb3\x12\xe0>\x02 l\x93=\x02m\xb4<\x90\xf4%\xf9Z${\xb7\xecO\x19\x15\xa3\xa3S\xf2Q\x81\xdcX\xfb\xd5&\x9e\xc5\x01\x01\x05iR!\x02"\x821\x12\xe5\xcc\x88K\x91\x16\xcb!B\x0c\xc7\x92\x98$\xcd/\xe8\xb7#[\xf9\x92\xe8\xae\xde\x14l"!\x02\x83\xcdG\xe5Sm\xcby\xe7\x11\x830\xe8\xe4\x80B\x12\xf6\x96\x19\xf1\xd6\xec\x99\r\xc75\xef\xb9\xce\xc5t!\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01S\xae"\x06\x02"\x821\x12\xe5\xcc\x88K\x91\x16\xcb!B\x0c\xc7\x92\x98$\xcd/\xe8\xb7#[\xf9\x92\xe8\xae\xde\x14l"\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x02\x83\xcdG\xe5Sm\xcby\xe7\x11\x830\xe8\xe4\x80B\x12\xf6\x96\x19\xf1\xd6\xec\x99\r\xc75\xef\xb9\xce\xc5t\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01iR!\x02\xad!\xd9\xad(\xab\x99\xac~\xdf\xd9\x1e"!O\x11YS\xab\t\xd1\xd5X\x10\x92\xfbG\xbd\xa5\x92r\xfe!\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v!\x03\xa1\xa8C\xfa-A\xd9;\xd6u)a\x91_nD\x8at\x19$J>\x02\xb8\xf4\xcfb\xbc\xc6\xa7\xa2kS\xae"\x02\x02\xad!\xd9\xad(\xab\x99\xac~\xdf\xd9\x1e"!O\x11YS\xab\t\xd1\xd5X\x10\x92\xfbG\xbd\xa5\x92r\xfe\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xa1\xa8C\xfa-A\xd9;\xd6u)a\x91_nD\x8at\x19$J>\x02\xb8\xf4\xcfb\xbc\xc6\xa7\xa2k\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    # Native Segwit Multisig with descriptor
    # wsh(sortedmulti(2,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*,[8cb36b38/48h/1h/0h/2h]tpubDESTVwqbbaSoN2mPq7tcWkPBpRBkaEADrUzUhRTVnNef6oVn6w2PHL4zoUjUAJSPLJQRBetkgX4sDRcoaCyFHxqHGyWyaiV8REKDkh7zQac/<0;1>/*,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*))#jpxgnm0a
    # tb1qv5msefky74hy2q3jtws7dn4cwjlzhtuhm4vdkvsrfar63adxs0tqj22u6n
    DESC_P2WSH_PSBT = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\'\xc8\x13r\x92m\x18\xc4\x9a\x98\xfe\xca\xf3F\x11c5\xc7\xb71:pz\xc8\xddbO\xd0d\xd3vi\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x03\xa0\x86\x01\x00\x00\x00\x00\x00\x16\x00\x14\x81@~\xa4-\xd4\xf1\xe3\x8c\xff\xf5i\xae\xa3\xb2\xb8[\x9dS\xdc@\r\x03\x00\x00\x00\x00\x00"\x00 \xd3{\x8a\xe1\xa4I`\x9e~o\xb0\x92\x88;\x05\xd4\xffu \xa7\x85xL\x8a\x8bf\xfcM\xdc\x05\xe7_\xc8\xbd\t\x00\x00\x00\x00\x00"\x00 y\xb6\xed,\xc2\xd7\xc2\xae\xf6\xcd\xe4\x9d{\x8f?~\xfc\x81\xa5\x8c\x9b\xdf1:M\xef\x83\x07\xeb\x11\x93\xa6>\x06\x01\x00O\x01\x045\x87\xcf\x04\xba\xc1H9\x80\x00\x00\x02\x1dO\xbe\xbd\xd9g\xe1\xafqL\t\x97\xd3\x8f\xcfg\x0b\\\xe9\xd3\x01\xc0D\x0b\xbc\xc3\xb6\xa2\x0e\xb7r\x1c\x03V\x8e\xa1\xf3`Q\x91n\xd1\xb6\x90\xc3\x9e\x12\xa8\xe7\x06\x03\xb2\x80\xbd0\xce_(\x1f)\x18\xa5Sc\xaa\x14s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04II\x11\x9b\x80\x00\x00\x02!b@\xe6\xb4\xfd`\xba^x!\x05\x06vc\xf3\xce\x17\xfc\xaf\x89;2Wk\x14\x05\xfb\x8f\x7f\xbc\xf3\x02\xe6\xa6\x9e\xe0i|^\x8e\xd6X\x93T\xdc\xf7\x9aKE\x90\xe5\x805m\xd7\x87\x1a\xe3\xac:p@\x1f\x0f\x14\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80O\x01\x045\x87\xcf\x04H\x89\xb3(\x80\x00\x00\x02x\x087\xf3\xb3\x13+\xc3dW2rH\xe4\xaauW\xc1p^#\xcaQ\x1a2\xd0guibb2\x03jUu5\xb0U\xa8\x19w\xdeXmsN,\xa1[\xd8T\xbd\xaaZ\x03|\xfeL\x00KJ\xe4\xdf\xb1\x14\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x01\x01+@B\x0f\x00\x00\x00\x00\x00"\x00 e7\x0c\xa6\xc4\xf5nE\x022[\xa1\xe6\xce\xb8t\xbe+\xaf\x97\xddX\xdb2\x03OG\xa8\xf5\xa6\x83\xd6\x01\x03\x04\x01\x00\x00\x00\x01\x05iR!\x02Bi\x80\xf9J\x9c\xbd:\xeeJ\x99\xa8\x04$\x1c\x98\xe9!\xc8Q4 \xe9f3\'\xffbtAc\n!\x02\xfcV-\xf5\xday-\x1a!\xb2\xac\x82\xe5\xe2\xd6\'u\x01\xf9Z\xf3\xdaZ\r\xac\xa4v\xb8@\xd6,w!\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01S\xae"\x06\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x02Bi\x80\xf9J\x9c\xbd:\xeeJ\x99\xa8\x04$\x1c\x98\xe9!\xc8Q4 \xe9f3\'\xffbtAc\n\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x02\xfcV-\xf5\xday-\x1a!\xb2\xac\x82\xe5\xe2\xd6\'u\x01\xf9Z\xf3\xdaZ\r\xac\xa4v\xb8@\xd6,w\x1c\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01iR!\x03\x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd!\x03,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87S\xae"\x02\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x02\x03,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x02\x03\x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd\x1c\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x01iR!\x02*\xd3\x9d\'a\x88\xa4U\xbb\x00\xcf\xd1s\xce\x1az\x8b\xae6\xf0\xebx\xe8\x02\x9eD\xfe\xc1\t:\xc5?!\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v!\x03\xa4\xbc\xa4b\xe0\xd5\xa2\x13\x11P\xb9\xc2\xb2P>\xa9Sb\x8eWH\x14\x7f^6o\xd37\xe9\x12\x07\xdcS\xae"\x02\x03\xa0};\xe0\xba\xd6<\x805\xd2\x1c\x97\xb4\x10\x89\r=:\x19\xd2\xe4\x03\xaf\xb3\xfc\xfch&\xaa&<v\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x02*\xd3\x9d\'a\x88\xa4U\xbb\x00\xcf\xd1s\xce\x1az\x8b\xae6\xf0\xebx\xe8\x02\x9eD\xfe\xc1\t:\xc5?\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xa4\xbc\xa4b\xe0\xd5\xa2\x13\x11P\xb9\xc2\xb2P>\xa9Sb\x8eWH\x14\x7f^6o\xd37\xe9\x12\x07\xdc\x1c\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00'
    DESC_P2WSH_PSBT_B43 = "3/6JFP0WH4Z9X7CPKDVO$8*3DH$NZCPN-$*3TN/E/KJNHYTO:W07H:D0BZAF74VNH+GPE2YELQ$X3F.5XI9F$BJ$25I1U.82XUY1HPDK/US8NGLTF.3JII1**LKAF9GQ5ZOUP0R.C127IUN6B7Z7US6M$8FN6/:*4PFJ//R3B2.NT3ITZO+7N24RQJW.XR9S5HU9SQX+5V+7Y/5T5LLMN3-64CIX:/+99881O9TCG*YH*PDT3+MJ9TI3MNM0GWAIEZVW*B*L6ZTYPHOCDO1+HHK*I+1YO.IVWBC:0585+J:DCG.**86V-EVV-NHS*/GPL/O*HQA11ZW7MH9-C:PM++$980X.YAMKQE7CSTUXVZNXFBARLIJPZ/KY0OG2:K:./1:LX-Z-DELF7$WQKJ07EPGC6F9DA4O8M9/RC6F.6BI2P2.1HKO2K3UMVV*85S-$MYK$60IP3E+J5E07L03TWZKIZ26R-G2:92Q24MZB*2FURCVC8I41B5OGFFZ/*5X7P1GQ*RGI65K1NO2-9-KXI3Y9.D.32A2ZKAXJF$*JP$OK8PGH38*+S:ZZO+S$ZJLRZ.VNSDR$T3G6KE-6FH+:W7*U921QCUI4G7Q6OMVKXN:XAI-T.TC4::5AEGYJKPWYCZ/KPRP4KMNHP4J4/C9Y/AX8JC:KFTJ3S5Z:/B:F9$Y1Y26GOF+6EEMYN.0LKWTKKQZ+:WCM-8IALYPY5H.KP8+6UDCD42W1N*0035.M*T4Y11ZL3BWFK06+79+Q1383T.H2AL8E-/3$4X$P*-PX/Y8DPLFTF8V$FAKBWMGJ4+:KNN4K7WWU0$EC+9ZQD2LFOP4GXN3/P-01-95QDT:V-M9$8:VQGA*1DM6QITM9I/SLTXYIQRQT5FV9VR6-B.HYAW9K-8+BD$$49+-ZEEXQJ:ULTAX5KB5VLXTN-YG77MJUEL.87-.EFWE10R8MGEE5I3*1C2F6I3*:BAPR17HF6DK7BBGVYG1:A514W:1+X*A8IZETH-GQ$APGF+XLF:3U:8GACB-S-$B.V1SK7B:TKYPF5BDG$JZ4A:SZ.F5XRQXH+H.:K948+VTDTASOJIP7XLHYFMXGL56US//B/I+HG/+.5$NOKLI3AIH/XO*HNXLG20RA60M7GU$VA22WC-B*3MHBTCHB170YB952IDBI2/0UB*MPS44$.V*863ZR:7PJ6:/*0XSG$M*QMIK*MZ2:970S0LB2TV5FP2J.B.M2PGKKH$4E94TCAT**HK78XO/0$RJ8.DBW/GT8-//P$QJ$1YA2YY$516:M$SKLBJO.GZOWG*LWUXIGJ5HI0IT/88HMDFT7P8WF9N$CD42-OKKQ+OHRNW$3$-X$$J-GG+9VFOLPOZ2G37ELDLR9U:$7+V-B$PV*N82AJ3K8O24NZ$Y*RQ0EW.33:D.+AFY85M4RQBJRRU38PO*VQZDAM9ZPBY..9*DOTH6IT/3UWUC*1:UVKCX/-3A7P/FVU$F.PZ8K71JZF*IYY.PMF4P2Y$UPLNRT*D7K4GE3SHC0OZDS7A0F7THR-COAA6LBX$4DM8+P4NL-NTH:7:A$OC08AG2MHE0CU6HTL52C2O/OWG/XRV+CHNCJEEEZQLJJ-AO3YJVLK:B9L4/1HTC1/0W.:+R8QEA7Q.TRH1H6D66JE$M8EMZXZ0MYE729E.-7CN020Q4C+YS0H/7MZ5K$0O0/PW6R4CMGYSJNSI:N+G2/.H4XQCQI2J221US22CPO18-K/3WO*D.:W::ZQ5S2+$HZPH-VX+C6RZD0.CTD/R9OIB7Y6NW+*K/R/CZN4VDV:-HA25I7CJR*0T0KZ0PZT+YIUP:Z81FIAN6W*S-I4YQ/D.Z2U3XHSY$3G4RRJL+G$M4OQESTFTJN.S/GNQKI:+.*43D/SKKGN2-59O3/YBSZ0./QXW**O.D5-E85SYXARPXUVWUQ/41EXU-QP587RGJ2PFP23GJ+6.NS-LN:R5GCDVN1L--0KV:Y00L6-J0-R+6/JE17K3N5IWPOS8FTG/3N381678BT1ZG86MFT/4VTL:/BX-N/QF:BG1PQLMNMLWD3*42E1.FSWSX29H*HJEBXP7O7GQOK$KN-JCT5B6YQD0IOV198W7:ZXP5"
    DESC_P2WSH_PSBT_B58 = "3jx2X8ZwCij2rNtfMg7mupXikVogYxqSzch7asET73FeLCVjUDuMSCmyaT7QYNGSpubqL1hGQVrB7d3m7bq5DeMEg6ndo3hSMvp7P9qrB71vQuJLogN8yrD7dFuQVhgGVCC7bHR7GjaWBEPS33rN8HycsqZxqaYR9KpVehrXRb6RUdrZ9TYuwDA1BEDuEsFmb746DPEfaFodqaRCJAo6RqKntThwN1fcXSxSu4yURrLer1aBGBvXEwX3yNMkSFignLGGjRV9uvjE8AQQSZpph39B5GDvopCUbcGDKh8EoN6NRzZmxoCgynfwzfreBBzgKtFjKfEAb3YFVVkuzUpGhtgNrvT1uAEWprFn7gqF9yHErZXUpGnsWoboFRG8zfvpcsagtx95PetX6DGrq7Z1Fz1MovpT4Z2YF7aytwuKx44pWU5765PXAfUegR7CXNkRsYpteZ5zjs2tuPK3AjAGvjKCfmidb1tbgtVmWPP2Mrc13h9ygdzpKCp6PJ3t78EGeKZFqEjxvV5BcjFdVSVG4JqMEEC3qbhn9jnVsKz1susod1YfyDAUAR7VZbvcNmzUjaCUs4hpMUZmJkZjun57Zi7h1Ua8tyJYphAMtmXqzSHLnKMpsHBhr9jpY66b16uo3FMcHULqVgeHs1mJZvEk7e3smpJBr6k1rifAkFvTyUYKpte3ytEZiyjvjGKuexLAm6QP7BVfmqTo2G2tPwj5F9VmjvRKoNXbmxACHvvRDdbVPutrAYWGBNBhq8ZfNBQy3aJEqC7gHk2mhUhVBiCYbSNRXja4fyK9vb78v2Madh67sBThaHtQH91L1Lb9jhDos1gsJvs67HpbBNcJk1KFXDvLwQJGDnXubyW8iKh3pff5qumQxk9GL6jN8MqDrCQWheRKEEsQcNVAZPZ2sK5DETMuaAbcpHvEjm484ZdZetPUM8vkZ769BSzipYXq7UKzPAzKbtSpyaavE6uSN9bETaKjBpmTeg1ftrb4Kt9GHGUwqqUUZc8KhR3ebCuGZH8CwzYAQmkFStR3oHJ3McTUrv1wSNL9QneQqEVhr2gk11TPodbQP3uWh2w6RaUfy37zAWWen4AbhzdGWjRNqikHzFYpb1nbzCdqjegS6hH1y7GV2NAfTdNMtUWhgL913T7649LCyywKQhmJLTcKtoRj1JafydzGQWMwWLc7HJKDgm5u9rcEouYiEaN6sXFmzgoihee9dCzQ5znEwPrnRVTryXhGfmZaGcbCV6S7JTFSKyPGGBroQiiXyo8XA9k18mtwF16D6rW7uZFPGswKX4zMEf2W4StPB91rjULYtCkB8PyZhKRf74kf5mV2tYLRxLHmUEsmqs73iZfb9wz6Ejk23zrhqzscEzip5U2UtN331VUEiw4cD3UVH2HqZSWQKvxRBZHuqaHty8FXo5LLWvDD691Ku8KjRL5GJbVNT7ywRxUY3XYhkvCRJLZ9xuNt6v6irbJnMDEuN9ygtDz32mWKzdJwCKwe4Ds5ZU1FWjSuwk52Z2Hw3q2rvfCvhRLBRkYFbgjC8ZSCnVakdjVe63ZH1aG71nt8FLdnwWGQa7u9KN3X7rAbaEKcTSEwjzUNdEjf8P5hsE2QdKY1X2FtXxi6cwKMzPvJna73s2mhAJBygSiJMSiEQfS4xn2rVrtTgHjj1drJ6jji3MTGj5nSzz7WoDAJYdd5orgdboqzdw9KaVrkXFoKg3QoiWhX55mHpYZcV6p976GD8EXacWgLJ2iCGWddGs2vhf1LPFs2Yc2cN4ddAhHHyGVUPuH95RobwoV14kqzqCjnAiQHmMyohmvVBUjRek6cBxpEuEixkJbAy2J4YguX3cBUafUg6UBmapY7GC938r2QWHWVHu6TtvzQNsbJT6cYiZUjDyHuiLggt15NJRe84fqDB7Ss9acefv5uhGA3UsFkbUfnsdmS3jZafEUGghVNLs74aDmn36nCDRy"
    DESC_P2WSH_PSBT_B64 = "cHNidP8BAKgCAAAAASfIE3KSbRjEmpj+yvNGEWM1x7cxOnB6yN1iT9Bk03ZpAQAAAAD9////A6CGAQAAAAAAFgAUgUB+pC3U8eOM//VprqOyuFudU9xADQMAAAAAACIAINN7iuGkSWCefm+wkog7BdT/dSCnhXhMiotm/E3cBedfyL0JAAAAAAAiACB5tu0swtfCrvbN5J17jz9+/IGljJvfMTpN74MH6xGTpj4GAQBPAQQ1h88EusFIOYAAAAIdT7692Wfhr3FMCZfTj89nC1zp0wHARAu8w7aiDrdyHANWjqHzYFGRbtG2kMOeEqjnBgOygL0wzl8oHykYpVNjqhRzxdoKMAAAgAEAAIAAAACAAgAAgE8BBDWHzwRJSRGbgAAAAiFiQOa0/WC6XnghBQZ2Y/POF/yviTsyV2sUBfuPf7zzAuamnuBpfF6O1liTVNz3mktFkOWANW3XhxrjrDpwQB8PFALov/IwAACAAQAAgAAAAIACAACATwEENYfPBEiJsyiAAAACeAg387MTK8NkVzJySOSqdVfBcF4jylEaMtBndWliYjIDalV1NbBVqBl33lhtc04soVvYVL2qWgN8/kwAS0rk37EUjLNrODAAAIABAACAAAAAgAIAAIAAAQErQEIPAAAAAAAiACBlNwymxPVuRQIyW6Hmzrh0viuvl91Y2zIDT0eo9aaD1gEDBAEAAAABBWlSIQJCaYD5Spy9Ou5KmagEJByY6SHIUTQg6WYzJ/9idEFjCiEC/FYt9dp5LRohsqyC5eLWJ3UB+Vrz2loNrKR2uEDWLHchAwuQ7S6GutfypP6XabtBfXupyqESSAfb+zYt++62Xn4BU64iBgMLkO0uhrrX8qT+l2m7QX17qcqhEkgH2/s2Lfvutl5+ARxzxdoKMAAAgAEAAIAAAACAAgAAgAAAAAAAAAAAIgYCQmmA+UqcvTruSpmoBCQcmOkhyFE0IOlmMyf/YnRBYwocAui/8jAAAIABAACAAAAAgAIAAIAAAAAAAAAAACIGAvxWLfXaeS0aIbKsguXi1id1Afla89paDaykdrhA1ix3HIyzazgwAACAAQAAgAAAAIACAACAAAAAAAAAAAAAAAEBaVIhAxJxGhUobdA8J0f7E7VomnEkvEUxMfwTRM7H+sSC6RvdIQMsxFJkFzYha8pYnAzBATjdV3NTdTOYsxKcFRr0f/k2kiEDaJVy4osP7anWmBwCN9nl3tv+wW3nFD9oCgLtXRWfdYdTriICA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHHHPF2gowAACAAQAAgAAAAIACAACAAAAAAAEAAAAiAgMsxFJkFzYha8pYnAzBATjdV3NTdTOYsxKcFRr0f/k2khwC6L/yMAAAgAEAAIAAAACAAgAAgAAAAAABAAAAIgIDEnEaFSht0DwnR/sTtWiacSS8RTEx/BNEzsf6xILpG90cjLNrODAAAIABAACAAAAAgAIAAIAAAAAAAQAAAAABAWlSIQIq050nYYikVbsAz9Fzzhp6i6428Ot46AKeRP7BCTrFPyEDoH074LrWPIA10hyXtBCJDT06GdLkA6+z/PxoJqomPHYhA6S8pGLg1aITEVC5wrJQPqlTYo5XSBR/XjZv0zfpEgfcU64iAgOgfTvgutY8gDXSHJe0EIkNPToZ0uQDr7P8/GgmqiY8dhxzxdoKMAAAgAEAAIAAAACAAgAAgAEAAAAAAAAAIgICKtOdJ2GIpFW7AM/Rc84aeouuNvDreOgCnkT+wQk6xT8cAui/8jAAAIABAACAAAAAgAIAAIABAAAAAAAAACICA6S8pGLg1aITEVC5wrJQPqlTYo5XSBR/XjZv0zfpEgfcHIyzazgwAACAAQAAgAAAAIACAACAAQAAAAAAAAAA"
    DESC_P2WSH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(DESC_P2WSH_PSBT).to_cbor())

    DESC_SIGNED_P2WSH_PSBT = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\'\xc8\x13r\x92m\x18\xc4\x9a\x98\xfe\xca\xf3F\x11c5\xc7\xb71:pz\xc8\xddbO\xd0d\xd3vi\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x03\xa0\x86\x01\x00\x00\x00\x00\x00\x16\x00\x14\x81@~\xa4-\xd4\xf1\xe3\x8c\xff\xf5i\xae\xa3\xb2\xb8[\x9dS\xdc@\r\x03\x00\x00\x00\x00\x00"\x00 \xd3{\x8a\xe1\xa4I`\x9e~o\xb0\x92\x88;\x05\xd4\xffu \xa7\x85xL\x8a\x8bf\xfcM\xdc\x05\xe7_\xc8\xbd\t\x00\x00\x00\x00\x00"\x00 y\xb6\xed,\xc2\xd7\xc2\xae\xf6\xcd\xe4\x9d{\x8f?~\xfc\x81\xa5\x8c\x9b\xdf1:M\xef\x83\x07\xeb\x11\x93\xa6>\x06\x01\x00\x00\x01\x01+@B\x0f\x00\x00\x00\x00\x00"\x00 e7\x0c\xa6\xc4\xf5nE\x022[\xa1\xe6\xce\xb8t\xbe+\xaf\x97\xddX\xdb2\x03OG\xa8\xf5\xa6\x83\xd6"\x02\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01G0D\x02 %W.f$%C\x19\xde|\x8b\x83J>\xb7\xcc\xdd\xcf0\xe3\x1e\xe5j\x90\x99\xa5OD"\xf5u\x85\x02 \x0b\x9a\x92\xb8\xa9\x9f[\xb9\xe4\xc5\xd6\\\x83\xc1\x8f9\xdbB?\x8b\xc0\xffW\x0b\x15\x98{\xd8\x92;\x8el\x01\x01\x05iR!\x02Bi\x80\xf9J\x9c\xbd:\xeeJ\x99\xa8\x04$\x1c\x98\xe9!\xc8Q4 \xe9f3\'\xffbtAc\n!\x02\xfcV-\xf5\xday-\x1a!\xb2\xac\x82\xe5\xe2\xd6\'u\x01\xf9Z\xf3\xdaZ\r\xac\xa4v\xb8@\xd6,w!\x03\x0b\x90\xed.\x86\xba\xd7\xf2\xa4\xfe\x97i\xbbA}{\xa9\xca\xa1\x12H\x07\xdb\xfb6-\xfb\xee\xb6^~\x01S\xae\x00\x00\x00\x00'
    DESC_SIGNED_P2WSH_PSBT_B43 = "4/.G:UYEK5AMD0MHBHG13G.LD0DMSN0DAO:0IJPF8RF0JH4ZNAC:TYRA2JIO2QX:GRSJ8E:QGO0M3VZCDZMCOTMN9E63370-UTOCR31LI024JWT$REDBLL6YC*.J2R0KOHHEKJ.XHZL8J3FK2W5M402A7/FF$IL24B:UAFC1YC/4342.B$P*BLP0N35YHQ$G7V3*V:+CKF$L7V5.T1U78YG6*B20KIQBOG56QQK8KS/X2G3O6W6HS.JXETL:-5S$EON-ZZ6FO.DN03G-6HUHI:Y8FQTZ6.B/VG/R8:Z.RDX9LUY+XWUYX-T8D017HPLG+9V397ZT3:T*7ZTAYD.NW.SI:Y3GMA72:9L:7GDAEKTS-CR2:RTDE9:JJ-JMBJLAPBYLNZ1267-EI-QOR84L-QNISTKW+Y8T9QDIMF7*ZS+H4AED7EH7R01-JE9CC7E//87KCNFPA+BB277SZRI41.F/EZJ5V7WZXL$KU/BEFG1GXM17EN+EAFVL7UE7D+MIW1IWNTA$R9GTT8.V$-EMGV7FVWK.UVVE$LU81JSD7GYM+NO.2WSXG17.BUP2Z.--UKUWUMU7-PUZ32FT2VTTLXTG4A/ERGP01/.823-PNP9T$QBGS5PKO66W6VN.0KB7G+H6T8FLH0V9"
    DESC_SIGNED_P2WSH_PSBT_B58 = "6U4CYuYnKrhe8dUK8v7w2Jg9m3oSVzMPucwDuvsiMsxPZSbBbHesQk5q3egGVfbe553KnFcwEFjPhRPWQ7MXPyZVinB2MPA3zeVuZHAHTphXCN3uS2TAiSpwGEAY1EWxjUywu3dPPhVDHUzz8sjiCfmvQYmXcLu9nBVG2S1v4sVWii3BvvxDmihkdSMDuoouFysRjttBB7RN9H2tDiSSNLRwWey6dMKr6hADHTXozKcgEr9R5sPhkXBmwMGwW2AbDAjaLBX3fAtDr8ExUtHBhADgE9JNZWRroRgHH9hkmG1FZkEQBGhpv1QuH8gdhonpgY7HYUXGmz1YUKuvjPybvQZrbwwGHViVNuiMvNFBsNJsyURz6U3Xv4RzQ3PwxrTkGwSW6wa4TqiLZACesQBB9taGVFEiVS7aNFAoSdRaTb5n1FsUR8rHiyPY2XsVM67ENHZ7TcGdpwsyeGL5aTm1Bu9GWKYxzFnhA7AW2ojjhZ7CT28rxg5cqCHZJWBL42ZowTiNVKRS87YqYQE7E5DHzh71jqVQ9dDPZAbec4QDnnT1LohBjsS9TWWevGYJ5dPFz93sMJyKstCjqcaqX94TP1LnQAo9"
    DESC_SIGNED_P2WSH_PSBT_B64 = "cHNidP8BAKgCAAAAASfIE3KSbRjEmpj+yvNGEWM1x7cxOnB6yN1iT9Bk03ZpAQAAAAD9////A6CGAQAAAAAAFgAUgUB+pC3U8eOM//VprqOyuFudU9xADQMAAAAAACIAINN7iuGkSWCefm+wkog7BdT/dSCnhXhMiotm/E3cBedfyL0JAAAAAAAiACB5tu0swtfCrvbN5J17jz9+/IGljJvfMTpN74MH6xGTpj4GAQAAAQErQEIPAAAAAAAiACBlNwymxPVuRQIyW6Hmzrh0viuvl91Y2zIDT0eo9aaD1iICAwuQ7S6GutfypP6XabtBfXupyqESSAfb+zYt++62Xn4BRzBEAiAlVy5mJCVDGd58i4NKPrfM3c8w4x7lapCZpU9EIvV1hQIgC5qSuKmfW7nkxdZcg8GPOdtCP4vA/1cLFZh72JI7jmwBAQVpUiECQmmA+UqcvTruSpmoBCQcmOkhyFE0IOlmMyf/YnRBYwohAvxWLfXaeS0aIbKsguXi1id1Afla89paDaykdrhA1ix3IQMLkO0uhrrX8qT+l2m7QX17qcqhEkgH2/s2Lfvutl5+AVOuAAAAAA=="
    DESC_SIGNED_P2WSH_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(DESC_SIGNED_P2WSH_PSBT).to_cbor()
    )

    # Nested Segwit Multisig
    P2SH_P2WSH_PSBT = b'psbt\xff\x01\x00r\x02\x00\x00\x00\x01\x1d\xf4\'\xad\xbd\x8bv?G\xcc(F\x92\xd0\xf4\x95\x1a\xdfZ\xca\xc7#>7.\r\x12\xc9\x9e\xe3\xc1\x96\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02\xdc9]\x05\x00\x00\x00\x00\x17\xa9\x14u!\x12s7Xj\x012N\x85TI|\x93\xf1T\xcd\xcf\xe3\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00O\x01\x045\x87\xcf\x04>b\xdf~\x80\x00\x00\x01\xdd\\H\xf6v\x7f\x04`\x9f\xabE\xd5\xc4b\xeeej\xae\xa5$\x8eL\xa7\xed\xed\xebw$\xc2\xdc\xb4\xe5\x02\xab$\x13O{\x08pA\xa1\x8fa\x18\x9f\xeb\xe5\xda\xc6\x8c\xc5^\xf4\xd7\x9f\xbaT\xdb\x81\xfa}\x1c\xb5\x17\x14\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80O\x01\x045\x87\xcf\x04\x9d\xb1\xd0\x00\x80\x00\x00\x01\xe7\x8e\xbf\x9e\xa8y\xa6\x85N\xb3h\x9c\xc2\x83\x1eMB\xf1\xba\xdbXaovW\x9cV\xe7\xbe\xbfO\xd1\x02\x7f\xe0\xe3"7\xa1\x8b2z~\xce9\xc4\xfbq\xa6%\xe0\xc9\xfb\x9d\x06\xf2\xa2q\xdc\xba\xc5\x11\xf8hs\x14&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80O\x01\x045\x87\xcf\x04\xba\xc1H9\x80\x00\x00\x01\xa7:\xdb\xe2\x87\x84\x87cM\xcb\xfc?~\xbd\xe8\xb1\xfc\x99O\x1e\xc0h`\xcf\x01\xc3\xfe.\xa7\x91\xdd\xb6\x02\xe6**\x99s\xeek:z\xf4|"\x9a[\xdep\xbc\xa5\x9b\xd0K\xbb)\x7fV\x93\xd7\xaa%k\x97m\x14s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x14\xaf\xde\t\'\xf3\xbd\xf5\xa9\xc3\xdbH;\xb8L\x93\xa5$\x96\x7f>\x87\x01\x04"\x00 \xe7\xa2\x14\x15\xf9\xc7K\xd7\xe8&\x9c\xac\x05\x15\xa2\xfa\xec\xd40\xc2p\xa2R\xe6\xaam\x15-\xec\x8e\x90\xe9\x01\x05iR!\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03!\x03f rK\xb0\x8d\xa8v\xf7\x08\x95F\x00:\xc0\\y\xd7\xee\x9a\xca\xbc\xde\x08\x846xN3\x7f\x13\xed!\x03\xa7RPg\xdbg\'\xd8#\xc2fC\x12#\xa7\x03i\x92\xb6JR\xd5\xdbJ\xd3\xea\x9a\x8c\xa1\x00\x89\xb0S\xae"\x06\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03f rK\xb0\x8d\xa8v\xf7\x08\x95F\x00:\xc0\\y\xd7\xee\x9a\xca\xbc\xde\x08\x846xN3\x7f\x13\xed\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03\xa7RPg\xdbg\'\xd8#\xc2fC\x12#\xa7\x03i\x92\xb6JR\xd5\xdbJ\xd3\xea\x9a\x8c\xa1\x00\x89\xb0\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00"\x00 d\x1c\x13\xabNQ\x92\x9a\x8a\xbf\xa1U\xe8\xb4#\xb8\xcd;B\xfd?m\x87\xd6U\xcfMQ\x03\x85\xbf\x04\x01\x01iR!\x027\xda5Ru8\x1e\xbb\xbf\x98d\xaa\xd6~\x03\x99\xd8\x9f\xcbW~\x9c\xe6\xb0h\x02\x94\xf3\x86\xb3e\x0c!\x02\xfa\x11*\x9bu\xe6F\xdf:\xd8\x01E{"{\xa7Y\xbc\x03\xe5{s8\xfa9\xa8\xd46\x00\x9f\x83\x81!\x03\xf3\x14U\xfcF\x87\x897>\x8d\xcb\x07\xc0\xa61\x1b/ w\x064\xed\x1e\x95H\x04M\xa2\x13d\r\xd4S\xae"\x02\x027\xda5Ru8\x1e\xbb\xbf\x98d\xaa\xd6~\x03\x99\xd8\x9f\xcbW~\x9c\xe6\xb0h\x02\x94\xf3\x86\xb3e\x0c\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x02\xfa\x11*\x9bu\xe6F\xdf:\xd8\x01E{"{\xa7Y\xbc\x03\xe5{s8\xfa9\xa8\xd46\x00\x9f\x83\x81\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xf3\x14U\xfcF\x87\x897>\x8d\xcb\x07\xc0\xa61\x1b/ w\x064\xed\x1e\x95H\x04M\xa2\x13d\r\xd4\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    P2SH_P2WSH_PSBT_B43 = "7ZB23D47D0SL*Y69MFM-Y64LVJD48X$9XZO1J/-L0B.624*OS$T6-RL6--2HB:BJ/CZLFHQ8XWAXNB5UZ91+Y*/SV.4J:VE$J9MMCCOVW$EB6++CJ.X-O8OJ$TSAWI8W38*U:08G+2NKH*CCZRGY0ZABPJ3ESQ6VFNNSDNEYC8KG/QX8R72LXF*4Z+8373D*LLYIOUH+LKJKP5LM+2ZOXD05+G2-H-ZL5N585FA7BF9SYRFRX:U59MND9DEKQ13CKD7+M9TA*3/UP$IIY/9MSQKFLAOQ71UC98XLJ2DP+YP0+-WRV.9CNTV2/X/*1+VQK2:Z0MPT$1H$I:RS1T3.+072$4EWIC:.C0QK4M7JA:HE19Q$9H3U.APAPQN$K7$A6.G6S*K.X2NAAARU5E1-$SOXU3D$$AFF-CF9QMXU4UDF.*7:2DV5P+J$59J8P$4I.FII$FK0U/S6LV$B9.ZG73BC57G77:.03T7B1A1IB6S8-Z:93C$GZO.Q+O/ZSEFG9TRQWACXPPA1KDTTAS4WDT9*/J72B+U52S2ER58Y93VQ4SEQ:X54CW4-8*YXIRZVPV6EOHRE:F.EFUU4LQO+3ZOX706F+GJ2AP+UIEB*XY$*9Z4Q0S3JC1+9J07AA21I3$S8:V0EOY$F$XO/T9PDFY*0D+3YSJW7QVTOT6KID::3F.3:K1-S*243V53H+W.$Y3:C$V8.7GMF7BDZST:7D$C$6AKI3BUVNR2.0Q+BPVC2-I/TUN93WBXM495N8T.7PRSSCZM1M1ZJU.W+G-Z94JK69UVKJI.Q8$WV2MGZENWV26NR14GD83GKE5UTMANK+/X4+CJI*6UI63UEDVN3-FY5R2-B$3JD1SY3+:0ELB/IPL4LM8R$W2*:+.G1PX6X.I-4:CY.TP-Q7XN3.PHRD://U+-LJ6LI9QB477PKMJWT.GS7RC*DLCKE4KW4PL4NP$90:LJHR*5-52JV$DCHL33QBPCQVUO:Z5U+U+XALJ.:AJV+ZBD:JFB+0V:5TZ:GEBFSNTQJOPIGBL6QSG9QLINU3*928744+NWR3NV90670ZN7*V1ET5:A:DUSFHCR64YBKVESO$Q5TYD/QR3$N9Z.ZS09+L*.7UWBVXG63TFA33CNGX0:T+VVTG-Y-H:6Y9OX79R6COJJ:A00PO/8I/UIA2*E+ILV/6/C29QHJL05HINPAJZEMYVZNUVSB5TZT0*GWRMYT*W95M:GO0.NE*/S9EU86IS.M/1DO9DP41HA8-BI.XK6VCPEPX3LAAW*842PZ+8/889ODKLRE2PHP0HY9GB3Q6Y74NYHFI:1XHPGURQ+6YLRLCB5OW9/XLDORE6ZC-AQO++I71AWR0FXHAOF0WCY:JWXONP:L*Y7Z-6I6PSF0V-D87MYD:9W2LS8CU8YCVOT978VUB:6JA:/5U+70JM-I5T+RHHF-3FA+IBPVUBKVZV11.+SN71G7X3:L+RV-79GTG$3QAYAVR2F24/-M0FG2DVJ$4RGHRT55RQHVJ5JVS+H3:0+B1YSX57Y94/Z0-+Z07B4-M0BZREBSGUXZU+IL1C59B5QRAR:6BG9+2J.MIJJ5GJT6*2R1D5Z2.H*$L09W$0KLP4C/HIQ$D8AQS*K8:DGKSISC:LW.BR:JSCV+2EVOFAP.O+WOV6P1DMUQX3LYG/3KXK"
    P2SH_P2WSH_PSBT_B58 = "iKPPtgBuDNJvZAkJsisSSKkAar78K5TV6Yt41d6teHVeAnqMdnN9j6cd3vgbKtuVYUFg6QJ6RyqarHnqd6jkYSxZxFPimGq9LG4BDffByiQnRkSzTm9CGVK5XYMP1U5REj1PVebpKoQrgXJyWdjautuAVrpkuAhUm7aHDYj5fYBVzqVRJ8GWpJrY3ZzhMNXLdej9UT3DhBHRf8ATeCZrn5JK3CKSkwTjF7Q97DqwjjSDnx9x8NX5v9UcWJyLnxc9Sj5TJDfBQ2MAjFgCd7fFXBxYbavLnhgfjjzades8wgAVxqMJSSN7tbhQacqu1FxVXLBxZsueHK6e4w2o7z3CGUYqJh53TN3KFENTyRh55HrnsAiBy9Kvnho3E4ey141PToTD3uShXef1s3kKKGhgUtYXmoCMqZshuce3wxjJP6A2Kzn6r9kcEXtNbrXEArnuihJ1bq2dS58Kg55WuwmXLZqMFwXTxj96Ds3hjeG8pJMpBKvUNRuJyPUUKPTtGAHUEsDzVL7kzcBLKdHiG8qPgS5PQHUW7jkik32BrHrDsvHK1t6SBLF8PKpdkZjPo6Pad4p7uS3vyXkV3bvucpjcR2jq4kmj1p5y73cUKFiopBujFRUTfX5dzU96KXZK5tkiWVcUF9hRvmaEfSKwfvVN5B7ThQrZkuMdKoB5VHAie3LrqEyzduJbwcA2ErTGCjArkJxY2YH9KeostknMwNn83C843L38nxqh2UXgd9CGgG57tvPg2BHqBd7pWXfbHCvazHao5i3M1QesrhDvW4tteabJjRQqsEaxiumg8R5J7ByRgxZFBgGQnU6PH8VkNQCVPBWpAdm4XCpccgFsSkbB1VaYJCfXF1qVCDvC9HZ2VfJCKwHvmagZ6hTeoxx1M4nh51tNeJEGSZahTxnWsF49me35MNXBS3agEQ42RACSgDUdPvCveyK2yUqnX5Ka4A5fMznqEZDhFQsfMrude688TKLyqtc4KfVXSDjZgK2xdpt8BsXHM77mA1vynDSkAps9L7qnPwx4UaGimG8XESSHBQSvyxE7U6j3UZiDLtuWeSwJMcjzEUAKuVhAAYAdv6qQkjwueHMPNifpgpoahUqhphExtzxsQujpsNAiYg5U3RqfbWQ77appzjFmGmvKrC8vXyGMzwM11Fve5ac8CKPssfjxeeZ53ufpCdgbLFLd7AVSA3HHhUpiEyuRVnhL5BGtQCvz1MvpbcNYyBwAZ6uRxnhjMmbxTnZ5qiyJEdmssTxZxhV5cYjZtngQun27QffbMqMvB83zrJKcr6SrahWmGabjXULdJVqqqbaY5KWsq5jFBh6B4FMR6zhxYj742d32zHWJWf4PwEQ1HdHZKiQgYrUKE5Rys2XKRSMK9AvYxEcMRTvW2Zhv4uDeDNS1ESsFQcS3ZR1kmZV8ZXzEfQFcXUa5dyjfYyoAXqkJZP8LcdjrUmWjdHezcn1CPJ4pf8zNirSufggFYhRbFkahK4rx9QzD2T4qCT5ygabSqUZHXgqnAxsHmoSD6w4oH7BrH55trHjRChXCVhs4qoU34s"
    P2SH_P2WSH_PSBT_B64 = "cHNidP8BAHICAAAAAR30J629i3Y/R8woRpLQ9JUa31rKxyM+Ny4NEsme48GWAAAAAAD9////Atw5XQUAAAAAF6kUdSESczdYagEyToVUSXyT8VTNz+OHgJaYAAAAAAAWABTmav7/w4OOcfCiewfjsA7eaujhYAAAAABPAQQ1h88EPmLffoAAAAHdXEj2dn8EYJ+rRdXEYu5laq6lJI5Mp+3t63ckwty05QKrJBNPewhwQaGPYRif6+XaxozFXvTXn7pU24H6fRy1FxQCCMt3MAAAgAEAAIAAAACAAQAAgE8BBDWHzwSdsdAAgAAAAeeOv56oeaaFTrNonMKDHk1C8brbWGFvdlecVue+v0/RAn/g4yI3oYsyen7OOcT7caYl4Mn7nQbyonHcusUR+GhzFCa7g8QwAACAAQAAgAAAAIABAACATwEENYfPBLrBSDmAAAABpzrb4oeEh2NNy/w/fr3osfyZTx7AaGDPAcP+LqeR3bYC5ioqmXPuazp69HwimlvecLylm9BLuyl/VpPXqiVrl20Uc8XaCjAAAIABAACAAAAAgAEAAIAAAQEgAOH1BQAAAAAXqRSv3gkn8731qcPbSDu4TJOlJJZ/PocBBCIAIOeiFBX5x0vX6CacrAUVovrs1DDCcKJS5qptFS3sjpDpAQVpUiECZ+pFYkOTVjB+eG+vQFA3MNjZWiA6DjRcs1Wl36A/zgMhA2Ygckuwjah29wiVRgA6wFx51+6ayrzeCIQ2eE4zfxPtIQOnUlBn22cn2CPCZkMSI6cDaZK2SlLV20rT6pqMoQCJsFOuIgYCZ+pFYkOTVjB+eG+vQFA3MNjZWiA6DjRcs1Wl36A/zgMcc8XaCjAAAIABAACAAAAAgAEAAIAAAAAAAAAAACIGA2Ygckuwjah29wiVRgA6wFx51+6ayrzeCIQ2eE4zfxPtHCa7g8QwAACAAQAAgAAAAIABAACAAAAAAAAAAAAiBgOnUlBn22cn2CPCZkMSI6cDaZK2SlLV20rT6pqMoQCJsBwCCMt3MAAAgAEAAIAAAACAAQAAgAAAAAAAAAAAAAEAIgAgZBwTq05RkpqKv6FV6LQjuM07Qv0/bYfWVc9NUQOFvwQBAWlSIQI32jVSdTgeu7+YZKrWfgOZ2J/LV36c5rBoApTzhrNlDCEC+hEqm3XmRt862AFFeyJ7p1m8A+V7czj6OajUNgCfg4EhA/MUVfxGh4k3Po3LB8CmMRsvIHcGNO0elUgETaITZA3UU64iAgI32jVSdTgeu7+YZKrWfgOZ2J/LV36c5rBoApTzhrNlDBwCCMt3MAAAgAEAAIAAAACAAQAAgAEAAAAAAAAAIgIC+hEqm3XmRt862AFFeyJ7p1m8A+V7czj6OajUNgCfg4EcJruDxDAAAIABAACAAAAAgAEAAIABAAAAAAAAACICA/MUVfxGh4k3Po3LB8CmMRsvIHcGNO0elUgETaITZA3UHHPF2gowAACAAQAAgAAAAIABAACAAQAAAAAAAAAAAA=="
    P2SH_P2WSH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(P2SH_P2WSH_PSBT).to_cbor())

    SIGNED_P2SH_P2WSH_PSBT = b"psbt\xff\x01\x00r\x02\x00\x00\x00\x01\x1d\xf4'\xad\xbd\x8bv?G\xcc(F\x92\xd0\xf4\x95\x1a\xdfZ\xca\xc7#>7.\r\x12\xc9\x9e\xe3\xc1\x96\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02\xdc9]\x05\x00\x00\x00\x00\x17\xa9\x14u!\x12s7Xj\x012N\x85TI|\x93\xf1T\xcd\xcf\xe3\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x14\xaf\xde\t'\xf3\xbd\xf5\xa9\xc3\xdbH;\xb8L\x93\xa5$\x96\x7f>\x87\"\x02\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03G0D\x02 \x1f\xa0f\x1ct\xd6\xb9S\xbd\xc4\"\x0cY\x19\xe0\xe4p\xdc\xe8qR\xc8$\xf4Hf\xa6\x07\x8e\xda\x16b\x02 W;\xfb\xc0\xbaWo]/\xcc\xd8\xdb\xe8\xc85\xee\x9bx\x1c\xea\xba\xf4[vM\xac\xc2\x11\xae-G\xc7\x01\x01\x04\"\x00 \xe7\xa2\x14\x15\xf9\xc7K\xd7\xe8&\x9c\xac\x05\x15\xa2\xfa\xec\xd40\xc2p\xa2R\xe6\xaam\x15-\xec\x8e\x90\xe9\x01\x05iR!\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03!\x03f rK\xb0\x8d\xa8v\xf7\x08\x95F\x00:\xc0\\y\xd7\xee\x9a\xca\xbc\xde\x08\x846xN3\x7f\x13\xed!\x03\xa7RPg\xdbg'\xd8#\xc2fC\x12#\xa7\x03i\x92\xb6JR\xd5\xdbJ\xd3\xea\x9a\x8c\xa1\x00\x89\xb0S\xae\x00\x00\x00"
    SIGNED_P2SH_P2WSH_PSBT_B43 = "CLQSGDZJQB4QIYKX08*DIBD23JSA8U413ZNG9T3LLKAV.2DC.M8794QPU1:E4Z06VG/+F$UKCBSIQH3V:N++4QS1NS:YJ1Z.JQ*+3T6D6PX-:WY8SYCHKR2GYKWNO46W:E$J65W$Y:1L*W0P5AUI9W:*PFQ*LX*+M$-BPO6-T31GOZFN$GMQ5RIB3VUKGNK-DXJKC6I236.$ZOEXVHM*D6ZM9+6QCXPMLG.P6O6O/P/QGGUEP8BMD.14T4H.1HEOF2*QI1PF*R.386+U8NOCJ3UE30ME5W$R*3APP:44M-WYBCU53QI1QV/QPVWF.T0$6EVP-YRSGZB34L+UTZ83H*NRJAYG79SXZATFWO9$R4XM5.O0WMVQ.3-*84Z8QVF38:O:6-PAOOUYUF1HK*+VKPC*JL6OSR-TH*FEQRPN4-9P4R*RWILCM5A:Y$48G4*B60N*E48WUH7$Q5PM8BCKWV-7UB0P4+TNUXR*P+E8/9FS$C$BFBOBL0GEU+5TGLVO:+8D-$OBU92TC43:0P17WZ1MINZKXD$B8.2$/9Z$Z*K7:QASII2WDNX7TQB416Q-C$J.:4-QCUF0X$FG+NRRD0-ABQ+ZX280T"
    SIGNED_P2SH_P2WSH_PSBT_B58 = "UHKpqoaYsQu3iUJNB2senWYdHBJvWXgfwPpJqqeAgk8xfULMYw45dxfzet7W38RH77S7DsUfemWVfASNVja4cwR3oN4233ve3Ma5tKQ3JoU9wLCkbRywAqepAah5sGDtx6QpS5G2w5ZYeVWjBdZ4obcNBQkT4umEjsALQfMwTHk31xivf9rmvQEizfP7geH6wufyXbMa3kg2h4c1CYE2eZC6tvcCKnHDJurq5yLfrhUSEjw8JpgSYxMiqmrMa8auJ25XQhpaPdcpYKXT9c7xhUNrTFuokHbfHiosxe8UMhRAHwmR2opgUBJvLq6ACokkn5UupGxrNmRSc1iJBBghokW1U9Wa9NtjiZLFcy86CS2wtt5UdtQ31BA3Capr5sBHER6vFLfVTqG6tdZ9LDaZmScBEzKsc6DRmhGGYFcGfaEBreiC6hvtHiN3xEFXS1DuJ4Xf6cE6QXit1q4vu1cMjhvnHV2LPTW8P6B696CXSa5FK4gn64FAn5G9WJNjJUfVuV3RHUgJwVXV83C2i5cXk2diUBFtDgzsboeqnh82GKKLkP5rjvBh"
    SIGNED_P2SH_P2WSH_PSBT_B64 = "cHNidP8BAHICAAAAAR30J629i3Y/R8woRpLQ9JUa31rKxyM+Ny4NEsme48GWAAAAAAD9////Atw5XQUAAAAAF6kUdSESczdYagEyToVUSXyT8VTNz+OHgJaYAAAAAAAWABTmav7/w4OOcfCiewfjsA7eaujhYAAAAAAAAQEgAOH1BQAAAAAXqRSv3gkn8731qcPbSDu4TJOlJJZ/PociAgJn6kViQ5NWMH54b69AUDcw2NlaIDoONFyzVaXfoD/OA0cwRAIgH6BmHHTWuVO9xCIMWRng5HDc6HFSyCT0SGamB47aFmICIFc7+8C6V29dL8zY2+jINe6beBzquvRbdk2swhGuLUfHAQEEIgAg56IUFfnHS9foJpysBRWi+uzUMMJwolLmqm0VLeyOkOkBBWlSIQJn6kViQ5NWMH54b69AUDcw2NlaIDoONFyzVaXfoD/OAyEDZiByS7CNqHb3CJVGADrAXHnX7prKvN4IhDZ4TjN/E+0hA6dSUGfbZyfYI8JmQxIjpwNpkrZKUtXbStPqmoyhAImwU64AAAA="
    SIGNED_P2SH_P2WSH_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(SIGNED_P2SH_P2WSH_PSBT).to_cbor()
    )
    SIGNED_P2SH_P2WSH_PSBT_SD = b'psbt\xff\x01\x00r\x02\x00\x00\x00\x01\x1d\xf4\'\xad\xbd\x8bv?G\xcc(F\x92\xd0\xf4\x95\x1a\xdfZ\xca\xc7#>7.\r\x12\xc9\x9e\xe3\xc1\x96\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x02\xdc9]\x05\x00\x00\x00\x00\x17\xa9\x14u!\x12s7Xj\x012N\x85TI|\x93\xf1T\xcd\xcf\xe3\x87\x80\x96\x98\x00\x00\x00\x00\x00\x16\x00\x14\xe6j\xfe\xff\xc3\x83\x8eq\xf0\xa2{\x07\xe3\xb0\x0e\xdej\xe8\xe1`\x00\x00\x00\x00O\x01\x045\x87\xcf\x04>b\xdf~\x80\x00\x00\x01\xdd\\H\xf6v\x7f\x04`\x9f\xabE\xd5\xc4b\xeeej\xae\xa5$\x8eL\xa7\xed\xed\xebw$\xc2\xdc\xb4\xe5\x02\xab$\x13O{\x08pA\xa1\x8fa\x18\x9f\xeb\xe5\xda\xc6\x8c\xc5^\xf4\xd7\x9f\xbaT\xdb\x81\xfa}\x1c\xb5\x17\x14\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80O\x01\x045\x87\xcf\x04\x9d\xb1\xd0\x00\x80\x00\x00\x01\xe7\x8e\xbf\x9e\xa8y\xa6\x85N\xb3h\x9c\xc2\x83\x1eMB\xf1\xba\xdbXaovW\x9cV\xe7\xbe\xbfO\xd1\x02\x7f\xe0\xe3"7\xa1\x8b2z~\xce9\xc4\xfbq\xa6%\xe0\xc9\xfb\x9d\x06\xf2\xa2q\xdc\xba\xc5\x11\xf8hs\x14&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80O\x01\x045\x87\xcf\x04\xba\xc1H9\x80\x00\x00\x01\xa7:\xdb\xe2\x87\x84\x87cM\xcb\xfc?~\xbd\xe8\xb1\xfc\x99O\x1e\xc0h`\xcf\x01\xc3\xfe.\xa7\x91\xdd\xb6\x02\xe6**\x99s\xeek:z\xf4|"\x9a[\xdep\xbc\xa5\x9b\xd0K\xbb)\x7fV\x93\xd7\xaa%k\x97m\x14s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x01\x01 \x00\xe1\xf5\x05\x00\x00\x00\x00\x17\xa9\x14\xaf\xde\t\'\xf3\xbd\xf5\xa9\xc3\xdbH;\xb8L\x93\xa5$\x96\x7f>\x87"\x02\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03G0D\x02 \x1f\xa0f\x1ct\xd6\xb9S\xbd\xc4"\x0cY\x19\xe0\xe4p\xdc\xe8qR\xc8$\xf4Hf\xa6\x07\x8e\xda\x16b\x02 W;\xfb\xc0\xbaWo]/\xcc\xd8\xdb\xe8\xc85\xee\x9bx\x1c\xea\xba\xf4[vM\xac\xc2\x11\xae-G\xc7\x01\x01\x04"\x00 \xe7\xa2\x14\x15\xf9\xc7K\xd7\xe8&\x9c\xac\x05\x15\xa2\xfa\xec\xd40\xc2p\xa2R\xe6\xaam\x15-\xec\x8e\x90\xe9\x01\x05iR!\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03!\x03f rK\xb0\x8d\xa8v\xf7\x08\x95F\x00:\xc0\\y\xd7\xee\x9a\xca\xbc\xde\x08\x846xN3\x7f\x13\xed!\x03\xa7RPg\xdbg\'\xd8#\xc2fC\x12#\xa7\x03i\x92\xb6JR\xd5\xdbJ\xd3\xea\x9a\x8c\xa1\x00\x89\xb0S\xae"\x06\x02g\xeaEbC\x93V0~xo\xaf@P70\xd8\xd9Z :\x0e4\\\xb3U\xa5\xdf\xa0?\xce\x03\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03f rK\xb0\x8d\xa8v\xf7\x08\x95F\x00:\xc0\\y\xd7\xee\x9a\xca\xbc\xde\x08\x846xN3\x7f\x13\xed\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"\x06\x03\xa7RPg\xdbg\'\xd8#\xc2fC\x12#\xa7\x03i\x92\xb6JR\xd5\xdbJ\xd3\xea\x9a\x8c\xa1\x00\x89\xb0\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00"\x00 d\x1c\x13\xabNQ\x92\x9a\x8a\xbf\xa1U\xe8\xb4#\xb8\xcd;B\xfd?m\x87\xd6U\xcfMQ\x03\x85\xbf\x04\x01\x01iR!\x027\xda5Ru8\x1e\xbb\xbf\x98d\xaa\xd6~\x03\x99\xd8\x9f\xcbW~\x9c\xe6\xb0h\x02\x94\xf3\x86\xb3e\x0c!\x02\xfa\x11*\x9bu\xe6F\xdf:\xd8\x01E{"{\xa7Y\xbc\x03\xe5{s8\xfa9\xa8\xd46\x00\x9f\x83\x81!\x03\xf3\x14U\xfcF\x87\x897>\x8d\xcb\x07\xc0\xa61\x1b/ w\x064\xed\x1e\x95H\x04M\xa2\x13d\r\xd4S\xae"\x02\x027\xda5Ru8\x1e\xbb\xbf\x98d\xaa\xd6~\x03\x99\xd8\x9f\xcbW~\x9c\xe6\xb0h\x02\x94\xf3\x86\xb3e\x0c\x1c\x02\x08\xcbw0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x02\xfa\x11*\x9bu\xe6F\xdf:\xd8\x01E{"{\xa7Y\xbc\x03\xe5{s8\xfa9\xa8\xd46\x00\x9f\x83\x81\x1c&\xbb\x83\xc40\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00"\x02\x03\xf3\x14U\xfcF\x87\x897>\x8d\xcb\x07\xc0\xa61\x1b/ w\x064\xed\x1e\x95H\x04M\xa2\x13d\r\xd4\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x01\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    MISSING_GLOBAL_XPUBS_PSBT = "cHNidP8BAFUCAAAAASeaIyOl37UfxF8iD6WLD8E+HjNCeSqF1+Ns1jM7XLw5AAAAAAD/////AaBa6gsAAAAAGXapFP/pwAYQl8w7Y28ssEYPpPxCfStFiKwAAAAAAAEBIJVe6gsAAAAAF6kUY0UgD2jRieGtwN8cTRbqjxTA2+uHIgIDsTQcy6doO2r08SOM1ul+cWfVafrEfx5I1HVBhENVvUZGMEMCIAQktY7/qqaU4VWepck7v9SokGQiQFXN8HC2dxRpRC0HAh9cjrD+plFtYLisszrWTt5g6Hhb+zqpS5m9+GFR25qaAQEEIgAgdx/RitRZZm3Unz1WTj28QvTIR3TjYK2haBao7UiNVoEBBUdSIQOxNBzLp2g7avTxI4zW6X5xZ9Vp+sR/HkjUdUGEQ1W9RiED3lXR4drIBeP4pYwfv5uUwC89uq/hJ/78pJlfJvggg71SriIGA7E0HMunaDtq9PEjjNbpfnFn1Wn6xH8eSNR1QYRDVb1GELSmumcAAACAAAAAgAQAAIAiBgPeVdHh2sgF4/iljB+/m5TALz26r+En/vykmV8m+CCDvRC0prpnAAAAgAAAAIAFAACAAAA="

    # WSH_MINISCRIPT = "wsh(or_d(pk([73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*),and_v(v:pkh([02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*),older(65535))))#466dtswe"
    # tb1qrtvmveqwrzsndt8tzzkgepp2mw8de95dk7hz70kr95f5dt7axvrsgq8lcp
    MINIS_P2WSH_PSBT = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\x96Y\x17$\xc8\xc8p\x00\x1e\x981\xe1\x14\xc9\nV7\x0c\x10\xff\xc2\xf6-\xbcyP\x05h\x88q\x9c\x9d\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00\x16\x00\x14V\x911\x9a\xfbg\x8b\xbfC\xad&\x8cE\xa8\x8a\x88\xcd\x8dOk@B\x0f\x00\x00\x00\x00\x00"\x00 \x9f\xef\xdeW\x0e\x8a}\xabP\xf15\x8e\x1df\xcdz\xba\xf6\xb2\xfb\x04\x85\xffu\xda\xcd\xdb\xd3\x8f\xdc\r\xf3\xab\x8d\x07\x00\x00\x00\x00\x00"\x00 \xdffN{{P\x15\\\xc0s\xeb\xa4n[\xfd(G\xe8T\x84\x13\xa4Eb\xf2\xbc\t\xcd\xa7/\x1cj\x00\x00\x00\x00\x00\x01\x00\xa2\x02\x00\x00\x00\x00\x01\x01O#\x9f\xea\xd3\xa8\x1f4|WJn=Bt\xeaV/\xdfR\xcb\xc7\xce^\xfb:\x88\xd4\x020c&\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07\x01@?\xd8Y\xef$\xc2\xc61\x90\xce\xa2\x11\xc7\xfe\xed\x16\x9a\x14}\xc9S\xe9\xc5)s\xbf\x80U\x17\xdbp\xe7\x803\xe9l\xd08\xb2\xaa\x13D\x9d\xff\xe6*5<\xb2YuF~O\xaf}\xc1\xf0,6\x1ca<\xe4\x00\x00\x00\x00\x01\x01+\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07\x01\x05D!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\xacsdv\xa9\x14Pf\xd5\xb4\x9de\xad\xceB\xdd\xc8\x8f\x05\xf1D?\xec\xa9\x90\x8a\x88\xad\x03\xff\xff\x00\xb2h"\x06\x03,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00"\x02\x02q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00"\x02\x02\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x00"\x02\x02|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00"\x02\x02\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x00'
    MINIS_P2WSH_PSBT_B43 = "75W:GGD-BWMM*4TP9NAF77L:6V/PUOLESPFPQKQ57CC5ELTGF:IWI89XQDFGV.VM2.-S*0PRBXHCPG8$52N:X.MU2Z29SS11P67*86UF8VKH05CL7GB5BRT:7O*VSFVEA$5Q0NHIQ+F+W2R.9LLY26K9IM*LWSAN3797LD8RP.1NPFJO:Q9Z+7TW.74-NW95D$6M1Q+FVC9PFF:LIL59I-PJYPPG6B58LYGOY.CC9X+DDN9*W1GQ02.3YDQT4H/3E.JV+ZSFC8P0Q8HV8BY7*VLG5RI/Z+301:T2G56ODNRAN$*RX:N$9YP1::D0*V96PZX7W/L3VI8UPP4ET:::ZJ4-F84FOTK7FP25:H+Y+2:48LLR-E74EHPB435$X1P6JZ**C*84Y8UIOVP*/VL:UG9ID2Q.66G$ON70V7KJ9K15ZMFMFEY3ADI0T7NEFT81AD8/1SIT5Y$ZZ3JB*AXVCPB3/0UAX8-D8M1SWD7L.I2-+JW8QPA$5J:6BNVZW1BIU4OUFJE131SX68GV/ZE6E:E.Y.6Q-JVPP.S2GDXNEXNR2GL4L+7I6X66CW3G1KUF6XL--5$AA74+R.-DC$0E5PHHB*CDN+Y-6*N66.T79*9N$1*9EGMWJSZGMKK7PBY-QF6Y-XRPIZ$$2*MVRG5*:DACDHHU/N725G:$OPTU8Q1XJH9C*0/TTPY67P-JM-432EC+1+TK:J4JGH24:*J:QFRE3VP.YF71.KLG-.9D-H6L+UZ4J3DFJK*BXPIWUKQUTGLKEY3XVXDEV+$PI0VH+NNQ1.QQ1LDVJO-OLA9H7*072I25H99+8745AWL2AET$Z:+USI*R$W+AH54B.D1YFO5421NGLTSQZ:+ZP2-YW*72YCB$E$F37$++9*X.BU/W1-M:OT0-19EW4ILXCD+0W*9$$ZUF49HX2BETK:9RC9XZZO2IKA.HQ9KSB2SPWM/NEJ3L9K++*0AZC*EIYQ0JD9V3C8J93HPLSG795DB$D:IJBQS.C4.LG-OCY0FOSGEB8O*VK*98LQVWMAXQNR/RUQDM5YJLMKNHAZ2VW$CZ5+93WJ4C.AH-*WISRKMN:SE.L*ZU/I9N2RR+71W:B0IQU2/5R6N.6W2TF+68.ZTPBOJZUL1FL*PA-J0/1L0-O.XDAG:65BS49/S933SNXT/4.*8Q779GOHHE8.53V39WKO1VE*.ZXV$$IMZG*WT6UI+A.72MH+-.8-LVOJHRKHOP:U69IG.H2WJ7:"
    MINIS_P2WSH_PSBT_B58 = "8vsnQ1aCezSMDDvQnutdZoPfBE3jeAtaVyAaJ2MFA3okEUQwcUsgJKkSo97SQe8yns793CxoYrMB7yDs2UFGvLJP4xwFaod14K14By9ByDVkSvKhka27fTSJd5aU4arYaUugGDcYVACZR1ZdK5k2bAPtjneKhq6CU7cqV9mz3ZRHskKw4zonXfMPZkfcwPxoYoW83aj2YbNaCmLyLvKnX3oJuniExGkHnBGkxjLNYyiHMZ17eTCzwactEEjgnbgRtHFdQv8sYQf6r6jjZsZ8UeLbKYoR43TFg27nz9AGhNQvA4KSH7wAm1r5x2WQh6oae9pRVKfQFKxzRAdqoYA1DAjXtWbqDXZ5wxhqqrFxBtns8kGjGqjmgvJarjGkjrXjQ9YpQRtrU8fzkVjfD8yMRZ8m1xeznQ3G5XCYN9XDkXTJ9hmLiK1qhtvU7thTZ1rFeP9rGgJbbrV1KWdd7s6G1BZfacSzWapoMgKUBZurcTPH5GD7BmTug5VK8bmyvQzn7FDrLXGwdDzHiVcBqfbHFTHgPmemNYRgjFvHC3v6MMd2rim3TBWCTJmo38SHmR4nJuZUy1JqyLnHndN5yJo5uhTwL54r68ReUw5uj8yjXdbszWqWPm4uZ42uV3VC6pcfu87nbPubYue3VFEHcW579EMB4bQXb3PLsBRuqAkbWDKFpfUEvzfqbjSJSzPM6446BTFkDg1wqTinJSfbcuaMj5jGzNC2RRDTey6haNEM18nhPHWtpyfVyynKNAQbT6U4UVMGfK5P52V3U36VLmNVy2PCXciBPwsCYtPoiJ9LECz3K2n2o1xqttFeEkHrVXTeVBgCs2bBG1ithZeoyXPfxayuxNEKw2DpmoH4qBFYmKSSdz1SeRn1rHdiN1BQ4HijPXtbjKm6ak3QvNWtCsNdJGFbG8aUN8HHTxcLCRyfRpL1beDPUauVXQr76jZoQLUrV3Ep3LX27uf1tbLp7J4CV1KWuET4YPcV48dE1PMwCzJKqrt7o2ukNGHuXXdf8X2fp5Y56kGvddL3Bk96VKKxUXVd6serKdebyNcCnS7vUjov92ph1LvbZ8byDvYf6jAe43tdNmuhNcvAgY76CghBbJpfsC2TJbHXyTZWoML5vJNnEW1seG1Let6gQ6yLXt4ZPQodh"
    MINIS_P2WSH_PSBT_B64 = "cHNidP8BAKgCAAAAAZZZFyTIyHAAHpgx4RTJClY3DBD/wvYtvHlQBWiIcZydAAAAAAD9////AyChBwAAAAAAFgAUVpExmvtni79DrSaMRaiKiM2NT2tAQg8AAAAAACIAIJ/v3lcOin2rUPE1jh1mzXq69rL7BIX/ddrN29OP3A3zq40HAAAAAAAiACDfZk57e1AVXMBz66RuW/0oR+hUhBOkRWLyvAnNpy8cagAAAAAAAQCiAgAAAAABAU8jn+rTqB80fFdKbj1CdOpWL99Sy8fOXvs6iNQCMGMmAQAAAAD9////AQZ5HgAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcBQD/YWe8kwsYxkM6iEcf+7RaaFH3JU+nFKXO/gFUX23DngDPpbNA4sqoTRJ3/5io1PLJZdUZ+T699wfAsNhxhPOQAAAAAAQErBnkeAAAAAAAiACAa2bZkDhihNqzrEKyMhCrbjtyWjbeuLz7DLRNGr90zBwEFRCEDaJVy4osP7anWmBwCN9nl3tv+wW3nFD9oCgLtXRWfdYesc2R2qRRQZtW0nWWtzkLdyI8F8UQ/7KmQioitA///ALJoIgYDLMRSZBc2IWvKWJwMwQE43VdzU3UzmLMSnBUa9H/5NpIcAui/8jAAAIABAACAAAAAgAIAAIAAAAAAAQAAACIGA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHHHPF2gowAACAAQAAgAAAAIACAACAAAAAAAEAAAAAACICAnEftmGVk/vJgt8Yn9ZQ0htivPcj0929eTfkCa5qm+oEHALov/IwAACAAQAAgAAAAIACAACAAAAAAAMAAAAiAgKxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBBxzxdoKMAAAgAEAAIAAAACAAgAAgAAAAAADAAAAACICAnxuOjHDK8ueogVkcyIpbFujaTY/E2747lrLIcj51R5QHALov/IwAACAAQAAgAAAAIACAACAAQAAAAEAAAAiAgL2bDCgfbz9YefFtvrPTmwn+Ue6+suz/A6igeAWfm6UjRxzxdoKMAAAgAEAAIAAAACAAgAAgAEAAAABAAAAAA=="
    MINIS_P2WSH_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(MINIS_P2WSH_PSBT).to_cbor())

    SIGNED_MINIS_P2WSH_PSBT = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\x96Y\x17$\xc8\xc8p\x00\x1e\x981\xe1\x14\xc9\nV7\x0c\x10\xff\xc2\xf6-\xbcyP\x05h\x88q\x9c\x9d\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00\x16\x00\x14V\x911\x9a\xfbg\x8b\xbfC\xad&\x8cE\xa8\x8a\x88\xcd\x8dOk@B\x0f\x00\x00\x00\x00\x00"\x00 \x9f\xef\xdeW\x0e\x8a}\xabP\xf15\x8e\x1df\xcdz\xba\xf6\xb2\xfb\x04\x85\xffu\xda\xcd\xdb\xd3\x8f\xdc\r\xf3\xab\x8d\x07\x00\x00\x00\x00\x00"\x00 \xdffN{{P\x15\\\xc0s\xeb\xa4n[\xfd(G\xe8T\x84\x13\xa4Eb\xf2\xbc\t\xcd\xa7/\x1cj\x00\x00\x00\x00\x00\x01\x00\xa2\x02\x00\x00\x00\x00\x01\x01O#\x9f\xea\xd3\xa8\x1f4|WJn=Bt\xeaV/\xdfR\xcb\xc7\xce^\xfb:\x88\xd4\x020c&\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07\x01@?\xd8Y\xef$\xc2\xc61\x90\xce\xa2\x11\xc7\xfe\xed\x16\x9a\x14}\xc9S\xe9\xc5)s\xbf\x80U\x17\xdbp\xe7\x803\xe9l\xd08\xb2\xaa\x13D\x9d\xff\xe6*5<\xb2YuF~O\xaf}\xc1\xf0,6\x1ca<\xe4\x00\x00\x00\x00\x01\x01+\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07"\x02\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87G0D\x02 +\xe4\x00\xa1\xcb\xf1\x87\x8b\xef\x07\x86\x89\x1aV\x99\x0b%3W\xfb\xe0v\xc2S\\\xaf\xc4T\x8ej\xe6p\x02 \x1d/\\\x9eS\x0e<\xff\xd0\x81UL\xd1\x15|\x1c}y\x8e?\xdc\xaa\xbc=6\xc1\xcc\x06ll\xca\xc9\x01\x01\x05D!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\xacsdv\xa9\x14Pf\xd5\xb4\x9de\xad\xceB\xdd\xc8\x8f\x05\xf1D?\xec\xa9\x90\x8a\x88\xad\x03\xff\xff\x00\xb2h\x00\x00\x00\x00'
    SIGNED_MINIS_P2WSH_PSBT_B43 = "1TFBDGI0U9N.JNF9JXZO5QI.R..ULE3SYFCOR2+C/2/N6GRF$UFW0$ONNTH.6JYIB/NLQX6H4IPU+P+BHLUB-40/ZB8IK$01$$CS3:5K6MD5R-1U7Z4Y$4QON+B9T:L3$V1OWNAAAK9PHL6:J:1FEHNJ1OV74-I*KNUCQ6G*JGP0/JC:N3Q-X-2-3+OF-:B$--I1TX8X7N+8606XP01.OV1CGGZ2R6R9+Z-KX9ZQXH-LXX75-P43.X6TO44.ARWD85RI1WHNLD903+IAV2FV6T5//T1EM9HNP*1EYDKUZN3*$U8L944W3K*Y2N0N7:AW-M:X0:PZURT:+4:ZBVOZ3$1BKQGHG1DDP8T8YO:NI7.NBVUVPN2-0-4:STS*GJM28W+B-J/T+IJTK4U.OV+MFEYLOC012A22J+L/37BE+E7PZ-2.7F:-UY/E$ZN1ZC2+P7V5FS4CIPRTDAGGCB-XBGZ7.3T7929P8$VPZQSAPU4V8/8BAR:PP/IE+DP.YWW1HJW/3JPDXE.Z90.BN91FW1HQSUVQDHL46*UXBX2BL9T23HT7F.TBS3:86MGX/I8M:YD*:+JMS$WKPWB65.T36WJP1.7A7H*K03GCUW0KGLU-H*5C6Z/0P*LQY2CL$-.P7XC1XG0HQPJM.FKGOC6S3+3KLZX:XW79I.-*4G.S6A05R:YE*6AU*UHA89R$RV.XJX5OQH:9UGKJ0X-JQ2EUTP2TBB/2B6933J.CNJW6M711I2GG-S9*8NTM*ONCBIBQ3BR87.HP17HKP*1P6$8*WRDVWUXRYRMDD9B-OG0+CZ7L3SKK0W64SUVH1-TRP8N$:.F1+6BQ0"
    SIGNED_MINIS_P2WSH_PSBT_B58 = "3UCmDenEJ8kw38Fft6J4JkeeDFYGE139af8mZigLkDsjrthMUBvRfHGs8vFUB8R4LP71PWpogqs6qnCbALrfbFCntEtFGPUNLR4WPrZAe1NCDVwGKHiJfBhxZidHBW2AzLStnJ5utyBZaWG1EjbiPbnhjVNymwy83FQjHjJNr6cqYf71efwP1QXqM33cT5SiFiFw2ANxSKyJxbvWkvVexKqc46fBBkbBnhnPzh5ycnjjNL8v6vx2yzigCPNpRs1xXrPWvdCKf6dFQbuDneqS4uFuUvR1eWv7DfWDVoMZaxvvttKAoUhEELibnSJFkuQoh4637PRbRaAL4EeyRnYP4mqiKEXvTbT4Dp2mYBvW28eZ1irrXkWsLhNyRyuE54NahJpd9vVfpBpa7U5EDRReN83xSaiboWNJ8dxc6UdGAkKqYmDu5RmPAxKYfmTWmA2s1o1WWpNchgaqkYPygMR1VyV8jrbNc8jnhfzGiH9Jo2Wjc8snnUPHY7mGXMmcgvtZtVQqBgMpqfgo1p5JP94LdiTrvu6fPxA9a8GpRw2hXBjeZd1BszHXcPeVWWx8LLkCAn5BiVmRG4RFh8pSfz4yQd5VDWGvrSepRnToPDQNPAYLbQCMKMgUPf3m2uRQtRRqf5t7wcwnSAdCzYVqKScZV3SRWZM2aNZD8fDnj4XKd6TJmmBTuxe51h3odc7fJWqZju2MuJQqAV4grSwE24xk478pyfXSN7Jg9f54MucGTeGFuVFYyiTkozkLjfaXY9mB6SpCBP5wo1R"
    SIGNED_MINIS_P2WSH_PSBT_B64 = "cHNidP8BAKgCAAAAAZZZFyTIyHAAHpgx4RTJClY3DBD/wvYtvHlQBWiIcZydAAAAAAD9////AyChBwAAAAAAFgAUVpExmvtni79DrSaMRaiKiM2NT2tAQg8AAAAAACIAIJ/v3lcOin2rUPE1jh1mzXq69rL7BIX/ddrN29OP3A3zq40HAAAAAAAiACDfZk57e1AVXMBz66RuW/0oR+hUhBOkRWLyvAnNpy8cagAAAAAAAQCiAgAAAAABAU8jn+rTqB80fFdKbj1CdOpWL99Sy8fOXvs6iNQCMGMmAQAAAAD9////AQZ5HgAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcBQD/YWe8kwsYxkM6iEcf+7RaaFH3JU+nFKXO/gFUX23DngDPpbNA4sqoTRJ3/5io1PLJZdUZ+T699wfAsNhxhPOQAAAAAAQErBnkeAAAAAAAiACAa2bZkDhihNqzrEKyMhCrbjtyWjbeuLz7DLRNGr90zByICA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHRzBEAiAr5AChy/GHi+8HhokaVpkLJTNX++B2wlNcr8RUjmrmcAIgHS9cnlMOPP/QgVVM0RV8HH15jj/cqrw9NsHMBmxsyskBAQVEIQNolXLiiw/tqdaYHAI32eXe2/7BbecUP2gKAu1dFZ91h6xzZHapFFBm1bSdZa3OQt3IjwXxRD/sqZCKiK0D//8AsmgAAAAA"
    SIGNED_MINIS_P2WSH_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(SIGNED_MINIS_P2WSH_PSBT).to_cbor()
    )
    SIGNED_MINIS_P2WSH_PSBT_SD = b'psbt\xff\x01\x00\xa8\x02\x00\x00\x00\x01\x96Y\x17$\xc8\xc8p\x00\x1e\x981\xe1\x14\xc9\nV7\x0c\x10\xff\xc2\xf6-\xbcyP\x05h\x88q\x9c\x9d\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00\x16\x00\x14V\x911\x9a\xfbg\x8b\xbfC\xad&\x8cE\xa8\x8a\x88\xcd\x8dOk@B\x0f\x00\x00\x00\x00\x00"\x00 \x9f\xef\xdeW\x0e\x8a}\xabP\xf15\x8e\x1df\xcdz\xba\xf6\xb2\xfb\x04\x85\xffu\xda\xcd\xdb\xd3\x8f\xdc\r\xf3\xab\x8d\x07\x00\x00\x00\x00\x00"\x00 \xdffN{{P\x15\\\xc0s\xeb\xa4n[\xfd(G\xe8T\x84\x13\xa4Eb\xf2\xbc\t\xcd\xa7/\x1cj\x00\x00\x00\x00\x00\x01\x00\xa2\x02\x00\x00\x00\x00\x01\x01O#\x9f\xea\xd3\xa8\x1f4|WJn=Bt\xeaV/\xdfR\xcb\xc7\xce^\xfb:\x88\xd4\x020c&\x01\x00\x00\x00\x00\xfd\xff\xff\xff\x01\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07\x01@?\xd8Y\xef$\xc2\xc61\x90\xce\xa2\x11\xc7\xfe\xed\x16\x9a\x14}\xc9S\xe9\xc5)s\xbf\x80U\x17\xdbp\xe7\x803\xe9l\xd08\xb2\xaa\x13D\x9d\xff\xe6*5<\xb2YuF~O\xaf}\xc1\xf0,6\x1ca<\xe4\x00\x00\x00\x00\x01\x01+\x06y\x1e\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07"\x02\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87G0D\x02 +\xe4\x00\xa1\xcb\xf1\x87\x8b\xef\x07\x86\x89\x1aV\x99\x0b%3W\xfb\xe0v\xc2S\\\xaf\xc4T\x8ej\xe6p\x02 \x1d/\\\x9eS\x0e<\xff\xd0\x81UL\xd1\x15|\x1c}y\x8e?\xdc\xaa\xbc=6\xc1\xcc\x06ll\xca\xc9\x01\x01\x05D!\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\xacsdv\xa9\x14Pf\xd5\xb4\x9de\xad\xceB\xdd\xc8\x8f\x05\xf1D?\xec\xa9\x90\x8a\x88\xad\x03\xff\xff\x00\xb2h"\x06\x03,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00"\x06\x03h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00"\x02\x02q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00"\x02\x02\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x00"\x02\x02|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\x1c\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00"\x02\x02\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x1cs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x00'
    SIGNED_MINIS_P2WSH_PSBT_B64_SD = "cHNidP8BAKgCAAAAAZZZFyTIyHAAHpgx4RTJClY3DBD/wvYtvHlQBWiIcZydAAAAAAD9////AyChBwAAAAAAFgAUVpExmvtni79DrSaMRaiKiM2NT2tAQg8AAAAAACIAIJ/v3lcOin2rUPE1jh1mzXq69rL7BIX/ddrN29OP3A3zq40HAAAAAAAiACDfZk57e1AVXMBz66RuW/0oR+hUhBOkRWLyvAnNpy8cagAAAAAAAQCiAgAAAAABAU8jn+rTqB80fFdKbj1CdOpWL99Sy8fOXvs6iNQCMGMmAQAAAAD9////AQZ5HgAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcBQD/YWe8kwsYxkM6iEcf+7RaaFH3JU+nFKXO/gFUX23DngDPpbNA4sqoTRJ3/5io1PLJZdUZ+T699wfAsNhxhPOQAAAAAAQErBnkeAAAAAAAiACAa2bZkDhihNqzrEKyMhCrbjtyWjbeuLz7DLRNGr90zByICA2iVcuKLD+2p1pgcAjfZ5d7b/sFt5xQ/aAoC7V0Vn3WHRzBEAiAr5AChy/GHi+8HhokaVpkLJTNX++B2wlNcr8RUjmrmcAIgHS9cnlMOPP/QgVVM0RV8HH15jj/cqrw9NsHMBmxsyskBAQVEIQNolXLiiw/tqdaYHAI32eXe2/7BbecUP2gKAu1dFZ91h6xzZHapFFBm1bSdZa3OQt3IjwXxRD/sqZCKiK0D//8AsmgiBgMsxFJkFzYha8pYnAzBATjdV3NTdTOYsxKcFRr0f/k2khwC6L/yMAAAgAEAAIAAAACAAgAAgAAAAAABAAAAIgYDaJVy4osP7anWmBwCN9nl3tv+wW3nFD9oCgLtXRWfdYccc8XaCjAAAIABAACAAAAAgAIAAIAAAAAAAQAAAAAAIgICcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gQcAui/8jAAAIABAACAAAAAgAIAAIAAAAAAAwAAACICArGhNdUqlR4BAOLGTMrY2ZJYTQNRudp7fU7i8crRJqgEHHPF2gowAACAAQAAgAAAAIACAACAAAAAAAMAAAAAIgICfG46McMry56iBWRzIilsW6NpNj8TbvjuWsshyPnVHlAcAui/8jAAAIABAACAAAAAgAIAAIABAAAAAQAAACICAvZsMKB9vP1h58W2+s9ObCf5R7r6y7P8DqKB4BZ+bpSNHHPF2gowAACAAQAAgAAAAIACAACAAQAAAAEAAAAA"

    # TR Miniscript - tr([73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*,and_v(v:pk([02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*),older(6)))#rfuhsd9c
    # tb1p3gev77tasfmd45w64dq5azkdl3y02cxlnkykw2v00x3jnu6yu8pskn06gu
    # tb1ph0aq68587rflxewpvs05axhn0lv4jes9zggzsc5jde05auag2mcqx6prnr
    # Liana simple inheritance, internal key signed

    MINIS_TR_PSBT = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03@B\x0f\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07 \xa1\x07\x00\x00\x00\x00\x00"Q @\x9b\x0e\x0b\x19s\xa6\xb0\xefX\x89\x869\xd3\xfbn\x1f\x86L0i\x07\x01y\x0c\xc0(\xb7\xd8\x03"\x87\xdd\x88\x07\x00\x00\x00\x00\x00"Q [\xf5T\x10]\x86\x9b0\x00\xa1-(\x1fr\\\x81\xc5\xef\xc4\xc8\x8fBm\xd5T\xe7\x94\xde\x04\x91rR\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3"\x15\xc0\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04% q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xadV\xb2\xc0!\x16q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x16\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x01\x17 \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x01\x18 \xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x00\x00\x01\x05 \n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb\x01\x06\'\x00\xc0$ 4!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83\xadV\xb2!\x07\n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00!\x074!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83=\x01\xf8s\xc9\xec\x12zCG\xb2\x13\xc4l\x893M\x98\xe4\xc8\xd3\x9d\xc9\xda\x11\xf8\xd1\x10\xfe2\x90\xd6d\xfd\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00\x00\x01\x05 \xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x01\x06\'\x00\xc0$ |n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\xadV\xb2!\x07|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP=\x01\xbf|\xea~\xde\xcc\xf2r\x0e\xd1\xbd\xcd\x00\xf6\xc4\xec\xc0\x057\xe5U\xff\x19\xb8\xce\xdc\t\xc7\xe6\xb7:T\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x00'
    MINIS_TR_PSBT_B43 = "C.ZHL9FPQGNRBX4AMRTEV*BIH.4L3ZH**OGKXMO2GFGP56LMHQJ-C+EVKTIKZQUT0SM+JBF9S/PTF$Y-1YCH+*ZD$6:$L5H5X5N*/5I-1CD7K0CN:ATQ0QSZRJI64B-6M/3GVU0D0TSGORS9JP:+:IOJERDBGFH-G/$C*HA7EIG81125R41B*11/*96/YZ8GE1*830+J19NCJIDAJ5D1JRAX2+Z-$-GPZ49RUSYH.IJ1E$Z2C$5XPIDKTMC:A7X/Q8EBPM.HG9*LAUZDHIM+GAJ/W-J5D/:NY8:A++I6YWHD97292:85NTU1B7/X0P.3L9OU:TF0AQPV6IC3IWR4D6Z163.S/C05PAABYKWF$.WFJTGI7/KD/0D52H3OYSIH5369MW8G+:NWBXW+*6N1QZZ*-6SNG3JJIF8K/$D4W1BT15VCTHHT$TA8J:.X.V/ZN1A9WJD1QRX1E.OX73Y1BMI5U6*6TUVK-DK64L563I/*F439WUVLDQU-IUQAAJHH+*$OUD73FY7DYJTBL*9BS/12F/B5TEPDI1QQFLPP*Q6/RH2UK1U.TINN7XS:$Q2ZNGPRUZLGW/9ZI+$8AHVGTH86ZUYE9GA$0IQ-1*Y$11/J$DTO78H$VU4L4*SB59O1YDP4MZA5U*JZ7QB7:V4C321JC/1D309MEKMWT5--2N1OLQG63/BAF$8TOGVILJ8Q5JYIS0M652TE:QA6LN$FRVPQE*BXCPFP50SNO6*OHTG.R+G7KAGO:.JXA/U7MSM6DU5MQ3IVW$UJHI4RI2Z/.OZIIGUX3+MZT.ZJH/5Q.27YVSU0V3I1$9CV-.+*9.FGHDJWJTMNPZA4VK0TIVDVNL+/.A-/UQVPALKZ93+C5VY839JHJK5CPK*J:W7F:Q6T*1UYDW65WZG:$9P3ONB7SRMHXQ1LIB40TH+7/PFU:FY1CV7ZHG6-.3SJ:6Y5HHVGT1JZ/5-XAYLF1$2LO6$SGG1WQ677LWIP1:ML/BQX1HR1$V*+X//TEGE-SFTJ3/RYHH*$$W+66WLAGH6PCQB-56/DS:B7DCIXDV34S.ZI*FC*+KRV5D8V2KL2Z$K*-X/2M1CW+WQG0PXPHSZ66Y7:1KIW19+R2.68$.65*F/89.:EXFYXW54TK*9$77Y-OIBH7H+++TEEW9AEN+SYFPM.BOVRB+KZ$UC:$BNBNH8*TJDLSQ:IJFRZ:BHW969+Y0468-PXBJ6$V/2ZZ9J+/1PPW03QCO4I89GZ1BQY9QD2AMD85//O+-MQK66Q-EDFYRYQ20L$JO3M.*JYZ$TM2F202TZICVC7FQC-:HQRI7L2-5MC5W8S2P+CRPC4.:7DT5/Z7FWUN$7JPDGTRBD3BBV59KL.9EWJ9RF:AM/EWI4FT8O7CR7L82N+7FV9CXQ-Z7UL$W$QDWAOBP+7G1X+K4GTSN6C6Y+Q48HDN9ZAH-A/VHYW43-9S/CC$W.T.15/HP-4883MZGFEYXORA6R17E+XU*UUJH"
    MINIS_TR_PSBT_B58 = "4U4YPeYHn8UsQ7XVsTRqLuoxaMQ8rhJsySbuRmzDdWziE1usHZu3cCA4rMpTKgF4dgauY6yGLhVQrz9jf2AF3LmW56uE5mPyCaxkW6GNWGY68jQUSE1Mf6VEdLT3BcA3HjspQGwk6FpRx6x7xYbonv3dU1CsWfp9YPDhqjfWipSCVf8H8YaaV7BwBeA9y9WyxUQjQ5oXHMyLPtCT2bryTj4G2J5QQCyUzvE9pKsn49rPMrXbVexjFPMWFG2XNxNs6uwrD4o4twbpBjohs3FiU2sgW96JzQ1PgBHN9TNLVmikHKsg4cgCfGKEmbWmN5Rmo1wHbqNmV77rR9txQxYMArfvmADbziQqEomVwi1sYjLysfRGdYe7dSe8uH2734aFyFs8oaRQx3ms8jRjnMYJpez3PyZa87NE3zAAwTNiEw6QJ2VgdgY3X1YAofvys2n9Qtt2ve6ehPCsCQvzbJe1MihCV8QAzc8t8LCJNcLcW87ZxMkoNdtJoszdhkZguoFs6xpFneS7VX4M3mzhxPtMz98i1z9eNQKKq1o8tWQHWt9znaMHsaLMtcDdaXXCHKQAdqvpWDWEtXgHy2J5T7jgzFMhreoDBkR3SAkr6D6fmdoNdHr6QPD1MFKP6RN97HC5tc4K1wNpyNTPHWNqLDAuakaKT85mNGX7Kk92suRG3vw6gqAQ1rvKUCWMe8GF4dzX5pCGuQiY1s3gq1pprApWiGKzEwDrvFL9XadKQpJGWHCTkKCaQVCt94ZT2ZtwkghMhaQ45ofehjU9RVE7gtnC64gCvrupg7zXAihGwxfqYPVfaiTyC4NaPU4CzKDDGwi133pV4W6RKYf2BBx4zJqEwwQSJFbPE1Y4fcfL2Zy9xe3p1v7HTp7H3h62uPBVDaRHWHnsmw2oAPdYVGFLbs3YyZKFpnMZCzvhLcF4BjoVdDe7nusjWfnZQx3ZN1fayr6hD8FZR2UzV8E8A9zV8GivvViHaQoSNygyQasGzLjgqYkYpcAykW8QvucGvjJWJdLRk8azXeGFmzzgCZxe1nY4MpSSTmZHpvEV15uLVuDvDHruBUzE2A5HEiaZUrQTJr4gUipK7Y9PATw3J1nencUT99noPJTFA5Kbq7P3rd8k8ruGswuYesuS91chmEW8ssEAhtTVpGmrY4oGrbuLo6F3EXntmLX6p6UKpuWCg8XgZWRdePnC5KcJc2AiKtBBVzu2dXFZgTyrkzpQkYBkHTvz6P4bM6oUBinwVBitt29GAME5M4Q8ZwkiFaW3iyLD9DqLVBxDiaEBeF8y9GRqNq6Q3gYTdgDERWF6fFmieDm3Wxz83fM9i6KFwjvPnLkkJeJFh3AkBPLiMmVPXwYCxFfQp2DefU72sb7nQu2GesYtYazB"
    MINIS_TR_PSBT_B64 = "cHNidP8BALQCAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAD9////A0BCDwAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcgoQcAAAAAACJRIECbDgsZc6aw71iJhjnT+24fhkwwaQcBeQzAKLfYAyKH3YgHAAAAAAAiUSBb9VQQXYabMAChLSgfclyBxe/EyI9CbdVU55TeBJFyUgAAAAAAAQEr73MeAAAAAAAiUSCKMs95fYJ22tHaq0FOis38SPVg352JZymPeaMp80ThwyIVwLGhNdUqlR4BAOLGTMrY2ZJYTQNRudp7fU7i8crRJqgEJSBxH7ZhlZP7yYLfGJ/WUNIbYrz3I9PdvXk35AmuapvqBK1WssAhFnEftmGVk/vJgt8Yn9ZQ0htivPcj0929eTfkCa5qm+oEPQH3BXv7e9eze4jSTr+PgvfiuCLkXs7bSOlAeCPQqaBnWALov/IwAACAAQAAgAAAAIACAACAAAAAAAMAAAAhFrGhNdUqlR4BAOLGTMrY2ZJYTQNRudp7fU7i8crRJqgEHQBzxdoKMAAAgAEAAIAAAACAAgAAgAAAAAADAAAAARcgsaE11SqVHgEA4sZMytjZklhNA1G52nt9TuLxytEmqAQBGCD3BXv7e9eze4jSTr+PgvfiuCLkXs7bSOlAeCPQqaBnWAAAAQUgCltZwSHuuC9ETlRoJyrNYv9NHUH8NLxR5mwpUS+4ousBBicAwCQgNCGNnpQXkylYa9f6nYj1HGwVeZN1xflZXOoQv2wj1IOtVrIhBwpbWcEh7rgvRE5UaCcqzWL/TR1B/DS8UeZsKVEvuKLrHQBzxdoKMAAAgAEAAIAAAACAAgAAgAAAAAAFAAAAIQc0IY2elBeTKVhr1/qdiPUcbBV5k3XF+Vlc6hC/bCPUgz0B+HPJ7BJ6Q0eyE8RsiTNNmOTI053J2hH40RD+MpDWZP0C6L/yMAAAgAEAAIAAAACAAgAAgAAAAAAFAAAAAAEFIPZsMKB9vP1h58W2+s9ObCf5R7r6y7P8DqKB4BZ+bpSNAQYnAMAkIHxuOjHDK8ueogVkcyIpbFujaTY/E2747lrLIcj51R5QrVayIQd8bjoxwyvLnqIFZHMiKWxbo2k2PxNu+O5ayyHI+dUeUD0Bv3zqft7M8nIO0b3NAPbE7MAFN+VV/xm4ztwJx+a3OlQC6L/yMAAAgAEAAIAAAACAAgAAgAEAAAABAAAAIQf2bDCgfbz9YefFtvrPTmwn+Ue6+suz/A6igeAWfm6UjR0Ac8XaCjAAAIABAACAAAAAgAIAAIABAAAAAQAAAAA="
    MINIS_TR_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(MINIS_TR_PSBT).to_cbor())

    IN_KEY_SIGNED_MINIS_TR_PSBT = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03@B\x0f\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07 \xa1\x07\x00\x00\x00\x00\x00"Q @\x9b\x0e\x0b\x19s\xa6\xb0\xefX\x89\x869\xd3\xfbn\x1f\x86L0i\x07\x01y\x0c\xc0(\xb7\xd8\x03"\x87\xdd\x88\x07\x00\x00\x00\x00\x00"Q [\xf5T\x10]\x86\x9b0\x00\xa1-(\x1fr\\\x81\xc5\xef\xc4\xc8\x8fBm\xd5T\xe7\x94\xde\x04\x91rR\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3\x01\x08B\x01@Q3\x98\xe4[\xd0}HM\x86\x00H\xb4\xa0\x16\xb19<i\xeb\xa1\xa8?\xc4i\x8c\xba~\x8djb\'\xb8MM\x80\x97\xa4\xf44\xf0\xb1\xbb\xd4\xf7\x17i\x07Pc:z\xbc\xfar\xad\x0er\xddb\xe4\xd0zJ\x01\x13@Q3\x98\xe4[\xd0}HM\x86\x00H\xb4\xa0\x16\xb19<i\xeb\xa1\xa8?\xc4i\x8c\xba~\x8djb\'\xb8MM\x80\x97\xa4\xf44\xf0\xb1\xbb\xd4\xf7\x17i\x07Pc:z\xbc\xfar\xad\x0er\xddb\xe4\xd0zJ\x00\x00\x00\x00'
    IN_KEY_SIGNED_MINIS_TR_PSBT_B43 = "BIOW5$16$7C7.QKRAZJCSEHQTU-XW0ZQ$+PPO66J:2K.7.LT5/ZR$Y/Z-X88.Z-UT5WQXF/12K2C0Y07B6JRFZHLOV2FD66J4AZ8IW9YJTGQKYN2DB2VMXT5XNP5Y$-7KPZ95MAWEG9CB/Q06VRY9THI8$YUQ6GB32*SDD27UVULMH/O+0PP-0IWW+R-AC$BBF88W/3RM-5G/AB$U2OD$XZ57TRQ9OHKKK:S$/YCPY4+2*A$.N6$Y55UXT4SSU+1R03V4AU87$6PH5ND034-0EXA*SX9W*OJ9$9/$ULQ6J4D$0HQ0MF1IHK41FYFY*C2OVD30PHBA8UH6D/H4BRZ6DUZB3-HFF374XQ5$3G533HZKGUO/.RQI6L6NVXMZ+8E476-L6WC:A5828*UZ91QZYM0NEM6KOV85N:OBP$1MQ./SI5-VL:Z1/5**43/6EUX2PWYSB7-QT$OLFDWS+X3T30XPHCSNJZ994PBJF-0LZ1*-0SV087T.HS$NIZN+895VDQZ*NGBW12X6N0DHJDM.1EK85/AI*6UIE9SSJ7+/"
    IN_KEY_SIGNED_MINIS_TR_PSBT_B58 = "inScThssu4fzeEVSrUbUGPftqsZ3YRxvu8gyPzNaU8zbBHvCEhm9uzqzeZq7dQ3nYaGqq51sMxMV1goB2pk8UTRLfytypdRU1dYXnwPVfeNWExpr621st3NoTfaBwrJMMJyiHUpUTwL183nrsxGaFG9aVjt6KeGjFTX71FjkazQ5pBqdkBkwMf7MpsNxM6RbD1YSNxnF3jMCPwZnHcqTayznwfKetnfJjDh4DhLXfU5cJmgM6kS7sYkJSHbnFpz81hnQpXvvgQYv1RNjwnfbSnA2U9UzHXSSVXyco4iVL5Q9iUEzAMQ4iLPZinVGWgArBpey2eyfpHXWsyrhvnfejnuhbxcXUj1vKd7xrbUNYGXBbXgnVMBxZfHNNfcTnxHmJDk49aDKaensLRZxT8mj9yh2WyPJM6y61PG5VoZ4no453kmXVtfRq6VU2swPw6k4bPGG4Q2F3tc8iHfqhXKMTsa2UirqC592ZueMPbcAQ76TvQnRNR2UvrQVZvyBso4j"
    IN_KEY_SIGNED_MINIS_TR_PSBT_B64 = "cHNidP8BALQCAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAD9////A0BCDwAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcgoQcAAAAAACJRIECbDgsZc6aw71iJhjnT+24fhkwwaQcBeQzAKLfYAyKH3YgHAAAAAAAiUSBb9VQQXYabMAChLSgfclyBxe/EyI9CbdVU55TeBJFyUgAAAAAAAQEr73MeAAAAAAAiUSCKMs95fYJ22tHaq0FOis38SPVg352JZymPeaMp80ThwwEIQgFAUTOY5FvQfUhNhgBItKAWsTk8aeuhqD/EaYy6fo1qYie4TU2Al6T0NPCxu9T3F2kHUGM6erz6cq0Oct1i5NB6SgETQFEzmORb0H1ITYYASLSgFrE5PGnroag/xGmMun6NamInuE1NgJek9DTwsbvU9xdpB1BjOnq8+nKtDnLdYuTQekoAAAAA"
    IN_KEY_SIGNED_MINIS_TR_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(IN_KEY_SIGNED_MINIS_TR_PSBT).to_cbor()
    )
    IN_KEY_SIGNED_MINIS_TR_PSBT_SD = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03@B\x0f\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07 \xa1\x07\x00\x00\x00\x00\x00"Q @\x9b\x0e\x0b\x19s\xa6\xb0\xefX\x89\x869\xd3\xfbn\x1f\x86L0i\x07\x01y\x0c\xc0(\xb7\xd8\x03"\x87\xdd\x88\x07\x00\x00\x00\x00\x00"Q [\xf5T\x10]\x86\x9b0\x00\xa1-(\x1fr\\\x81\xc5\xef\xc4\xc8\x8fBm\xd5T\xe7\x94\xde\x04\x91rR\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3\x01\x08B\x01@Q3\x98\xe4[\xd0}HM\x86\x00H\xb4\xa0\x16\xb19<i\xeb\xa1\xa8?\xc4i\x8c\xba~\x8djb\'\xb8MM\x80\x97\xa4\xf44\xf0\xb1\xbb\xd4\xf7\x17i\x07Pc:z\xbc\xfar\xad\x0er\xddb\xe4\xd0zJ\x01\x13@Q3\x98\xe4[\xd0}HM\x86\x00H\xb4\xa0\x16\xb19<i\xeb\xa1\xa8?\xc4i\x8c\xba~\x8djb\'\xb8MM\x80\x97\xa4\xf44\xf0\xb1\xbb\xd4\xf7\x17i\x07Pc:z\xbc\xfar\xad\x0er\xddb\xe4\xd0zJ"\x15\xc0\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04% q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xadV\xb2\xc0!\x16q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x16\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x01\x17 \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x01\x18 \xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x00\x00\x01\x05 \n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb!\x07\n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00!\x074!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83=\x01\xf8s\xc9\xec\x12zCG\xb2\x13\xc4l\x893M\x98\xe4\xc8\xd3\x9d\xc9\xda\x11\xf8\xd1\x10\xfe2\x90\xd6d\xfd\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00\x01\x06\'\x00\xc0$ 4!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83\xadV\xb2\x00\x01\x05 \xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d!\x07|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP=\x01\xbf|\xea~\xde\xcc\xf2r\x0e\xd1\xbd\xcd\x00\xf6\xc4\xec\xc0\x057\xe5U\xff\x19\xb8\xce\xdc\t\xc7\xe6\xb7:T\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x01\x06\'\x00\xc0$ |n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\xadV\xb2\x00'
    IN_KEY_SIGNED_MINIS_TR_PSBT_B64_SD = "cHNidP8BALQCAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAD9////A0BCDwAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcgoQcAAAAAACJRIECbDgsZc6aw71iJhjnT+24fhkwwaQcBeQzAKLfYAyKH3YgHAAAAAAAiUSBb9VQQXYabMAChLSgfclyBxe/EyI9CbdVU55TeBJFyUgAAAAAAAQEr73MeAAAAAAAiUSCKMs95fYJ22tHaq0FOis38SPVg352JZymPeaMp80ThwwEIQgFAUTOY5FvQfUhNhgBItKAWsTk8aeuhqD/EaYy6fo1qYie4TU2Al6T0NPCxu9T3F2kHUGM6erz6cq0Oct1i5NB6SgETQFEzmORb0H1ITYYASLSgFrE5PGnroag/xGmMun6NamInuE1NgJek9DTwsbvU9xdpB1BjOnq8+nKtDnLdYuTQekoiFcCxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBCUgcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gStVrLAIRZxH7ZhlZP7yYLfGJ/WUNIbYrz3I9PdvXk35AmuapvqBD0B9wV7+3vXs3uI0k6/j4L34rgi5F7O20jpQHgj0KmgZ1gC6L/yMAAAgAEAAIAAAACAAgAAgAAAAAADAAAAIRaxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBB0Ac8XaCjAAAIABAACAAAAAgAIAAIAAAAAAAwAAAAEXILGhNdUqlR4BAOLGTMrY2ZJYTQNRudp7fU7i8crRJqgEARgg9wV7+3vXs3uI0k6/j4L34rgi5F7O20jpQHgj0KmgZ1gAAAEFIApbWcEh7rgvRE5UaCcqzWL/TR1B/DS8UeZsKVEvuKLrIQcKW1nBIe64L0ROVGgnKs1i/00dQfw0vFHmbClRL7ii6x0Ac8XaCjAAAIABAACAAAAAgAIAAIAAAAAABQAAACEHNCGNnpQXkylYa9f6nYj1HGwVeZN1xflZXOoQv2wj1IM9AfhzyewSekNHshPEbIkzTZjkyNOdydoR+NEQ/jKQ1mT9Aui/8jAAAIABAACAAAAAgAIAAIAAAAAABQAAAAEGJwDAJCA0IY2elBeTKVhr1/qdiPUcbBV5k3XF+Vlc6hC/bCPUg61WsgABBSD2bDCgfbz9YefFtvrPTmwn+Ue6+suz/A6igeAWfm6UjSEHfG46McMry56iBWRzIilsW6NpNj8TbvjuWsshyPnVHlA9Ab986n7ezPJyDtG9zQD2xOzABTflVf8ZuM7cCcfmtzpUAui/8jAAAIABAACAAAAAgAIAAIABAAAAAQAAACEH9mwwoH28/WHnxbb6z05sJ/lHuvrLs/wOooHgFn5ulI0dAHPF2gowAACAAQAAgAAAAIACAACAAQAAAAEAAAABBicAwCQgfG46McMry56iBWRzIilsW6NpNj8TbvjuWsshyPnVHlCtVrIA"

    # Liana simple inheritance recovery PSBT - Tap tree signed
    RECOV_M_TR_PSBT = b'psbt\xff\x01\x00^\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\x06\x00\x00\x00\x01\xe5n\x1e\x00\x00\x00\x00\x00"Q S+\x82\x18\xb4|S\xa2\xf3\x15\xb1RH\xd0\xc3\x1d\xde)\xb3\xe2\xd6M\r\xeaP\xdb\xce\xae\x13g\xf5\xfb\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3"\x15\xc0\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04% q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xadV\xb2\xc0!\x16q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x16\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x01\x17 \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x01\x18 \xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x00\x00'
    RECOV_M_TR_PSBT_B43 = "1O4HGFPIQ-$.KIIHSB$QWW5D51IGXH7O11TXGA+HQ.4L/ZXG7AMSYR*2UJCUJ2EOWI:VBL3LJFRFH198+.T9Y/001EXT+QA5$V85R14-K2HWNK+9TQG60F26:N*P8S/*+7JRZKR3GB*A56VIB7:1:IN5J.RJR8NESUDO+:7P.T.CW.GP7XFI0A4KU$9ZD/2J0A-A+XFZJ30QS$-O*OON-5IH$0ES-$ZHV4Y4V5/HWLKSVV*-Q*/7/8+-KDL-CGL4H*UKBS:/X20QG/RQTSUKR759P+H90NZRXQDV3YZ$E6:F.MO3.GJECC6437MSC.G90SN*A52NA9*UI*QPD0K0G*SVHR4K*GX.HB2GL.:R2I--XC8LOZZSU/*I3IQ2EIWZ6R+F2VD8J5$5NIOMQ-$4RRCH1JS.F7IHZH0Q1S/L4CS*N.KIYYRWP.-*PELTJ$V7IA$5WSY/F66IF6H0/A+PS7.I5RXF1P7NPL2E+NOOPKCS:B.ICMCT0YHUHIGW6A3JBRJLKY*-P8LRE0EYK0C8NOM5QZSTEDGBXQG1J.PF/KO83HF16+KCN$B.DAC2N1DSBKTJQONKUDPJK-:K$6G.-6Z/6W*$DRYZUBG0RO4BH.XE.5RID1ZNY0:AVY:W80LPPC6N9*J1IR9:NHT349YXADJ7G8ZD+2"
    RECOV_M_TR_PSBT_B58 = "TQg8LbQjsiNzFXb3gyFabELir3GQCcKKJH25NkxR44rBxUhuuZu7XZ5rBDB256orGyzqnbxcytCZ92mAKSgwxMk1owyRefcpqrqRi8Ff1LcVeexCaWvpuRmNFXgFa3GcBNBu9f4jAg9KXQhMFfP4wikCm2V7FBRocjG8dDqbJ7oUqjZJ92ZNUeyjQv7f5jZMW8ievzN1UppVj8oSLh2cX4HdpxXjZD8SZU3g9EfNCCKoDHMEjWwjTr44Pd3qpAA99H7ZnzH683cLoABrvR8GCkDjxYuqX1SzRoCDyVWVWHnnRuDcas8LWQ6pmKSuWJBQoWxUKicBcxcySXcqQxNw9mjEDgtBSwj3PWKumwpvGfxzqjU7HnVG5MJQcWeG1FnqVAGJyujsu6uKxLNRZ8sysrCKiG6RBD4VazSc1mVqbzYjnCN5hsupjWuyC7NRuK5qxPQGhr4qGyFfeSYEKAGGU2t6eQhVLQh9WynPsp7x2fPnGRhYj6u4eoei5FPGhy7CppN7B1KWtoK7Q9YWzAM4vSSTeGL1JudmT6PhsbyG2qntbeWP5jb2Xa1rMZg8ii5eAPePe3rabBcEkDU5Mvc29PfKSNCeyz2ZQEmARwxH45vP"
    RECOV_M_TR_PSBT_B64 = "cHNidP8BAF4CAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAAGAAAAAeVuHgAAAAAAIlEgUyuCGLR8U6LzFbFSSNDDHd4ps+LWTQ3qUNvOrhNn9fsAAAAAAAEBK+9zHgAAAAAAIlEgijLPeX2CdtrR2qtBTorN/Ej1YN+diWcpj3mjKfNE4cMiFcCxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBCUgcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gStVrLAIRZxH7ZhlZP7yYLfGJ/WUNIbYrz3I9PdvXk35AmuapvqBD0B9wV7+3vXs3uI0k6/j4L34rgi5F7O20jpQHgj0KmgZ1gC6L/yMAAAgAEAAIAAAACAAgAAgAAAAAADAAAAIRaxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBB0Ac8XaCjAAAIABAACAAAAAgAIAAIAAAAAAAwAAAAEXILGhNdUqlR4BAOLGTMrY2ZJYTQNRudp7fU7i8crRJqgEARgg9wV7+3vXs3uI0k6/j4L34rgi5F7O20jpQHgj0KmgZ1gAAA=="
    RECOV_M_TR_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(RECOV_M_TR_PSBT).to_cbor())

    TAP_TREE_SIGNED_RECOV_PSBT = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03@B\x0f\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07 \xa1\x07\x00\x00\x00\x00\x00"Q @\x9b\x0e\x0b\x19s\xa6\xb0\xefX\x89\x869\xd3\xfbn\x1f\x86L0i\x07\x01y\x0c\xc0(\xb7\xd8\x03"\x87\xdd\x88\x07\x00\x00\x00\x00\x00"Q [\xf5T\x10]\x86\x9b0\x00\xa1-(\x1fr\\\x81\xc5\xef\xc4\xc8\x8fBm\xd5T\xe7\x94\xde\x04\x91rR\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3A\x14q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX@\xe0\xf3\n\xf0\x1b;\xf6\xde\x1d@X\xc0o\xe1s`\xea\xe2\x0bJ(\xbc4\xc1H\xa9%\xd7`q\xddC\x8b\xd3\xcd\xeb\x1d\xcc"w\x93\xcbj\x02[hW\xf0\xcd\xbc3>\xd3S\xf0a\xce\xfd\x92\x14\\\x9e\x1a\x17\x00\x00\x00\x00'
    TAP_TREE_SIGNED_RECOV_PSBT_B43 = "2ZMQXUW070H/C$O912IUP38PY-B:Y$-RMWPWCEVH4INJ0O18-TBJ48CZOD$TWI4I/NE8VN6KM12$5ZSVRTAG309P5CUJ2C2//V/10X86GODPB2R6A.-1F03RUUBF1+7YE8I/JYD4EB9C+U2E*ECO6IS/FAIE8CSCDLXC3$O$N*WQ9M1R*V*AKQ0$1T9RPNVBEVDGRPOJH8W.+6WV5M8.F3BOON/VSH39A5Z17$:50YW8.QS+AO7ZR.:RO*PD-DZPBFCDLJY*9QV/+BT1W9PT7JQ0XX81B::I9YOOIUKCJ$V*39Q$GYUKV887917VA-S7U1*4RHVHP64V$L6+Y0Y-S-8MTY99L*VA*$C*IA1YRVZ.A85M07KQF:CUR1RYODG6IXQHI*J/LWU$I46Y*6OIR*B40O-0+7U6.B:..O*YZZHA-*UAKA3J.DJBUP9ZYOV34+9K4-5R074W7NP$ZSXH*YL1B0YFUBQSLB:LE*K7UM.$L-8L759$8R/A8NZQLYMHBAAK/Y8MDL.17RIOJE4$:QD+N4HTN3BOL+"
    TAP_TREE_SIGNED_RECOV_PSBT_B58 = "2SudmehyNb1LkDuASe1chZCVpPJRP43zF2Ub1pehVv1WnSr4xckuEfFbCXCeSVuL2r43s6voxZbf4k8JeqvVwsVseK557UvqnpJ45Nts2vs274zxo1Pw1kEpZcKsMpsnaxp1rscFNrorxYGBQFBa3phYf39obkfjBcdTFuH724TJp95dPy3m66uegpNzCbWd3UnGbdXmALngVxMtZf26T4jEJrthxXZCDgQMM3ucGuYoVU1qdsGVCKvYo9NawBmRHsQGxxbEAdVkjDShJMMcpH9TpyVo8QUq28MNAMQYiBGFTTNGtm1iuQ118Tu37YAzCMtsEFL18hWNGjVGLPzednoie9iwxUrmm1fvHuxoZnjeop6h5aEJkksqZZESo8AYJXwVnv2NGvUn3KDMrRpEwWNp5m3Uj61UEeLWxav5kbf86x1rKukjpqA2GJBf3GqDvXHDf8EVoGTcNW7aAc3Edccd5dA4sy2QwfX2Ht1RHsfgVSWVRgfjZNUJGo"
    TAP_TREE_SIGNED_RECOV_PSBT_B64 = "cHNidP8BALQCAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAD9////A0BCDwAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcgoQcAAAAAACJRIECbDgsZc6aw71iJhjnT+24fhkwwaQcBeQzAKLfYAyKH3YgHAAAAAAAiUSBb9VQQXYabMAChLSgfclyBxe/EyI9CbdVU55TeBJFyUgAAAAAAAQEr73MeAAAAAAAiUSCKMs95fYJ22tHaq0FOis38SPVg352JZymPeaMp80Thw0EUcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gT3BXv7e9eze4jSTr+PgvfiuCLkXs7bSOlAeCPQqaBnWEDg8wrwGzv23h1AWMBv4XNg6uILSii8NMFIqSXXYHHdQ4vTzesdzCJ3k8tqAltoV/DNvDM+01PwYc79khRcnhoXAAAAAA=="
    TAP_TREE_SIGNED_RECOV_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(TAP_TREE_SIGNED_RECOV_PSBT).to_cbor()
    )
    TAP_TREE_SIGNED_RECOV_PSBT_SD = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01]p\x9b\x12\xc2\xd4\x8d\xb3\x84\x1b\xdb\xff\x1c\xfd\x0f\x8e\xeb\xe8\xb8\xf5("\xf4\xc6\xbdc\xa9-\xf2L\x85\xff\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03@B\x0f\x00\x00\x00\x00\x00"\x00 \x1a\xd9\xb6d\x0e\x18\xa16\xac\xeb\x10\xac\x8c\x84*\xdb\x8e\xdc\x96\x8d\xb7\xae/>\xc3-\x13F\xaf\xdd3\x07 \xa1\x07\x00\x00\x00\x00\x00"Q @\x9b\x0e\x0b\x19s\xa6\xb0\xefX\x89\x869\xd3\xfbn\x1f\x86L0i\x07\x01y\x0c\xc0(\xb7\xd8\x03"\x87\xdd\x88\x07\x00\x00\x00\x00\x00"Q [\xf5T\x10]\x86\x9b0\x00\xa1-(\x1fr\\\x81\xc5\xef\xc4\xc8\x8fBm\xd5T\xe7\x94\xde\x04\x91rR\x00\x00\x00\x00\x00\x01\x01+\xefs\x1e\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3A\x14q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX@\xe0\xf3\n\xf0\x1b;\xf6\xde\x1d@X\xc0o\xe1s`\xea\xe2\x0bJ(\xbc4\xc1H\xa9%\xd7`q\xddC\x8b\xd3\xcd\xeb\x1d\xcc"w\x93\xcbj\x02[hW\xf0\xcd\xbc3>\xd3S\xf0a\xce\xfd\x92\x14\\\x9e\x1a\x17"\x15\xc0\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04% q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xadV\xb2\xc0!\x16q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01\xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x16\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x01\x17 \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\x01\x18 \xf7\x05{\xfb{\xd7\xb3{\x88\xd2N\xbf\x8f\x82\xf7\xe2\xb8"\xe4^\xce\xdbH\xe9@x#\xd0\xa9\xa0gX\x00\x00\x01\x05 \n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb!\x07\n[Y\xc1!\xee\xb8/DNTh\'*\xcdb\xffM\x1dA\xfc4\xbcQ\xe6l)Q/\xb8\xa2\xeb\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00!\x074!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83=\x01\xf8s\xc9\xec\x12zCG\xb2\x13\xc4l\x893M\x98\xe4\xc8\xd3\x9d\xc9\xda\x11\xf8\xd1\x10\xfe2\x90\xd6d\xfd\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x05\x00\x00\x00\x01\x06\'\x00\xc0$ 4!\x8d\x9e\x94\x17\x93)Xk\xd7\xfa\x9d\x88\xf5\x1cl\x15y\x93u\xc5\xf9Y\\\xea\x10\xbfl#\xd4\x83\xadV\xb2\x00\x01\x05 \xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d!\x07|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP=\x01\xbf|\xea~\xde\xcc\xf2r\x0e\xd1\xbd\xcd\x00\xf6\xc4\xec\xc0\x057\xe5U\xff\x19\xb8\xce\xdc\t\xc7\xe6\xb7:T\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\x1d\x00s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x01\x06\'\x00\xc0$ |n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\xadV\xb2\x00'
    TAP_TREE_SIGNED_RECOV_PSBT_B64_SD = "cHNidP8BALQCAAAAAV1wmxLC1I2zhBvb/xz9D47r6Lj1KCL0xr1jqS3yTIX/AAAAAAD9////A0BCDwAAAAAAIgAgGtm2ZA4YoTas6xCsjIQq247clo23ri8+wy0TRq/dMwcgoQcAAAAAACJRIECbDgsZc6aw71iJhjnT+24fhkwwaQcBeQzAKLfYAyKH3YgHAAAAAAAiUSBb9VQQXYabMAChLSgfclyBxe/EyI9CbdVU55TeBJFyUgAAAAAAAQEr73MeAAAAAAAiUSCKMs95fYJ22tHaq0FOis38SPVg352JZymPeaMp80Thw0EUcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gT3BXv7e9eze4jSTr+PgvfiuCLkXs7bSOlAeCPQqaBnWEDg8wrwGzv23h1AWMBv4XNg6uILSii8NMFIqSXXYHHdQ4vTzesdzCJ3k8tqAltoV/DNvDM+01PwYc79khRcnhoXIhXAsaE11SqVHgEA4sZMytjZklhNA1G52nt9TuLxytEmqAQlIHEftmGVk/vJgt8Yn9ZQ0htivPcj0929eTfkCa5qm+oErVaywCEWcR+2YZWT+8mC3xif1lDSG2K89yPT3b15N+QJrmqb6gQ9AfcFe/t717N7iNJOv4+C9+K4IuRezttI6UB4I9CpoGdYAui/8jAAAIABAACAAAAAgAIAAIAAAAAAAwAAACEWsaE11SqVHgEA4sZMytjZklhNA1G52nt9TuLxytEmqAQdAHPF2gowAACAAQAAgAAAAIACAACAAAAAAAMAAAABFyCxoTXVKpUeAQDixkzK2NmSWE0DUbnae31O4vHK0SaoBAEYIPcFe/t717N7iNJOv4+C9+K4IuRezttI6UB4I9CpoGdYAAABBSAKW1nBIe64L0ROVGgnKs1i/00dQfw0vFHmbClRL7ii6yEHCltZwSHuuC9ETlRoJyrNYv9NHUH8NLxR5mwpUS+4ousdAHPF2gowAACAAQAAgAAAAIACAACAAAAAAAUAAAAhBzQhjZ6UF5MpWGvX+p2I9RxsFXmTdcX5WVzqEL9sI9SDPQH4c8nsEnpDR7ITxGyJM02Y5MjTncnaEfjREP4ykNZk/QLov/IwAACAAQAAgAAAAIACAACAAAAAAAUAAAABBicAwCQgNCGNnpQXkylYa9f6nYj1HGwVeZN1xflZXOoQv2wj1IOtVrIAAQUg9mwwoH28/WHnxbb6z05sJ/lHuvrLs/wOooHgFn5ulI0hB3xuOjHDK8ueogVkcyIpbFujaTY/E2747lrLIcj51R5QPQG/fOp+3szycg7Rvc0A9sTswAU35VX/GbjO3AnH5rc6VALov/IwAACAAQAAgAAAAIACAACAAQAAAAEAAAAhB/ZsMKB9vP1h58W2+s9ObCf5R7r6y7P8DqKB4BZ+bpSNHQBzxdoKMAAAgAEAAIAAAACAAgAAgAEAAAABAAAAAQYnAMAkIHxuOjHDK8ueogVkcyIpbFujaTY/E2747lrLIcj51R5QrVayAA=="

    # TR expanding multisig - tr(tpubD6NzVbkrYhZ4YYQjuKXFp85eRGCk4oA94MXbbHJW6zNAibMfkwZh7JQNVHEhpcQYaRCUs3b5PhvKPKESGoAJptiLvF8Rm1jhoFsryyFuR1P/<0;1>/*,{and_v(v:multi_a(2,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<2;3>/*,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<2;3>/*,[8cb36b38/48h/1h/0h/2h]tpubDESTVwqbbaSoN2mPq7tcWkPBpRBkaEADrUzUhRTVnNef6oVn6w2PHL4zoUjUAJSPLJQRBetkgX4sDRcoaCyFHxqHGyWyaiV8REKDkh7zQac/<0;1>/*),older(6)),multi_a(2,[73c5da0a/48h/1h/0h/2h]tpubDFH9dgzveyD8zTbPUFuLrGmCydNvxehyNdUXKJAQN8x4aZ4j6UZqGfnqFrD4NqyaTVGKbvEW54tsvPTK2UoSbCC1PJY8iCNiwTL3RWZEheQ/<0;1>/*,[02e8bff2/48h/1h/0h/2h]tpubDESmyzX6RMHRHvzxgLVXymd193CSYYT6C9M9wa4XK649tbAy2WeEvkPwBgoC7i76MypQxpuruUazQjqibbCogTZuENJX6YiuZ5Fy8sf7GNi/<0;1>/*)})#6ga85u82
    # tb1p2v4cyx9503f69uc4k9fy35xrrh0znvlz6exsm6jsm082uym87hasr4urrx

    EXP_TR_MINIS_PSBT = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01\x7f\xca\x84\x9d\xd9\x85\xd8s\xa9Lz\xbd\x95\x05b\x1f<\xb1\xf3\x01:\x05j\xcda;\xc1\x8d\x88G\\\xf1\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00"Q \x87\\?;;\x80\x10\xc0\xfe\x06\xe3\xdc\xcbj\xed\x00\xc4\x9a\r\x91?\x8d\xc3\x1a\xb1\xda%;\ne\x8a\x82@B\x0f\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3\xda\x81\x07\x00\x00\x00\x00\x00"Q \x12Z\xa5\xd2\xc5\x8bR\xc8~\xbd\x8d\xbb\x1dK\r,\xea\x10\xf2\x16G\x98\x90g<\x88\xa4\x0cP\'\xff:\x00\x00\x00\x00\x00\x01\x01+\xe5n\x1e\x00\x00\x00\x00\x00"Q S+\x82\x18\xb4|S\xa2\xf3\x15\xb1RH\xd0\xc3\x1d\xde)\xb3\xe2\xd6M\r\xeaP\xdb\xce\xae\x13g\xf5\xfbB\x15\xc1\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9k R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e\xac w\xb7\xdf\x08\xb0a\xca\xeb\xa5\xc0\xc4YE\x16q\x88 \x00\xdaG\x12\x9aWN6C\r\xa4\xfb\xa7\xe4A\xba \x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd\xbaR\x9dV\xb2\xc0B\x15\xc1\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdzG h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\xac ,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92\xbaR\x9c\xc0!\x16\x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\r\x00|F\x1e]\x00\x00\x00\x00\x01\x00\x00\x00!\x16,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92=\x01W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdzs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x01\x00\x00\x00!\x16h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87=\x01W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16w\xb7\xdf\x08\xb0a\xca\xeb\xa5\xc0\xc4YE\x16q\x88 \x00\xdaG\x12\x9aWN6C\r\xa4\xfb\xa7\xe4A=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x01\x00\x00\x00\x01\x17 \x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\x01\x18 \x97J\x82\x1dSk\x03O\xd0\xce\xdf~\xfbw0\x83\xccb\xfcY\x06_L\x9b\xd3|\xd3\xb7\xcd\\\x9b3\x00\x01\x05 \xb2\x8d\xb420\x90=\xed\x82\xf8\xdf\xe3\xa3\xd5\xae\xe3\xbe\xad\x88\xe3o\xa9\xb0\xe6x\x90\xf3W\xbeo\xee#\x01\x06\xb6\x01\xc0F \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\xac q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xbaR\x9c\x01\xc0j \x8d\x14\xa0!lo\xaf\x02(\xba\xba\x88\x96\xfd-k\x8a\xea\x06\x80\xcf\xe7\x16\xe5\xd0L\x9e1Q\x82\xefl\xac \x93L3\xca\x11c(=\xc5\xed\x8aRl\xfez\xd3\x9e\xea\xce)\x0c\x8c\xe2\xffy\x03`[\xea\x7f?.\xba \xb7O\xab\x0f\xe3{\x8b\xac\x8a7$\x9cH\xf6x\xd9f\xbe\x8a\x97\xc6~\x17\x91\x97j\x0f\x00\x0f"\xd52\xbaR\x9dV\xb2!\x07q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01Br\xf1\xe7\xf2\xd3\\|\xaf\x01\xc6\x11\x820\xde\x0e]BaL|&\x8b`\x993\x8b\\\x82S\x0e\xb8\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x07\x8d\x14\xa0!lo\xaf\x02(\xba\xba\x88\x96\xfd-k\x8a\xea\x06\x80\xcf\xe7\x16\xe5\xd0L\x9e1Q\x82\xefl=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaas\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x03\x00\x00\x00!\x07\x93L3\xca\x11c(=\xc5\xed\x8aRl\xfez\xd3\x9e\xea\xce)\x0c\x8c\xe2\xffy\x03`[\xea\x7f?.=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaa\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x03\x00\x00\x00!\x07\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04=\x01Br\xf1\xe7\xf2\xd3\\|\xaf\x01\xc6\x11\x820\xde\x0e]BaL|&\x8b`\x993\x8b\\\x82S\x0e\xb8s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x07\xb2\x8d\xb420\x90=\xed\x82\xf8\xdf\xe3\xa3\xd5\xae\xe3\xbe\xad\x88\xe3o\xa9\xb0\xe6x\x90\xf3W\xbeo\xee#\r\x00|F\x1e]\x00\x00\x00\x00\x03\x00\x00\x00!\x07\xb7O\xab\x0f\xe3{\x8b\xac\x8a7$\x9cH\xf6x\xd9f\xbe\x8a\x97\xc6~\x17\x91\x97j\x0f\x00\x0f"\xd52=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaa\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\x05 \x05/\x9b\x92\xfe\x84)\xe3L\x1c\x11\x07\x7f`!\x8c.\n\xaa\x84\xe3\xf2\xec|\xe26\x0e\xb4\x9b\xe550\x01\x06\xb6\x01\xc0F \xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\xac |n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\xbaR\x9c\x01\xc0j \xe6r\x85\xe7\\\x8a\xe5tB\x90\xef\xdf-C\x14\x8a\x8a\xd3{\xda[!\xf3\x89\xf1X;\xa6\xe6(\x96\xee\xac i\x94\x0c\x81\xcd\xb2\x17\xab\x86A\xc8\xbb!\x9fL\xad\xc9\r\xf1J\xa5\xc1l11\xac\xb7\x9f|\x11\xb4\xf6\xba \x9b\x105\xbc\xba\x1b\x96o\xff6\xa2\xc1\xb1R7\xbc\x99Q\xb9\x91Zr\xbd\xf4%/\xae_\x9a\x08\xb5\xff\xbaR\x9dV\xb2!\x07\x05/\x9b\x92\xfe\x84)\xe3L\x1c\x11\x07\x7f`!\x8c.\n\xaa\x84\xe3\xf2\xec|\xe26\x0e\xb4\x9b\xe550\r\x00|F\x1e]\x01\x00\x00\x00\x01\x00\x00\x00!\x07i\x94\x0c\x81\xcd\xb2\x17\xab\x86A\xc8\xbb!\x9fL\xad\xc9\r\xf1J\xa5\xc1l11\xac\xb7\x9f|\x11\xb4\xf6=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x03\x00\x00\x00\x01\x00\x00\x00!\x07|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP=\x01\x08\xbeb^\x87gy\x83fF\xa6T\xed\x08\xca|C\x11\x9b\x03EP\x98\x14\xa0O\xde\x066\x7f\xfb\x08\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\x9b\x105\xbc\xba\x1b\x96o\xff6\xa2\xc1\xb1R7\xbc\x99Q\xb9\x91Zr\xbd\xf4%/\xae_\x9a\x08\xb5\xff=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\xe6r\x85\xe7\\\x8a\xe5tB\x90\xef\xdf-C\x14\x8a\x8a\xd3{\xda[!\xf3\x89\xf1X;\xa6\xe6(\x96\xee=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x03\x00\x00\x00\x01\x00\x00\x00!\x07\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d=\x01\x08\xbeb^\x87gy\x83fF\xa6T\xed\x08\xca|C\x11\x9b\x03EP\x98\x14\xa0O\xde\x066\x7f\xfb\x08s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x00'
    EXP_TR_MINIS_PSBT_B43 = "2+0M:*ILDQYN:FA2VEHKQ63OAENOFWPYRKA*/JXTUAIUQ/F8V2P2U/15CPXZPC6MRDM.5RR+:VRHCBI025RT8KUSR9$/1EQ8D5D86BQ+.QA9+$Y*FQI-AJW4HB2Y57BDE$X.-9R:/1B-BW-3S.UOYDMI/WOLJJ+VTCQECQ3+C91G5K7OSR96Q8.-Z+ZA66E96RJ5YT2*5:RB9-TBJ9F4ENHEK77//P*86FSM26G1S74HJ2$9UBSY+RAB9VP/3VSK1M3MUZCLBPRQSH7A4S3LC42ZEU7X93UKAWD$QDXK:T41-NVGQ0-5/U48574QI.ZFB5CO.7UJH+..EXQXU/OM--F4G*+$JCNBVC+Y4:--YJWJ9Y1Y3-0OL*FSCWB$ZVRKF-0M/Z4XXLJLJ6AILVQF$9YJ/1W$OF.T.AVK6+USK:0B60TLHJ:*1R*:*QPF48KP*RTXJQG84I*7NB7D8NF:X0MA9W9Z$C45G2D:8TREV59ZLC3G5FP8ZG-F-EFFEXGHBRAI+GLHU6Q+L50ZW.PR0GI/6/E72/81W::WJ+:Q9C89GCPM6AG7L0MWTN4L/EQJ:QP8UJ.TNQ4-.$1:X48$H-$E.MJ1DUT+T.CGEX1USNNC.TI+W+-L3U78GO:T:9R:/6YJ-B4TI2Y$.R2HA313-7GRAZ+YER6D4ZH5UX.FNCKJ2-N--M-4G0RF953GKW-MW3MVG0SOUIQC:DLLSNL588NFE4HKRMGJJ/NU4PFUOY+*ZB-4+P4PU*HLL*15K05LTH41+W6N547WSD:$FU9PAI68WUOVRQ7DRS09+YK$:KSV+*JX:P.45NIP/AM:ZLA1N/.K0$:N-MP+I.N89WCW*8-F7:KQQ*DNDSTQC$*H6CVCE.4*G+729:W9M-F1CTDP28R6DWH.JKNJGTYZVUWOKR684S4WHTTH*I1:G4TSB$DSVSM/T*ZAM3T9Q*NKWGKZL7UA3.SQ6A2IIZRADHA*SMASAWHEVU:RO9DB7NA65LOY5.$VU2.YI7WG0RKAFSUS.CTKM/.9EJ:0SSP1VNQX5$97HM1D6P*I4N$B$S$BB4HDU4C:MD89N6EPYRPPS4:GYR9TN9E96UJRW*EU4H$D6DC*.0J9P+H.+BRYGM$0SZI0-6W/X6UKPG8H-/QC$74-4K:C1JXTO.7QTOY24KE*E:-Q1.P3XSM$FAAM*Y6B6LTAS1VQJMI8YKI6.DE1338V$F$S/.IPP75$$VFW+MG1A:FXLMVD.Q73Z5MULV$QGJ5JY/0050-::MULH.+A.2LEMW92W8/*X+UN.5TBEPW9.-01G6T4U:L4:H6U30*WR4ZMBM6VJ6Q7OVWV1JK4U$R11IFLG:6PUHKNYEIXV+60UTL4NTGN$8GRUV2D5R+K/9OBO3IORN44L-7JJ-O7HNN*IE-IGAR*WUCKU5SCU9*0+*JP$4V/J9O.I6E4VX9WMMP+0-R6SFAJ+NJ2RDKDH4N:DQB8:.FYN3IK9/:WPH1TS-NVAHAUTWJXK6X7*5Y5C2V4N.199-4QSQT/B7ZYX16YF9PAV4DWKJT*1UGZUPNTJK/OC-01WFY35IY/BC02OTZ8QP.4L2KWQSTN+PIDQ*SYDH-1C9UQ-.G8YPM1O/8I92DOB/951U44D4QK4BXZBW/I+H4+PBUOJCC280BGUN5VI525F$0S:4G6M7CNB8ZNZDJ7:IKRH5+XZW*.2ZE6..PWJW178/3GL925KDR40T+6-XPJD9CEF1GQ6FXM:+Y.0:/WM:WGTRR.IEBA$QF963K445ME8NFRZ8//QWCU7S93R68*T*88UMYSTZSAS0FT89XRV-4N+Q0:XT2-0HU5+QG0S3DZ:2M9:1D2.V-16:G$BMDID6K.DXQ4CQZ4QACIIP.L$KLG9VLIK-HHV4N0PXP1XG07DAHSW07RXUQURG*/IS3$RB+X.W0-LRV3M90KE/E/K1CH$$JRGPEW*$50+X.93JN:S5RWT4NMO17ZSX25MGS71*2S*0HFFPM8SW4.CXNJAQW/UX-.8CA6HOI2:HGBT5V/H3R238:X97NBZJSWF/-8$FDRKRMVZFOQVQE5QYCV:151S-NY3$7Q:GTRDAB3Z$5M-R1$38GLLW8P$S47LRZB5RVQQVUY.$P2PLWZA8FBIM2WRPM*D34XCFC05$HX6EHM4F5QUP*$HOWGAY9IK-GC31.A23*NTPN1XR5Y$B*RP40P+X6ANI8KRQ-TY7$Z46/I.LRC55ZNV8J:QCN.B1M7B8/7:YNO410WAFGJ*8GD-0+XB:680J812L0:81$NPKW/.T37QMOAD$7G9GKWL2TMG6DOKZA-MK8+8SPZ$VOQTKG/7SZXLJK1L8$9SZ84RAI8K18G4BT.FDS$XA-G/Y584/39ETKU4LF5I7X0*X:/LLU.*:URSF:A18F/-3:4/QYS1V/K:8V+*F3QP*2Q7JI/+NHFZTDB/9W0NBJXUC8I3+X177NBS2.WDD1DQLWLC/Y:OITJ:F4-ZE0WXOWSQCJ/CZ$RU$SMIKL*.4X6D-9PSRR34NSOU.7LSXAQNEN5AYMFR*J*I.5$O3X.8.JVPZS$+Q73DBMD4Y5EIT3LAHJWRLWU+4$SJ88AAA.JNUPW.WIBI7JRL9C./MO*V:CAWRZ4/OH8X653SP*6ED:ZR25NGP-WQ6PM:/HKP0Z:1G+$-9.1:O$P9E2.4K.PN*Y//3U$5ORFNV29T6IV-CI/NP9/LHGSI+NQXSIO78UXEZT3XSX/0G7Z54/XE$V-1S5D*4KP/$IQ.E23.*XR/8$HK5-6Z+J3DYJTXG3IOSVWP$K1JQH-P2MZYS/GTEI03QTIP2RWM6I1EV3-W7NM*ZKN38KGG/CGNH/-CYGR$KVNLT9J$CB1$6ETSX$-HN4QQVV2TH.YW5S4/CBUR3Y-T0EBP::$D44YA$I**ZMM3/E*OXV:MX40067BGFKC*WUEV3Z7Q:CA*OYR2MKRY8OO.7.VQGEFWBIIQ2L7NTDBN+9BA3$7XPB:KYZV/GSLM:7LYI6C0V4AGCD*YKXXW*6C/DK0PB+-N1998D7JTP4J28ZGG*M/VV1F$FPCZ.3BN61OKD17+NU7ZYF$-03:EIGPJ*7U0-YH/5FJ.D/MRMFL+//JDKDOY.6SU$1IPF1CHDMA3FV.9B-VFC0$QMQDLRW05-VBTSP6PJSVOMUVZIS5N9$J*37$NC97ZLJ$C0B$SJ93$IGWDR6-/-ACZHS5WA97AW$3-H:DWA$MIZ190-7*G/LF9$J*CBRW51BXL4NBATDC55P++ZZYRG-K0WAAM5+9*LN9JV+CE2H313TA6F.XC6.:X-K++B.TZ3J+WV8O/R-CK1:L:9C38J0YL5LZ.GG797RO3XLZ$DEVLW69URIG*ML7-3NQHQXABICL9OXWT2$9+OK8Q+GTVC4Y*ELJK29EH1QEWVCC$UGZWFO8W9X7JOEH4W21WKJPL1U:93ZM+T0YHU8$O9B*LOOD$D:JVSV.OFPQ:YYXTSCO/GOY.XSM44RH8+Y.3HII7J7OH6FVM:WMPH0Q+1Z:44+DN.FF$2CZ*HSE15DIRCH3$H*JHPT6R:LH7$B:MBJG418TNRL7D/C6-Q1UTGZJMI-.-E:DX6439.RXYL+QSMCE3EQ849Q-:G4:O/D9LQ7Y-7PSZ7+MKI-4JBF:P7KV$U*JLRO4VXEAJYW/H75PKER$H2B7O:I-IW9-GM.MXJAZ$YXXO0L9FWCI8QOE0$9M4:M5GO6O5QQ/7:RA+HBDJCUCYNRUOE9*-ATGTTVNV4YLNU6M0EWECTAVJZ6YPJNYWOWE5F+KCHHNUC+93I+DM*2XHL-LPJFC6VO97MB$EQ3EAC:3+8C.HV48LLM0R8XXFF78PYOGF-V7JMP:W+6$OE7Q9B13GEL7PRZ4L/Y8T4GXKY:7FL2I2RMG5A+"
    EXP_TR_MINIS_PSBT_B58 = "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"
    EXP_TR_MINIS_PSBT_B64 = "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"
    EXP_TR_MINIS_PSBT_UR_PSBT = UR("crypto-psbt", PSBT(EXP_TR_MINIS_PSBT).to_cbor())

    SIGNED_EXP_TR_MINIS_PSBT = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01\x7f\xca\x84\x9d\xd9\x85\xd8s\xa9Lz\xbd\x95\x05b\x1f<\xb1\xf3\x01:\x05j\xcda;\xc1\x8d\x88G\\\xf1\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00"Q \x87\\?;;\x80\x10\xc0\xfe\x06\xe3\xdc\xcbj\xed\x00\xc4\x9a\r\x91?\x8d\xc3\x1a\xb1\xda%;\ne\x8a\x82@B\x0f\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3\xda\x81\x07\x00\x00\x00\x00\x00"Q \x12Z\xa5\xd2\xc5\x8bR\xc8~\xbd\x8d\xbb\x1dK\r,\xea\x10\xf2\x16G\x98\x90g<\x88\xa4\x0cP\'\xff:\x00\x00\x00\x00\x00\x01\x01+\xe5n\x1e\x00\x00\x00\x00\x00"Q S+\x82\x18\xb4|S\xa2\xf3\x15\xb1RH\xd0\xc3\x1d\xde)\xb3\xe2\xd6M\r\xeaP\xdb\xce\xae\x13g\xf5\xfbA\x14R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz@\x04<\xc8F"\x889\xc5\x99\xa5G\xff;\x8f\xdd\x18MVG;\xcf\x1f\xd1]\x1634\xa4\xb8D\x1a\x08\x92\n1N\xea\xdd\xcd\x86\x96\x96\x80\x02^W\x7f#\xc6s\xb4Lp\xb2\x02\x8fMx\xc5\x14vy\xf7\x86A\x14h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9@\xf9:GjU\xfb$9\xa8>\xc8\xf3\xde@f\x8b\x87\x96I\x17\xe7\xaa\xc8y\xeb\x97\xf9GSX:\xf5+\x11eJ\x9bx\x18x\xaa\x1ax\xb8\x1d\xe9R\x0e\xe2jK\x8e\xadr\xcd\xc5VV\x1f\t\x11\xad\xcf\x93\x00\x00\x00\x00'
    SIGNED_EXP_TR_MINIS_PSBT_B43 = "4TT$EW2BC750K0.EQ*OESR*TGYF.-DD/LNKXNKCH-6XECST3IQQE+:F6.Y/0JLF7F+GJN5RT*NFF:IV5+NZPT63T2:7-N/5Z67XO/QU*-Y5A/*5HX89U7DJWQ0I-6YIYT15-50EHV:4HD0T5J+M:FBO80S+V8R.NKPC86Y:EM/J8WSHFX$S$IQD.Q0/GQHLNY$R8$MRS6V*Y5VE6TMNMZU4$$AL/0P1*0VIWH:F5SI/UIRS46O64DL:VURGAY39L/FWKSPR9FWE6I43KBC27/1GSJN+FXOX*:Q3O-6BYTXWK5Z93Y3979VKYOP8VE/EQ6XUV14$J06O.NMPACBX/N.2-V+ODBBY-R8.6NPDSYJ:/XX0RWZ2:*P.BRF+9C*XQT.LBNN-DVA7.Q14LGOOENSM/I6$43M5271UL/Q+HM.-9-HV2:4Q6+WMP*IOWFIN.CA0ZR/414P7Y8$J41RYF11YMQ8.+8CFL:*W43S$DBC$JHKG8G*8UW*QTJ9R:JR42.W0DZ2RUW+MWIJ/YG6:XVR8V$594TU0QO0PDG-AAFEA+S/1ONG*05SNXP29T34$:-0OMFMUL:ZN330:GFKIT9RVMO$FT+Y8/*1C9JTU61R5661+-.WZ.U/8F9F:9ECFSHWS4$Z4-T*NK1LYPB1P7JJ8MJYD/6L+8.+/RZ6JGM$14Q$AA+*G29W$3.7OZMAH$HYVXUC9$NLMLYXG1352L..SF-+F-Q573B7*"
    SIGNED_EXP_TR_MINIS_PSBT_B58 = "yBmUhxPER5LACMorWNH5G7qrTgLkwgd6sudwBgzFT78eurc9c2xwb7bhjyY7codASWJZsTU7tAAo51pgQMghHf64iBgA4V18jHKvEUSV9c47uTVoug7uZsx6DxcSSCnduUrh9L5oxoScPMkBR2dUjkEJYL9tJfZdtfztPy8m2MP587kj375NhNu3vHPb5mNrDaLtLC2rh5DZ6cASa4Vt1taRtpGLquwJE9NPQ7V6eEYvhpagxZvCvErNQZaSnhQQ3hgbHQgwQegmHehkXpVLTV3NqLh3uEWUosqNNhZesCRP9BTwp41dGETHi2Ksz8YRmjnyoFrL8g6xrX4j4YCMxkmf2tXY1XCPdMaLPJAmKu9f8o9MdJQrzHJCi6VuuvkfBKG6R9MAAPPkWE1Prj3GicD4aU7wWmo8A7eRZPpHbxwWxC3DMgveT4XPsGpe3MyMkzs6yG3Wfi3v5ae47oLhQuKexbwzDHtcNcNYsocS3d1fEAMW3SshGYpBzSY5YJiPX2JUZJ3Hr7QchnZmvAh37LAJRHHWELufq3xHpkGaWUExomR26eVFWyMwLjvpgUGxkuET9u4ByTwx1SWbygqmmtUsv15yLcnuoeuGVJr6KutdoWRShLdUDYQ8iHXgxSWFfMre75Ac6Ko9xzaarwKvGPcSxjtA18ZbyHyeP7xoYumZ"
    SIGNED_EXP_TR_MINIS_PSBT_B64 = "cHNidP8BALQCAAAAAX/KhJ3ZhdhzqUx6vZUFYh88sfMBOgVqzWE7wY2IR1zxAAAAAAD9////AyChBwAAAAAAIlEgh1w/OzuAEMD+BuPcy2rtAMSaDZE/jcMasdolOwplioJAQg8AAAAAACJRIIoyz3l9gnba0dqrQU6KzfxI9WDfnYlnKY95oynzROHD2oEHAAAAAAAiUSASWqXSxYtSyH69jbsdSw0s6hDyFkeYkGc8iKQMUCf/OgAAAAAAAQEr5W4eAAAAAAAiUSBTK4IYtHxTovMVsVJI0MMd3imz4tZNDepQ286uE2f1+0EUUrEvnMbNNYuX+qDx0JJG4ybhHQdvYA6ncG5ztzxuEmXLToX/NmN8axrk+UvWU+drbTU4piY9m8SD4Zj49o39ekAEPMhGIog5xZmlR/87j90YTVZHO88f0V0WMzSkuEQaCJIKMU7q3c2GlpaAAl5XfyPGc7RMcLICj014xRR2efeGQRRolXLiiw/tqdaYHAI32eXe2/7BbecUP2gKAu1dFZ91h1e7ZIMQ2OzUSBPaEsAhalhjV3AIb1wvXmo/GDKFVcSpQPk6R2pV+yQ5qD7I895AZouHlkkX56rIeeuX+UdTWDr1KxFlSpt4GHiqGni4HelSDuJqS46tcs3FVlYfCRGtz5MAAAAA"
    SIGNED_EXP_TR_MINIS_PSBT_UR_PSBT = UR(
        "crypto-psbt", PSBT(SIGNED_EXP_TR_MINIS_PSBT).to_cbor()
    )
    SIGNED_EXP_TR_MINIS_PSBT_SD = b'psbt\xff\x01\x00\xb4\x02\x00\x00\x00\x01\x7f\xca\x84\x9d\xd9\x85\xd8s\xa9Lz\xbd\x95\x05b\x1f<\xb1\xf3\x01:\x05j\xcda;\xc1\x8d\x88G\\\xf1\x00\x00\x00\x00\x00\xfd\xff\xff\xff\x03 \xa1\x07\x00\x00\x00\x00\x00"Q \x87\\?;;\x80\x10\xc0\xfe\x06\xe3\xdc\xcbj\xed\x00\xc4\x9a\r\x91?\x8d\xc3\x1a\xb1\xda%;\ne\x8a\x82@B\x0f\x00\x00\x00\x00\x00"Q \x8a2\xcfy}\x82v\xda\xd1\xda\xabAN\x8a\xcd\xfcH\xf5`\xdf\x9d\x89g)\x8fy\xa3)\xf3D\xe1\xc3\xda\x81\x07\x00\x00\x00\x00\x00"Q \x12Z\xa5\xd2\xc5\x8bR\xc8~\xbd\x8d\xbb\x1dK\r,\xea\x10\xf2\x16G\x98\x90g<\x88\xa4\x0cP\'\xff:\x00\x00\x00\x00\x00\x01\x01+\xe5n\x1e\x00\x00\x00\x00\x00"Q S+\x82\x18\xb4|S\xa2\xf3\x15\xb1RH\xd0\xc3\x1d\xde)\xb3\xe2\xd6M\r\xeaP\xdb\xce\xae\x13g\xf5\xfbA\x14R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz@\x04<\xc8F"\x889\xc5\x99\xa5G\xff;\x8f\xdd\x18MVG;\xcf\x1f\xd1]\x1634\xa4\xb8D\x1a\x08\x92\n1N\xea\xdd\xcd\x86\x96\x96\x80\x02^W\x7f#\xc6s\xb4Lp\xb2\x02\x8fMx\xc5\x14vy\xf7\x86A\x14h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9@\xf9:GjU\xfb$9\xa8>\xc8\xf3\xde@f\x8b\x87\x96I\x17\xe7\xaa\xc8y\xeb\x97\xf9GSX:\xf5+\x11eJ\x9bx\x18x\xaa\x1ax\xb8\x1d\xe9R\x0e\xe2jK\x8e\xadr\xcd\xc5VV\x1f\t\x11\xad\xcf\x93B\x15\xc1\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9k R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e\xac w\xb7\xdf\x08\xb0a\xca\xeb\xa5\xc0\xc4YE\x16q\x88 \x00\xdaG\x12\x9aWN6C\r\xa4\xfb\xa7\xe4A\xba \x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd\xbaR\x9dV\xb2\xc0B\x15\xc1\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdzG h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87\xac ,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92\xbaR\x9c\xc0!\x16\x12q\x1a\x15(m\xd0<\'G\xfb\x13\xb5h\x9aq$\xbcE11\xfc\x13D\xce\xc7\xfa\xc4\x82\xe9\x1b\xdd=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16\x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\r\x00|F\x1e]\x00\x00\x00\x00\x01\x00\x00\x00!\x16,\xc4Rd\x176!k\xcaX\x9c\x0c\xc1\x018\xddWsSu3\x98\xb3\x12\x9c\x15\x1a\xf4\x7f\xf96\x92=\x01W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16R\xb1/\x9c\xc6\xcd5\x8b\x97\xfa\xa0\xf1\xd0\x92F\xe3&\xe1\x1d\x07o`\x0e\xa7pns\xb7<n\x12e=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdzs\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x01\x00\x00\x00!\x16h\x95r\xe2\x8b\x0f\xed\xa9\xd6\x98\x1c\x027\xd9\xe5\xde\xdb\xfe\xc1m\xe7\x14?h\n\x02\xed]\x15\x9fu\x87=\x01W\xbbd\x83\x10\xd8\xec\xd4H\x13\xda\x12\xc0!jXcWp\x08o\\/^j?\x182\x85U\xc4\xa9s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x01\x00\x00\x00!\x16w\xb7\xdf\x08\xb0a\xca\xeb\xa5\xc0\xc4YE\x16q\x88 \x00\xdaG\x12\x9aWN6C\r\xa4\xfb\xa7\xe4A=\x01\xcbN\x85\xff6c|k\x1a\xe4\xf9K\xd6S\xe7km58\xa6&=\x9b\xc4\x83\xe1\x98\xf8\xf6\x8d\xfdz\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x01\x00\x00\x00\x01\x17 \x12\x97\x80=D@o\x05S\xab\xcbu\x93h\xb7\xb05\r\xa3\xa6!\x04[G\x8dtVX\x87\xaan\x99\x01\x18 \x97J\x82\x1dSk\x03O\xd0\xce\xdf~\xfbw0\x83\xccb\xfcY\x06_L\x9b\xd3|\xd3\xb7\xcd\\\x9b3\x00\x01\x05 \xb2\x8d\xb420\x90=\xed\x82\xf8\xdf\xe3\xa3\xd5\xae\xe3\xbe\xad\x88\xe3o\xa9\xb0\xe6x\x90\xf3W\xbeo\xee#!\x07q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04=\x01Br\xf1\xe7\xf2\xd3\\|\xaf\x01\xc6\x11\x820\xde\x0e]BaL|&\x8b`\x993\x8b\\\x82S\x0e\xb8\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x07\x8d\x14\xa0!lo\xaf\x02(\xba\xba\x88\x96\xfd-k\x8a\xea\x06\x80\xcf\xe7\x16\xe5\xd0L\x9e1Q\x82\xefl=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaas\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x03\x00\x00\x00!\x07\x93L3\xca\x11c(=\xc5\xed\x8aRl\xfez\xd3\x9e\xea\xce)\x0c\x8c\xe2\xffy\x03`[\xea\x7f?.=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaa\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x02\x00\x00\x00\x03\x00\x00\x00!\x07\xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04=\x01Br\xf1\xe7\xf2\xd3\\|\xaf\x01\xc6\x11\x820\xde\x0e]BaL|&\x8b`\x993\x8b\\\x82S\x0e\xb8s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00!\x07\xb2\x8d\xb420\x90=\xed\x82\xf8\xdf\xe3\xa3\xd5\xae\xe3\xbe\xad\x88\xe3o\xa9\xb0\xe6x\x90\xf3W\xbeo\xee#\r\x00|F\x1e]\x00\x00\x00\x00\x03\x00\x00\x00!\x07\xb7O\xab\x0f\xe3{\x8b\xac\x8a7$\x9cH\xf6x\xd9f\xbe\x8a\x97\xc6~\x17\x91\x97j\x0f\x00\x0f"\xd52=\x01[m\x83v\xc1v\xdcT\xa5/,-\xa4\x0ci=\xf4\xd9\xd18\xe0O\x96\x829\x87\x9b\x9c\x96Dt\xaa\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x00\x00\x00\x00\x03\x00\x00\x00\x01\x06\xb6\x01\xc0F \xb1\xa15\xd5*\x95\x1e\x01\x00\xe2\xc6L\xca\xd8\xd9\x92XM\x03Q\xb9\xda{}N\xe2\xf1\xca\xd1&\xa8\x04\xac q\x1f\xb6a\x95\x93\xfb\xc9\x82\xdf\x18\x9f\xd6P\xd2\x1bb\xbc\xf7#\xd3\xdd\xbdy7\xe4\t\xaej\x9b\xea\x04\xbaR\x9c\x01\xc0j \x8d\x14\xa0!lo\xaf\x02(\xba\xba\x88\x96\xfd-k\x8a\xea\x06\x80\xcf\xe7\x16\xe5\xd0L\x9e1Q\x82\xefl\xac \x93L3\xca\x11c(=\xc5\xed\x8aRl\xfez\xd3\x9e\xea\xce)\x0c\x8c\xe2\xffy\x03`[\xea\x7f?.\xba \xb7O\xab\x0f\xe3{\x8b\xac\x8a7$\x9cH\xf6x\xd9f\xbe\x8a\x97\xc6~\x17\x91\x97j\x0f\x00\x0f"\xd52\xbaR\x9dV\xb2\x00\x00\x01\x05 \x05/\x9b\x92\xfe\x84)\xe3L\x1c\x11\x07\x7f`!\x8c.\n\xaa\x84\xe3\xf2\xec|\xe26\x0e\xb4\x9b\xe550!\x07\x05/\x9b\x92\xfe\x84)\xe3L\x1c\x11\x07\x7f`!\x8c.\n\xaa\x84\xe3\xf2\xec|\xe26\x0e\xb4\x9b\xe550\r\x00|F\x1e]\x01\x00\x00\x00\x01\x00\x00\x00!\x07i\x94\x0c\x81\xcd\xb2\x17\xab\x86A\xc8\xbb!\x9fL\xad\xc9\r\xf1J\xa5\xc1l11\xac\xb7\x9f|\x11\xb4\xf6=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x03\x00\x00\x00\x01\x00\x00\x00!\x07|n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP=\x01\x08\xbeb^\x87gy\x83fF\xa6T\xed\x08\xca|C\x11\x9b\x03EP\x98\x14\xa0O\xde\x066\x7f\xfb\x08\x02\xe8\xbf\xf20\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\x9b\x105\xbc\xba\x1b\x96o\xff6\xa2\xc1\xb1R7\xbc\x99Q\xb9\x91Zr\xbd\xf4%/\xae_\x9a\x08\xb5\xff=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2\x8c\xb3k80\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00!\x07\xe6r\x85\xe7\\\x8a\xe5tB\x90\xef\xdf-C\x14\x8a\x8a\xd3{\xda[!\xf3\x89\xf1X;\xa6\xe6(\x96\xee=\x01\xd6\xa0\xf1\xa1\x89\xe3\x84\t\xbe\xcaV\xd7\x97g/e\xb3\x7f\x99{\x8b)\x9axZ\xeb\x06\x9e\x13\xdft\xe2s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x03\x00\x00\x00\x01\x00\x00\x00!\x07\xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d=\x01\x08\xbeb^\x87gy\x83fF\xa6T\xed\x08\xca|C\x11\x9b\x03EP\x98\x14\xa0O\xde\x066\x7f\xfb\x08s\xc5\xda\n0\x00\x00\x80\x01\x00\x00\x80\x00\x00\x00\x80\x02\x00\x00\x80\x01\x00\x00\x00\x01\x00\x00\x00\x01\x06\xb6\x01\xc0F \xf6l0\xa0}\xbc\xfda\xe7\xc5\xb6\xfa\xcfNl\'\xf9G\xba\xfa\xcb\xb3\xfc\x0e\xa2\x81\xe0\x16~n\x94\x8d\xac |n:1\xc3+\xcb\x9e\xa2\x05ds")l[\xa3i6?\x13n\xf8\xeeZ\xcb!\xc8\xf9\xd5\x1eP\xbaR\x9c\x01\xc0j \xe6r\x85\xe7\\\x8a\xe5tB\x90\xef\xdf-C\x14\x8a\x8a\xd3{\xda[!\xf3\x89\xf1X;\xa6\xe6(\x96\xee\xac i\x94\x0c\x81\xcd\xb2\x17\xab\x86A\xc8\xbb!\x9fL\xad\xc9\r\xf1J\xa5\xc1l11\xac\xb7\x9f|\x11\xb4\xf6\xba \x9b\x105\xbc\xba\x1b\x96o\xff6\xa2\xc1\xb1R7\xbc\x99Q\xb9\x91Zr\xbd\xf4%/\xae_\x9a\x08\xb5\xff\xbaR\x9dV\xb2\x00'
    SIGNED_EXP_TR_MINIS_PSBT_B64_SD = "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"

    return namedtuple(
        "TestData",
        [
            "TEST_MNEMONIC",
            "TEST_MNEMONIC_BIP85_I0",
            "P2PKH_PSBT",
            "P2PKH_PSBT_B43",
            "P2PKH_PSBT_B58",
            "P2PKH_PSBT_B64",
            "P2PKH_PSBT_UR_PSBT",
            "SIGNED_P2PKH_PSBT",
            "SIGNED_P2PKH_PSBT_B43",
            "SIGNED_P2PKH_PSBT_B58",
            "SIGNED_P2PKH_PSBT_B64",
            "SIGNED_P2PKH_PSBT_UR_PSBT",
            "SIGNED_P2PKH_PSBT_SD",
            "SIGNED_P2PKH_PSBT_B64_SD",
            "P2WPKH_PSBT",
            "P2WPKH_PSBT_B43",
            "P2WPKH_PSBT_B58",
            "P2WPKH_PSBT_B64",
            "P2WPKH_PSBT_UR_PSBT",
            "P2WPKH_PSBT_BBQR_PSBT",
            "SIGNED_P2WPKH_PSBT",
            "SIGNED_P2WPKH_PSBT_B43",
            "SIGNED_P2WPKH_PSBT_B58",
            "SIGNED_P2WPKH_PSBT_B64",
            "SIGNED_P2WPKH_PSBT_UR_PSBT",
            "SIGNED_P2WPKH_PSBT_BBQR_PSBT",
            "SIGNED_P2WPKH_PSBT_SD",
            "SIGNED_P2WPKH_PSBT_B64_SD",
            "P2SH_P2WPKH_PSBT",
            "P2SH_P2WPKH_PSBT_B43",
            "P2SH_P2WPKH_PSBT_B58",
            "P2SH_P2WPKH_PSBT_B64",
            "P2SH_P2WPKH_PSBT_UR_PSBT",
            "SIGNED_P2SH_P2WPKH_PSBT",
            "SIGNED_P2SH_P2WPKH_PSBT_B43",
            "SIGNED_P2SH_P2WPKH_PSBT_B58",
            "SIGNED_P2SH_P2WPKH_PSBT_B64",
            "SIGNED_P2SH_P2WPKH_PSBT_UR_PSBT",
            "SIGNED_P2SH_P2WPKH_PSBT_SD",
            "SIGNED_P2SH_P2WPKH_PSBT_B64_SD",
            "P2TR_PSBT",
            "P2TR_PSBT_B43",
            "P2TR_PSBT_B58",
            "P2TR_PSBT_B64",
            "P2TR_PSBT_UR_PSBT",
            "SIGNED_P2TR_PSBT",
            "SIGNED_P2TR_PSBT_B43",
            "SIGNED_P2TR_PSBT_B58",
            "SIGNED_P2TR_PSBT_B64",
            "SIGNED_P2TR_PSBT_UR_PSBT",
            "SIGNED_P2TR_PSBT_SD",
            "SIGNED_P2TR_PSBT_B64_SD",
            "P2WSH_PSBT",
            "P2WSH_PSBT_B43",
            "P2WSH_PSBT_B58",
            "P2WSH_PSBT_B64",
            "P2WSH_PSBT_UR_PSBT",
            "SIGNED_P2WSH_PSBT",
            "SIGNED_P2WSH_PSBT_B43",
            "SIGNED_P2WSH_PSBT_B58",
            "SIGNED_P2WSH_PSBT_B64",
            "SIGNED_P2WSH_PSBT_UR_PSBT",
            "SIGNED_P2WSH_PSBT_SD",
            "DESC_P2WSH_PSBT",
            "DESC_P2WSH_PSBT_B43",
            "DESC_P2WSH_PSBT_B58",
            "DESC_P2WSH_PSBT_B64",
            "DESC_P2WSH_PSBT_UR_PSBT",
            "DESC_SIGNED_P2WSH_PSBT",
            "DESC_SIGNED_P2WSH_PSBT_B43",
            "DESC_SIGNED_P2WSH_PSBT_B58",
            "DESC_SIGNED_P2WSH_PSBT_B64",
            "DESC_SIGNED_P2WSH_PSBT_UR_PSBT",
            "P2SH_P2WSH_PSBT",
            "P2SH_P2WSH_PSBT_B43",
            "P2SH_P2WSH_PSBT_B58",
            "P2SH_P2WSH_PSBT_B64",
            "P2SH_P2WSH_PSBT_UR_PSBT",
            "SIGNED_P2SH_P2WSH_PSBT",
            "SIGNED_P2SH_P2WSH_PSBT_B43",
            "SIGNED_P2SH_P2WSH_PSBT_B58",
            "SIGNED_P2SH_P2WSH_PSBT_B64",
            "SIGNED_P2SH_P2WSH_PSBT_UR_PSBT",
            "SIGNED_P2SH_P2WSH_PSBT_SD",
            "MISSING_GLOBAL_XPUBS_PSBT",
            "MINIS_P2WSH_PSBT",
            "MINIS_P2WSH_PSBT_B43",
            "MINIS_P2WSH_PSBT_B58",
            "MINIS_P2WSH_PSBT_B64",
            "MINIS_P2WSH_PSBT_UR_PSBT",
            "SIGNED_MINIS_P2WSH_PSBT",
            "SIGNED_MINIS_P2WSH_PSBT_B43",
            "SIGNED_MINIS_P2WSH_PSBT_B58",
            "SIGNED_MINIS_P2WSH_PSBT_B64",
            "SIGNED_MINIS_P2WSH_PSBT_UR_PSBT",
            "SIGNED_MINIS_P2WSH_PSBT_SD",
            "SIGNED_MINIS_P2WSH_PSBT_B64_SD",
            "MINIS_TR_PSBT",
            "MINIS_TR_PSBT_B43",
            "MINIS_TR_PSBT_B58",
            "MINIS_TR_PSBT_B64",
            "MINIS_TR_PSBT_UR_PSBT",
            "IN_KEY_SIGNED_MINIS_TR_PSBT",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_B43",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_B58",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_B64",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_UR_PSBT",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_SD",
            "IN_KEY_SIGNED_MINIS_TR_PSBT_B64_SD",
            "RECOV_M_TR_PSBT",
            "RECOV_M_TR_PSBT_B43",
            "RECOV_M_TR_PSBT_B58",
            "RECOV_M_TR_PSBT_B64",
            "RECOV_M_TR_PSBT_UR_PSBT",
            "TAP_TREE_SIGNED_RECOV_PSBT",
            "TAP_TREE_SIGNED_RECOV_PSBT_B43",
            "TAP_TREE_SIGNED_RECOV_PSBT_B58",
            "TAP_TREE_SIGNED_RECOV_PSBT_B64",
            "TAP_TREE_SIGNED_RECOV_PSBT_UR_PSBT",
            "TAP_TREE_SIGNED_RECOV_PSBT_SD",
            "TAP_TREE_SIGNED_RECOV_PSBT_B64_SD",
            "EXP_TR_MINIS_PSBT",
            "EXP_TR_MINIS_PSBT_B43",
            "EXP_TR_MINIS_PSBT_B58",
            "EXP_TR_MINIS_PSBT_B64",
            "EXP_TR_MINIS_PSBT_UR_PSBT",
            "SIGNED_EXP_TR_MINIS_PSBT",
            "SIGNED_EXP_TR_MINIS_PSBT_B43",
            "SIGNED_EXP_TR_MINIS_PSBT_B58",
            "SIGNED_EXP_TR_MINIS_PSBT_B64",
            "SIGNED_EXP_TR_MINIS_PSBT_UR_PSBT",
            "SIGNED_EXP_TR_MINIS_PSBT_SD",
            "SIGNED_EXP_TR_MINIS_PSBT_B64_SD",
        ],
    )(
        TEST_MNEMONIC,
        TEST_MNEMONIC_BIP85_I0,
        P2PKH_PSBT,
        P2PKH_PSBT_B43,
        P2PKH_PSBT_B58,
        P2PKH_PSBT_B64,
        P2PKH_PSBT_UR_PSBT,
        SIGNED_P2PKH_PSBT,
        SIGNED_P2PKH_PSBT_B43,
        SIGNED_P2PKH_PSBT_B58,
        SIGNED_P2PKH_PSBT_B64,
        SIGNED_P2PKH_PSBT_UR_PSBT,
        SIGNED_P2PKH_PSBT_SD,
        SIGNED_P2PKH_PSBT_B64_SD,
        P2WPKH_PSBT,
        P2WPKH_PSBT_B43,
        P2WPKH_PSBT_B58,
        P2WPKH_PSBT_B64,
        P2WPKH_PSBT_UR_PSBT,
        P2WPKH_PSBT_BBQR_PSBT,
        SIGNED_P2WPKH_PSBT,
        SIGNED_P2WPKH_PSBT_B43,
        SIGNED_P2WPKH_PSBT_B58,
        SIGNED_P2WPKH_PSBT_B64,
        SIGNED_P2WPKH_PSBT_UR_PSBT,
        SIGNED_P2WPKH_PSBT_BBQR_PSBT,
        SIGNED_P2WPKH_PSBT_SD,
        SIGNED_P2WPKH_PSBT_B64_SD,
        P2SH_P2WPKH_PSBT,
        P2SH_P2WPKH_PSBT_B43,
        P2SH_P2WPKH_PSBT_B58,
        P2SH_P2WPKH_PSBT_B64,
        P2SH_P2WPKH_PSBT_UR_PSBT,
        SIGNED_P2SH_P2WPKH_PSBT,
        SIGNED_P2SH_P2WPKH_PSBT_B43,
        SIGNED_P2SH_P2WPKH_PSBT_B58,
        SIGNED_P2SH_P2WPKH_PSBT_B64,
        SIGNED_P2SH_P2WPKH_PSBT_UR_PSBT,
        SIGNED_P2SH_P2WPKH_PSBT_SD,
        SIGNED_P2SH_P2WPKH_PSBT_B64_SD,
        P2TR_PSBT,
        P2TR_PSBT_B43,
        P2TR_PSBT_B58,
        P2TR_PSBT_B64,
        P2TR_PSBT_UR_PSBT,
        SIGNED_P2TR_PSBT,
        SIGNED_P2TR_PSBT_B43,
        SIGNED_P2TR_PSBT_B58,
        SIGNED_P2TR_PSBT_B64,
        SIGNED_P2TR_PSBT_UR_PSBT,
        SIGNED_P2TR_PSBT_SD,
        SIGNED_P2TR_PSBT_B64_SD,
        P2WSH_PSBT,
        P2WSH_PSBT_B43,
        P2WSH_PSBT_B58,
        P2WSH_PSBT_B64,
        P2WSH_PSBT_UR_PSBT,
        SIGNED_P2WSH_PSBT,
        SIGNED_P2WSH_PSBT_B43,
        SIGNED_P2WSH_PSBT_B58,
        SIGNED_P2WSH_PSBT_B64,
        SIGNED_P2WSH_PSBT_UR_PSBT,
        SIGNED_P2WSH_PSBT_SD,
        DESC_P2WSH_PSBT,
        DESC_P2WSH_PSBT_B43,
        DESC_P2WSH_PSBT_B58,
        DESC_P2WSH_PSBT_B64,
        DESC_P2WSH_PSBT_UR_PSBT,
        DESC_SIGNED_P2WSH_PSBT,
        DESC_SIGNED_P2WSH_PSBT_B43,
        DESC_SIGNED_P2WSH_PSBT_B58,
        DESC_SIGNED_P2WSH_PSBT_B64,
        DESC_SIGNED_P2WSH_PSBT_UR_PSBT,
        P2SH_P2WSH_PSBT,
        P2SH_P2WSH_PSBT_B43,
        P2SH_P2WSH_PSBT_B58,
        P2SH_P2WSH_PSBT_B64,
        P2SH_P2WSH_PSBT_UR_PSBT,
        SIGNED_P2SH_P2WSH_PSBT,
        SIGNED_P2SH_P2WSH_PSBT_B43,
        SIGNED_P2SH_P2WSH_PSBT_B58,
        SIGNED_P2SH_P2WSH_PSBT_B64,
        SIGNED_P2SH_P2WSH_PSBT_UR_PSBT,
        SIGNED_P2SH_P2WSH_PSBT_SD,
        MISSING_GLOBAL_XPUBS_PSBT,
        MINIS_P2WSH_PSBT,
        MINIS_P2WSH_PSBT_B43,
        MINIS_P2WSH_PSBT_B58,
        MINIS_P2WSH_PSBT_B64,
        MINIS_P2WSH_PSBT_UR_PSBT,
        SIGNED_MINIS_P2WSH_PSBT,
        SIGNED_MINIS_P2WSH_PSBT_B43,
        SIGNED_MINIS_P2WSH_PSBT_B58,
        SIGNED_MINIS_P2WSH_PSBT_B64,
        SIGNED_MINIS_P2WSH_PSBT_UR_PSBT,
        SIGNED_MINIS_P2WSH_PSBT_SD,
        SIGNED_MINIS_P2WSH_PSBT_B64_SD,
        MINIS_TR_PSBT,
        MINIS_TR_PSBT_B43,
        MINIS_TR_PSBT_B58,
        MINIS_TR_PSBT_B64,
        MINIS_TR_PSBT_UR_PSBT,
        IN_KEY_SIGNED_MINIS_TR_PSBT,
        IN_KEY_SIGNED_MINIS_TR_PSBT_B43,
        IN_KEY_SIGNED_MINIS_TR_PSBT_B58,
        IN_KEY_SIGNED_MINIS_TR_PSBT_B64,
        IN_KEY_SIGNED_MINIS_TR_PSBT_UR_PSBT,
        IN_KEY_SIGNED_MINIS_TR_PSBT_SD,
        IN_KEY_SIGNED_MINIS_TR_PSBT_B64_SD,
        RECOV_M_TR_PSBT,
        RECOV_M_TR_PSBT_B43,
        RECOV_M_TR_PSBT_B58,
        RECOV_M_TR_PSBT_B64,
        RECOV_M_TR_PSBT_UR_PSBT,
        TAP_TREE_SIGNED_RECOV_PSBT,
        TAP_TREE_SIGNED_RECOV_PSBT_B43,
        TAP_TREE_SIGNED_RECOV_PSBT_B58,
        TAP_TREE_SIGNED_RECOV_PSBT_B64,
        TAP_TREE_SIGNED_RECOV_PSBT_UR_PSBT,
        TAP_TREE_SIGNED_RECOV_PSBT_SD,
        TAP_TREE_SIGNED_RECOV_PSBT_B64_SD,
        EXP_TR_MINIS_PSBT,
        EXP_TR_MINIS_PSBT_B43,
        EXP_TR_MINIS_PSBT_B58,
        EXP_TR_MINIS_PSBT_B64,
        EXP_TR_MINIS_PSBT_UR_PSBT,
        SIGNED_EXP_TR_MINIS_PSBT,
        SIGNED_EXP_TR_MINIS_PSBT_B43,
        SIGNED_EXP_TR_MINIS_PSBT_B58,
        SIGNED_EXP_TR_MINIS_PSBT_B64,
        SIGNED_EXP_TR_MINIS_PSBT_UR_PSBT,
        SIGNED_EXP_TR_MINIS_PSBT_SD,
        SIGNED_EXP_TR_MINIS_PSBT_B64_SD,
    )


def test_init_singlesig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR, FORMAT_BBQR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    cases = [
        (tdata.P2PKH_PSBT, FORMAT_NONE),
        (tdata.P2PKH_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2PKH_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2PKH_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2PKH_PSBT_UR_PSBT, FORMAT_UR),
        (tdata.P2WPKH_PSBT, FORMAT_NONE),
        (tdata.P2WPKH_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2WPKH_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2WPKH_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2WPKH_PSBT_UR_PSBT, FORMAT_UR),
        (tdata.P2WPKH_PSBT_BBQR_PSBT, FORMAT_BBQR),
        (tdata.P2SH_P2WPKH_PSBT, FORMAT_NONE),
        (tdata.P2SH_P2WPKH_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2SH_P2WPKH_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2SH_P2WPKH_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2SH_P2WPKH_PSBT_UR_PSBT, FORMAT_UR),
        (tdata.P2TR_PSBT, FORMAT_NONE),
        (tdata.P2TR_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2TR_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2TR_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2TR_PSBT_UR_PSBT, FORMAT_UR),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        assert isinstance(signer, PSBTSigner)


def test_init_singlesig_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    cases = [
        (tdata.P2PKH_PSBT, FORMAT_NONE),
        (tdata.P2WPKH_PSBT, FORMAT_NONE),
        (tdata.P2SH_P2WPKH_PSBT, FORMAT_NONE),
        (tdata.P2TR_PSBT, FORMAT_NONE),
    ]

    for case in cases:
        mocker.patch("builtins.open", mock_open(MockFile(case[0])))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        assert isinstance(signer, PSBTSigner)


def test_init_empty_file_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    mocker.patch("builtins.open", mock_open(MockFile()))
    with pytest.raises(ValueError):
        PSBTSigner(wallet, None, FORMAT_NONE, "dummy.psbt")


def test_init_multisig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    cases = [
        (tdata.P2WSH_PSBT, FORMAT_NONE),
        (tdata.P2WSH_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2WSH_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2WSH_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2WSH_PSBT_UR_PSBT, FORMAT_UR),
        (tdata.P2SH_P2WSH_PSBT, FORMAT_NONE),
        (tdata.P2SH_P2WSH_PSBT_B43, FORMAT_PMOFN),
        (tdata.P2SH_P2WSH_PSBT_B58, FORMAT_PMOFN),
        (tdata.P2SH_P2WSH_PSBT_B64, FORMAT_PMOFN),
        (tdata.P2SH_P2WSH_PSBT_UR_PSBT, FORMAT_UR),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        assert isinstance(signer, PSBTSigner)


def test_init_multisig_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    cases = [
        (tdata.P2WSH_PSBT, FORMAT_NONE),
        (tdata.P2SH_P2WSH_PSBT, FORMAT_NONE),
    ]

    for case in cases:
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", return_value=mock_file)
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        assert isinstance(signer, PSBTSigner)


def test_init_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"]))
    cases = [
        (tdata.MINIS_P2WSH_PSBT, FORMAT_NONE),
        (tdata.MINIS_P2WSH_PSBT_B43, FORMAT_PMOFN),
        (tdata.MINIS_P2WSH_PSBT_B58, FORMAT_PMOFN),
        (tdata.MINIS_P2WSH_PSBT_B64, FORMAT_PMOFN),
        (tdata.MINIS_P2WSH_PSBT_UR_PSBT, FORMAT_UR),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        assert isinstance(signer, PSBTSigner)


def test_init_miniscript_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"]))
    cases = [
        (tdata.MINIS_P2WSH_PSBT, FORMAT_NONE),
    ]

    for case in cases:
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", return_value=mock_file)
        signer = PSBTSigner(wallet, None, FORMAT_NONE, "dummy.psbt")
        assert isinstance(signer, PSBTSigner)


def test_init_tr_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE),
        (tdata.MINIS_TR_PSBT_B43, FORMAT_PMOFN),
        (tdata.MINIS_TR_PSBT_B58, FORMAT_PMOFN),
        (tdata.MINIS_TR_PSBT_B64, FORMAT_PMOFN),
        (tdata.MINIS_TR_PSBT_UR_PSBT, FORMAT_UR),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        assert isinstance(signer, PSBTSigner)


def test_init_tr_miniscript_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE),
    ]

    for case in cases:
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", return_value=mock_file)
        signer = PSBTSigner(wallet, None, FORMAT_NONE, "dummy.psbt")
        assert isinstance(signer, PSBTSigner)


def test_init_fails_on_invalid_psbt(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from ur.ur import UR
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))

    cases = [
        ("thisisnotavalidpsbt", FORMAT_NONE),
        (UR("unknown-type", bytearray("thisisnotavalidpsbt".encode())), FORMAT_UR),
    ]
    for case in cases:
        with pytest.raises(ValueError):
            PSBTSigner(wallet, case[0], case[1])


def test_init_fails_on_invalid_psbt_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from ur.ur import UR
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))

    mock_file = MockFile("thisisnotavalidpsbt")
    mocker.patch("builtins.open", return_value=mock_file)
    with pytest.raises(ValueError):
        PSBTSigner(wallet, None, FORMAT_NONE, "dummy.psbt")


def test_init_singlesig_fails_not_singlesig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        tdata.P2WSH_PSBT,
        tdata.MINIS_P2WSH_PSBT,
        tdata.MINIS_TR_PSBT,
    ]

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    for case in cases:
        with pytest.raises(ValueError, match="Invalid PSBT: Not a single-sig PSBT"):
            PSBTSigner(wallet, case, FORMAT_NONE)


def test_init_multisig_fails_not_multisig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        tdata.P2PKH_PSBT,
        tdata.MINIS_P2WSH_PSBT,
        tdata.MINIS_TR_PSBT,
    ]

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    for case in cases:
        with pytest.raises(ValueError, match="Invalid PSBT: Not a multisig PSBT"):
            PSBTSigner(wallet, case, FORMAT_NONE)


def test_init_wsh_miniscript_fails_not_wsh_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        tdata.P2PKH_PSBT,
        tdata.P2WSH_PSBT,
        tdata.MINIS_TR_PSBT,
    ]

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"]))
    wallet.load(WSH_MINISCRIPT, FORMAT_NONE)
    for i, case in enumerate(cases):
        error = (
            "Invalid PSBT: Not a miniscript PSBT"
            if i < 2
            # Case 2: Taproot miniscript PSBT vs wsh wallet discrepancy
            # A tr miniscript PSBT vs wsh miniscript wallet discrepancy
            # will only get caught if a descriptor is loaded
            else "Invalid PSBT: policy mismatch"
        )
        with pytest.raises(ValueError, match=error):
            PSBTSigner(wallet, case, FORMAT_NONE)


def test_init_tr_miniscript_fails_not_tr_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        tdata.P2PKH_PSBT,
        tdata.P2WSH_PSBT,
        tdata.MINIS_P2WSH_PSBT,
    ]

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    wallet.load(TR_MINISCRIPT, FORMAT_NONE)
    for i, case in enumerate(cases):
        error = (
            "Invalid PSBT: Not a miniscript PSBT"
            if i < 2
            # Case 2: wsh miniscript PSBT vs tr wallet discrepancy
            # A wsh miniscript PSBT vs tr miniscript wallet discrepancy
            # will only get caught if a descriptor is loaded
            else "Invalid PSBT: policy mismatch"
        )
        with pytest.raises(ValueError, match=error):
            PSBTSigner(wallet, case, FORMAT_NONE)


def test_sign_singlesig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR, FORMAT_BBQR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    cases = [
        (tdata.P2PKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2PKH_PSBT),
        (tdata.P2PKH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2PKH_PSBT_B43),
        (tdata.P2PKH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2PKH_PSBT_B58),
        (tdata.P2PKH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2PKH_PSBT_B64),
        (tdata.P2PKH_PSBT_UR_PSBT, FORMAT_UR, tdata.SIGNED_P2PKH_PSBT_UR_PSBT),
        (tdata.P2WPKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2WPKH_PSBT),
        (tdata.P2WPKH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2WPKH_PSBT_B43),
        (tdata.P2WPKH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2WPKH_PSBT_B58),
        (tdata.P2WPKH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2WPKH_PSBT_B64),
        (tdata.P2WPKH_PSBT_UR_PSBT, FORMAT_UR, tdata.SIGNED_P2WPKH_PSBT_UR_PSBT),
        (tdata.P2WPKH_PSBT_BBQR_PSBT, FORMAT_BBQR, tdata.SIGNED_P2WPKH_PSBT_BBQR_PSBT),
        (tdata.P2SH_P2WPKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2SH_P2WPKH_PSBT),
        (tdata.P2SH_P2WPKH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WPKH_PSBT_B43),
        (tdata.P2SH_P2WPKH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WPKH_PSBT_B58),
        (tdata.P2SH_P2WPKH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WPKH_PSBT_B64),
        (
            tdata.P2SH_P2WPKH_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.SIGNED_P2SH_P2WPKH_PSBT_UR_PSBT,
        ),
        (tdata.P2TR_PSBT, FORMAT_NONE, tdata.SIGNED_P2TR_PSBT),
        (tdata.P2TR_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2TR_PSBT_B43),
        (tdata.P2TR_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2TR_PSBT_B58),
        (tdata.P2TR_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2TR_PSBT_B64),
        (tdata.P2TR_PSBT_UR_PSBT, FORMAT_UR, tdata.SIGNED_P2TR_PSBT_UR_PSBT),
        (tdata.P2WPKH_PSBT, FORMAT_PMOFN, tdata.SIGNED_P2WPKH_PSBT_B64),
        (tdata.P2SH_P2WPKH_PSBT, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WPKH_PSBT_B64),
    ]

    num = 0
    for case in cases:
        print("test_sign_singlesig case: ", num)
        num += 1
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        if case[1] == FORMAT_BBQR:
            psbt_qr = signer.psbt_qr()
            assert psbt_qr[0].payload == case[2].payload
            assert psbt_qr[1] == case[1]
        else:
            assert signer.psbt_qr() == (case[2], case[1])


def test_sign_singlesig_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    cases = [
        (tdata.P2PKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2PKH_PSBT_SD),
        (tdata.P2PKH_PSBT_B64, FORMAT_NONE, tdata.SIGNED_P2PKH_PSBT_B64_SD),
        (tdata.P2WPKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2WPKH_PSBT_SD),
        (tdata.P2WPKH_PSBT_B64, FORMAT_NONE, tdata.SIGNED_P2WPKH_PSBT_B64_SD),
        (tdata.P2SH_P2WPKH_PSBT, FORMAT_NONE, tdata.SIGNED_P2SH_P2WPKH_PSBT_SD),
        (tdata.P2SH_P2WPKH_PSBT_B64, FORMAT_NONE, tdata.SIGNED_P2SH_P2WPKH_PSBT_B64_SD),
        (tdata.P2TR_PSBT, FORMAT_NONE, tdata.SIGNED_P2TR_PSBT_SD),
        (tdata.P2TR_PSBT_B64, FORMAT_NONE, tdata.SIGNED_P2TR_PSBT_B64_SD),
    ]

    num = 0
    for case in cases:
        print("test_sign_singlesig_from_sdcard case: ", num)
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", mock_open(mock_file))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        if num % 2 == 1:
            # If test case num is odd, check if detected as base64
            assert signer.is_b64_file
            signed_psbt, _ = signer.psbt_qr()
            with open("/sd/" + "dummy-signed.psbt", "w") as f:
                f.write(signed_psbt)
        else:
            with open("/sd/" + "dummy-signed.psbt", "wb") as f:
                signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]
        num += 1


def test_sign_multisig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    cases = [
        (tdata.P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_P2WSH_PSBT),
        (tdata.P2WSH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2WSH_PSBT_B43),
        (tdata.P2WSH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2WSH_PSBT_B58),
        (tdata.P2WSH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2WSH_PSBT_B64),
        (tdata.P2WSH_PSBT_UR_PSBT, FORMAT_UR, tdata.SIGNED_P2WSH_PSBT_UR_PSBT),
        (tdata.P2SH_P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_P2SH_P2WSH_PSBT),
        (tdata.P2SH_P2WSH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WSH_PSBT_B43),
        (tdata.P2SH_P2WSH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WSH_PSBT_B58),
        (tdata.P2SH_P2WSH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WSH_PSBT_B64),
        (
            tdata.P2SH_P2WSH_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.SIGNED_P2SH_P2WSH_PSBT_UR_PSBT,
        ),
        (tdata.P2WSH_PSBT, FORMAT_PMOFN, tdata.SIGNED_P2WSH_PSBT_B64),
        (tdata.P2SH_P2WSH_PSBT, FORMAT_PMOFN, tdata.SIGNED_P2SH_P2WSH_PSBT_B64),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_multisig_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    cases = [
        (tdata.P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_P2WSH_PSBT_SD),
        (tdata.P2SH_P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_P2SH_P2WSH_PSBT_SD),
    ]

    for case in cases:
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", return_value=mock_file)
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        with open("dummy-signed.psbt", "wb") as f:
            signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]


def test_sign_multisig_with_descriptor(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    cases = [
        (tdata.DESC_P2WSH_PSBT, FORMAT_NONE, tdata.DESC_SIGNED_P2WSH_PSBT),
        (tdata.DESC_P2WSH_PSBT_B43, FORMAT_PMOFN, tdata.DESC_SIGNED_P2WSH_PSBT_B43),
        (tdata.DESC_P2WSH_PSBT_B58, FORMAT_PMOFN, tdata.DESC_SIGNED_P2WSH_PSBT_B58),
        (tdata.DESC_P2WSH_PSBT_B64, FORMAT_PMOFN, tdata.DESC_SIGNED_P2WSH_PSBT_B64),
        (
            tdata.DESC_P2WSH_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.DESC_SIGNED_P2WSH_PSBT_UR_PSBT,
        ),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])

    # Repeat signatures with descriptor loaded and more checks
    wallet.load(WSH_MULTISIG, FORMAT_NONE)
    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"]))
    cases = [
        (tdata.MINIS_P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_MINIS_P2WSH_PSBT),
        (tdata.MINIS_P2WSH_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_MINIS_P2WSH_PSBT_B43),
        (tdata.MINIS_P2WSH_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_MINIS_P2WSH_PSBT_B58),
        (tdata.MINIS_P2WSH_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_MINIS_P2WSH_PSBT_B64),
        (
            tdata.MINIS_P2WSH_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.SIGNED_MINIS_P2WSH_PSBT_UR_PSBT,
        ),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])

    # Repeat signatures with descriptor loaded and more checks
    wallet.load(WSH_MINISCRIPT, FORMAT_NONE)
    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_miniscript_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"]))
    cases = [
        (tdata.MINIS_P2WSH_PSBT, FORMAT_NONE, tdata.SIGNED_MINIS_P2WSH_PSBT_SD),
        (tdata.MINIS_P2WSH_PSBT_B64, FORMAT_NONE, tdata.SIGNED_MINIS_P2WSH_PSBT_B64_SD),
    ]

    for i, case in enumerate(cases):
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", mock_open(mock_file))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        if i == 1:
            assert signer.is_b64_file
            signed_psbt, _ = signer.psbt_qr()
            with open("/sd/" + "dummy-signed.psbt", "w") as f:
                f.write(signed_psbt)
        else:
            with open("/sd/" + "dummy-signed.psbt", "wb") as f:
                signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]


def test_sign_tr_miniscript_internal_key(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE, tdata.IN_KEY_SIGNED_MINIS_TR_PSBT),
        (tdata.MINIS_TR_PSBT_B43, FORMAT_PMOFN, tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_B43),
        (tdata.MINIS_TR_PSBT_B58, FORMAT_PMOFN, tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_B58),
        (tdata.MINIS_TR_PSBT_B64, FORMAT_PMOFN, tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_B64),
        (
            tdata.MINIS_TR_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_UR_PSBT,
        ),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])

    # Repeat signatures with descriptor loaded and more checks
    wallet.load(TR_MINISCRIPT, FORMAT_NONE)
    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_tr_miniscript_internal_key_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE, tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_SD),
        (
            tdata.MINIS_TR_PSBT_B64,
            FORMAT_NONE,
            tdata.IN_KEY_SIGNED_MINIS_TR_PSBT_B64_SD,
        ),
    ]

    for i, case in enumerate(cases):
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", mock_open(mock_file))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        if i == 1:
            assert signer.is_b64_file
            signed_psbt, _ = signer.psbt_qr()
            with open("/sd/" + "dummy-signed.psbt", "w") as f:
                f.write(signed_psbt)
        else:
            with open("/sd/" + "dummy-signed.psbt", "wb") as f:
                signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]


def test_sign_tr_miniscript_tap_tree(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(
        Key(
            tdata.TEST_MNEMONIC_BIP85_I0,
            TYPE_MINISCRIPT,
            NETWORKS["test"],
            script_type=P2TR,
        )
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE, tdata.TAP_TREE_SIGNED_RECOV_PSBT),
        (tdata.MINIS_TR_PSBT_B43, FORMAT_PMOFN, tdata.TAP_TREE_SIGNED_RECOV_PSBT_B43),
        (tdata.MINIS_TR_PSBT_B58, FORMAT_PMOFN, tdata.TAP_TREE_SIGNED_RECOV_PSBT_B58),
        (tdata.MINIS_TR_PSBT_B64, FORMAT_PMOFN, tdata.TAP_TREE_SIGNED_RECOV_PSBT_B64),
        (
            tdata.MINIS_TR_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.TAP_TREE_SIGNED_RECOV_PSBT_UR_PSBT,
        ),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])

    # Repeat signatures with descriptor loaded and more checks
    wallet.load(TR_MINISCRIPT, FORMAT_NONE)
    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_tr_miniscript_tap_tree_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(
        Key(
            tdata.TEST_MNEMONIC_BIP85_I0,
            TYPE_MINISCRIPT,
            NETWORKS["test"],
            script_type=P2TR,
        )
    )
    cases = [
        (tdata.MINIS_TR_PSBT, FORMAT_NONE, tdata.TAP_TREE_SIGNED_RECOV_PSBT_SD),
        (tdata.MINIS_TR_PSBT_B64, FORMAT_NONE, tdata.TAP_TREE_SIGNED_RECOV_PSBT_B64_SD),
    ]

    for i, case in enumerate(cases):
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", mock_open(mock_file))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        if i == 1:
            assert signer.is_b64_file
            signed_psbt, _ = signer.psbt_qr()
            with open("/sd/" + "dummy-signed.psbt", "w") as f:
                f.write(signed_psbt)
        else:
            with open("/sd/" + "dummy-signed.psbt", "wb") as f:
                signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]


def test_sign_tr_expanding_multisig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE, FORMAT_PMOFN, FORMAT_UR

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.EXP_TR_MINIS_PSBT, FORMAT_NONE, tdata.SIGNED_EXP_TR_MINIS_PSBT),
        (tdata.EXP_TR_MINIS_PSBT_B43, FORMAT_PMOFN, tdata.SIGNED_EXP_TR_MINIS_PSBT_B43),
        (tdata.EXP_TR_MINIS_PSBT_B58, FORMAT_PMOFN, tdata.SIGNED_EXP_TR_MINIS_PSBT_B58),
        (tdata.EXP_TR_MINIS_PSBT_B64, FORMAT_PMOFN, tdata.SIGNED_EXP_TR_MINIS_PSBT_B64),
        (
            tdata.EXP_TR_MINIS_PSBT_UR_PSBT,
            FORMAT_UR,
            tdata.SIGNED_EXP_TR_MINIS_PSBT_UR_PSBT,
        ),
    ]

    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])

    # Repeat signatures with descriptor loaded and more checks
    wallet.load(TR_EXP_MULTI_MINISCRIPT, FORMAT_NONE)
    for case in cases:
        signer = PSBTSigner(wallet, case[0], case[1])
        signer.sign()
        assert signer.psbt_qr() == (case[2], case[1])


def test_sign_tr_expanding_multisig_from_sdcard(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(
        Key(tdata.TEST_MNEMONIC, TYPE_MINISCRIPT, NETWORKS["test"], script_type=P2TR)
    )
    cases = [
        (tdata.EXP_TR_MINIS_PSBT, FORMAT_NONE, tdata.SIGNED_EXP_TR_MINIS_PSBT_SD),
        (
            tdata.EXP_TR_MINIS_PSBT_B64,
            FORMAT_NONE,
            tdata.SIGNED_EXP_TR_MINIS_PSBT_B64_SD,
        ),
    ]

    for i, case in enumerate(cases):
        mock_file = MockFile(case[0])
        mocker.patch("builtins.open", mock_open(mock_file))
        signer = PSBTSigner(wallet, None, case[1], "dummy.psbt")
        signer.sign(trim=False)
        if i == 1:
            assert signer.is_b64_file
            signed_psbt, _ = signer.psbt_qr()
            with open("/sd/" + "dummy-signed.psbt", "w") as f:
                f.write(signed_psbt)
        else:
            with open("/sd/" + "dummy-signed.psbt", "wb") as f:
                signer.psbt.write_to(f)
        assert mock_file.write_data == case[2]


def test_sign_fails_with_0_sigs_added(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    signer = PSBTSigner(wallet, tdata.P2WSH_PSBT, FORMAT_NONE)
    mocker.patch.object(signer.psbt, "sign_with", mocker.MagicMock(return_value=0))

    with pytest.raises(ValueError):
        signer.sign()
    signer.psbt.sign_with.assert_called_with(wallet.key.root)


def test_outputs_singlesig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG, P2PKH, P2WPKH, P2SH_P2WPKH, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        (
            tdata.P2PKH_PSBT,
            [
                "Inputs (3): ₿ 0.00 001 856\n\nSpend (1): ₿ 0.00 001 000\n\nFee: ₿ 0.00 000 856 (85.6%) ~1.8 sat/vB",
                "1. Spend: \n\ntb1q4mx3ahp7laj65gyaqg27w0tsjpwuz6rvaxx3tl\n\n₿ 0.00 001 000",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_SINGLESIG,
                    NETWORKS["test"],
                    script_type=P2PKH,
                )
            ),
        ),
        (
            tdata.P2WPKH_PSBT,
            [
                "Inputs (1): ₿ 1.00 000 000\n\nSpend (1): ₿ 0.10 000 000\n\nSelf-transfer or Change (1): ₿ 0.89 997 180\n\nFee: ₿ 0.00 002 820 (0.1%) ~20.0 sat/vB",
                "1. Spend: \n\ntb1que40al7rsw88ru9z0vr78vqwme4w3ctqj694kx\n\n₿ 0.10 000 000",
                "1. Change: \n\ntb1q9u62588spffmq4dzjxsr5l297znf3z6j5p2688\n\n₿ 0.89 997 180",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_SINGLESIG,
                    NETWORKS["test"],
                    script_type=P2WPKH,
                )
            ),
        ),
        (
            tdata.P2SH_P2WPKH_PSBT,
            [
                "Inputs (1): ₿ 1.00 000 000\n\nSpend (1): ₿ 0.10 000 000\n\nSelf-transfer or Change (1): ₿ 0.89 996 700\n\nFee: ₿ 0.00 003 300 (0.1%) ~20.0 sat/vB",
                "1. Spend: \n\ntb1que40al7rsw88ru9z0vr78vqwme4w3ctqj694kx\n\n₿ 0.10 000 000",
                "1. Change: \n\n2MvdUi5o3f2tnEFh9yGvta6FzptTZtkPJC8\n\n₿ 0.89 996 700",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_SINGLESIG,
                    NETWORKS["test"],
                    script_type=P2SH_P2WPKH,
                )
            ),
        ),
        (
            tdata.P2TR_PSBT,
            [
                "Inputs (1): ₿ 0.00 010 111\n\nSpend (1): ₿ 0.00 001 000\n\nSelf-transfer or Change (2): ₿ 0.00 008 738\n\nFee: ₿ 0.00 000 373 (3.9%) ~2.0 sat/vB",
                "1. Spend: \n\ntb1q4mx3ahp7laj65gyaqg27w0tsjpwuz6rvaxx3tl\n\n₿ 0.00 001 000",
                "1. Self-transfer: \n\ntb1pn5kekm0xpnwd6kg8c8qfvv2fr0w5xnhw42927wem7xwk84f7gzvsvctkhp\n\n₿ 0.00 001 000",
                "1. Change: \n\ntb1pwhn9lzpaukrjwvwe365x7hcgvtcfywwsaxcq7j04jgrfcxzdq23qhzr7wt\n\n₿ 0.00 007 738",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_SINGLESIG,
                    NETWORKS["test"],
                    script_type=P2TR,
                )
            ),
        ),
    ]
    case_num = 0
    for case in cases:
        print("test_outputs_singlesig case: ", case_num)
        signer = PSBTSigner(case[2], case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[1]
        case_num += 1


def test_outputs_multisig(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG, P2WSH, P2SH_P2WSH
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        # 0 - PSBT
        # 1 - Expected outputs without descriptor
        # 2 - Wallet
        # 3 - Descriptor
        # 4 - Expected outputs with descriptor
        (
            tdata.P2WSH_PSBT,
            [
                "Inputs (2): ₿\u20090.20 000 000\n\nSpend (2): ₿\u20090.19 993 880\n\nFee: ₿\u20090.00 006 120 (0.1%) ~20.1 sat/vB",
                "1. Spend: \n\ntb1q4xgr8suxvgenukgf4c7r6qaawxxmy9zelh24q8hg5pfxzn2ekn3qfw808t\n\n₿\u20090.01 000 000",
                "2. Spend: \n\ntb1q35pg2rdt3p0v27dmdh9st43q8vzl29cps6kt3yradnqmg55eahfqfgn83n\n\n₿\u20090.18 993 880",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MULTISIG,
                    NETWORKS["test"],
                    script_type=P2WSH,
                )
            ),
            None,
            None,
        ),
        (
            tdata.P2SH_P2WSH_PSBT,
            [
                "Inputs (1): ₿\u20091.00 000 000\n\nSpend (2): ₿\u20090.99 995 740\n\nFee: ₿\u20090.00 004 260 (0.1%) ~20.0 sat/vB",
                "1. Spend: \n\n2N3vYfcg14Axr4NN33ADUorE2kEGEchFJpC\n\n₿\u20090.89 995 740",
                "2. Spend: \n\ntb1que40al7rsw88ru9z0vr78vqwme4w3ctqj694kx\n\n₿\u20090.10 000 000",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MULTISIG,
                    NETWORKS["test"],
                    script_type=P2SH_P2WSH,
                )
            ),
            None,
            None,
        ),
        (
            tdata.DESC_P2WSH_PSBT,
            [
                "Inputs (1): ₿\u20090.01 000 000\n\nSpend (3): ₿\u20090.00 938 408\n\nFee: ₿\u20090.00 061 592 (6.6%) ~265.5 sat/vB",
                "1. Spend: \n\ntb1qs9q8afpd6nc78r8l7456agajhpde657uzn9uh4\n\n₿\u20090.00 100 000",
                "2. Spend: \n\ntb1q6dac4cdyf9sfuln0kzfgswc96nlh2g98s4uyez5tvm7ymhq9ua0sa0z6h7\n\n₿\u20090.00 200 000",
                "3. Spend: \n\ntb1q0xmw6txz6lp2aakdujwhhrel0m7grfvvn00nzwjda7ps06c3jwnqk7m0ww\n\n₿\u20090.00 638 408",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MULTISIG,
                    NETWORKS["test"],
                    script_type=P2WSH,
                ),
            ),
            WSH_MULTISIG,
            [
                "Inputs (1): ₿\u20090.01 000 000\n\nSpend (1): ₿\u20090.00 100 000\n\nSelf-transfer or Change (2): ₿\u20090.00 838 408\n\nFee: ₿\u20090.00 061 592 (6.6%) ~265.5 sat/vB",
                "1. Spend: \n\ntb1qs9q8afpd6nc78r8l7456agajhpde657uzn9uh4\n\n₿\u20090.00 100 000",
                "1. Self-transfer: \n\ntb1q6dac4cdyf9sfuln0kzfgswc96nlh2g98s4uyez5tvm7ymhq9ua0sa0z6h7\n\n₿\u20090.00 200 000",
                "1. Change: \n\ntb1q0xmw6txz6lp2aakdujwhhrel0m7grfvvn00nzwjda7ps06c3jwnqk7m0ww\n\n₿\u20090.00 638 408",
            ],
        ),
    ]

    for case in cases:
        wallet = case[2]
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[1]
        if case[3] is not None:
            wallet.load(case[3], FORMAT_NONE)
            signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
            outputs, _ = signer.outputs()
            assert outputs == case[4]


def test_outputs_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2WSH
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        # 0 - PSBT
        # 1 - Expected outputs without descriptor
        # 2 - Wallet
        # 3 - Descriptor
        # 4 - Expected outputs with descriptor
        (
            tdata.MINIS_P2WSH_PSBT,
            [
                "Inputs (1): ₿\u20090.01 997 062\n\nSpend (3): ₿\u20090.01 995 019\n\nFee: ₿\u20090.00 002 043 (0.1%)",
                "1. Spend: \n\ntb1q26gnrxhmv79m7sady6xyt2y23rxc6nmt50dfyq\n\n₿\u20090.00 500 000",
                "2. Spend: \n\ntb1qnlhau4cw3f76k583xk8p6ekd02a0dvhmqjzl7aw6ehda8r7upheskzwzea\n\n₿\u20090.01 000 000",
                "3. Spend: \n\ntb1qmanyu7mm2q24esrnawjxukla9pr7s4yyzwjy2chjhsyumfe0r34q5dzsug\n\n₿\u20090.00 495 019",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MINISCRIPT,
                    NETWORKS["test"],
                    script_type=P2WSH,
                )
            ),
            WSH_MINISCRIPT,
            [
                "Inputs (1): ₿\u20090.01 997 062\n\nSpend (1): ₿\u20090.00 500 000\n\nSelf-transfer or Change (2): ₿\u20090.01 495 019\n\nFee: ₿\u20090.00 002 043 (0.1%)",
                "1. Spend: \n\ntb1q26gnrxhmv79m7sady6xyt2y23rxc6nmt50dfyq\n\n₿\u20090.00 500 000",
                "1. Self-transfer: \n\ntb1qnlhau4cw3f76k583xk8p6ekd02a0dvhmqjzl7aw6ehda8r7upheskzwzea\n\n₿\u20090.01 000 000",
                "1. Change: \n\ntb1qmanyu7mm2q24esrnawjxukla9pr7s4yyzwjy2chjhsyumfe0r34q5dzsug\n\n₿\u20090.00 495 019",
            ],
        ),
    ]
    for case in cases:
        wallet = case[2]
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[1]
        wallet.load(case[3], FORMAT_NONE)
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[4]


def test_outputs_tr_miniscript(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        # 0 - PSBT
        # 1 - Expected outputs without descriptor
        # 2 - Wallet
        # 3 - Descriptor
        # 4 - Expected outputs with descriptor
        (
            tdata.MINIS_TR_PSBT,
            [
                "Inputs (1): ₿\u20090.01 995 759\n\nSpend (3): ₿\u20090.01 993 789\n\nFee: ₿\u20090.00 001 970 (0.1%)",
                "1. Spend: \n\ntb1qrtvmveqwrzsndt8tzzkgepp2mw8de95dk7hz70kr95f5dt7axvrsgq8lcp\n\n₿\u20090.01 000 000",
                "2. Spend: \n\ntb1pgzdsuzcewwntpm6c3xrrn5lmdc0cvnpsdyrsz7gvcq5t0kqry2rswl8vnz\n\n₿\u20090.00 500 000",
                "3. Spend: \n\ntb1pt064gyzas6dnqq9p955p7ujus8z7l3xg3apxm425u72dupy3wffqjzkszd\n\n₿\u20090.00 493 789",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MINISCRIPT,
                    NETWORKS["test"],
                    script_type=P2TR,
                )
            ),
            TR_MINISCRIPT,
            [
                "Inputs (1): ₿\u20090.01 995 759\n\nSpend (1): ₿\u20090.01 000 000\n\nSelf-transfer or Change (2): ₿\u20090.00 993 789\n\nFee: ₿\u20090.00 001 970 (0.1%)",
                "1. Spend: \n\ntb1qrtvmveqwrzsndt8tzzkgepp2mw8de95dk7hz70kr95f5dt7axvrsgq8lcp\n\n₿\u20090.01 000 000",
                "1. Self-transfer: \n\ntb1pgzdsuzcewwntpm6c3xrrn5lmdc0cvnpsdyrsz7gvcq5t0kqry2rswl8vnz\n\n₿\u20090.00 500 000",
                "1. Change: \n\ntb1pt064gyzas6dnqq9p955p7ujus8z7l3xg3apxm425u72dupy3wffqjzkszd\n\n₿\u20090.00 493 789",
            ],
        ),
    ]
    for case in cases:
        wallet = case[2]
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[1]
        wallet.load(case[3], FORMAT_NONE)
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[4]


def test_outputs_tr_miniscript_provably_unspendable(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MINISCRIPT, P2TR
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        # 0 - PSBT
        # 1 - Expected outputs without descriptor
        # 2 - Wallet
        # 3 - Descriptor
        # 4 - Expected outputs with descriptor
        (
            tdata.EXP_TR_MINIS_PSBT,
            [
                "Inputs (1): ₿\u20090.01 994 469\n\nSpend (3): ₿\u20090.01 991 994\n\nFee: ₿\u20090.00 002 475 (0.2%)",
                "1. Spend: \n\ntb1psawr7wemsqgvplsxu0wvk6hdqrzf5rv387xuxx43mgjnkzn932pqne6l2c\n\n₿\u20090.00 500 000",
                "2. Spend: \n\ntb1p3gev77tasfmd45w64dq5azkdl3y02cxlnkykw2v00x3jnu6yu8pskn06gu\n\n₿\u20090.01 000 000",
                "3. Spend: \n\ntb1pzfd2t5k93dfvsl4a3ka36jcd9n4ppuskg7vfqeeu3zjqc5p8luaqs7f0ct\n\n₿\u20090.00 491 994",
            ],
            Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_MINISCRIPT,
                    NETWORKS["test"],
                    script_type=P2TR,
                )
            ),
            TR_EXP_MULTI_MINISCRIPT,
            [
                "Inputs (1): ₿\u20090.01 994 469\n\nSpend (1): ₿\u20090.01 000 000\n\nSelf-transfer or Change (2): ₿\u20090.00 991 994\n\nFee: ₿\u20090.00 002 475 (0.2%)",
                "1. Spend: \n\ntb1p3gev77tasfmd45w64dq5azkdl3y02cxlnkykw2v00x3jnu6yu8pskn06gu\n\n₿\u20090.01 000 000",
                "1. Self-transfer: \n\ntb1psawr7wemsqgvplsxu0wvk6hdqrzf5rv387xuxx43mgjnkzn932pqne6l2c\n\n₿\u20090.00 500 000",
                "1. Change: \n\ntb1pzfd2t5k93dfvsl4a3ka36jcd9n4ppuskg7vfqeeu3zjqc5p8luaqs7f0ct\n\n₿\u20090.00 491 994",
            ],
        ),
    ]

    for case in cases:
        wallet = case[2]
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[1]
        wallet.load(case[3], FORMAT_NONE)
        signer = PSBTSigner(wallet, case[0], FORMAT_NONE)
        outputs, _ = signer.outputs()
        assert outputs == case[4]


def test_xpubs_fails_with_no_xpubs(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    wallet = Wallet(Key(tdata.TEST_MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))

    with pytest.raises(ValueError, match="missing xpubs"):
        signer = PSBTSigner(wallet, tdata.MISSING_GLOBAL_XPUBS_PSBT, FORMAT_NONE)
        signer.xpubs()


def test_sign_single_1_input_1_output_no_change(m5stickv):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_PMOFN

    MNEMONIC = "action action action action action action action action action action action action"
    PSBT_B64 = "cHNidP8BAFMCAAAAAcfPlS2RvKvXxP/UxRmlAzMZcpLPKTOsBNbFM1JpT5Q7BwAAAAD9////AXAXAAAAAAAAF6kUK7ey9d8Pcw7ufsChrS3L5Ays13SHEgQlAE8BBDWHzwNOAaDGgAAAAA6sE2xHBRocbxB2m7sG3JvBy6PH2P+6FU8Xz26TLNf+Ax8/bmYn6gHZ6KY5opTh2Ajf+3sKBpZ40s59aYtcEnY+EODFlcVUAACAAQAAgAAAAIAAAQD9fQECAAAAAwZh04JGb3rJ3RJGINf/5lNG3RFk9DQyfqaKJK336OcaAQAAAAD9////pZE7Tecrp3E9O5JGSLma4D5TCG5N3uD4deLODBvkt4EAAAAAAP3///+lkTtN5yuncT07kkZIuZrgPlMIbk3e4Ph14s4MG+S3gQEAAAAA/f///wgsAQAAAAAAABYAFARbVWJaVJuYh2b3/HFtU3tQ9eoCLAEAAAAAAAAWABT4gSb5k7/g3ZrEXLyHFlP/C11NFCwBAAAAAAAAFgAU04NlSannloiWwZHvG1uf9aL0NPosAQAAAAAAABYAFNDJ5cj/6H72UNT95nAOLylXp/S5LAEAAAAAAAAWABTj8DqdkD3qZujRRRl4HlpWaADUBywBAAAAAAAAFgAUmPKKcthXsgBlI5AZbJtdEUrFe6gsAQAAAAAAABYAFF1lFcZm2E/gjALNKEfBtzGMsrsqmRgAAAAAAAAWABRk/PxLrogzR/Meytzu0v72RMgGh878JAABAR+ZGAAAAAAAABYAFGT8/EuuiDNH8x7K3O7S/vZEyAaHAQMEAQAAACIGAloQH2tjbm2ayZtJb2Gb0juSNIH9MIoEfX2UW0zE3l/SGODFlcVUAACAAQAAgAAAAIAAAAAAYwAAAAAA"
    OUTPUT = [
        "Inputs (1): ₿ 0.00 006 297\n\nSpend (1): ₿ 0.00 006 000\n\nFee: ₿ 0.00 000 297 (5.0%) ~2.7 sat/vB",
        "1. Spend: \n\n2MwEP7AfPt8NC65ACmcUhUtDZgGSxYiWUy4\n\n₿ 0.00 006 000",
    ]

    wallet = Wallet(Key(MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))
    signer = PSBTSigner(wallet, PSBT_B64, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert outputs == OUTPUT


def test_path_mismatch(mocker, m5stickv, tdata):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, P2WPKH, P2SH_P2WPKH, P2TR, TYPE_SINGLESIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_NONE

    cases = [
        (
            # Legacy wallet vs Legacy PSBT
            P2WPKH,
            tdata.P2WPKH_PSBT,
            "",
        ),
        (
            # Legacy wallet vs Taproot PSBT
            P2WPKH,
            tdata.P2TR_PSBT,
            "m/86h/1h/0h",
        ),
        (
            # Nested Segwit wallet vs Legacy PSBT
            P2SH_P2WPKH,
            tdata.P2PKH_PSBT,
            "m/44h/1h/0h",
        ),
        (
            # Nested Segwit wallet vs Nested Segwit PSBT
            P2SH_P2WPKH,
            tdata.P2SH_P2WPKH_PSBT,
            "",
        ),
        (
            # Native Segwit wallet vs Taproot PSBT
            P2WPKH,
            tdata.P2TR_PSBT,
            "m/86h/1h/0h",
        ),
        (
            # Native Segwit wallet vs Native Segwit PSBT
            P2WPKH,
            tdata.P2WPKH_PSBT,
            "",
        ),
        (
            # Taproot wallet vs Native Segwit PSBT
            P2TR,
            tdata.P2WPKH_PSBT,
            "m/84h/1h/0h",
        ),
        (
            # Taproot wallet vs Taproot PSBT
            P2TR,
            tdata.P2TR_PSBT,
            "",
        ),
        (
            # Native Segwit mainnet wallet vs Native Segwit testnet PSBT
            P2WPKH,
            tdata.P2WPKH_PSBT,
            "m/84h/1h/0h",
            NETWORKS["main"],
        ),
    ]

    for case in cases:
        if len(case) > 3:
            wallet = Wallet(
                Key(tdata.TEST_MNEMONIC, TYPE_SINGLESIG, case[3], script_type=case[0])
            )
        else:
            wallet = Wallet(
                Key(
                    tdata.TEST_MNEMONIC,
                    TYPE_SINGLESIG,
                    NETWORKS["test"],
                    script_type=case[0],
                )
            )
        signer = PSBTSigner(wallet, case[1], FORMAT_NONE)
        path_mismatch = signer.path_mismatch()
        assert path_mismatch == case[2]


def test_sign_sats_vB(m5stickv):
    from embit.networks import NETWORKS
    from krux.psbt import PSBTSigner
    from krux.key import Key, TYPE_SINGLESIG, TYPE_MULTISIG
    from krux.wallet import Wallet
    from krux.qr import FORMAT_PMOFN

    MNEMONIC = "action action action action action action action action action action action action"
    wallet = Wallet(Key(MNEMONIC, TYPE_SINGLESIG, NETWORKS["test"]))

    PSBT_satvB_1_31 = "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"
    signer = PSBTSigner(wallet, PSBT_satvB_1_31, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (5): ₿ 0.00 001 500\n\nSpend (1): ₿ 0.00 001 000\n\nFee: ₿ 0.00 000 500 (50.0%) ~1.3 sat/vB"
    )

    PSBT_satvB_28_04 = "cHNidP8BAH4CAAAAAcfPlS2RvKvXxP/UxRmlAzMZcpLPKTOsBNbFM1JpT5Q7BwAAAAD9////AugDAAAAAAAAIgAguKIqvP6jJ6Lj5PVWAoa1nazfyQ8DzfgI34hQnNxYStPoAwAAAAAAABepFGJYgmsnwywOzlosjYc84fGiiGPTh7r5KgBPAQQ1h88DTgGgxoAAAAAOrBNsRwUaHG8Qdpu7Btybwcujx9j/uhVPF89ukyzX/gMfP25mJ+oB2eimOaKU4dgI3/t7CgaWeNLOfWmLXBJ2PhDgxZXFVAAAgAEAAIAAAACAAAEA/X0BAgAAAAMGYdOCRm96yd0SRiDX/+ZTRt0RZPQ0Mn6miiSt9+jnGgEAAAAA/f///6WRO03nK6dxPTuSRki5muA+UwhuTd7g+HXizgwb5LeBAAAAAAD9////pZE7Tecrp3E9O5JGSLma4D5TCG5N3uD4deLODBvkt4EBAAAAAP3///8ILAEAAAAAAAAWABQEW1ViWlSbmIdm9/xxbVN7UPXqAiwBAAAAAAAAFgAU+IEm+ZO/4N2axFy8hxZT/wtdTRQsAQAAAAAAABYAFNODZUmp55aIlsGR7xtbn/Wi9DT6LAEAAAAAAAAWABTQyeXI/+h+9lDU/eZwDi8pV6f0uSwBAAAAAAAAFgAU4/A6nZA96mbo0UUZeB5aVmgA1AcsAQAAAAAAABYAFJjyinLYV7IAZSOQGWybXRFKxXuoLAEAAAAAAAAWABRdZRXGZthP4IwCzShHwbcxjLK7KpkYAAAAAAAAFgAUZPz8S66IM0fzHsrc7tL+9kTIBofO/CQAAQEfmRgAAAAAAAAWABRk/PxLrogzR/Meytzu0v72RMgGhwEDBAEAAAAiBgJaEB9rY25tmsmbSW9hm9I7kjSB/TCKBH19lFtMxN5f0hjgxZXFVAAAgAEAAIAAAACAAAAAAGMAAAAAAAA="
    signer = PSBTSigner(wallet, PSBT_satvB_28_04, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (1): ₿ 0.00 006 297\n\nSpend (2): ₿ 0.00 002 000\n\nFee: ₿ 0.00 004 297 (214.9%) ~27.9 sat/vB"
    )

    PSBT_satvB_12_03 = "cHNidP8BAP0WAQIAAAABx8+VLZG8q9fE/9TFGaUDMxlyks8pM6wE1sUzUmlPlDsHAAAAAP3///8GTAEAAAAAAAAiACC4oiq8/qMnouPk9VYChrWdrN/JDwPN+AjfiFCc3FhK0xwCAAAAAAAAF6kUYliCayfDLA7OWiyNhzzh8aKIY9OHTAEAAAAAAAAiACDwabzM44F/2f9evGkQqXxhFwjzErVHgJfc2IE2I91E/U0BAAAAAAAAIlEgJeBfcLU573hJOaYb6XQGR/eOKVSvBR9TW3+FoxRQEWIkAgAAAAAAABl2qRRrgQv3nFAPaNKPYAXmsjT7Ru6DJoisHAIAAAAAAAAXqRSDAQVKg8ZQzf3pc5CIXtSjjvybt4e/+SoATwEENYfPA04BoMaAAAAADqwTbEcFGhxvEHabuwbcm8HLo8fY/7oVTxfPbpMs1/4DHz9uZifqAdnopjmilOHYCN/7ewoGlnjSzn1pi1wSdj4Q4MWVxVQAAIABAACAAAAAgAABAP19AQIAAAADBmHTgkZvesndEkYg1//mU0bdEWT0NDJ+pookrffo5xoBAAAAAP3///+lkTtN5yuncT07kkZIuZrgPlMIbk3e4Ph14s4MG+S3gQAAAAAA/f///6WRO03nK6dxPTuSRki5muA+UwhuTd7g+HXizgwb5LeBAQAAAAD9////CCwBAAAAAAAAFgAUBFtVYlpUm5iHZvf8cW1Te1D16gIsAQAAAAAAABYAFPiBJvmTv+DdmsRcvIcWU/8LXU0ULAEAAAAAAAAWABTTg2VJqeeWiJbBke8bW5/1ovQ0+iwBAAAAAAAAFgAU0MnlyP/ofvZQ1P3mcA4vKVen9LksAQAAAAAAABYAFOPwOp2QPepm6NFFGXgeWlZoANQHLAEAAAAAAAAWABSY8opy2FeyAGUjkBlsm10RSsV7qCwBAAAAAAAAFgAUXWUVxmbYT+CMAs0oR8G3MYyyuyqZGAAAAAAAABYAFGT8/EuuiDNH8x7K3O7S/vZEyAaHzvwkAAEBH5kYAAAAAAAAFgAUZPz8S66IM0fzHsrc7tL+9kTIBocBAwQBAAAAIgYCWhAfa2NubZrJm0lvYZvSO5I0gf0wigR9fZRbTMTeX9IY4MWVxVQAAIABAACAAAAAgAAAAABjAAAAAAAAAAAAAA=="
    signer = PSBTSigner(wallet, PSBT_satvB_12_03, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (1): ₿ 0.00 006 297\n\nSpend (6): ₿ 0.00 002 625\n\nFee: ₿ 0.00 003 672 (139.9%) ~12.0 sat/vB"
    )

    PSBT_satvB_8_75 = "cHNidP8BAP0WAQIAAAABx8+VLZG8q9fE/9TFGaUDMxlyks8pM6wE1sUzUmlPlDsHAAAAAP3///8GJAIAAAAAAAAZdqkUa4EL95xQD2jSj2AF5rI0+0bugyaIrDUFAAAAAAAAIlEgJeBfcLU573hJOaYb6XQGR/eOKVSvBR9TW3+FoxRQEWIcAgAAAAAAABepFIMBBUqDxlDN/elzkIhe1KOO/Ju3hxwCAAAAAAAAF6kUYliCayfDLA7OWiyNhzzh8aKIY9OHTAEAAAAAAAAiACC4oiq8/qMnouPk9VYChrWdrN/JDwPN+AjfiFCc3FhK00wBAAAAAAAAIgAg8Gm8zOOBf9n/XrxpEKl8YRcI8xK1R4CX3NiBNiPdRP2/+SoATwEENYfPA04BoMaAAAAADqwTbEcFGhxvEHabuwbcm8HLo8fY/7oVTxfPbpMs1/4DHz9uZifqAdnopjmilOHYCN/7ewoGlnjSzn1pi1wSdj4Q4MWVxVQAAIABAACAAAAAgAABAP19AQIAAAADBmHTgkZvesndEkYg1//mU0bdEWT0NDJ+pookrffo5xoBAAAAAP3///+lkTtN5yuncT07kkZIuZrgPlMIbk3e4Ph14s4MG+S3gQAAAAAA/f///6WRO03nK6dxPTuSRki5muA+UwhuTd7g+HXizgwb5LeBAQAAAAD9////CCwBAAAAAAAAFgAUBFtVYlpUm5iHZvf8cW1Te1D16gIsAQAAAAAAABYAFPiBJvmTv+DdmsRcvIcWU/8LXU0ULAEAAAAAAAAWABTTg2VJqeeWiJbBke8bW5/1ovQ0+iwBAAAAAAAAFgAU0MnlyP/ofvZQ1P3mcA4vKVen9LksAQAAAAAAABYAFOPwOp2QPepm6NFFGXgeWlZoANQHLAEAAAAAAAAWABSY8opy2FeyAGUjkBlsm10RSsV7qCwBAAAAAAAAFgAUXWUVxmbYT+CMAs0oR8G3MYyyuyqZGAAAAAAAABYAFGT8/EuuiDNH8x7K3O7S/vZEyAaHzvwkAAEBH5kYAAAAAAAAFgAUZPz8S66IM0fzHsrc7tL+9kTIBocBAwQBAAAAIgYCWhAfa2NubZrJm0lvYZvSO5I0gf0wigR9fZRbTMTeX9IY4MWVxVQAAIABAACAAAAAgAAAAABjAAAAAAAAAAAAAA=="
    signer = PSBTSigner(wallet, PSBT_satvB_8_75, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (1): ₿ 0.00 006 297\n\nSpend (6): ₿ 0.00 003 625\n\nFee: ₿ 0.00 002 672 (73.8%) ~8.7 sat/vB"
    )

    PSBT_satvB_5_48 = "cHNidP8BAP0WAQIAAAABx8+VLZG8q9fE/9TFGaUDMxlyks8pM6wE1sUzUmlPlDsHAAAAAP3///8GJAIAAAAAAAAZdqkUa4EL95xQD2jSj2AF5rI0+0bugyaIrBwCAAAAAAAAF6kUYliCayfDLA7OWiyNhzzh8aKIY9OHHAIAAAAAAAAXqRSDAQVKg8ZQzf3pc5CIXtSjjvybt4dMAQAAAAAAACIAIPBpvMzjgX/Z/168aRCpfGEXCPMStUeAl9zYgTYj3UT9TAEAAAAAAAAiACC4oiq8/qMnouPk9VYChrWdrN/JDwPN+AjfiFCc3FhK0x0JAAAAAAAAIlEgJeBfcLU573hJOaYb6XQGR/eOKVSvBR9TW3+FoxRQEWK/+SoATwEENYfPA04BoMaAAAAADqwTbEcFGhxvEHabuwbcm8HLo8fY/7oVTxfPbpMs1/4DHz9uZifqAdnopjmilOHYCN/7ewoGlnjSzn1pi1wSdj4Q4MWVxVQAAIABAACAAAAAgAABAP19AQIAAAADBmHTgkZvesndEkYg1//mU0bdEWT0NDJ+pookrffo5xoBAAAAAP3///+lkTtN5yuncT07kkZIuZrgPlMIbk3e4Ph14s4MG+S3gQAAAAAA/f///6WRO03nK6dxPTuSRki5muA+UwhuTd7g+HXizgwb5LeBAQAAAAD9////CCwBAAAAAAAAFgAUBFtVYlpUm5iHZvf8cW1Te1D16gIsAQAAAAAAABYAFPiBJvmTv+DdmsRcvIcWU/8LXU0ULAEAAAAAAAAWABTTg2VJqeeWiJbBke8bW5/1ovQ0+iwBAAAAAAAAFgAU0MnlyP/ofvZQ1P3mcA4vKVen9LksAQAAAAAAABYAFOPwOp2QPepm6NFFGXgeWlZoANQHLAEAAAAAAAAWABSY8opy2FeyAGUjkBlsm10RSsV7qCwBAAAAAAAAFgAUXWUVxmbYT+CMAs0oR8G3MYyyuyqZGAAAAAAAABYAFGT8/EuuiDNH8x7K3O7S/vZEyAaHzvwkAAEBH5kYAAAAAAAAFgAUZPz8S66IM0fzHsrc7tL+9kTIBocBAwQBAAAAIgYCWhAfa2NubZrJm0lvYZvSO5I0gf0wigR9fZRbTMTeX9IY4MWVxVQAAIABAACAAAAAgAAAAABjAAAAAAAAAAAAAA=="
    signer = PSBTSigner(wallet, PSBT_satvB_5_48, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (1): ₿ 0.00 006 297\n\nSpend (6): ₿ 0.00 004 625\n\nFee: ₿ 0.00 001 672 (36.2%) ~5.5 sat/vB"
    )

    PSBT_satvB_2_2 = "cHNidP8BAP0WAQIAAAABx8+VLZG8q9fE/9TFGaUDMxlyks8pM6wE1sUzUmlPlDsHAAAAAP3///8GJAIAAAAAAAAZdqkUa4EL95xQD2jSj2AF5rI0+0bugyaIrAUNAAAAAAAAIlEgJeBfcLU573hJOaYb6XQGR/eOKVSvBR9TW3+FoxRQEWJMAQAAAAAAACIAILiiKrz+oyei4+T1VgKGtZ2s38kPA834CN+IUJzcWErTHAIAAAAAAAAXqRSDAQVKg8ZQzf3pc5CIXtSjjvybt4dMAQAAAAAAACIAIPBpvMzjgX/Z/168aRCpfGEXCPMStUeAl9zYgTYj3UT9HAIAAAAAAAAXqRRiWIJrJ8MsDs5aLI2HPOHxoohj04e/+SoATwEENYfPA04BoMaAAAAADqwTbEcFGhxvEHabuwbcm8HLo8fY/7oVTxfPbpMs1/4DHz9uZifqAdnopjmilOHYCN/7ewoGlnjSzn1pi1wSdj4Q4MWVxVQAAIABAACAAAAAgAABAP19AQIAAAADBmHTgkZvesndEkYg1//mU0bdEWT0NDJ+pookrffo5xoBAAAAAP3///+lkTtN5yuncT07kkZIuZrgPlMIbk3e4Ph14s4MG+S3gQAAAAAA/f///6WRO03nK6dxPTuSRki5muA+UwhuTd7g+HXizgwb5LeBAQAAAAD9////CCwBAAAAAAAAFgAUBFtVYlpUm5iHZvf8cW1Te1D16gIsAQAAAAAAABYAFPiBJvmTv+DdmsRcvIcWU/8LXU0ULAEAAAAAAAAWABTTg2VJqeeWiJbBke8bW5/1ovQ0+iwBAAAAAAAAFgAU0MnlyP/ofvZQ1P3mcA4vKVen9LksAQAAAAAAABYAFOPwOp2QPepm6NFFGXgeWlZoANQHLAEAAAAAAAAWABSY8opy2FeyAGUjkBlsm10RSsV7qCwBAAAAAAAAFgAUXWUVxmbYT+CMAs0oR8G3MYyyuyqZGAAAAAAAABYAFGT8/EuuiDNH8x7K3O7S/vZEyAaHzvwkAAEBH5kYAAAAAAAAFgAUZPz8S66IM0fzHsrc7tL+9kTIBocBAwQBAAAAIgYCWhAfa2NubZrJm0lvYZvSO5I0gf0wigR9fZRbTMTeX9IY4MWVxVQAAIABAACAAAAAgAAAAABjAAAAAAAAAAAAAA=="
    signer = PSBTSigner(wallet, PSBT_satvB_2_2, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (1): ₿ 0.00 006 297\n\nSpend (6): ₿ 0.00 005 625\n\nFee: ₿ 0.00 000 672 (12.0%) ~2.2 sat/vB"
    )

    PSBT_satvB_1_8 = "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"
    signer = PSBTSigner(wallet, PSBT_satvB_1_8, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (7): ₿ 0.00 002 100\n\nSpend (3): ₿ 0.00 000 997\n\nFee: ₿ 0.00 001 103 (110.7%) ~1.8 sat/vB"
    )

    wallet = Wallet(Key(MNEMONIC, TYPE_MULTISIG, NETWORKS["test"]))
    PSBT_satvB_164_83 = "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"
    signer = PSBTSigner(wallet, PSBT_satvB_164_83, FORMAT_PMOFN)
    outputs, _ = signer.outputs()
    assert (
        outputs[0]
        == "Inputs (2): ₿\u20090.00 130 622\n\nSpend (9): ₿\u20090.00 028 343\n\nFee: ₿\u20090.00 102 279 (360.9%) ~165.2 sat/vB"
    )

    # TODO: Add a multisig with descriptor so change can be deteted
