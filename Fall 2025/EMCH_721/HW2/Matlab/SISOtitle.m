function [tfig] = SISOtitle(f,z)
    % This function creates a title for SISO system plots
    % Inputs:
    %   f - frequency vector
    %   z - damping vector
    % Output:
    %   tfig - Title string
    
    tfig = [ 'f=' num2str(f(1),'%0.4f') ' Hz, z= ' num2str(z(1)*100) '%'];
    
end % function ends