function isEqual = checkEqual(a, b)
    d = a - b;
    
    if (sum(sum(abs(d))) < 0.001)
        fprintf("The two inputs are equal\n");
        isEqual = 1;
    else
        fprintf("The two inputs are NOT equal\n");
        isEqual = 0;
end