#ifndef TENSOR_HPP
#define TENSOR_HPP
#include <iostream>
#include <vector>
#include <stdexcept>
#include <random>
#include <iomanip>
#include <functional>
#include <memory>
#include <cmath>
#include <algorithm>

class Tensor
{
private:
    int m_rows = 0, m_cols = 0;
    std::vector<std::vector<double>> mat;
public:
    bool null = false;
    Tensor () : null(true) {}
    Tensor(int r, int c, double val = 0.0) : m_rows(r), m_cols(c), mat(r, std::vector<double>(c, val)){}
    Tensor(const std::vector<std::vector<double>> M) : m_rows(M.size()), m_cols(M[0].size()), mat(M) {}
    int size(int dim) const;
    std::pair<int, int> size() const;
    std::vector<std::vector<double>> get_matrix() { return mat; }
    const std::vector<std::vector<double>> *get_mat_pointor() const { return &mat; }
    Tensor T();
    Tensor& operator=(const Tensor &other);
    double& operator ()(int x, int y);
    const double& operator ()(int x, int y) const;
    Tensor operator +(const Tensor &other) const;
    Tensor operator +(double x) const;
    friend Tensor operator +(double x, const Tensor &other) { return other + x; }
    Tensor operator -(const Tensor &other) const;
    Tensor operator *(const Tensor &other) const;
    Tensor operator *(double x) const;
    friend Tensor operator *(double x, const Tensor &other) { return other * x; }
    Tensor operator /(double x) const;
    Tensor& operator +=(const Tensor &other);
    Tensor mul(const Tensor &other);
    double sum();
    Tensor sum(int dim);
    void apply(std::function<double(double)> func);
    Tensor after(std::function<double(double)> func);
};

Tensor zeros(int rows, int cols);
Tensor ones(int rows, int cols);
Tensor tensor(int rows, int cols, double val);
Tensor tensor(const std::vector<std::vector<double>> &M);
Tensor rands(int rows, int cols, double range = 0.5);

int Tensor::size(int dim) const
{
    if (dim == 0) return m_rows;
    else if (dim == 1) return m_cols;
    else throw std::out_of_range("size error: tensor size dim is neither 0 or 1");
}

std::pair<int, int> Tensor::size() const
{
    return std::make_pair(m_rows, m_cols);
}

Tensor Tensor::T()
{
    Tensor res(m_cols, m_rows);
    for (int i = 0; i < m_cols; i++) {
        for (int j = 0; j < m_rows; j++) {
            res.mat[i][j] = mat[j][i];
        }
    }
    return res;
}

Tensor& Tensor::operator=(const Tensor &other)
{
    if (this == &other) return *this;
    m_rows = other.m_rows;
    m_cols = other.m_cols;
    mat = other.mat;
    null = other.null;
    return *this;
}

double& Tensor::operator ()(int x, int y)
{
    if (x < 0 || x >= m_rows || y < 0 || y >= m_cols) throw std::out_of_range("Index out of bounds!");
    return mat[x][y];
}
const double& Tensor::operator ()(int x, int y) const
{
    if (x < 0 || x >= m_rows || y < 0 || y >= m_cols) throw std::out_of_range("Index out of bounds!");
    return mat[x][y];
}

Tensor Tensor::operator+(const Tensor &other) const
{
    int r1 = m_rows, c1 = m_cols;
    int r2 = other.size(0), c2 = other.size(1);
    if ((r1 != r2 && r1 != 1 && r2 != 1) || (c1 != c2 && c2 != 1 && c2 != 1)) {
        throw std::invalid_argument("Invalid dimensions for matrix additon");
    }
    int rows = std::max(r1, r2), cols = std::max(c1, c2);
    Tensor res = zeros(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double val1 = mat[(i < r1) ? i : 0][(j < c1) ? j : 0];
            double val2 = other.mat[(i < r2) ? i : 0][(j < c2) ? j : 0];
            res.mat[i][j] = val1 + val2;
        }
    }
    return res;
}

Tensor Tensor::operator+(double x) const
{
    Tensor res = zeros(m_rows, m_cols);
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            res.mat[i][j] = mat[i][j] + x;
        }
    }
    return res;
}

Tensor Tensor::operator-(const Tensor &other) const
{
    int r1 = m_rows, c1 = m_cols;
    int r2 = other.size(0), c2 = other.size(1);
    if ((r1 != r2 && r1 != 1 && r2 != 1) || (c1 != c2 && c2 != 1 && c2 != 1)) {
        throw std::invalid_argument("Invalid dimensions for matrix additon");
    }
    int rows = std::max(r1, r2), cols = std::max(c1, c2);
    Tensor res = zeros(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double val1 = mat[(i < r1) ? i : 0][(j < c1) ? j : 0];
            double val2 = other.mat[(i < r2) ? i : 0][(j < c2) ? j : 0];
            res.mat[i][j] = val1 - val2;
        }
    }
    return res;
}

