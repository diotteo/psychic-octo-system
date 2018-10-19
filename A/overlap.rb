#! /usr/bin/env ruby

# Parse the array of strings as an array of arrays of ints
# E.g.: ["(1,2)", "(3,4)"] becomes [[1, 2], [3, 4]]
# If no argument is provided, ARGV is used.
# Exit the program with a help message if an error if bogus input is encountered
# Parentheses are optional
def parse_arguments(args = ARGV)
	help = ->() {
			puts "Usage: #{$0} (x1,x2) (x3,x4)"
			exit 1
	}

	if args.length != 2
		help.call
	end

	begin
		lines = args.map do |x|
			x.strip
			.match(/^\(?(\s*-?[\d\s]+),(\s*-?[\d\s]+)\)?$/)[1,2]
			.map {|y| y.to_i}
			.sort #Sort the points so 6,2 becomes 2,6
		end
	rescue
		help.call
	end
	lines.sort #Sort the lines so the lowest minimum line is first
end

lines = parse_arguments

puts lines.to_s

if lines[0][0] <= lines[1][0] && lines[0][1] >= lines[1][0]
	puts "Overlap"
else
	puts "No overlap"
end
