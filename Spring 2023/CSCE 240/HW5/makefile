truefalsequestion.o : truefalsequestion.h truefalsequestion.cc
	g++ -Wall -std=c++17 -I . -c truefalsequestion.cc

shortanswerquestion.o : shortanswerquestion.h shortanswerquestion.cc
	g++ -Wall -std=c++17 -I . -c shortanswerquestion.cc

multiplechoicequestion.o : multiplechoicequestion.h multiplechoicequestion.cc
	g++ -Wall -std=c++17 -I . -c multiplechoicequestion.cc

checkit : checkit.cc
	g++ -Wall -std=c++17 checkit.cc -o checkit

testtf : testtf.cc truefalsequestion.o checkit
	g++ -Wall -std=c++17 -I . testtf.cc truefalsequestion.o -o testtf
	./testtf > ./output/studenttf.txt
	./checkit 0

testsa : testsa.cc shortanswerquestion.o checkit
	g++ -Wall -std=c++17 -I . testsa.cc shortanswerquestion.o -o testsa
	./testsa > ./output/studentsa.txt
	./checkit 1

testmc1 : testmc1.cc multiplechoicequestion.o checkit
	g++ -Wall -std=c++17 -I . testmc1.cc multiplechoicequestion.o -o testmc1
	./testmc1 > ./output/studentmc1.txt
	./checkit 2

testmc2 : testmc2.cc multiplechoicequestion.o checkit
	g++ -Wall -std=c++17 -I . testmc2.cc multiplechoicequestion.o -o testmc2
	./testmc2 > ./output/studentmc2.txt
	./checkit 3

clean :
	rm *.o ./output/student* testmc2 testmc1 testsa testtf
