#ifndef TOOLS_HPP
#define TOOLS_HPP
#include "tensor.hpp"

namespace tools
{
    std::vector<std::pair<Tensor, Tensor>> DataLoader(std::vector<std::pair<std::vector<double>, std::vector<double>>> data, int batch_size, bool shuffle = false)
    {
        if (shuffle == true)
        {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::shuffle(data.begin(), data.end(), gen);
        }
        std::vector<std::pair<Tensor, Tensor>> data_iter;
        int tot_size = data.size();
        for (int i = 0; i < tot_size; i += batch_size)
        {
            std::vector<std::vector<double>> features, labels;
            for (int j = i; j < std::min(i + batch_size, tot_size); j++)
            {
                features.push_back(data[j].first);
                labels.push_back(data[j].second);
            }
            Tensor features_tensor(features);
            Tensor labels_tensor(labels);
            data_iter.push_back(std::make_pair(features_tensor, labels_tensor));
        }
        return data_iter;
    }
}
#endif