#include "include/tenet.hpp"
#include "include/tools.hpp"
using namespace std;

class Simple_Model : public nn::Module
{
public:
    nn::Linear fc1 = nn::Linear(5, 8);
    nn::Linear fc2 = nn::Linear(8, 1);
    Simple_Model()
    {
        register_layer(fc1);
        register_layer(fc2);
    }
    Telo forward(Telo x)
    {
        x = fc1.forward(x);
        x = fc2.forward(x);
        return x;
    }
};

double func(double a, double b, double c, double d, double e)
{
    return 2 * a + 0.1 * exp(b) + 3 * c + 0.3 * d * d + 2;
}

vector<pair<vector<double>, vector<double>>> get_data(int tot_num)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> r1(0, 3);
    normal_distribution<double> r2(0, 0.2);
    vector<pair<vector<double>, vector<double>>> res;
    for (int i = 0; i < tot_num; i++)
    {
        double a = r1(gen), b = r1(gen), c = r1(gen), d = r1(gen), e = r1(gen);
        double f = func(a, b, c, d, e) + r2(gen);
        vector<double> features, labels;
        features.push_back(a);
        features.push_back(b);
        features.push_back(c);
        features.push_back(d);
        features.push_back(e);
        labels.push_back(f);
        res.push_back(make_pair(features, labels));
    }
    return res;
}

int main()
{
    int num_epoch = 10, batch_size = 32;
    double lr = 0.005;
    vector<pair<vector<double>, vector<double>>> data = get_data(400);
    auto train_iter = tools::DataLoader(data, batch_size, true);
    Simple_Model model;
    nn::MSELoss criterion;
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
}