## Bad hashing functions
from collections.abc import Callable
from math import sqrt, floor
import cityhash
import farmhash


def identity_hash(_table_size: int) -> Callable[[int], int]:
    """
    Hash an integer by returning it.
    """
    return lambda key: key


def modulo_hash(_table_size: int, modulo: int = 10) -> Callable[[int], int]:
    """
    Return the modulo function of a number.
    """
    return lambda number: number % modulo


def multiplication_hash(table_size: int,
                        constant: int = 42) -> Callable[[int], int]:
    """
    Return a hash function that uses the multiplication method with a constant.
    """
    return lambda key: (key * constant) % table_size


def left_shift_hash(table_size: int, shift: int = 3) -> Callable[[int], int]:
    """
    Return a hash function that uses the left shift method with a shift.
    """
    return lambda key: (key << shift) % table_size


def right_shift_hash(table_size: int, shift: int = 3) -> Callable[[int], int]:
    """
    Return a hash function that uses the right shift method with a shift.
    """
    return lambda key: (key >> shift) % table_size


def add_hash(table_size: int, add: int = 42) -> Callable[[int], int]:
    """
    Return a hash function that uses the right shift method with a shift.
    """
    return lambda key: (key + add) % table_size


def xor_hash(table_size: int, xor: int = 42) -> Callable[[int], int]:
    """
    Return a hash function that uses the right shift method with a shift.
    """
    return lambda key: (key ^ xor) % table_size


def minus_hash(table_size: int, minus: int = 42) -> Callable[[int], int]:
    """
    Return a hash function that uses the right shift method with a shift.
    """
    return lambda key: (key - minus) % table_size


## Good hashing functions

def multiplicative_method_hash(table_size: int,
                               A: float = 0.42) -> Callable[[int], int]:
    return lambda key: floor(table_size * ((key * A) % 1))


def knuth_multiplicative_method_hash(table_size: int) -> Callable[[int], int]:
    """
    Return a hash function that uses the Knuth multiplicative method.
    """
    return lambda key: floor((key * (sqrt(5) - 1) / 2) % 1 * table_size)


def murmur_hash3_x86_32_hash(table_size: int, seed=0) -> Callable[[int], int]:
    """
    Return a hash function that uses the MurmurHash3 algorithm.
    https://en.wikipedia.org/wiki/MurmurHash
    """

    def fmix(h):
        h ^= h >> 16
        h = (h * 0x85ebca6b) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0xc2b2ae35) & 0xFFFFFFFF
        h ^= h >> 16
        return h

    def murmur_hash3_x86_32(key: int) -> int:
        key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
        data = bytearray(key_bytes)
        nblocks = len(data) // 4

        h1 = seed

        c1 = 0xcc9e2d51
        c2 = 0x1b873593

        for i in range(nblocks):
            k1 = (data[4 * i + 3] << 24) | (data[4 * i + 2] << 16) | (
                data[4 * i + 1] << 8) | data[4 * i]

            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = ((k1 << 15) | (k1 >> (32 - 15))) & 0xFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFF

            h1 ^= k1
            h1 = ((h1 << 13) | (h1 >> (32 - 13))) & 0xFFFFFFFF
            h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

        tail = data[nblocks * 4:]
        k1 = 0
        if len(tail) >= 3:
            k1 ^= tail[2] << 16
        if len(tail) >= 2:
            k1 ^= tail[1] << 8
        if len(tail) >= 1:
            k1 ^= tail[0]
            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = ((k1 << 15) | (k1 >> (32 - 15))) & 0xFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFF
            h1 ^= k1

        h1 ^= len(data)

        h1 = fmix(h1)

        return h1 % table_size

    return murmur_hash3_x86_32


def farm_hash_hash(table_size: int, seed=0) -> Callable[[int], int]:
    """
    Return a hash function that uses the FarmHash algorithm.
    https://github.com/google/farmhash
    """

    def farm_hash(key: int) -> int:
        key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
        hash_value = farmhash.FarmHash32WithSeed(key_bytes, seed)
        return hash_value % table_size

    return farm_hash


def city_hash_hash(table_size: int, seed=0) -> Callable[[int], int]:
    """
    Return a hash function that uses the CityHash algorithm.
    https://github.com/google/cityhash
    """

    def city_hash(key: int) -> int:
        key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
        hash_value = cityhash.CityHash64WithSeed(key_bytes, seed)
        return hash_value % table_size

    return city_hash
