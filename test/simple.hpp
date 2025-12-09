#include <print>

namespace simple {

enum class Color {
  Red,
  Green,
  Blue,
};

enum class Size {
  Small,
  Medium,
  Large,
};

struct MyStruct {
  int x;
  float y;
  bool z;
};

class MyClass {
 public:
  MyClass();
  ~MyClass();

  void voidMethod();
  int intMethod(int param);
  float floatMethod(float param1, float param2);
  double doubleMethod(double param1, double param2, double param3);
  char charMethod(char param);

  void* voidPtrMethod(void* param);
  int* intPtrMethod(int* param);

  Color colorMethod(Color color);
  Size sizeMethod(Size size);

  int getValue() const;
  void setValue(int value);

  void hello(simple::MyClass* other);

  void a() {}
};
}  // namespace simple
