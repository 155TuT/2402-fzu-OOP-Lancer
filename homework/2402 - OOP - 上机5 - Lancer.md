---
link: https://pintia.cn/problem-sets/1917909441679470592/exam/problems/type/1
---
### 2402 - OOP - 上机5 - Lancer

------

#### 判断题

1. 友元函数不是类的成员函数，只是独立于该类的一般函数。(T)
2. 静态成员函数可以访问非静态成员函数。(F)
3. 抽象类可以被直接实例化，但是它的纯虚函数必须在派生类中被重写。(F)
4. 下面两个函数构成函数重载。(F)
   int Add(int a, int b) {return a+b;}

   double Add(int x, int y) {return x*y;}
5. 若一个类中没有定义构造函数，编译器会为其自动生成默认构造函数。(T)
6. 在 C++ 中，静态成员变量可以在类体内直接初始化，无需在类外部进行。(F)
7. 函数模板的所有模板参数类型必须相同。(F)
8. 成员函数形式的运算符重载不需要通过对象来调用。(F)
9. 面向对象编程（OOP）相比于面向过程编程的一个主要优点是它可以增加代码的复用性、灵活性和扩展性，从而更适合大规模软件开发。(T)
10. C++中的引用是对一个对象起了别名，且必须初始化。(T)

------

#### 单选题

1. 在 C++ 中，使用虚基类主要是为了解决哪一种继承中的特定问题？（C）

   A. 增强派生类的封装性

   B. 允许在多个派生类中共享同一基类的方法

   **C. 防止当多个类继承自同一个基类时，基类数据被多次复制的问题**

   D. 允许派生类重写所有基类的方法

2. 在C++中，关于引用和指针的说法，以下哪个是错误的？（C）

   A. 引用必须在声明时初始化

   B. 引用一旦初始化后，不能再指向其他对象

   **C. 引用和指针在内存中的存储方式是一样的**

   D. 引用在语法上可以被视为变量的别名

3. 如果一个基类的指针指向了一个派生类的对象，那么调用的是哪个类的成员函数？（C）

   A. 基类

   B. 派生类

   **C. 取决于函数是否为虚函数**

   D. 无法确定

4. 在C++中，运算符重载的主要目的是(  )。（C）

   A. 改变运算符的优先级

   B. 减少代码量

   **C. 允许用户为自定义类型定义运算符的行为**

   D. 提高程序的执行速度

5. 在 C++ 中，哪种继承方式确保基类的公有成员在派生类及其后代类中不能被外部访问，且这些后代类也无法访问这些成员？（B）

   A. 公有继承

   **B. 私有继承**

   C. 保护继承

   D. 虚拟继承

6. 类模板的主要目的是什么？（B）

   A. 提高代码的可读性

   **B. 促进代码的重用**

   C. 实现运行时多态

   D. 所有答案都不正确

7. 关于友元的描述中，（）是错误的。（A）

   **A. 友元函数是成员函数，它被说明在类体内**

   B. 友元函数可直接访问类中的私有成员

   C. 友元函数破坏了封装性，使用时尽量少用

   D. 友元类中的所有成员函数都是友元函数

8. 在C++中，使用new运算符动态创建的对象应如何释放？（A）

   **A. 使用delete运算符。**

   B. 使用free()函数。

   C. 对象会在程序结束时自动释放。

   D. 无法释放动态创建的对象。

9. 关于抽象类，以下描述中正确的是（     ）。（D）

   A. 一个包含至少一个纯虚函数的类

   B. 一个不能被实例化的类

   C. 一个没有数据成员的类

   **D. A和B都正确**

10. 常对象的特点不包括：（D）

   A. 不能修改成员变量

   B. 可以调用常成员函数

   C. 不能调用非常成员函数

   **D. 不能被复制**


------

#### 程序填空题

1.（2024Final）篮球运动员管理 (程序填空题)

以下C++程序，展示了一个简单的篮球球员类`BasketballPlayer`的实现。该类的成员包括球员姓名（name）、球衣号码（jerseyNumber）和位置（position），以及构造函数、展示球员信息的成员函数、更新位置的成员函数以及析构函数。

