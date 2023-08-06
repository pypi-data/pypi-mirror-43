from pyske.core.list.slist import SList
from pyske.core.list.plist import PList


def app(l1, l2):
    return SList(l1 + l2)


msg = "hello world!"


def test_init_to_seq_empty():
    pl = PList()
    res = pl.to_seq()
    exp = []
    assert res == exp


def test_init_to_seq_non_empty():
    pl = PList.init(lambda i: msg[i], len(msg))
    res = pl.to_seq()
    exp = list(msg)
    assert res == exp


def test_map_empty():
    f = lambda x: x.upper()
    input = PList()
    res = input.map(f).to_seq()
    exp = []
    assert res == exp


def test_map_non_empty():
    f = lambda x: x.upper()
    input = PList.init(lambda i: msg[i], len(msg))
    res = input.map(f).to_seq()
    exp = list(f(msg))
    assert res == exp


def test_mapi_empty():
    f = lambda i, x: f'{i}:{x.upper()}'
    input = PList()
    res = input.mapi(f).to_seq()
    exp = []
    assert res == exp


def test_mapi_non_empty():
    f = lambda i, x: f'{i}:{x.upper()}'
    input = PList.init(lambda i: msg[i], len(msg))
    res = input.mapi(f).to_seq()
    exp = SList(msg).mapi(f)
    assert res == exp


def test_scanr_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res = input.scanr(f).to_seq()
    exp = SList(range(0, size)).scanr(f)
    assert res == exp


def test_scanl_empty():
    f = lambda x, y: x + y
    size = 0
    input = PList.init(lambda i: i, size)
    res = input.scanl(f, 0).to_seq()
    exp = SList(range(0, size)).scanl(f, 0)
    assert res == exp


def test_scanl_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res = input.scanl(f, 0).to_seq()
    exp = SList(range(0, size)).scanl(f, 0)
    assert res == exp


def test_scanl_last_empty():
    f = lambda x, y: x + y
    size = 0
    input = PList.init(lambda i: i, size)
    res_pl, res_scalar = input.scanl_last(f, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(f, 0)
    assert res == exp


def test_scanl_last_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res_pl, res_scalar = input.scanl_last(f, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(f, 0)
    assert res == exp
