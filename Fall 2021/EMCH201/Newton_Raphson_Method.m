clc; clear;

% Newton-Raphon Method program to locate roots
syms x;
f = (9.81*68.1/x)*(1-exp(-(x/68.1)*10))-40;     % the function
fprime=diff(f);

xold = 15;         % estimate of the solution 
es = 0.1;       % percent error
imax = 100;     % the maximum number of iterations(stops infinite loops)

iter = 0;       % iteration. Initilized to zero, will be incremented each iteration

doLoop = true;

while doLoop==true
    fx=vpa(subs(f,x,xold));
    fprimex=vpa(subs(fprime,x,xold));
    xi = xold-(fx/fprimex); 
    
    if xi~=0 %get Error if xi not = 0
        ea=abs((xi-xold)/xi)*100;
    end

    fprintf('iteration = %d, Estimate=%f, error = %f\n', iter, xi, ea);
    xold = xi;
    iter=iter+1;

    if ea<=es
        doLoop=false;
    elseif (iter >= imax)
        doLoop = false;
    end
end 
fprintf('root found: %f', xold);
