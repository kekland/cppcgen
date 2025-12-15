namespace shadow_synthetic_field {
class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;

  void setValueWord(int v);

  int valueWord;
};
}