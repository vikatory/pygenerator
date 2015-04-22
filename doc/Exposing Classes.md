#导出类
> * 构造函数
> * 类数据成员
> * 类属性
> * 继承
> * 类虚函数
> * 使用默认实现的虚函数
> * 类操作符/特殊函数

------

现在让我们导出C++类到Python.
思考一个我们要导出到Python的C++类/结构体:

```c++
struct World
{
    void set(std::string msg) { this->msg = msg; }
    std::string greet() { return msg; }
    std::string msg;
};
```

我们可以通过写相应的Boost.Python C++封装将他导出到Python:
```c++
#include <boost/python.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(hello)
{
    class_<World>("World")
        .def("greet", &World::greet)
        .def("set", &World::set)
    ;
}
```

这里, 我们写了一个greet和set的C++类封装. 现在, 在构建模块作为共享库后, 我们可以在Python中使用我们的类. 下面是一个Python会话示例:

```python
>>> import hello
>>> planet = hello.World()
>>> planet.set('howdy')
>>> planet.greet()
'howdy'
```

##构造函数

Our previous example didn't have any explicit constructors. Since World is declared as a plain struct, it has an implicit default constructor. Boost.Python exposes the default constructor by default, which is why we were able to write


