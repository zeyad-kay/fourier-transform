// MathLibrary.h - Contains declarations of math functions
#pragma once
#include <complex>

#ifdef FOURIER_EXPORTS
#define FOURIER_API __declspec(dllexport)
#else
#define FOURIER_API __declspec(dllimport)
#endif


extern "C" FOURIER_API std::complex<double> * DFT(const std::complex<double> * data_ptr, size_t size);
extern "C" FOURIER_API std::complex<double> * FFT(const std::complex<double> * data_ptr, size_t size);