现在，你需要完成下面的每个填空题，以完善该程序功能：

样例程序：

```c++
#include <iostream>
#include <string>
// 引入需要的名字空间
/*（using namespace std;）（2分）*/

class BasketballPlayer {
// 私有成员
/*（private:）（2分）*/
    string name;
    int jerseyNumber;
    string position;

// 公共成员
/*（public:）（1分）*/
    // 构造函数
    BasketballPlayer(string playerName, int number, string pos)
       /*（: name(playerName), jerseyNumber(number), position(pos) {）（1分）*/  // 用参数初始化表，初始化相关参数
        cout << "Basketball player " << name << " created." << endl;
    }

    // 成员函数，用于展示球员信息
    void displayPlayerInfo() const {
        cout << "Name: " << name << endl;
        cout << "Jersey Number: " << jerseyNumber << endl;
        cout << "Position: " << position << endl;
    }

    // 使用this指针更新球员位置position为newPos
    void updatePosition(string newPos) {
        /*（this->position = newPos;）（1分）*/
    }

    // 析构函数
    /*（~BasketballPlayer() {）（1分）*/
        cout << "Information of " << name << " is destroyed." << endl;
    }
};

int main() {
    BasketballPlayer player1("Yao", 11, "Center");
    BasketballPlayer player2("Wang", 15, "Forward");

    cout << "
Player Information:
";
    // 输出第一位球员信息
    /*（player1.displayPlayerInfo();）（1分）*/
    // 输出第二位球员信息
    /*（player2.displayPlayerInfo();）（1分）*/

    // 更新球员位置
    player2.updatePosition("Guard");

    cout << "
Updated Player Information:
";
    player1.displayPlayerInfo();
    player2.displayPlayerInfo();

    return 0;
}
```

2.A Fill in the blanks

```
#include <iostream>
using namespace std;
class IndexError{};
template /*（<class T>）（2分）*/
class ARRAY
{
	size_t m_size;
	T *m_ptr;
public:
	ARRAY(size_t size) : m_size(size)
	{
		m_ptr = new T[size];
		memset(m_ptr, 0, size*sizeof(int));
	}
	~ARRAY()
	{
		delete[] m_ptr;
	}
	T& at(int index);
};

template <typename T>
/*（T& ARRAY<T>）（2分）*/::at(int index)
{
	if(index<0||/*（index >= m_size）（2分）*/)
	{
		/*（throw）（2分）*/ IndexError();
	}
	return m_ptr[index];
}

int main()
{
	ARRAY<int> a(50);
	int i;
	cin >> i;
	/*（try）（2分）*/
    {
		for(int j=0;j<i;j++)
			a.at(i) = j;
	}
	catch(IndexError e)
	{
		return 0;
	}
	return 0;
}
```


------

#### 函数题

##### 1.（2024Final）小组投篮计分程序

有若干个人组成一个小队参加投篮比赛，投篮比赛分前后两个批次进行。第一个批次已经完成，考生需要设计一个统计第二个批次小组成员得分，并计算小队两个批次投篮平均命中数（计算公式：两个批次总人数/两个批次总得分）的程序。**Member**类中包含每个人的投篮命中个数，其部分代码如下：
**Member类的部分定义如下：**
```c++
class Member {
public:
void setShot(int _shot);
/* 你编写的代码将被嵌入这里*/
```
请根据题意将代码补充完整（包括Member类的代码及类外部分的代码），以输出一个小队投完篮后的平均进球数（注：输出形式为cout << std::setprecision(2)<<(自定义的输出变量)）。
**裁判测试程序样例：**
```c++
#include
#include
using namespace std;
class Member {
public:
void setShot(int _shot);
/* 你编写的代码将被嵌入这里*/
//读取n个小组成员的投篮命中数
void read(Member mem[], int n) {
int shot;
for (int i = 0; i < n; i++) {
cin >> shot;
mem[i].setShot(shot);
}
}
int main() {
int n;
cin >> n; ////输入第二批次将参与的投篮的人数
cin >> Member::totalShot; //输入小组第一批成员投篮命中的总数（单位：个）
cin >> Member::numMember; //输入小组第一批投篮的成员数（第一批完成比赛成员数>0，单位：人）
Member::printTotal(); //输出小组已完成比赛成员投篮命中数的总和（当前输出第一批比赛成员的投篮命中数总和）
Member *m = new Member[n];
read(m, n);
Member::printTotal(); //输出小组已完成比赛成员投篮命中数的总和（输出两个批次所有成员投篮命中数的总和）
Member::printAVG(); //输出小组投篮平均命中数（计算公式：两个批次总人数/两个批次总得分）
delete[] m;
return 0;
}
```
**输入样例：**
在这里给出一组输入。例如：
```in
2
5
4
1
6
```
**输出样例：**
在这里给出相应的输出（注意此题输出与输入穿插，这里隐去了输入部分）：
```out
5
12
2
```

