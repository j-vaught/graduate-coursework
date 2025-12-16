%% INITIALIZATION
% Clear workspace and set up environment
clc;              % Clear command window
clear;            % Clear workspace variables
format compact;   % Compact display format
set(0, 'DefaultFigureWindowStyle', 'docked');  % Dock figures in MATLAB
nfig = 1;         % Figure counter
tol = 1e-10;      % Tolerance for discarding machine zero

%% CHOOSE WHAT SECTION TO RUN
% Set flags to control which sections of the code to execute
ifSectionB_GVT = 0;        % Perform GVT (Ground Vibration Test) analysis

ifSectionC_Flutter = 0;    % Perform flutter analysis
    ifC2basicFlutter = 0;  % Perform basic flutter analysis
    ifC3Zoom = 0;          % Zoom around flutter speed
    ifC4UFvsCP = 0;        % Plot flutter speed vs static offset (xCP)
    ifC5UFvsQP = 0;        % Plot flutter speed vs aerodynamic offset (xQP)
    ifC6Div = 0;           % Calculate and plot divergence speed

ifSectionD_Damping = 1;    % Perform analysis with damping
    ifDampedGVT = 0;       % Perform damped GVT analysis
    ifDampedFlutter = 1;   % Perform damped Flutter analysis

%% INPUT DATA FOR HOMEWORK 1
% Physical properties and parameters
rho = 1.225;        % Air density (kg/m^3)
a1 = 2*pi;          % Ideal lift curve slope (2π for thin airfoil theory)

% ------ Main aircraft parameters ---------
c = 0.48;           % Airfoil chord (m)
m = 3.8;            % Mass (kg)
I0 = 0.065;         % Moment of inertia about center of mass (kg*m^2)
fh = 3.2;           % Uncoupled plunge frequency (Hz)
ft = 6.8;           % Uncoupled pitch frequency (Hz)
CPratioDefault = -15e-2;   % Static offset (-10% of chord)
QPratioDefault = 25e-2;    % Aerodynamic offset (35% of chord)

% ------ Parameters for homework C.2 (Basic Flutter Analysis) ---------
UendUF = 14;        % End airspeed for flutter diagram (m/s)
NU = 1001;          % Number of airspeed points

% ------ Parameters for homework C.3 (Mode Near Flutter) ---------
U_second = 9;        % End airspeed for flutter diagram (m/s)
U_first = 0;          % Number of airspeed points

% ------ Parameters for homework C.4 (Static Offset Study) ---------
UstartCP = 10;       % Start airspeed for xCP variation (m/s)
UendCP = 25;        % End airspeed for xCP variation (m/s)
%CPratioRange = [-20 -15 -10 -5 -1 -0.1]/100;  % Static offset range (% of chord)
CPratioRange = [20 15 10 5 1 0.1 0]/100; % uncomment for Part e
N_CP = length(CPratioRange); 

% ------ Parameters for homework C.5 (Aerodynamic Offset Study) ---------
UstartQP = 10.5;       % Start airspeed for xQP variation (m/s)
UendQP = 16;        % End airspeed for xQP variation (m/s)
QPratioRange = [20 25 30]/100;  % Aerodynamic offset range (% of chord)
N_QP = length(QPratioRange);

% ------ Parameters for homework C.6 (Divergence Analysis) ---------
UendDiv = 25;       % End airspeed for divergence analysis (m/s)

% ------ Parameters for homework D.2 (Damping Analysis) ---------
zh = 4e-2;          % Plunge damping ratio (3%)
zt = 3.5e-2;          % Pitch damping ratio (2%)


