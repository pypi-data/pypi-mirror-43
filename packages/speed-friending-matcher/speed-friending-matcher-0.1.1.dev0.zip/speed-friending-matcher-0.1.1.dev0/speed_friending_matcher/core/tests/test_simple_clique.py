# -*- coding: utf-8 -*-
import pytest
from speed_friending_matcher.core.person import Person, MatchingFlags


@pytest.fixture
def testdata():
    data = []
    tobi = Person(
        name='Tobi',
        number=1,
        email='tobi@gmail.com',
        phone='0123456789',
        marked_numbers={2, 3, 5},
    )
    sara = Person(
        name='Sara Mustermann',
        number=2,
        email='',
        phone='123456789',
        marked_numbers={1, 4, 3},
    )
    mark = Person(
        name='Mark',
        number=3,
        email='mark@mark.com',
        phone='987654321',
        marked_numbers={2, 4, 5},
    )
    luisa = Person(
        name='Luisa', number=4, email='', phone='49123456789', marked_numbers={5, 1}
    )
    data.append(tobi)
    data.append(sara)
    data.append(mark)
    data.append(luisa)
    return data


@pytest.fixture
def matchmaker():
    from speed_friending_matcher.core.simple_clique import SimpleClique

    return SimpleClique()


def test_clique_matching_matches_everyone_in_the_clique_of_a_person(
    matchmaker, testdata
):
    matchmaker.run(testdata)

    tobi, sara, mark, luisa = testdata
    assert tobi.results.matches == {tobi, sara, mark}
