#include <vector>
#include <string>
#include <cctype>
#include <boost/algorithm/string.hpp>

#include "version.hpp"

using namespace std;

VersionNumber::VersionNumber(string subVersionStr) {
	string str = boost::to_lower_copy<std::string>(subVersionStr);
	/* We prevalidate the string since strtol accepts a leading +/- but we don't */
	bool b_space = true;
	for (auto it = str.cbegin();
			 it != str.cend();
			 it++) {
		if (isspace(*it)) {
			continue;
		} else if (!isdigit(*it)) {
			throw invalid_argument("version numbers must start with a digit");
		} else {
			break;
		}
	}
	const char *start = str.c_str();
	char *p = NULL;
	errno = 0;
	value = strtol(str.c_str(), &p, 10);
	if (p == NULL || p <= start) {
		throw invalid_argument("no conversion");
	} else if (errno != 0) {
		throw invalid_argument("value out of range");
	}
}

VersionNumber::~VersionNumber () {
}

string VersionNumber::getValue() {
	return to_string(value);
}

std::ostream& operator<<(std::ostream& os, VersionNumber const& v) {
	os << v.value;
	return os;
}

bool VersionNumber::operator==(const VersionNumber& rhs) const {
	return value == rhs.value;
}

bool VersionNumber::operator< (const VersionNumber& rhs) const {
	return value < rhs.value;
}

bool VersionNumber::operator!=(const VersionNumber& rhs) const {return !operator==(rhs);}
bool VersionNumber::operator> (const VersionNumber& rhs) const {return  rhs.operator< (*this);}
bool VersionNumber::operator<=(const VersionNumber& rhs) const {return !operator> (rhs);}
bool VersionNumber::operator>=(const VersionNumber& rhs) const {return !operator< (rhs);}


Version::Version(string versionStr) {
	auto substrs = splitVersionStr(versionStr);
	for (auto subVersionStr: substrs) {
		numbers.push_back(VersionNumber(subVersionStr));
	}
}

Version::~Version () {
}

vector<VersionNumber> Version::getVersionNumbers() {
	return numbers;
}

vector<string> Version::splitVersionStr(string versionStr, char sep) {
	vector<string> substrs = vector<string>();

	size_t start = 0;
	for (size_t i = 0; versionStr[i] != '\0'; i++) {
		if (versionStr[i] == sep) {
			substrs.push_back(versionStr.substr(start, i-start));
			start = i+1;
		}
	}
	substrs.push_back(versionStr.substr(start));
	return substrs;
}

std::ostream& operator<<(std::ostream& os, Version const& v) {
	bool first = true;
	for (auto it = v.numbers.cbegin(); it != v.numbers.cend(); it++) {
		if (first) {
			first = false;
		} else {
			os << ".";
		}
		os << *it;
	}
	return os;
}

bool Version::operator== (const Version& rhs) const {
	auto it1 = numbers.cbegin();
	auto it2 = rhs.numbers.cbegin();
	for (;
			 it1 != numbers.cend() || it2 != rhs.numbers.cend();
			 it1++, it2++) {
		/* We need only test one iterator for end since we can't
		 * be in the loop if both have ended
		 */
		if (it1 == numbers.cend()) {
			return false;
		} else if (it2 == rhs.numbers.cend()) {
			return false;
		} else if (*it1 != *it2) {
			return false;
		}
	}
	return true;
}

bool Version::operator< (const Version& rhs) const {
	auto it1 = numbers.cbegin();
	auto it2 = rhs.numbers.cbegin();
	for (;
			 it1 != numbers.cend() || it2 != rhs.numbers.cend();
			 it1++, it2++) {
		/* We need only test one iterator for end since we can't
		 * be in the loop if both have ended
		 */
		if (it1 == numbers.cend()) {
			return true;
		} else if (it2 == rhs.numbers.cend()) {
			return false;
		} else if (*it1 < *it2) {
			return true;
		} else if (*it1 > *it2) {
			return false;
		}
	}
	return false;
}

bool Version::operator!=(const Version& rhs) const {return !operator==(rhs);}
bool Version::operator> (const Version& rhs) const {return  rhs.operator< (*this);}
bool Version::operator<=(const Version& rhs) const {return !operator> (rhs);}
bool Version::operator>=(const Version& rhs) const {return !operator< (rhs);}
