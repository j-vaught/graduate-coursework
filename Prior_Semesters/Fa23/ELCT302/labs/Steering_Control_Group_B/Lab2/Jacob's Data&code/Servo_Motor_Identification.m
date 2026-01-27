clc
clear
close all

% Step 1: Load the data from Excel
data = xlsread('edits.xlsx'); 
time = data(:,1); 
input_signal = data(:,3);
output_signal = data(:,2);

% Interpolate the signals to create an evenly spaced time vector.
dt = mean(diff(time));
new_time = (time(1):dt:time(end))'; 
input_signal = interp1(time, input_signal, new_time, 'linear', 'extrap');
output_signal = interp1(time, output_signal, new_time, 'linear', 'extrap');

% Step 2: Create an iddata object
data_id = iddata(output_signal, input_signal, dt);

% Step 3: Identify the transfer function
sys = tfest(data_id, 2);
display(sys)

% Define the potential controller types for comparison
controller_types = {'P', 'PI', 'PD', 'PID'};

for i = 1:length(controller_types)
    % Create a new figure for each plot
    figure('Position', [100, 100, 1920, 1080]); % Set the figure size

    % Tune a controller of the given type
    switch controller_types{i}
        case 'P'
            C = pidtune(sys, 'P');
        case 'PI'
            C = pidtune(sys, 'PI');
        case 'PD'
            C = pidtune(sys, 'PD');
        case 'PID'
            C = pidtune(sys, 'PID');
    end
    
    % Form the closed-loop transfer function for the system with the controller
    T = feedback(C*sys, 1);
    
    % Generate the simulated response for this controller type
    y_sim = lsim(T, input_signal, new_time);
    
    % Plot the actual data, the simulated response, and the input
    plot(new_time, output_signal, 'b-', 'DisplayName', 'Practical Data');
    hold on;
    plot(new_time, y_sim, 'r--', 'DisplayName', 'Simulated Data');
    plot(new_time, input_signal, 'g:', 'DisplayName', 'Input Data');
    title(controller_types{i});
    legend;
    hold off;
    
    % Save the figure
    filename = sprintf('%s.png', controller_types{i});
    saveas(gcf, filename);
    close(gcf); % Close the figure after saving
end
