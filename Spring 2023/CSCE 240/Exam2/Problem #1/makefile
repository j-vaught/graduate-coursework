flags = -std=c++17 -Wall -I .

length.o : length.cc length.h
	g++ $(flags) -c $< -I .

testlengthparta : testlengthparta.cc length.o
	g++ $(flags) $^ -o $@
	./$@

testlengthpartb : testlengthpartb.cc length.o
	g++ $(flags) $^ -o $@
	./$@

clean :
	rm student-lengthpartb.txt length.o testlengthparta testlengthpartb