**code:**

```c++
    static int totalShot;
    static int numMember;
    static void printTotal() {
        cout << totalShot << endl;
    }
    static void printAVG() {
        double avg = static_cast<double>(totalShot) / numMember;
        cout << setprecision(2) << avg << endl;
    }
};
int Member::totalShot = 0;
int Member::numMember = 0;
void Member::setShot(int _shot) {
    totalShot += _shot;
    numMember++;
}
```

##### 2.（2024Final）打印学生成绩

定义一个学生类，定义一个友元教师类，使得教师可以访问学生的私有成绩，打印所有学生信息,同时找出最高分学生并按输入顺序输出学生信息。
###
**裁判测试程序样例：**
```c++
#include
using namespace std;
/* 请在这里填写答案 */
int main()
{
Student stu[50];
int n,i;
string Sname,Tname;
int score;
cin>>n;
for(i=0;i> Sname >> score;
stu[i].set(Sname, score);
}
cin>>Tname;
Teacher t(Tname);
t.print(stu,n);
return 0;
}
```
**输入样例：**
在这里给出一组输入。例如：
```in
3
Zhao 92
Wang 88
Yu 95
Li
```
**输出样例：**
在这里给出相应的输出。例如：
```out
Zhao 92
Wang 88
Yu 95
The Students with the highest score:
Yu 95
```

**code:**

```c++
class Student {
private:
    string name;
    int score;
public:
    void set(string n, int s) {
        name = n;
        score = s;
    }
    friend class Teacher;
};
class Teacher {
private:
    string tname;
public:
    Teacher(string name) : tname(name) {}
    void print(Student stu[], int n) {
        for (int i = 0; i < n; i++) cout << stu[i].name << " " << stu[i].score << endl;
        int max_score = -1;
        for (int i = 0; i < n; ++i) {
            if (stu[i].score > max_score) {
                max_score = stu[i].score;
            }
        }
        cout << "The Students with the highest score:" << endl;
        for (int i = 0; i < n; i++) if (stu[i].score == max_score) cout << stu[i].name << " " << stu[i].score << endl;
    }
};
```

##### 3.数组排序输出（函数模板）