%% SECTION B: GROUND VIBRATION TEST (GVT)
% Perform GVT analysis to determine structural properties
if ifSectionB_GVT
    display('Section B. Ground Vibration Test (GVT) Analysis')
    close all; % Close all figures
    
    %% Display input data
    display('(a) Input data')
    fprintf('  c = %2.2f m, m = %2.1f kg/m, I0 = %5.4f kg*m^2/m \n', c, m, I0)
    fprintf('  Uncoupled frequencies: fh = %2.1f Hz, ft = %2.1f Hz \n', fh, ft)
    display(' ')
    
    %% Run GVT function
    GVT(c, m, I0, fh, ft, CPratioDefault); % Execute GVT analysis
    
    display(' ')
    display('(e) Every student should insert here discussion of results')
end % ifSectionB_GVT ends here


%% SECTION C: FLUTTER ANALYSIS
% Perform flutter eigenvalue analysis across various airspeeds
if ifSectionC_Flutter
    display('Section C. Flutter Eigen Analysis')
    close all; % Close all figures
    
    %% Display input data
    CPratio = CPratioDefault; xCP = CPratio * c;  % Static offset
    QPratio = QPratioDefault; xQP = QPratio * c;  % Aerodynamic offset
    
    display('Input data:')
    fprintf('  rho = %4.3f kg/m^3 (air density) \n', rho)
    fprintf('  c = %2.1f m, m = %2.1f kg/m, I0 = %5.4f kg*m^2/m \n', c, m, I0)
    fprintf('  Uncoupled frequencies: fh = %2.1f Hz, ft = %2.1f Hz \n', fh, ft)
    fprintf('  Static offset xCP = %2.1f%%, %5.4f m \n', CPratio*100, xCP)
    fprintf('  Aerodynamic offset xQP = %2.1f%%, %5.4f m \n', QPratio*100, xQP)
    
    %% Calculate structural matrices MS (mass) and KS (stiffness)
    wt = 2*pi*ft;  % Pitch angular frequency (rad/s)
    wh = 2*pi*fh;  % Plunge angular frequency (rad/s)
    Ip = I0 + m*xCP^2;  % Moment of inertia about elastic center (kg*m^2)
    
    % Structural mass matrix
    MS = [1, -xCP;
         -m/I0*xCP, Ip/I0];
         
    % Structural stiffness matrix  
    KS = [wh^2, 0;
          0, wt^2];
    
    %% Define aerodynamic lift function
    L0 = @(UU) rho * UU^2 / 2 * c * a1; % Lift function for airspeed UU
    
    %% Define airspeed range for analysis
    Ustart = 0; 
    Uend = UendUF; % Normal flutter diagram range
    
    % Extended diagram for divergence analysis if enabled
    if ifC6Div
        Uend = UendDiv;
    end
    
    % Generate linearly spaced airspeed vector
    U = linspace(Ustart, Uend, NU);
    
    % Zoom around flutter speed if enabled
    if ifC3Zoom
        % Prompt user for flutter speed from previous analysis
        UF = input('Enter flutter speed read on the flutter diagram UF = ');
        eps = 1e-2;
        % Create detailed airspeed range around flutter speed
        U = [U_first, U_second, (1-eps)*UF, UF, (1+eps)*UF];
    end
    
    NU = length(U); % Update airspeed count
    %% Run basic flutter analysis
    % Compute eigenvalues and eigenvectors across the airspeed range
    [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, 0, KS);
    
    %% Plot basic flutter diagram if enabled
    if ifC2basicFlutter
        % Only plot if there are enough points
        % if NU > 10; % only plot if more than ten points to plot
        
        display([' Ustart = ' num2str(Ustart) ' m/s, Uend = ' num2str(Uend) ' m/s,' ...
                ' NU = ' num2str(NU)])
        
        close all; % Close all figures
        
        % Create plot title with current parameters
        plotTitle = {[ 'xCP = ' num2str(CPratio*1e2) '%, xQP = ' num2str(QPratio*1e2) '% ']};
        
        % Generate flutter diagram (frequency and damping vs airspeed)
        figure; 
        plot_f_z(U, f, z, plotTitle);
    end
    
    %% Display detailed frequency/modeshape data if zoom enabled
    if ifC3Zoom
        displayUfv(U, f, v); % Print zoom-in values
    end
    
    %% UF variation with xCP (Static Offset Study)
    if ifC4UFvsCP
        close all; % Close all figures
        figure(1);
        
        %% Define airspeed range for xCP variation study
        Ustart = UstartCP; 
        Uend = UendCP; 
        NU = 1001; 
        U = linspace(Ustart, Uend, NU);
        
        display([' Ustart = ' num2str(Ustart) ' m/s, Uend = ' num2str(Uend) ' m/s,' ...
                ' NU = ' num2str(NU)])
        
        QPratio = QPratioDefault; 
        xQP = QPratio * c; % Aerodynamic offset
        
        display([' QPratio = ' num2str(QPratio*100) '%'])
        display(CPratioRange*100, ' CPratioRange %')
        
        %% LOOP OVER ALL CPratio values
        for nCP = 1:N_CP
            %% Set current static offset parameters
            CPratio = CPratioRange(nCP); 
            xCP = CPratio * c; % Static offset
            
            % Calculate moment of inertia about elastic center
            Ip = I0 + m * xCP^2; % Moment of inertia (kg*m^2)
            
            %% Recalculate structural mass matrix for current xCP
            MS = [1, -xCP;
                 -m/I0*xCP, Ip/I0]; % Structural mass matrix
            
            %% Perform eigenvalue analysis for current parameters
            [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, 0, KS);
            
            %% Plot results for current xCP value
            plotTitle = {[ 'xQP = ' num2str(QPratio*1e2) '%, various xCP']};
            plot_f_z(U, f, z, plotTitle);
            hold on;
            
            %% Identify flutter speeds for current xCP
            fprintf(' CPratio = %0.1f%% \n', CPratio*100);
            display('Put datatips on plot to identify UF');
            display('When done, press any key into the command window to continue');
            pause;
        end % nCP loop ends here
        
        %% Collect user-input flutter speeds from plots
        UF_CP = input(['Enter [UF1, UF2, UF3, ...] values ' ...
                      'from datatips on plot in the order of appearance = ']);
        display(' ');
        
        %% Plot flutter speed vs static offset
        display(CPratioRange*100, ' xCP %');
        display(UF_CP, ' UF, m/s');
        
        figure(2);
        plot(CPratioRange*100, UF_CP, '-r');
        xlim([-20, 20]); 
        ylim([0, Uend]); 
        xlabel('xCP, %'); 
        ylabel('U_F, m/s');
        title(['U_F vs. x_C_P for x_Q_P = ' num2str(QPratio*100) ' %'],...
              'FontSize', 11, 'FontWeight', 'normal');
        grid on;
    end % ifUFvsCP ends here
    %% UF variation with xQP (Aerodynamic Offset Study)
    if ifC5UFvsQP
        close all; % Close all figures
        
        %% Define airspeed range for xQP variation study
        Ustart = UstartQP; 
        Uend = UendQP; 
        NU = 1001; 
        U = linspace(Ustart, Uend, NU);
        
        display([' Ustart = ' num2str(Ustart) ' m/s, Uend = ' num2str(Uend) ' m/s,' ...
                ' NU = ' num2str(NU)])
        
        %% Set static offset parameters
        CPratio = CPratioDefault; 
        xCP = CPratio * c; % Static offset
        
        display([' CPratio = ' num2str(CPratio*100) '%'])
        
        %% Calculate moment of inertia and structural matrices
        Ip = I0 + m * xCP^2; % Moment of inertia about elastic center (kg*m^2)
        
        % Structural mass matrix
        MS = [1, -xCP;
             -m/I0*xCP, Ip/I0]; % Structural mass matrix
        
        figure(1);
        display([' QPratioRange % = ' num2str(QPratioRange*100)])
        
        %% LOOP OVER ALL QPratio values
        for nQP = 1:N_QP
            %% Set current aerodynamic offset parameters
            QPratio = QPratioRange(nQP); 
            xQP = QPratio * c; % Aerodynamic offset
            
            %% Perform eigenvalue analysis for current parameters
            [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, 0, KS);
            
            %% Plot results for current xQP value
            plotTitle = {[ 'xCP = ' num2str(CPratio*1e2) '%, various xQP']};
            plot_f_z(U, f, z, plotTitle);
            hold on;
            
            %% Identify flutter speeds for current xQP
            fprintf(' QPratio = %0.0f%% \n', QPratio*100);
            display('Put datatips on plot to identify UF ');
            display('When done, press any key into the command window to continue');
            pause;
        end % nQP loop ends here
        
        %% Collect user-input flutter speeds from plots
        UF_QP = zeros(1, N_QP);
        UF_QP = input(['Enter [UF1, UF2, UF3, ...] values ' ...
                      'from datatips on plot in the order of appearance = ']);
        display(' ');
        
        %% Plot flutter speed vs aerodynamic offset
        display(QPratioRange*100, ' xQP %');
        display(UF_QP, ' UF, m/s');
        
        figure(2);
        plot(QPratioRange*100, UF_QP, '-b');
        xlim([20, 30]); 
        ylim([0, Uend]); 
        xlabel('xQP, %'); 
        ylabel('U_F, m/s');
        title(['U_F vs. x_Q_P for x_C_P = ' num2str(CPratio*100) ' %'],...
              'FontSize', 11, 'FontWeight', 'normal');
        grid on;
    end % ifUFvsQP ends here
    
    %% Calculate and plot divergence speed UD
    if ifC6Div
        display([' Ustart = ' num2str(Ustart) ' m/s, Uend = ' num2str(Uend) ' m/s,' ...
                ' NU = ' num2str(NU)])
        close all; % Close all figures
        
        %% Part (a): Extended flutter diagram showing divergence
        QPratio = QPratioDefault; 
        xQP = QPratio * c;
        
        % Perform eigenvalue analysis
        [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, 0, KS);
        
        figure;
        plotTitle = {[ 'xCP = ' num2str(CPratio*1e2) '% ' ...
                     'xQP = ' num2str(QPratio*1e2) '%']};
        plot_f_sigmaExtended(U, f, sigma, plotTitle);
        
        %% Part (b): Divergence speed vs aerodynamic offset
        QPratio = [20, 25, 30] * 1e-2;
        xQP = QPratio * c;
        
        % Calculate divergence speed using theoretical formula
        UD = wt * sqrt(2 * I0 ./ (xQP * a1 * rho * c));
        
        % Display results
        display(QPratio*100, 'QPratio, %');
        display(UD, 'Divergence speed UD, m/s');
        
        figure;
        plot(QPratio*1e2, UD, '-b');
        ylim([0, Uend]);
        xlabel('x_Q_P, %');
        ylabel('U_D, m/s');
        title('U_D vs. x_Q_P', 'FontSize', 11, 'FontWeight', 'normal');
        grid on;
    end % ifDiv ends here
