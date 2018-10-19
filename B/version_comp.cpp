#include <iostream>
#include <string>

#include "version.hpp"

int main(int argc, char *argv[]) {
	if (argc != 3) {
		std::cerr << "Usage: " << argv[0] << " version-str1 version-str2" << std::endl;
		exit(1);
	}
	Version v1 = Version(argv[1]);
	Version v2 = Version(argv[2]);

	string op;
	if (v1 == v2) {
		op = "=";
	} else if (v1 < v2) {
		op = "<";
	} else {
		op = ">";
	}

	std::cout << v1 << op << v2 << std::endl;

	return 0;
}
