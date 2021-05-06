#include "pch.h"
#include <complex>
#include <cmath>
#include "Fourier.h"

using namespace std::complex_literals;

const double PI = 3.1415926536;

std::complex<double>* FFT(const std::complex<double>* data_ptr, size_t size)
{
    // DFT
    std::complex<double>* cpy = new std::complex<double>[size];
    std::copy(data_ptr, data_ptr + size, cpy);
    size_t k = size, n;
    double thetaT = PI / size;
    std::complex<double> phiT = std::complex<double>(cos(thetaT), -sin(thetaT)), T;
    while (k > 1)
    {
        n = k;
        k >>= 1;
        phiT = phiT * phiT;
        T = 1.0L;
        for (size_t l = 0; l < k; l++)
        {
            for (size_t a = l; a < size; a += n)
            {
                unsigned int b = a + k;
                std::complex<double> t = cpy[a] - cpy[b];
                cpy[a] += cpy[b];
                cpy[b] = t * T;
            }
            T *= phiT;
        }
    }
    // Decimate
    size_t m = (size_t)log2(size);
    for (size_t a = 0; a < size; a++)
    {
        size_t b = a;
        // Reverse bits
        b = (((b & 0xaaaaaaaa) >> 1) | ((b & 0x55555555) << 1));
        b = (((b & 0xcccccccc) >> 2) | ((b & 0x33333333) << 2));
        b = (((b & 0xf0f0f0f0) >> 4) | ((b & 0x0f0f0f0f) << 4));
        b = (((b & 0xff00ff00) >> 8) | ((b & 0x00ff00ff) << 8));
        b = ((b >> 16) | (b << 16)) >> (32 - m);
        if (b > a)
        {
            std::complex<double> t = cpy[a];
            cpy[a] = cpy[b];
            cpy[b] = t;
        }
    }
    return cpy;
}

std::complex<double>* DFT(const std::complex<double> *data_ptr, size_t size)
{
    std::complex<double>* transform = new std::complex<double>[size];
    double arg, cosarg, sinarg;
    double* real = new double[size], * imag = new double[size];

    for (size_t j = 0; j < size; j++)
    {
        real[j] = 0;
        imag[j] = 0;
        arg = -1 * 2.0 * PI * (double)j / (double)size;
        for (size_t k = 0; k < size; k++)
        {
            cosarg = cos(k * arg);
            sinarg = sin(k * arg);
            real[j] += (data_ptr[k].real() * cosarg - data_ptr[k].imag() * sinarg);
            imag[j] += (data_ptr[k].real() * sinarg + data_ptr[k].imag() * cosarg);
        }
        transform[j] = real[j] + imag[j] * 1i;
    }

    delete[] real;
    delete[] imag;
    return transform;
}