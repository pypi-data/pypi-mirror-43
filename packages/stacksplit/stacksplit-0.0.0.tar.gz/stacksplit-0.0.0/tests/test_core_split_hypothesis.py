import stacksplit

from hypothesis import given, settings
import hypothesis.strategies as st


def check_valid_len_sum_smallest(gen, num, parts, smallest):
    """This checks the following properties:
    * the length of a given solution is equal to parts,
    * the sum of a given solution is equal to num,
    * the smallest element in a solution is greater or equal to smallest,
    * every successor in a solution is greater or equal to its predecessor"""
    for comb in gen:
        length, sums, small, last = 0, 0, smallest, smallest
        for i in comb:
            length += 1
            sums += i
            small = min([i, small])
            assert last <= i
            last = i
        assert length == parts
        assert sums == num
        assert small >= smallest


# HYPOTHESIS PARAMETERS:
MIN_NUM = -5  # negative numbers are not as interesting (no usecase)
MAX_NUM = 100  # positive numbers are much more interesting
# this test slows down drastically the bigger MAX_PARTS (not higher than 10)
MAX_PARTS = 5


@settings(max_examples=500, deadline=None)
@given(
    num=st.integers(min_value=MIN_NUM, max_value=MAX_NUM),
    parts=st.integers(min_value=1, max_value=MAX_PARTS),
    smallest=st.integers(min_value=MIN_NUM, max_value=MAX_NUM)
)
def test_valid_numbers(num, parts, smallest):
    res = stacksplit.split(num, parts, smallest)
    check_valid_len_sum_smallest(res, num, parts, smallest)
