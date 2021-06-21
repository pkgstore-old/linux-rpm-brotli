# Brotli

**Brotli** is a generic-purpose lossless compression algorithm that compresses data using a combination of a modern variant of the LZ77 algorithm, Huffman coding and 2nd order context modeling, with a compression ratio comparable to the best currently available general-purpose compression methods. It is similar in speed with deflate but offers more dense compression.

## Install

### Fedora COPR

```
$ dnf copr enable pkgstore/brotli
$ dnf install -y brotli
```

### Open Build Service (OBS)

```
# Work in Progress
```

## Update

```
$ dnf upgrade -y brotli
```

## How to Build

1. Get source from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/brotli).
2. Write last commit SHA from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/brotli) to [CHANGELOG](CHANGELOG).
3. Modify & update source (and `*.spec`).
4. Build SRPM & RPM.
