function [s_TF,f_TF,z_TF] = TFpolesFreqDamping(G,tol)
    % This function extracts poles, frequencies, and damping from a transfer function
    % Inputs:
    %   G - Transfer function
    %   tol - Tolerance for damping values
    % Outputs:
    %   s_TF - Poles
    %   f_TF - Frequencies
    %   z_TF - Damping values
    
    % Extract poles from transfer function
    [~,poles_TF,~] = zpkdata(G); 
    s_TF = poles_TF{1,1}; % poles
    
    % Calculate frequencies
    f_TF = abs(imag(s_TF)/(2*pi)); % frequencies
    
    % Calculate damping values
    zz = -real(s_TF)./abs(s_TF); 
    z_TF = zz.*(abs(zz)>tol); % damping
    
end % function ends here