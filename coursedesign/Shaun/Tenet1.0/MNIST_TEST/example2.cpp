#include <iostream>
#include <bits/stdc++.h>
#include "include/mnist_reader.hpp"
#include "include/mnist_utils.hpp"
#include "../include/tenet.hpp"
using namespace std;
using namespace nn;
using namespace tools;

void get_data(std::vector<std::pair<std::vector<double>, std::vector<double>>> &res, bool show_data = false)
{
    /*
    struct Dataset {
        std::vector<std::vector<double>> training_images; // 训练图片 (double 类型，每个像素存为 double)
        std::vector<uint8_t> training_labels;             // 训练标签 (uint8_t 类型，值范围 0~9)
        std::vector<std::vector<double>> test_images;     // 测试图片 (double 类型)
        std::vector<uint8_t> test_labels;                 // 测试标签 (uint8_t 类型)
    };
    */
    auto dataset = mnist::read_dataset<std::vector, std::vector, double, uint8_t>("dataset");
    mnist::normalize_dataset(dataset);
    if (show_data)
    {
        cout << "show labels:" << endl;
        std::vector<uint8_t> labels = dataset.training_labels;
        for (int i = 0; i < 20; i++) {
            double num = static_cast<int>(labels[i]);
            cout << num << " ";
        }
        cout << endl;
        cout << "show img:" << endl;
        std::vector<double> img = dataset.training_images[0];
        std::ios old_fmt(nullptr);
        old_fmt.copyfmt(std::cout);
        for (int i = 0; i < 28 * 28; i += 28) {
            for (int j = i; j < i + 28; j++) {
                cout << setw(4) << fixed << setprecision(1) << img[j] << " ";
            }
            cout << endl;
        }
        std::cout.copyfmt(old_fmt);
    }
    auto tr_imgs = dataset.training_images;
    auto tr_labs = dataset.training_labels;
    cout << "start loading_data" << endl;
    for (int i = 0; i < 10000; i++)
    {
        std::pair<std::vector<double>, std::vector<double>> temp_res;
        double num = static_cast<int>(tr_labs[i]);
        vector<double> label;
        label.push_back(num);
        vector<double> feature = tr_imgs[i];
        res.push_back(make_pair(feature, label));
    }
}

class Simple_Model : public nn::Module
{
public:
    nn::Linear fc1 = nn::Linear(784, 10);
    //nn::ReLU relu1 = nn::ReLU();
    //nn::Linear fc2 = nn::Linear(128, 10);
    //nn::ReLU relu2 = nn::ReLU();
    //nn::Linear fc3 = nn::Linear(64, 10);
    Simple_Model()
    {
        register_layer(fc1);
        //register_layer(fc2);
        //register_layer(fc3);
    }
    Telo forward(Telo x)
    {
        x = fc1.forward(x);
        //x = relu1.forward(x);
        //x = fc2.forward(x);
        //x = relu2.forward(x);
        //x = fc3.forward(x);
        return x;
    }
};

int main()
{
    int num_epoch = 15, batch_size = 64;
    double lr = 0.01;
    std::vector<std::pair<std::vector<double>, std::vector<double>>> dataset;
    get_data(dataset);
    cout << "loading_data finished" << endl;
    auto train_iter = tools::DataLoader(dataset, batch_size, true);
    Simple_Model model;
    nn::CrossEntropyLoss criterion;
    nn::SGD optimizer(model.parameters(), lr);
    for (int epoch = 1; epoch <= num_epoch; epoch++)
    {
        double tot_loss = 0;
        for (auto DATA : train_iter)
        {
            Tensor features = DATA.first, labels = DATA.second;
            Telo outputs = model(features);
            double loss = criterion(outputs, labels);
            optimizer.zero_grad();
            criterion.backward();
            optimizer.step();
            tot_loss += loss;
        }
        cout << "epoch[" << epoch << "] loss: " << tot_loss / train_iter.size() << endl;
    }
    return 0;
}