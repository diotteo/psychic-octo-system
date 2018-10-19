#include <string>
#include <vector>

using namespace std;

class VersionNumber {
	protected:
		bool b_prerelease;
		string prereleaseStr;
		int value;

	public:
		VersionNumber(string subVersionStr);
		~VersionNumber ();

		string getValue();

		bool operator==(const VersionNumber& rhs) const;
		bool operator< (const VersionNumber& rhs) const;
		bool operator!=(const VersionNumber& rhs) const;
		bool operator> (const VersionNumber& rhs) const;
		bool operator<=(const VersionNumber& rhs) const;
		bool operator>=(const VersionNumber& rhs) const;

		friend std::ostream& operator<<(std::ostream& os, const VersionNumber& v);
};

class Version {
	protected:
		vector<VersionNumber> numbers;

	public:
		Version(string versionStr);
		~Version ();

		vector<VersionNumber> getVersionNumbers();
		static vector<string> splitVersionStr(string versionStr, char sep = '.');

		bool operator< (const Version& rhs) const;
		bool operator==(const Version& rhs) const;
		bool operator!=(const Version& rhs) const;
		bool operator> (const Version& rhs) const;
		bool operator<=(const Version& rhs) const;
		bool operator>=(const Version& rhs) const;

		friend std::ostream& operator<<(std::ostream& os, const Version& v);
};
