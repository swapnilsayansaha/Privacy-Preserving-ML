module aby;

kind aby {
    type uint64;
}

/*
 * ABY supports uint types with different secret sharing schemes (arithmetic,
 * boolean and Yao's circuits). However, currently there is no easy way to add
 * new types to SecreC. This will be changed in future versions.

 * We overload some operators to call protocols for a specific secret sharing
 * scheme.
 */

template <domain D : aby, type T>
D T [[1]] operator+(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("aby::add_arith_$T\_vec", __domainid (D), a, b, a);
    return a;
}

template <domain D : aby, type T>
D T [[1]] operator*(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("aby::mul_arith_$T\_vec", __domainid (D), a, b, a);
    return a;
}

template <domain D : aby, type T>
D T [[1]] operator-(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("aby::sub_arith_$T\_vec", __domainid (D), a, b, a);
    return a;
}