对于输入的每一批数，按从小到大排序后输出。
一行输入为一批数，第一个输入为数据类型（1表示整数，2表示字符型数，3表示有一位小数的浮点数，4表示字符串，0表示输入结束），第二个输入为该批数的数量size（0
void sort(T *a, int size)；
```
**裁判测试程序样例：**
```c++
#include
#include
using namespace std;
/* 请在这里填写答案 */
template
void display(T* a, int size){
for(int i=0; i>ty;
while(ty>0){
cin>>size;
switch(ty){
case 1:sort(a,size); display(a,size); break;
case 2:sort(b,size); display(b,size); break;
case 3:sort(c,size); display(c,size); break;
case 4:sort(d,size); display(d,size); break;
}
cin>>ty;
}
return 0;
}
```
**输入样例：**
```in
1 3 3 2 1
2 2 a A
3 3 1.5 2.6 2.2
4 2 bca abc
0
```
**输出样例：**
```out
1 2 3
A a
1.5 2.2 2.6
abc bca
```

**code:**

```c++
template <class T>
void sort(T *a, int size) {
    for (int i = 0;i < size; i++) cin >> a[i];
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - 1 - i; j++) {
            if (a[j] > a[j + 1]) {
                T temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
}
```


------

#### 编程题

##### 1.（2024Final）车类的派生与继承

**题目描述:**
设计一个基类 **`Car`** 和两个派生类 **`Sedan`** 和 `SUV`。基类 **`Car`** 包含私有成员 `brand`（品牌）和 `year`（年份），以及一个公共的构造函数，该构造函数接收两个参数用于初始化 **`brand`** 和 **`year`。**`Car` 类还应包含一个析构函数，用于输出一条销毁消息。
派生类 **`Sedan`** 和 **`SUV`** 每个都包含额外的特定属性`attribute`。例如，`Sedan`有一个 `trunkSize`（行李箱容量）成员，而 **`SUV`** 有一个 `seatCount`（座位数）成员。每个派生类都需要一个构造函数，用于接收自己特有的属性以及传递给基类构造函数的属性。此外，派生类还需一个析构函数，用于提升该类已被销毁。主函数已给出，请根据“任务”编写完整代码：
**主函数**
```
#include
#include
#include
using namespace std;
int main() {
string brands[2] = { "Toyota", "Ford" };
string line;
int typeIndex, brandIndex, year, attribute;
int n;
Car myCar = Car("BYD", 2020);
cin >> n;
cin.ignore(); // 舍弃换行符
for (int i = 0; i < n; i++) {
getline(cin, line); //读取一行输入数据
istringstream iss(line);
iss >> typeIndex >> brandIndex >> year >> attribute;
string brand = brands[brandIndex];
if (typeIndex == 0) { // Sedan
Sedan sedan(brand, year, attribute);
}
else if (typeIndex == 1) { // SUV
SUV suv(brand, year, attribute);
}
}
}
```
**任务:**
1. 定义基类 **`Car`** 和派生类 `Sedan`**、**`SUV`。
2. 为每个类编写构造函数和析构函数。
3. 构造函数应输出车的基本信息。
4. 析构函数应输出一个销毁消息，表明哪种车型被销毁。
**输入格式:**
用户需要输入多行数据，第一行为接下来输入的行数n，之后输入n行，每行代表一个车辆。其数据包括以下四种信息，不同信息之间通过空格隔开：
1. 车辆类型编号：`0` 代表 **`Sedan`，**`1` 代表 **`SUV`**
2. 品牌编号：`0` 代表 **`Toyota`，**`1` 代表 **`Ford`**
3. 年份：如 **`2021`、**`2022` 等
4. 特定属性：对于 **`Sedan`** 是行李箱容量（整数，单位：升），对于 **`SUV`** 是座位数（整数）
**输出格式:**
程序的输出应包含以下信息：
1. **车辆创建时**：
* 对每一个 **`Car`** 对象，输出格式为：`Car  () created.`
* 对每一个 **`Sedan`** 对象，输出格式为：`Sedan with trunk size  liters created.`
* 对每一个 **`SUV`** 对象，输出格式为：`SUV with  seats created.`
2. **车辆销毁时**：
* 对每一个 **`SUV`** 对象，输出格式为：`SUV destroyed.`
* 对每一个 **`Sedan`** 对象，输出格式为：`Sedan destroyed.`
* 对每一个 **`Car`** 对象，输出格式为：`Car  destroyed.`
**输入样例：**
```in
2
0 0 2021 480
1 1 2022 7
```
**输出样例:**
在这里给出相应的输出（注意此题输出与输入穿插，这里隐去了输入部分）：
```out
Car BYD (2020) created.
Car Toyota (2021) created.
Sedan with trunk size 480 liters created.
Sedan destroyed.
Car Toyota destroyed.
Car Ford (2022) created.
SUV with 7 seats created.
SUV destroyed.
Car Ford destroyed.
Car BYD destroyed.
```

**code:**

```c++
#include <iostream>
#include <string>
#include <sstream>
using namespace std;
class Car {
private:
    string brand;
    int year;
public:
    Car(string b, int y) : brand(b), year(y) {
        cout << "Car " << brand << " (" << year << ") created." << endl;
    }
    ~Car() {
        cout << "Car " << brand << " destroyed." << endl;
    }
};
class Sedan : public Car {
private:
    int trunkSize;
public:
    Sedan(string b, int y, int ts) : Car(b, y), trunkSize(ts) {
        cout << "Sedan with trunk size " << trunkSize << " liters created." << endl;
    }
    ~Sedan() {
        cout << "Sedan destroyed." << endl;
    }
};
class SUV : public Car {
private:
    int seatCount;
public:
    SUV(string b, int y, int sc) : Car(b, y), seatCount(sc) {
        cout << "SUV with " << seatCount << " seats created." << endl;
    }
    ~SUV() {
        cout << "SUV destroyed." << endl;
    }
};
int main() {
    string brands[2] = { "Toyota", "Ford" };
    string line;
    int typeIndex, brandIndex, year, attribute;
    int n;
    Car myCar = Car("BYD", 2020);
    cin >> n;
    cin.ignore();
    for (int i = 0; i < n; i++) {
        getline(cin, line);
        istringstream iss(line);
        iss >> typeIndex >> brandIndex >> year >> attribute;
        string brand = brands[brandIndex];
        if (typeIndex == 0) Sedan sedan(brand, year, attribute);
        else if (typeIndex == 1) SUV suv(brand, year, attribute);
    }
}
```

##### 2.立方体类

定义立方体类Box，数据成员有长宽高且都是整数，构造函数初始化数据成员，成员函数计算体积，主函数中输入长宽高，输出立方体体积。

**输入格式:**

输入立方体的长宽高，中间用空格分隔。

**输出格式:**

输出体积并换行。

**输入样例:**

在这里给出一组输入。例如：

```in
1 2 3
```

**输出样例:**

在这里给出相应的输出。例如：

```out
6
```

**code:**

```c++
#include <iostream>
using namespace std;
class Box {
private:
    int length, width, height;
public:
    Box(int l, int w, int h) : length(l), width(w), height(h) {}
    int volume() {
        return length * width * height;
    }
};
int main() {
    int l, w, h;
    cin >> l >> w >> h;
    Box box(l, w, h);
    cout << box.volume() << endl;
    return 0;
}
```

##### 3.复数的比较

题目描述：建立一个复数类，实数和虚数是其私有数据成员。建立一个>（大于号）的运算符重载，比较两个复数间模的大小。

输入格式：测试输入包含若干测试用例，每个测试用例占一行。每个测试用例包括四个数字，前两个数字分别表示第一个复数的实部和虚部，第三个和第四个数字分别表示第二个复数的实部和虚部。每个数字之间用空格间隔。当读入一个测试用例是0 0 0 0时输入结束，相应的结果不要输出。

输出格式：对每个测试用例输出一行。当第一个复数的模大于第二个复数的模时，输出 true ，当第一个复数的模小于或等于第二个复数的模时，输出false

输入样例：

　　　3 5 4 0

　　　0 3 4 1

　　　0 0 0 0

输出样例：

　　　true

　　　false

**code:**

```c++
#include <iostream>
using namespace std;
class Complex {
private:
    int real;
    int imag;
public:
    Complex(int r, int i) : real(r), imag(i) {}
    bool operator>(const Complex &other) const {
        int mod1 = real * real + imag * imag;
        int mod2 = other.real * other.real + other.imag * other.imag;
        return mod1 > mod2;
    }
};
int main() {
    int a, b, c, d;
    while (cin >> a >> b >> c >> d) {
        if (a == 0 && b == 0 && c == 0 && d == 0) break;
        Complex c1(a, b), c2(c, d);
        cout << (c1 > c2 ? "true" : "false") << endl;
    }
    return 0;
}
```


------
