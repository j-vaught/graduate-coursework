function [s,f,z] = ssPolesFreqDamping(ss_sys,tol)
    % This function extracts poles, frequencies, and damping from a state-space system
    % Inputs:
    %   ss_sys - State-space system
    %   tol - Tolerance for damping values
    % Outputs:
    %   s - Poles
    %   f - Frequencies
    %   z - Damping values
    
    [~,zz,poles] = damp(ss_sys);
    
    % Extract poles
    s = poles; 
    
    % Calculate frequencies
    f = abs(imag(poles))/(2*pi); 
    
    % Extract damping values above tolerance
    z = zz.*(abs(zz)>tol); 
    
end % function ends here