function [sys_CL] = SISO_ssModel_FB(wn,z,H)
    % This function creates a SISO state-space model with feedback
    % Inputs:
    %   wn - Natural frequency
    %   z - Damping ratio
    %   H - Feedback gain matrix
    % Output:
    %   sys_CL - Closed-loop state-space system
    
    %---------------- state space matrices -----------
    AA = [ 0 1 ;
          -wn^2 -2*z*wn];
    
    BB = [ 0 ;
          wn^2];
    
    CC = [1 0];
    DD = [0];
    
    % State matrix AA with feedback
    AA_CL = AA - BB*H; 
    
    sys_CL = ss(AA_CL, BB, CC, DD);
    
end % function ends here