from library import one, two, Three, six


assert one() + two() == Three().three()
assert one() * two() * Three().three() == six()
