function [sys_CL] = MIMOssModel_FB(M,C,K,Omega,H)
    % This function creates a MIMO state-space model with feedback
    % Inputs:
    %   M - Mass matrix
    %   C - Damping matrix  
    %   K - Stiffness matrix
    %   Omega - Input matrix
    %   H - Feedback gain matrix
    % Output:
    %   sys_CL - Closed-loop state-space system

    %---------------- state space matrices -----------
    AA = [zeros(2,2) eye(2) ;
          -M\K -M\C ];
    
    BB = [zeros(2,2);
          M\Omega ];
    
    CC = [eye(2) zeros(2,2)];
    DD = zeros(2,2);
    
    % State matrix AA with feedback
    AA_CL = AA - BB*H; 
    
    sys_CL = ss(AA_CL,BB,CC,DD);

end % function ends here