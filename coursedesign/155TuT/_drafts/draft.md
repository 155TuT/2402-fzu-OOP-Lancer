---
title: 草稿
date: 2025/03/16 23:49:00
---
## 基础

### 效果

前缀数组中的区间运算（和，积）同时满足**结合律**和**可逆性**时，可通过预处理将区间查询复杂度降至O(1)。前缀差分则特殊处理差商/逆运算关系，通过**构造增量数组**优化区间更新。

### 核心

找到运算的**代数结构特征**（结合律/可逆性/同余性）来构造中间状态：当目标运算满足结合律时，可构造累积结构加速区间查询（如和/积）；当运算存在逆元时，可构造差分结构优化区间更新（如加减/异或）。

### 本质

**预处理**思想在代数系统中的应用。通过预处理将运算的代数性质转化为时空效率的优化，对模运算、矩阵乘法等具备代数结构的操作同样适用。

------

### 时间复杂度

|                     | 区间查询 | 单点查询 | 区间修改 |
| ------------------- | -------- | -------- | -------- |
| 前缀和/积           | O(1)     | O(1)     | O(n)     |
| 差分                | O(n)     | O(n)     | O(1)     |
| ~~树状数组/线段树~~ | O(logn)  | O(logn)  | O(logn)  |

## coding

### 前缀和

#### 简单构建：partial_sum

```c++
#include <numeric>//不在algorithm中
#include <vector>
vector<int> arr(n);//原数组
vector<int> prefix(n);//前缀和数组
partial_sum(arr.begin(), arr.end(), prefix.begin());//正常格式

partial_sum(arr.begin(), arr.end(), arr.begin());//直接覆盖
```

~~太过简单，在这个过程中基本不需要，但是后面会有用~~

#### 查询：下标特判或从1开始

```c++
sum(L, R) = prefix[R] - prefix[L - 1];//会越界

auto presum = [&](int l, int r){
    return l ? prefix[r] - prefix[l - 1] : prefix[r];//特判
}

arr.insert(arr.begin(), 0);//下标从1开始
partial_sum(arr.begin(), arr.end(), prefix.begin());//刚刚好
```

### 前缀积

```c++
mul(L, R) = prefix[R] / prefix[L - 1];//超过64个2就会溢出，基本只能高精度，用处不大
```

但日常使用还是取模居多，因此乘法逆元便成了需要用到的逆运算

```c++
const int mod = 1e9 + 7;//假设mod为质数
int qpow(int a, int k){
    int res = 1;
    while(k){
        if(k & 1)res = 1LL * res * a % mod;
        a = 1LL * a * a % mod;
        k >>= 1;
    }
    return res;
}

vector<int> prefix, inv_prefix;

void build(const vector<int>& arr){
    int n = arr.size();
    prefix.resize(n + 1, 1);
    for(int i = 0; i < n; i++) 
        prefix[i + 1] = 1LL * prefix[i] * arr[i] % mod;
    inv_prefix.resize(n + 1, 1);
    inv_prefix[n] = qpow(prefix[n], mod -  2);//计算整体逆元
    for(int i = n - 1; i >= 0; i--)//逆向递推局部逆元
        inv_prefix[i] = 1LL * inv_prefix[i + 1] * arr[i] % mod;
}

int query(int l, int r){//闭区间[l, r]，0-based索引
    return 1LL * prefix[r + 1] * inv_prefix[l] % mod;
}
```

### 前缀异或

异或的逆运算是其本身，~~太方便啦~~

```c++
xor(L, R) = prefix[R] ^ prefix[L - 1];//注意不取任何元素的前缀是0，少了会漏统计

partial_sum(arr.begin(), arr.end(), xorarr.begin(), [](int prev, int cur){return prev ^ cur;});
```

partial_sum的第四个参数可以接受一个二元操作函数表示如何进行统计，其中prev是已统计的结果，cur是当前元素，因此非累加运算也可通过这样的方式编写。

### 二维前缀及多维前缀

容斥原理来理解即可

```c++
sum(x1, y1, x2, y2) = p[x2][y2] - p[x2][y1-1] - p[x1 - 1][y2] + p[x1 - 1][y1 - 1];
```

### 推广：普遍前缀

前缀只是表示从开始到当前位置的运算结果，因此没有逆运算的运算也可以做前缀数组来预处理，只是无法求解区间问题

~~以及后缀~~

## end

树状数组和线段树在面对大部分题目时都是更优的，但学习前缀思想对培养算法思维是不可或缺的一环。~~才不是这周时间不够还没复习~~

[原文链接](https://155tut.github.io/2025/03/16/partial-sum/)
