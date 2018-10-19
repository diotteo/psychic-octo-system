QB_SRC := $(wildcard *.cpp)
QB_OBJ := $(patsubst %.cpp,%.o,$(QB_SRC))
QB_PRGM := qb

.DEFAULT: all
.PHONY: all
all: test-qb

test-qb: $(QB_PRGM)
	@echo "Running tests..."
	@./test_qb

run-qb: $(QB_PRGM)
	./$(QB_PRGM)

$(QB_PRGM): $(QB_OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

$(QB_OBJ): %.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $< -o $@
