#ifndef TENET_HPP
#define TENET_HPP
#include "tensor.hpp"
#include "tools.hpp"

namespace functions {
    double ReLU(double x) {
        return (x > 0) ? x : 0;
    }
    double dReLU(double x) {
        return (x > 0) ? 1 : 0;
    }
    double Sigmoid(double x) {
        return 1.0 / (1.0 + exp(-x));
    }
    double dSigmoid(double x) {
        double s = Sigmoid(x);
        return s * (1 - s);
    }
    double square(double x) {
        return x * x;
    }
    double ln(double x) {
        return log(x);
    }
    std::vector<std::vector<double>> softmax(Tensor X) {
        int rows = X.size(0), cols = X.size(1);
        std::vector<std::vector<double>> res(rows, std::vector<double>(cols, 0));
        const std::vector<std::vector<double>> *p = X.get_mat_pointor();
        for (int i = 0; i < rows; i++) {
            double max_val = *max_element((*p)[i].begin(), (*p)[i].end()), sum = 0;
            for (int j = 0; j < cols; j++) {
                res[i][j] = exp((*p)[i][j] - max_val);
                sum += res[i][j];
            }
            for (int j = 0; j < cols; j++) {
                res[i][j] /= sum;
            }
        }
        return res;
    }
}

namespace nn {
    class Layer
    {
    public:
        bool requires_grad = true;
        std::vector<Tensor> params;
        std::vector<Tensor> grads;
        Layer* parent;
        std::shared_ptr<Tensor> inputs;
        virtual std::pair<Layer*, Tensor> forward(std::pair<Layer*, Tensor> P) {
            throw std::runtime_error("forward function NotImplemente");
        }
        virtual void backward(Tensor grad) {
            throw std::runtime_error("backward function NotImplemente");
        }
    };
    
    class Linear : public Layer
    {
    public:
        Linear(int input_size, int output_size)
        {
            requires_grad = true;
            params.push_back(rands(input_size, output_size, 0.1));
            grads.push_back(zeros(input_size, output_size));
            params.push_back(zeros(1, output_size));
            grads.push_back(zeros(1, output_size));
        }
        std::pair<Layer*, Tensor> forward(std::pair<Layer*, Tensor> P) override
        {
            parent = P.first;
            inputs = std::make_shared<Tensor>(P.second.get_matrix());
            Tensor outputs = mul(*inputs, params[0]) + params[1];
            return std::make_pair(this, outputs);
        }
        void backward(Tensor grad) override
        {
            grads[0] += (*inputs).T().mul(grad);
            grads[1] += grad.sum(0);
            if (parent != nullptr) parent->backward(mul(grad, params[0].T()));
        }
    };

    class ReLU : public Layer
    {
    public:
        ReLU() {
            requires_grad = false;
        }
        std::pair<Layer*, Tensor> forward(std::pair<Layer*, Tensor> P) override
        {
            parent = P.first;
            inputs = std::make_shared<Tensor>(P.second.get_matrix());
            Tensor outputs = (*inputs).after(functions::ReLU);
            return std::make_pair(this, outputs);
        }
        void backward(Tensor grad) override {
            if (parent != nullptr) parent->backward(grad.after(functions::dReLU));
        }
    };

    class Sigmoid : public Layer
    {
    public:
        Sigmoid() {
            requires_grad = false;
        }
        std::pair<Layer*, Tensor> forward(std::pair<Layer*, Tensor> P) override
        {
            parent = P.first;
            inputs = std::make_shared<Tensor>(P.second.get_matrix());
            Tensor outputs = (*inputs).after(functions::Sigmoid);
            return std::make_pair(this, outputs);
        }
        void backward(Tensor grad) override {
            if (parent != nullptr) parent->backward(grad.after(functions::dSigmoid));
        }
    };

    class MSELoss
    {
    public:
        int num = 0;
        Layer* parent;
        std::shared_ptr<Tensor> outputs, labels;
        double operator ()(std::pair<Layer*, Tensor> P, Tensor Y)
        {
            outputs = std::make_shared<Tensor>(P.second.get_matrix());
            labels = std::make_shared<Tensor>(Y.get_matrix());
            if ((*outputs).size(1) != 1 || Y.size(1) != 1) {
                throw std::invalid_argument("MSELoss Error: inputs' second dim size must be 1");
            }
            if ((*outputs).size(0) != Y.size(0)) {
                throw std::invalid_argument("MSELoss Error: two inputs' size do not match");
            }
            parent = P.first;
            num = Y.size(0);
            Tensor temp = *outputs - Y;
            return temp.after(functions::square).sum() / (double)num;
        }
        void backward() {
            if (parent != nullptr) parent->backward((2.0 / (double)num) * ((*outputs) - (*labels)));
        }
    };

