module spdz_fresco;

kind spdz_fresco {
    type uint64;
}

template <domain D : spdz_fresco, type T>
D T [[1]] operator+(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("spdz_fresco::add_$T\_vec", __domainid (D), a, b, a);
    return a;
}

template <domain D : spdz_fresco, type T>
D T [[1]] operator*(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("spdz_fresco::mul_$T\_vec", __domainid (D), a, b, a);
    return a;
}

template <domain D : spdz_fresco, type T>
D T [[1]] operator-(D T [[1]] a, D T [[1]] b) {
    assert(size(a) == size(b));
    __syscall("spdz_fresco::sub_$T\_vec", __domainid (D), a, b, a);
    return a;
}
