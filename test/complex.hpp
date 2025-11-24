#include <string>

namespace complex {

enum class Status { Ok, Error, Unknown };

class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;
  MyClass(std::string data, std::optional<int> optional_value)
      : data(std::move(data)), optional_value(std::move(optional_value)) {}

  std::string concat(const std::string& str1, const std::string& str2);
  std::string repeat(const std::string& str, int times);
  std::string to_upper(const std::string& str);

  std::vector<std::string> split(const std::string& str, char delimiter);
  std::vector<int> parse_numbers(const std::string& str);

  std::optional<std::string> find_substring(const std::string& str, const std::string& substr);
  std::vector<std::vector<int>> nested_vector(const std::vector<std::vector<int>>& vec);

  std::optional<int> maybe_get_number(bool return_number);

  std::array<int, 10> create_array();

  std::pair<int, std::string> create_pair(int number, const std::string& text);

  std::optional<complex::Status> get_status(bool valid);

  std::vector<int> getNumbers() const;
  void setNumbers(const std::vector<int>& numbers);

  std::string data;
  std::optional<int> optional_value;
};
}  // namespace complex