def replace_chars(string, k):
    result = []
    seen = set()
    for i, char in enumerate(string):
        if char in seen:
            result.append('-')
        else:
            result.append(char)
            seen.add(char)
        if i >= k:
            seen.discard(string[i - k + 1])
    return ''.join(result)


def main():
    input_str = input("请输入字符串：")
    k = int(input("请输入k值："))
    output_str = replace_chars(input_str, k)
    print("Input:", input_str, k)
    print("Output:", output_str)


if __name__ == '__main__':
    main()
# # 测试样例
# input_str = "abcdefaxc"
# k = 10
# output_str = replace_chars(input_str, k)
# print("Input:", input_str)
# print("Output:", output_str)
#
# input_str = "abcdefaxcqwertba"
# output_str = replace_chars(input_str, k)
# print("Input:", input_str)
# print("Output:", output_str)