Tensor Tensor::operator *(const Tensor &other) const
{
    int r1 = m_rows, c1 = m_cols;
    int r2 = other.m_rows, c2 = other.m_cols;
    if ((r1 != r2 && r1 != 1 && r2 != 1) || (c1 != c2 && c1 != 1 && c2 != 1)) {
        throw std::invalid_argument("Invalid dimensions for matrix dot");
    }
    int rows = std::max(r1, r2), cols = std::max(c1, c2);
    Tensor res = zeros(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double val1 = mat[(i < r1) ? i : 0][(j < c1) ? j : 0];
            double val2 = other.mat[(i < r2) ? i : 0][(j < c2) ? j : 0];
            res.mat[i][j] = val1 * val2;
        }
    }
    return res;
}

Tensor Tensor::operator *(double x) const
{
    Tensor res = zeros(m_rows, m_cols);
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            res.mat[i][j] = mat[i][j] * x;
        }
    }
    return res;
}

Tensor Tensor::operator /(double x) const
{
    if (x == 0) throw std::runtime_error("Tensor operator / Error : Division by zero is not allowed");
    Tensor res = zeros(m_rows, m_cols);
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            res.mat[i][j] = mat[i][j] / x;
        }
    }
    return res;
}

Tensor& Tensor::operator+=(const Tensor &other)
    {
    if ((m_rows != other.m_rows && other.m_rows != 1) || (m_cols != other.m_cols && other.m_cols != 1)) {
        throw std::invalid_argument("Invalid dimensions for +=");
    }
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            this->mat[i][j] += other.mat[(i < other.m_rows) ? i : 0][(j < other.m_cols) ? j : 0];
        }
    }
    return *this;
}

Tensor Tensor::mul(const Tensor &other)
{
    if (m_cols != other.m_rows) {
        throw std::invalid_argument("Invalid dimensions for matrix multiplication");
    }
    Tensor res(m_rows, other.m_cols);
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < other.m_cols; j++) {
            for (int k = 0; k < m_cols; k++) {
                res.mat[i][j] += mat[i][k] * other.mat[k][j];
            }
        }
    }
    return res;
}

double Tensor::sum()
{
    double tot = 0;
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            tot += mat[i][j];
        }
    }
    return tot;
}

Tensor Tensor::sum(int dim)
{
    if (dim == 0)
    {
        Tensor res = zeros(1, m_cols);
        for (int i = 0; i < m_rows; i++) {
            for (int j = 0; j < m_cols; j++) {
                res.mat[0][j] += mat[i][j];
            }
        }
        return res;
    }
    else if (dim == 1)
    {
        Tensor res = zeros(m_rows, 1);
        for (int i = 0; i < m_rows; i++) {
            for (int j = 0; j < m_cols; j++) {
                res.mat[i][0] += mat[i][j];
            }
        }
        return res;
    }
    else throw std::out_of_range("sum error: tensor size dim is neither 0 or 1");
}

Tensor mul(Tensor A, Tensor B)
{
    return A.mul(B);
}

void Tensor::apply(std::function<double(double)> func)
{
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            mat[i][j] = func(mat[i][j]);
        }
    }
}

Tensor Tensor::after(std::function<double(double)> func)
{
    Tensor res = zeros(m_rows, m_cols);
    for (int i = 0; i < m_rows; i++) {
        for (int j = 0; j < m_cols; j++) {
            res.mat[i][j] = func(mat[i][j]);
        }
    }
    return res;
}

Tensor zeros(int rows, int cols)
{
    return Tensor(rows, cols, 0);
}

Tensor ones(int rows, int cols)
{
    return Tensor(rows, cols, 1);
}

Tensor tensor(int rows, int cols, double val)
{
    return Tensor(rows, cols, val);
}

Tensor tensor(const std::vector<std::vector<double>> &M)
{
    return Tensor(M);
}

Tensor rands(int rows, int cols, double range)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dis(-range, range);
    std::vector<std::vector<double>> M(rows, std::vector<double>(cols));
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            M[i][j] = dis(gen);
        }
    }
    Tensor Res(M);
    return Res;
}

void print(Tensor X)
{
    std::ios old_fmt(nullptr);
    old_fmt.copyfmt(std::cout);
    std::pair<int, int>siz = X.size();
    int r = siz.first, c = siz.second;
    if (r == 0 || c == 0) {
        std::cout << "Error!" << std::endl;
        return;
    }
    std::vector<std::vector<double>> M = X.get_matrix();
    std::cout << "Tensor(" << r << "," << c << "):" << std::endl;
    for (int i = 0; i < r; i++) {
        std::cout << '[';
        for (int j = 0; j < c; j++) {
            std::cout << std::setw(6) << std::fixed << std::setprecision(2) << M[i][j];
            if (j != c - 1) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
    std::cout.copyfmt(old_fmt);
}

void print(std::pair<int, int> P)
{
    std::cout << '(' << P.first << "," << P.second << ')' << std::endl;
}

void print(double x)
{
    std::cout << x << std::endl;
}

#endif