    class CrossEntropyLoss
    {
    public:
        int num = 0, cls = 0;
        Layer* parent;
        std::shared_ptr<Tensor> outputs, preds, labels;
        double operator ()(std::pair<Layer*, Tensor> P, Tensor Y)
        {
            outputs = std::make_shared<Tensor>(P.second.get_matrix());
            if (Y.size(1) != 1) {
                throw std::invalid_argument("CrossEntropyLoss Error: labels' second dim size must be 1");
            }
            if ((*outputs).size(0) != Y.size(0)) {
                throw std::invalid_argument("CrossEntropyLoss Error: two inputs' size do not match");
            }
            parent = P.first;
            num = Y.size(0), cls = outputs->size(1);
            preds = std::make_shared<Tensor>(functions::softmax(*outputs));
            labels = std::make_shared<Tensor>(num, cls, 0);
            for (int i = 0; i < num; i++) {
                int pos = round(Y(i, 0));
                if (pos < 0 || pos >= cls) {
                    throw std::out_of_range("CrossEntropyLoss Error: labels value out of range");
                }
                (*labels)(i, pos) = 1;
            }
            return -((*labels) * (*preds).after(functions::ln)).sum() / (double)num;
        }
        void backward() {
            if (parent != nullptr) parent->backward(*preds - *labels);
        }
    };

    class Module
    {
    private:
        std::vector<std::pair<Tensor*, Tensor*>> params;
    public:
        std::vector<std::pair<Tensor*, Tensor*>> parameters() {
            return params;
        }
        void register_layer(Layer &L)
        {
            if (L.requires_grad == false) return;
            for (int i = 0; i < L.params.size(); i++)
            {
                Tensor *param_pointer = &L.params[i];
                Tensor *grad_pointer = &L.grads[i];
                params.push_back(std::make_pair(param_pointer, grad_pointer));
            }
        }
        virtual std::pair<Layer*, Tensor> forward(std::pair<Layer*, Tensor> x)
        {
            throw std::runtime_error("Module Error: forward function NotImplemente");
        }
        std::pair<Layer*, Tensor> operator ()(Tensor inputs) {
            return forward(std::make_pair(nullptr, inputs));
        }
        void normal_init(double mean, double std_dev)
        {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::normal_distribution<double> dis(mean, std_dev); 
            for (auto P : params)
            {
                Tensor *param = P.first;
                int rows = (*param).size(0), cols = (*param).size(1);
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        (*param)(i, j) = dis(gen);
                    }
                }
            }
        }
        void uniform_init(double lower, double upper)
        {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_real_distribution<double> dis(lower, upper);
            for (auto P : params)
            {
                Tensor *param = P.first;
                int rows = (*param).size(0), cols = (*param).size(1);
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        (*param)(i, j) = dis(gen);
                    }
                }
            }
        }
    };

    class SGD
    {
    private:
        std::vector<std::pair<Tensor*, Tensor*>> parameters;
        double learning_rate, weight_decay;
    public:
        SGD(std::vector<std::pair<Tensor*, Tensor*>> p, double lr, double w_d = 0) : parameters(p), learning_rate(lr) {
            weight_decay = w_d;
        }
        void step()
        {
            for (auto P : parameters)
            {
                Tensor *param = P.first, *grad = P.second;
                int rows = (*param).size(0), cols = (*param).size(1);
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        (*param)(i, j) -= learning_rate * (*grad)(i, j) + weight_decay * (*param)(i, j);
                    }
                }
            }
        }
        void zero_grad()
        {
            for (auto P : parameters)
            {
                Tensor *grad = P.second;
                int rows = (*grad).size(0), cols = (*grad).size(1);
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        (*grad)(i, j) = 0.0;
                    }
                }
            }
        }
    };
}

using Telo = std::pair<nn::Layer*, Tensor>;
Tensor get_result(Telo P) { return P.second; }

#endif