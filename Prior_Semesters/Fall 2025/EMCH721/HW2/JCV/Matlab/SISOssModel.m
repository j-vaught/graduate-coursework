function [ss_sys] = SISOssModel(wn,z)
    % This function creates a SISO state-space model
    % Inputs:
    %   wn - Natural frequency
    %   z - Damping ratio
    % Output:
    %   ss_sys - State-space system
    
    %---------------- state space matrices -----------
    AA = [ 0 1 ;
          -wn^2 -2*z*wn];
    
    BB = [ 0 ;
          wn^2];
    
    CC = [1 0];
    DD = [0];
    
    ss_sys = ss(AA,BB,CC,DD);
    
end % function ends here