end % ifFlutter ends here



%% SECTION D: INCLUDE DAMPING
% Perform analysis with structural damping included
if ifSectionD_Damping
    display('Section D. Damped GVT and Flutter')
    close all; % Close all figures
    
    %% Display input data
    display('Input data')
    if ifDampedFlutter
        fprintf('  rho = %4.3f kg/m^3 (air density) \n', rho); 
    end
    fprintf('  c = %2.1f m, m = %2.1f kg/m, I0 = %5.4f kg*m^2/m \n', c, m, I0)
    fprintf('  Uncoupled frequencies: fh = %2.1f Hz, ft = %2.1f Hz \n', fh, ft)
    fprintf('  Damping ratios: zh = %2.0f%%, zt = %2.0f%% \n', [zh, zt]*100)
    
    %% Calculate structural parameters
    CPratio = CPratioDefault; 
    xCP = CPratio * c;  % Static offset
    Ip = I0 + m * xCP^2; % Moment of inertia about elastic center (kg*m^2/m)
    
    fprintf('  Static offset xCP = %2.1f%%, %5.4f m \n', CPratio*100, xCP)
    
    QPratio = QPratioDefault; 
    xQP = QPratio * c; % Aerodynamic offset
    
    fprintf('  Aerodynamic offset xQP = %2.1f%%, %5.4f m \n', QPratio*100, xQP)
    
    %% CALCULATE STRUCTURAL MATRICES MS (Mass), CS (Damping), KS (Stiffness)
    wt = 2*pi*ft;  % Pitch angular frequency (rad/s)
    wh = 2*pi*fh;  % Plunge angular frequency (rad/s)
    
    % Structural mass matrix
    MS = [1, -xCP;
         -m/I0*xCP, Ip/I0]; % Structural mass matrix
    
    % Structural viscous damping matrix
    CS = [2*zh*wh, 0;
          0, 2*zt*wt]; % Structural viscous damping
    
    % Structural stiffness matrix
    KS = [wh^2, 0;
          0, wt^2]; % Structural stiffness matrix
    
    %% DAMPED GVT ANALYSIS
    if ifDampedGVT
        % Run damped GVT analysis function
        dampedGVT(zh, zt, MS, CS, KS);
    end % ifDampedGVT ends here
    
    %% DAMPED FLUTTER ANALYSIS
    if ifDampedFlutter
        display('Damped Flutter Analysis')
        close all; % Close all figures
        
        %% DEFINE AIRSPEED RANGE FOR ANALYSIS
        Ustart = 0; 
        Uend = UendUF; % Flutter diagram range
        NU = 1001; 
        U = linspace(Ustart, Uend, NU); % Airspeed range vector
        
        %% Calculate and plot damped flutter diagram
        figure;
        
        % Perform eigenvalue analysis with damping
        [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, CS, KS);
        
        % Create plot title with current parameters
        plotTitle = {[ ['xCP = ' num2str(CPratio*1e2) '% ' 'xQP = ' num2str(QPratio*1e2) '%'] ...
                     [' zh = ' num2str(zh*1e02) '%'] [' zt = ' num2str(zt*1e02) '%']]};
        
        % Plot options for damped case (red dots)
        plotOptions = '.r';
        
        % Generate damped flutter diagram
        plot_f_z_Damped(U, f, z, plotTitle, plotOptions);
        
        %% Identify damped flutter speeds from plot
        display('Put datatips on plot to identify damped flutter speeds (UF)')
        display('When done, press any key into the command window to continue')
        pause;
        
        %% OVERLAY UNDAMPED PLOT FOR COMPARISON
        zh = 0; 
        zt = 0; % Undamped case (zero damping)
        
        % Recalculate damping matrix for undamped case
        CS = [2*zh*wh, 0;
              0, 2*zt*wt]; % Structural viscous damping (zero)
        
        % Perform eigenvalue analysis for undamped case
        [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, CS, KS);
        
        % Create plot title for undamped case
        plotTitle = {[ ['xCP = ' num2str(CPratio*1e2) '% ' 'xQP = ' num2str(QPratio*1e2) '%'] ...
                     [' zh = ' num2str(zh*1e02) '%'] [' zt = ' num2str(zt*1e02) '%']]};
        
        % Plot options for undamped case (blue dots)
        plotOptions = '.b';
        
        % Overlay undamped flutter diagram on same plot
        plot_f_z_Damped(U, f, z, plotTitle, plotOptions);
    end % ifDampedFlutter ends here
end % ifDamping ends here

%% FINISH
display(' ')
display(' ---------------')
display(['Success! ' mfilename ' finished successfully'])