function [sys] = MIMOssModel(M,C,K,Omega)
    % This function creates a MIMO state-space model
    % Inputs:
    %   M - Mass matrix
    %   C - Damping matrix  
    %   K - Stiffness matrix
    %   Omega - Input matrix
    % Output:
    %   sys - State-space system
    
    %---------------- state space matrices -----------
    AA = [zeros(2,2) eye(2) ;
          -M\K -M\C ];
    
    BB = [zeros(2,2);
          M\Omega ];
    
    CC = [eye(2) zeros(2,2)];
    DD = zeros(2,2);
    
    sys = ss(AA,BB,CC,DD);

end % function ends here