template <typename T>
struct ref {
 public:
  ref() : ptr(std::make_shared<T>()) {}
  explicit ref(T* v) : ptr(v, [](T* v) {}) {}
  ref(const T& v) : ptr(std::make_shared<T>(v)) {}
  ref(T&& v) : ptr(std::make_shared<T>(std::move(v))) {}
  explicit ref(std::shared_ptr<T> v) : ptr(std::move(v)) {}
  explicit ref(std::unique_ptr<T> v) : ptr(std::move(v)) {}

  T& get() { return *ptr; }
  T* unwrap() { return ptr.get(); }

  std::shared_ptr<T> as_shared() { return ptr; }
  std::unique_ptr<T> as_unique() {
    if (ptr.use_count() != 1) return nullptr;
    auto unique = std::make_unique<T>(std::move(*ptr));
    ptr.reset();
    return unique;
  }

 private:
  std::shared_ptr<T> ptr;
};

template <typename CType, typename CppType>
struct ffi_cv {
  inline static CType* wrap(CppType* ref_ptr) { return reinterpret_cast<CType*>(ref_ptr); }
  inline static CType* wrap(CppType& ref) { return reinterpret_cast<CType*>(&ref); }
  inline static CppType* unwrap(void* raw) { return reinterpret_cast<CppType*>(raw); }
};
