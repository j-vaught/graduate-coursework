%% DESCRIPTION
%{
HW02
A. SISO TF representation vs SS representation
B. Time response analysis of flutter
C. SISO SS feedback
D. Feedback control of flutter
E. Flutter control through aileron feedback
F. Challenge problems
%}

%% initialization
opengl hardwarebasic % switch to basic hardware graphics functions
clc % clear command window
clear % clear workspace
format compact
set(0,'DefaultFigureWindowStyle','docked')
% nfig=1;
tol = 1e-10; % tolerance for discarding machine zero




%% Section selector (use the section of the HW you are on)
sectionChoice = "F";  % "A","B","B3","B4","B5","C","D","E","F"


ifSectionA = 0; % SISO TF vs SS
ifSectionB = 0; % time response analysis of flutter
ifSectionB3 = 0; % perform GVT simulation
ifSectionB4 = 0; % perform flutter simulation
ifSectionB5 = 0; % adjust UF to obtain exact flutter conditions
ifSectionC = 0; % SISO SS feedback
ifSectionD = 0; % feedback control of flutter
ifSectionE = 0; % aileron feedback
ifSectionF = 0; % challenge problems

switch upper(string(sectionChoice))
    case "A",  ifSectionA=1;
    case "B",  ifSectionB=1;
    case "B3", ifSectionB=1; ifSectionB3=1;
    case "B4", ifSectionB=1; ifSectionB4=1;
    case "B5", ifSectionB=1; ifSectionB5=1;
    case "C",  ifSectionC=1;
    case "D",  ifSectionD=1;
    case "E",  ifSectionE=1;
    case "F",  ifSectionF=1;
    otherwise, error("Unknown sectionChoice.");
end

%% input data
display('EMCH 721 - HW02')

% ------ airfoil data ---------
rho = 1.225; % air density, 1.225 kg/m3
a1 = 2*pi; % ideal lift curve slope value for the wing
ad = 2*pi; % ideal lift curve slope value for the aileron in Section E
c = 0.48; % airfoil chord, m
m = 3.8; % mass, kg
I0 = 0.065; % moment of inertia about the center of mass, kg*m^2
fh = 3.2; % plunge frequency, Hz
ft = 6.8; % pitch frequency, Hz
wt = 2*pi*ft; 
wh = 2*pi*fh;
zh = 3e-2; % plunge damping ratio
zt = 2e-2; % pitch damping ratio
CPratio = -15e-2; 
xCP = CPratio*c; % static offset
QPratio = 25e-2; 
xQP = QPratio*c; % aerodynamic offset

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ip = I0 + m*xCP^2; % moment of inertia about the elastic center, kg*m^2/m

% --- SISO data from C.2
fn = 1.8; % SISO frequency, Hz
z0 = 2e-2; % SISO damping ratio

% ------ UF data ------
eps = 2e-1; % used to define the vicinity of UF
Umin = 2; % set minimum airspeed

% ---- FB data from C.2 ----
zCLratio = 3.2; % Section C: desired CL damping increase over
                % the absolute value of the negative damping
                
% ---- ----
UFdamped = 13.034; % enter UFadjusted from section B.5

% --- aileron data from E.1 ---
cd_ratio = 10e-2; 
e_ratio = 43e-2; % aileron chord ratio and offset ratio

% --- CL damping ratio from F.1 ---
zhCLratio = 3.7; 
ztCLratio = 2.8; % Section F: zh desired CL damping increase
                 % over the absolute value of the negative damping

% ---- Calculated data ----                 
UFadjusted = 13.04408; % YOU will need to adjust this until the time 
                     % response has 0 damping. used in Sections D, E. 
                     % From Section B5

KK = 3.2219e-2; % YOU adjust this Gain Coefficinet for Section D3 until last column of zCL row2,3 = 13



% --- search ranges for section E3 auto-search algorithm. Feel free to
% change the search space and step size.
Kdh_min = -50;
Kdh_max =  50;
Kdt_min = -50;
Kdt_max =  50;
step = 0.1;
Kdh = 23; %default value to use if search fails
Kdt = -15; %default value to use if search fails

%% Define time range
f = min([fh,ft]); 
T = 1/f; % time scale
tmax = 50*T; 
Nt = 1000; 
t = linspace(0,tmax,Nt); % time range

%% Calculate structural matrices MS, CS, KS, Omega
wt = 2*pi*ft; 
wh = 2*pi*fh;
MS = [ 1 -xCP ;
      -m/I0*xCP Ip/I0 ]; % structural mass matrix
      
CS = [2*zh*wh 0 ;
      0 2*zt*wt ]; % structural viscous damping
      
KS = [wh^2 0 ;
      0 wt^2 ]; % structural stiffness matrix
      
Omega = [wh^2 0 ;
         0 wt^2 ];

%% Define aerodynamic lift function
L0 = @(UU) a1*rho*UU^2/2*c; % Lift function for a generic speed UU
%% Section A. SISO TF representation vs SS representation
if ifSectionA
    close all
    % nfig=1;
    display('Section A. SISO TF representation vs SS representation')
    
    %% display input data
    fprintf(' (a) input data: fn=%2.1f Hz, z=%2.1f%% \n',fn,z0*100)
    
    %% Define time range
    T = 1/fn; 
    tmax = 150*T; 
    Nt = 1000; 
    t = linspace(0,tmax,Nt); % time range
    
    %% Calculate SISO transfer function (TF) model
    wn = 2*pi*fn; 
    G = tf(wn^2,[1 2*z0*wn wn^2]); % transfer function G
    
    %% Calculate poles of G, frequency, damping
    [s_TF,f_TF,z_TF] = TFpolesFreqDamping(G,tol);
    
    %% Display TF results
    display(' (b) poles, frequencies, damping ratios')
    display(s_TF, ' TF poles');
    display([f_TF z_TF*100], ' f_TF, Hz; z_TF%');
    
    %% Calculate SISO state space model
    ss_sys = SISOssModel(wn,z0);
    
    %% Extract poles, frequency, damping and display SS results
    [s_SS,f_SS,z_SS] = ssPolesFreqDamping(ss_sys,tol);
    display(s_SS, ' SS poles');
    display([f_SS z_SS*100], ' f_SS, Hz; z_SS%');
    
    %% PLot impulse response of TF model
    display(' (c) please see plots')
    display(' (d) students should write their own comments')
    figure
    subplot(2,1,1); 
    impulse(G,t);
    title(['impulse response of TF model: ' ...
        'f_T_F=' num2str(f_TF(1),'%0.1f') ' Hz, '...
        'z_T_F=' num2str(z_TF(1)*100) '%'], ...
        'FontSize', 11,'FontWeight','normal')
        
    %% Plot impulse response of SS system
    subplot(2,1,2); 
    impulse(ss_sys,t);
    title(['impulse response of SS model: ' ...
        'f_S_S=' num2str(f_SS(1),'%0.1f') ' Hz, '...
        'z_S_S=' num2str(z_SS(1)*100) '%'], ...
        'FontSize', 11,'FontWeight','normal')
    % display('End of Section A')
end % ifSectionA ends here
%% Section B. Time response analysis of flutter
if ifSectionB
    display('Section B. Time response analysis of flutter')
    close all
    
    %% setup for time response calculations
    % display input data and Umin, UF, UD
    display('B.2 Setup for time response flutter calculations')
    display(' (a) display input data')
    fprintf(' rho=%4.3f kg/m^3 (air density) \n',rho)
    fprintf(' c=%2.1fm, m=%2.1fkg/m I0=%5.4f kg*m^2/m \n',c,m,I0)
    fprintf(' uncoupled frequencies fh=%2.1f Hz, ft=%2.1f Hz \n',fh,ft)
    fprintf(' damping ratios zh=%2.0f%%, zt=%2.0f%%, \n',[zh, zt]*100)
    fprintf(' static offset xCP=%2.1f%%, %5.4f m \n',CPratio*100,xCP)
    fprintf(' aerodynamic offset xQP=%2.1f%%, %5.4f m \n',QPratio*100, xQP)
    fprintf(' (b) Umin=%0.0f m/s \n',Umin)
    fprintf(' (c) UFdamped=%2.4f m/s -- damped flutter speed from HW01\n',UFdamped)
    UF = UFdamped; % UFdamped is the recalled damped flutter speed from HW01
    fprintf(' (d) UF=%2.4f m/s -- damped flutter speed \n',UF)
    UD = wt*sqrt(2*I0./(xQP*a1*rho*c)); % calculate divergence speed UD
    fprintf(' (e) UD=%0.4f m/s -- divergence speed \n',UD)
    
    if UF >= UD
        display([' error UF is NOT less than UD,' ...
            'program stops']); 
    else
        display(' (f) verified UF<UD')
        display(' ')
        
        if ifSectionB3 ~= 0 || ifSectionB4 ~= 0 || ifSectionB5 ~= 0
            %% Define time range
            f = min([fh,ft]); 
            T = 1/f; % time scale
            % tmax=100*T; Nt=1000; t=linspace(0,tmax,Nt); % time range
            tmax = 50*T; 
            Nt = 1000; 
            t = linspace(0,tmax,Nt); % time range
            
            %% Calculate structural matrices MS, CS, KS
            wt = 2*pi*ft; 
            wh = 2*pi*fh;
            MS = [ 1 -xCP ;
                  -m/I0*xCP Ip/I0 ]; % structural mass matrix
                  
            CS = [2*zh*wh 0 ;
                0 2*zt*wt ]; % structural viscous damping
                
            KS = [wh^2 0 ;
                  0 wt^2 ]; % structural stiffness matrix
                  
            Omega = [wh^2 0 ;
                     0 wt^2 ];
            
            %% Define aerodynamic lift function
            L0 = @(UU) a1*rho*UU^2/2*c; % Lift function for a generic speed UU
            
            %% Define airspeed range
            % ---- assign values to U -----
            if ifSectionB3
                U = [0]; 
                display('B.3 GVT time response'); 
            end % GVT conditions
            
            if ifSectionB4
                display('B.4 Flutter time response')
                eps = 1e-2; 
                U = [Umin [(1-eps) 1 (1+eps)]*UF]; 
            end % airspeeds m/s
            
            if ifSectionB5
                display(' ');
                fprintf('B.5 adjusted flutter speed UFadjusted=%2.8f m/s \n', UFadjusted)
                U = UFadjusted;
            end % ifAdjustUF ends here
            
            NU = length(U); % number of air speeds
            
            %% Reserve space
            f = zeros(4,NU); 
            z = zeros(4,NU); 
            s = zeros(4,NU);
            f_CL = zeros(4,NU); 
            z_CL = zeros(4,NU); 
            s_CL = zeros(4,NU);
            


            
            %% Loop over all airspeeds
            for jU = 1:NU
                L = L0(U(jU));
                
                %% Calculate MIMO state space model
                MA = zeros(2,2); % aerodynamic mass matrix MA=0
                CA = zeros(2,2); % aerodynamic damping matrix, CA=0
                KA = [0 L0(U(jU))/m ;
                      0 -xQP*L0(U(jU))/I0 ]; % aerodynamic stiffness matrix
                M = MS + MA; % system mass matrix
                C = CS + CA; % system viscous damping matrix
                K = KS + KA; % system stiffness matrix
                ss_sys = MIMOssModel(M,C,K,Omega);
                
                %% Extract poles, frequency, damping
                [s(:,jU),f(:,jU),z(:,jU)] = ssPolesFreqDamping(ss_sys,tol);
                
                %% Plot MIMO impulse response
                figure;
                impulse(ss_sys, t);
                
                % Build a single string for the title (MIMOtitle may return 
                % cell/char-matrix/string array)
                tFig = MIMOtitle(fh,ft,zh,zt,CPratio,QPratio,U(jU),f(:,jU),z(:,jU));
                if iscell(tFig)
                    tFig = strjoin(tFig(:).', '\n');               % cell array -> one 
                                                                   % string with newlines
                elseif isstring(tFig)
                    tFig = strjoin(tFig(:).', '\n');               % string array -> one 
                                                                   % string with newlines
                elseif ischar(tFig) && size(tFig,1) > 1
                    tFig = strjoin(cellstr(tFig), '\n');           % char matrix -> one 
                                                                   % string with newlines
                end
                
                title(gca, tFig, 'FontSize', 11, 'FontWeight', 'normal');

            end
            
            %% Display results
            display(U,'U, m/s');
            display(' (a) poles, frequencies, damping ratios')
            display(s,' poles of ss_sys');
            display([f],' f, Hz')
            display([z*100],' z%')
            display(' (b) please see plots')
            display(' (c) students should write their own discussion of results')
            % display('End of Section B')
        end % ifGVT~=0 && ifFlutter~=0 && ifAdjustUF~=0 loop ends here
    end % if UFdamped>=UD loop ends here
end % ifSectionB ends here
%% Section C. SISO SS feedback
if ifSectionC
    display('Section C: SISO SS Feedback')
    close all % close all plots
    
    %% input data
    % ----- data for example -----
    z = -z0; % -ve damping, i.e., unstable system
    display(' (a) input data')
    fprintf(' fn=%2.1f Hz, z=%2.1f%% \n',fn,z*100)
    fprintf([' desired CL damping: %0.2f times increase \n ' ...
    ' over the absolute value of the negative damping \n'], zCLratio)
    
    %% Calculate critical FB gain
    wn = 2*pi*fn;
    Kcr = -2*z/wn; % critical FB gain
    display([' (b) critical FB gain Kcr=' num2str(Kcr)])
    
    %% Calculate closed loop damping zCL and z_ratio
    zCL = zCLratio*abs(z); % +ve damping, desired closed loop damping zCL
    z_ratio = zCL/z; % z_ratio defined as zCL/z
    fprintf(' (c) zCL=%2.1f%%, z_ratio=%2.1f \n',zCL*100,z_ratio)
    
    %% Calculate velocity feedback gain to improve damping
    Kratio = 1-z_ratio;
    fprintf(' (d) Kratio=%1.2f \n',Kratio )
    K = Kratio*Kcr; % FB gain
    fprintf(' calculated FB gain K=%1.8f \n',K)
    
    %% Calculate poles, freq., damping ratios for TF and SS w/o and w FB
    display(' (e) Calculate poles, freq., damping ratios for')
    display(' TF and SS representations without and with FB')
    
    % Calculate transfer function G for the TF model
    G = tf(wn^2,[1 2*z*wn wn^2]); % transfer function G
    
    % Extract and display TF poles, frequency, damping
    [s_TF,f_TF,z_TF] = TFpolesFreqDamping(G,tol);
    display(s_TF, ' TF poles');
    display([f_TF z_TF*100], ' f_TF, Hz; z_TF%');
    
    % Calculate SS model
    ss_sys = SISOssModel(wn,z);
    
    % Extract and display SS poles, frequency, damping
    [s_SS,f_SS,z_SS] = ssPolesFreqDamping(ss_sys,tol);
    display(s_SS, ' SS poles');
    display([f_SS z_SS*100], ' f_SS, Hz; z_SS%');
    
    % Calculate TF model with FB
    H = K*tf([1 0],1);
    G_CL = feedback(G,H);
    
    % Calculate SS model with FB
    H = [0 K]; % FB matrix for SS model
    ss_sys_CL = SISO_ssModel_FB(wn,z,H);
    
    % Extract and display poles, frequency, damping of TF model with FB
    [s_CL_TF,f_CL_TF,z_CL_TF] = TFpolesFreqDamping(G_CL,tol);
    display(s_CL_TF, ' TF FB poles');
    display([f_CL_TF z_CL_TF*100], ' f_CL_TF, Hz; zh_CL_TF %');
    
    % Extract and display poles, frequency, damping of SS model with FB
    [s_CL_SS,f_CL_SS,z_CL_SS] = ssPolesFreqDamping(ss_sys_CL,tol);
    display(s_CL_SS, ' SS FB poles');
    display([f_CL_SS z_CL_SS*100], ' f_CL_SS, Hz; z_CL_SS%');
    
    %% (f) plot side by side impulse response for TF and SS w/o and w FB
    display(' (f) plot impulse response for TF and SS w/o and w FB')
    display(' please see plots')
    
    % Define time range
    T = 1/fn; 
    tmax = 150*T; 
    Nt = 1000; 
    t = linspace(0,tmax,Nt); % time range
    
    % Plot TF impulse response
    figure; 
    subplot(2,2,1); 
    impulse(G,t);
    tfig = SISOtitle(f_TF, z_TF);
    title(['TF model: ' tfig],'FontSize', 11,'FontWeight','normal')
    
    % Plot SS impulse response
    subplot(2,2,2); 
    impulse(ss_sys,t);
    tfig = SISOtitle(f_SS, z_SS);
    title(['SS model: ' tfig],'FontSize', 11,'FontWeight','normal')
    
    % Plot impulse response of TF model with FB
    subplot(2,2,3);
    impulse(G_CL, t)
    [line1,line2] = SISOtitleFB(f_TF, z_TF, Kratio, f_CL_TF, z_CL_TF);
    
    ax = gca;
    ttl = sprintf('TF model with FB\n%s\n%s', line1, line2);
    title(ax, ttl, 'FontSize', 11, 'FontWeight', 'normal');  % no color/style changes
    
    % Plot impulse response of SS model with FB
    subplot(2,2,4);
    impulse(ss_sys_CL, t);
    [line1,line2] = SISOtitleFB(f_SS, z_SS, Kratio, f_CL_SS, z_CL_SS);
    
    ax = gca;
    ttl = sprintf('SS model with FB\n%s\n%s', line1, line2);
    title(ax, ttl, 'FontSize', 11, 'FontWeight', 'normal');

    
    display(' (g) students should write their own discussion of results')
    % display('End of Section C')
end % ifSectionC ends here
%% Section D. Feedback control of flutter
if ifSectionD
    display('Section D. Feedback control of flutter')
    close all
    
    %% setup for FB control of flutter
    display('D.2 Setup for feedback control of flutter')
    display(' (a) input data')
    fprintf(' rho=%4.3f kg/m^3 (air density) \n',rho)
    fprintf(' c=%2.1fm, m=%2.1fkg/m I0=%5.4f kg*m^2/m \n',c,m,I0)
    fprintf(' uncoupled frequencies fh=%2.1f Hz, ft=%2.1f Hz \n',fh, ft)
    fprintf(' damping ratios zh=%2.0f%%, zt=%2.0f%%, \n',[zh, zt]*100)
    fprintf(' static offset xCP=%2.1f%%, %5.4f m \n',CPratio*100,xCP)
    fprintf(' aerodynamic offset xQP=%2.1f%%, %5.4f m \n',QPratio*100, xQP)
    fprintf(' (b) Umin=%0.0f m/s \n',Umin)
    UF = UFadjusted; % recall adjusted flutter speed UF from Section B
    fprintf(' (c) UF=%2.8f m/s -- adjusted flutter speed from Section B \n',UF)
    UD = wt*sqrt(2*I0./(xQP*a1*rho*c)); % calculate divergence speed UD
    fprintf(' (d) UD=%2.4f m/s -- divergence speed \n',UD)
    
    if UF >= UD
        display([' error UF is NOT less than UD,' ...
        'program stops']); 
    else
        display(' (e) verified UF<UD')
        Umax = floor(UD); % calculate Umax
        fprintf(' (f) Umax=%0.0f m/s \n',Umax)
        display(' ')
        %% Define time range
        f = min([fh,ft]); 
        T = 1/f; % time scale
        tmax = 100*T; 
        Nt = 1000; 
        t = linspace(0,tmax,Nt); % time range
        
        %% Calculate structura matrices MS, CS, KS
        MS = [ 1 -xCP ;
              -m/I0*xCP Ip/I0 ]; % structural mass matrix
              
        CS = [2*zh*wh 0 ;
              0 2*zt*wt ]; % structural viscous damping
              
        KS = [wh^2 0 ;
              0 wt^2 ]; % structural stiffness matrix
              
        Omega = [wh^2 0 ;
                 0 wt^2 ];
        
        %% Define aerodynamic lift function
        L0 = @(UU) a1*rho*UU^2/2*c; % Lift function for a generic speed UU
        
        %% Define airspeed range
        U = [Umin Umax];
        U = [Umax];
        eps = 1e-2; 
        U = [Umin [(1-eps) 1 (1+eps)]*UF Umax];
        NU = length(U); % number of airspeeds
        
        %% ========== select FB gain KK through trial and error =========
        % modify the value of KK in input data section upfront until
        % reaching the value that gives z=1% at Umax
        display(' ')
        Khh = KK; 
        Kht = 0; 
        Kth = 0; 
        Ktt = KK;
        
        H = [0 0 Khh Kht;
             0 0 Kth Ktt]; % FB matrix
        
        %% Reserve space
        f = zeros(4,NU); 
        z = zeros(4,NU); 
        s = zeros(4,NU);
        f_CL = zeros(4,NU); 
        z_CL = zeros(4,NU); 
        s_CL = zeros(4,NU);
        
        %% Loop over all airspeeds
        for jU = 1:NU
            L = L0(U(jU));
            
            %% CALCULATE MIMO STATE SPACE MODEL
            % ----- aeroelastic mass, damping, stiffness, Omega matrices
            MA = zeros(2,2); % aerodynamic mass matrix MA=0
            CA = zeros(2,2); % aerodynamic damping matrix, CA=0
            KA = [0 L0(U(jU))/m ;
                  0 -xQP*L0(U(jU))/I0 ]; % aerodynamic stiffness matrix
            M = MS + MA; % system mass matrix
            C = CS + CA; % system viscous damping matrix
            K = KS + KA; % system stiffness matrix
            
            %---------------- state space matrices -----------
            sys = MIMOssModel(M,C,K,Omega);
            
            %% Extract poles, frequency, damping
            [s(:,jU),f(:,jU),z(:,jU)] = ssPolesFreqDamping(sys,tol);
            
            %% CALCULATE IMPULSE RESPONSE
            figure;
            subplot(2,1,1);
            impulse(sys, t);
            
            % --- Open-loop title (two neat lines; TeX subscripts) ---
            ax = gca;
            ttl_ol = sprintf([ ...
                'U = %.3f m/s   |   f_1 = %.2f Hz,  z_1 = %.1f%%%%   |   f_2 = %.2f Hz,  z_2 = %.1f%%%%\n' ...
                'f_h = %.2f Hz,  f_t = %.2f Hz   |   z_h = %.1f%%%%,  z_t = %.1f%%%%   |   x_{CP} = %.1f%%%%,  x_{QP} = %.1f%%%%' ], ...
                U(jU), ...
                f(1,jU), 100*z(1,jU),  f(3,jU), 100*z(3,jU), ...
                fh, ft, 100*zh, 100*zt, 100*CPratio, 100*QPratio);
            title(ax, ttl_ol, 'FontSize', 11, 'FontWeight', 'normal', 'Interpreter','tex');
            
            %% ADD VELOCITY FEEDBACK TO IMPROVE DAMPING
            sys_CL = MIMOssModel_FB(M,C,K,Omega,H);
            
            %% EXTRACT POLES, FREQUENCY, DAMPING of FB SYSTEM
            [~,zz_CL,poles_CL] = damp(sys_CL);
            s_CL(:,jU) = poles_CL;                       % poles
            f_CL(:,jU) = abs(imag(poles_CL))/(2*pi);     % frequencies
            z_CL(:,jU) = zz_CL.*(abs(zz_CL)>tol);        % damping
            
            %% Plot impulse response with FB
            subplot(2,1,2);
            impulse(sys_CL, t);
            
            % --- Closed-loop title (compact gains on line 1; CL metrics on line 2) ---
            ax = gca;
            ttl_cl = sprintf([ ...
                'FB: K_{hh} = %.3g,  K_{ht} = %.3g,  K_{th} = %.3g,  K_{tt} = %.3g   |   U = %.3f m/s\n' ...
                'f_1^{CL} = %.2f Hz,  z_1^{CL} = %.1f%%%%   |   f_2^{CL} = %.2f Hz,  z_2^{CL} = %.1f%%%%   |   x_{CP} = %.1f%%%%,  x_{QP} = %.1f%%%%' ], ...
                Khh, Kht, Kth, Ktt, U(jU), ...
                f_CL(1,jU), 100*z_CL(1,jU),  f_CL(3,jU), 100*z_CL(3,jU), ...
                100*CPratio, 100*QPratio);
            title(ax, ttl_cl, 'FontSize', 11, 'FontWeight', 'normal', 'Interpreter','tex');


        end
        
        %% Display results
        display('D.3 Feedback control of flutter')
        display('(a) poles, freq., damping of original system')
        ff = zeros(4,NU); 
        zz = zeros(4,NU); 
        poles = zeros(4,NU);
        
        for i = 1:4
            for jU = 1:NU
                poles(i,jU) = s(i,jU); 
                ff(i,jU) = f(i,jU); 
                zz(i,jU) = z(i,jU);
            end
        end
        
        display(U,' U, m/s');
        display(s,' poles of ss_sys');
        display([f],' f, Hz')
        display([z*100],' z%')
        
        %% Display FB results
        display(' (b) FB Flutter control')
        fprintf(' trail-and-error feedback gain KK=%1.8f \n',KK)
        display(' (c) CL poles, freq., damping')
        display(U,' U, m/s');
        display(s_CL,' poles of ss_sys_CL');
        display([f_CL],' f_CL, Hz')
        display([z_CL*100],' z_CL %')
        display(' (d) please see plots')
        display(' (e) Students should write their own discussion')
    end % if UFdamped>=UD ends here
end % ifSectionD ends here
%% Section E. Flutter control through aileron feedback
if ifSectionE
    display('Section E. Flutter control through aileron feedback')
    close all
    
    %% setup for flutter control through aileron FB
    display('E.2 Setup for flutter control through aileron FB')
    display(' (a) input data')
    fprintf(' rho=%4.3f kg/m^3 (air density) \n',rho)
    display(' wing parameters')
    fprintf(' c=%2.1fm, m=%2.1fkg/m I0=%5.4f kg*m^2/m \n',c,m,I0)
    fprintf(' uncoupled frequencies fh=%2.1f Hz, ft=%2.1f Hz \n',fh,ft)
    fprintf(' damping ratios zh=%2.0f%%, zt=%2.0f%%, \n',[zh, zt]*100)
    fprintf(' static offset xCP=%2.1f%%, %5.4f m \n',CPratio*100,xCP)
    fprintf(' aerodynamic offset xQP=%2.1f%%, %5.4f m \n',QPratio*100, xQP)
    display(' aileron parameters')
    fprintf(' aileron chord ratio cd_ratio = %2.3f \n',cd_ratio)
    fprintf(' aileron offset ratio e_ratio = %2.3f \n',e_ratio)
    fprintf(' (b) Umin=%0.0f m/s \n',Umin)
    UF = UFadjusted; % recall adjusted flutter speed UF from Section B
    fprintf(' (c) UF=%2.8f m/s -- adjusted flutter speed from Section B \n',UF)
    UD = wt*sqrt(2*I0./(xQP*a1*rho*c)); % calculate divergence speed UD
    fprintf(' (d) UD=%2.4f m/s -- divergence speed \n',UD)
    
    if UF >= UD
        display([' error UF is NOT less than UD,' ...
        'program stops']); 
    else
        display(' (e) verified UF<UD')
        Umax = floor(UD); % calculate Umax
        fprintf(' (f) Umax=%0.0f m/s \n',Umax)
        cd = cd_ratio*c; % aileron chord
        e = e_ratio*c; % aileron offset
        fprintf(' (g) aileron chord cd = %2.3f \n',cd)
        fprintf(' aileron offset e = %2.3f \n',e)
        
        %% Define time range
        f = min([fh,ft]); 
        T = 1/f; % time scale
        tmax = 100*T;
        Nt = 1000; 
        t = linspace(0,tmax,Nt); % time range
        
        %% Calculate structural matrices MS, CS, KS
        wt = 2*pi*ft; 
        wh = 2*pi*fh;
        MS = [ 1 -xCP ;
              -m/I0*xCP Ip/I0 ]; % structural mass matrix
              
        CS = [2*zh*wh 0 ;
              0 2*zt*wt ]; % structural viscous damping
              
        KS = [wh^2 0 ;
              0 wt^2 ]; % structural stiffness matrix
        
        %% Define aerodynamic lift function
        L0 = @(UU) a1*rho*UU^2/2*c; % wing lift function for a generic speed UU
        Ld0 = @(UU) ad*rho*UU^2/2*cd; % aileron lift function for a generic speed UU
        
        %% Define airspeed range
        % U=[Umin Umax];
        eps = 1e-2; 
        U = [Umin [(1-eps) 1 (1+eps)]*UF Umax];
        NU = length(U); % number of airspeeds
        
        %% ========== select FB gain KK through trial and error =========
        % modify the values of Kdh and Kdt in input data section upfront until
        % reaching the values that gives z>=1% at Umin and z~1% at Umax
        
        %% Reserve space
        f = zeros(4,NU); 
        z = zeros(4,NU); 
        s = zeros(4,NU);
        f_CL = zeros(4,NU); 
        z_CL = zeros(4,NU); 
        s_CL = zeros(4,NU);

        
%%%%%% STUDENT ADDED CODE TO AUTO-FIND IDEAL Kdh Kdt VALUES
        %% ---------- call external auto-search function ----------
        params = struct();
        params.Kdh_min = Kdh_min;
        params.Kdh_max = Kdh_max;
        params.Kdt_min = Kdt_min;
        params.Kdt_max = Kdt_max;
        params.step = step;
        params.U = U;
        params.Umin_idx = 1;
        params.Umax_idx = numel(U);
        params.target = 0.01;
        params.tolTarget = 5e-2;
        params.tolTargetRow4 = 1e-3;
        params.minPos = 1e-6;
        params.target_idx = 4;   % enforce closeness at column 4 (just above UF)
        params.minUminZ = params.target; % ensure Umin rows stay ≥ 1%
        params.L0fun = L0;
        params.Ld0fun = Ld0;
        params.MS = MS; params.CS = CS; params.KS = KS;
        params.xQP = xQP; params.e = e; params.m = m; params.I0 = I0;
        params.outfname = 'solutions_KdhKdt_-50_50_0p1.csv';
        params.useParallel = false;  % set to false if you don't have Parallel Toolbox
        params.reportEvery = 50000;
        
        % [Tsol, best, stats] = auto_search_KdhKdt(params);
        % 
        % if isempty(best)
        %     fprintf('No feasible auto-search solution found. Please relax tolerances or expand grid.\n');
        %     % leave user-defined Kdh,Kdt in place or prompt to change manually
        % else
        %     Kdh = best.Kdh;
        %     Kdt = best.Kdt;
        %     fprintf('Auto-selected Kdh=%.6f, Kdt=%.6f (SSE=%.3e). See %s\n', Kdh, Kdt, best.SSE, params.outfname);
        % end
        % fprintf('Auto search finished. Time elapsed: %.1fs. Found %d candidates.\n', stats.elapsed, stats.count);
%%%%%%STUDENT ADDED CODE TO AUTO-FIND IDEAL Kdh Kdt VALUES

        %% Loop over all airspeeds
        for jU = 1:NU
            L  = L0(U(jU));
            Ld = Ld0(U(jU));
        
            %% Calculate MIMO state space model
            MA = zeros(2,2); % aerodynamic mass matrix MA=0
            CA = zeros(2,2); % aerodynamic damping matrix, CA=0
            KA = [0  L0(U(jU))/m ;
                  0 -xQP*L0(U(jU))/I0 ]; % aerodynamic stiffness matrix
            M = MS + MA;              % system mass matrix
            C = CS + CA;              % system viscous damping matrix
            K = KS + KA;              % system stiffness matrix
            Omega = [wh^2 0 ;
                     0   wt^2 ];
        
            % ========== aileron matrices ===========
            E = [-Ld/m ;
                 -e*Ld/I0];
        
            %---------------- state space matrices -----------
            AA = [zeros(2,2) eye(2) ;
                  -M\K      -M\C ];
            BB = [0 ;
                  0 ;
                  M\E];
            CC = [eye(2) zeros(2,2)];
            DD = zeros(2,1);
            ss_sys = ss(AA,BB,CC,DD);
        
            %% Extract poles, frequency, damping
            [s(:,jU),f(:,jU),z(:,jU)] = ssPolesFreqDamping(ss_sys,tol);
        
            %% Plot MIMO impulse response (open-loop)
            figure;
            subplot(2,1,1);
            impulse(ss_sys,t);
        
            ttl = sprintf(['Aeroelastic 2x2 MIMO — U = %.3f m/s\n' ...
                           'fh = %.1f Hz   ft = %.1f Hz   |   zh = %.1f%%%%   zt = %.1f%%%%\n' ...
                           'Modes:  f1 = %.1f Hz  z1 = %.1f%%%%   |   f2 = %.1f Hz  z2 = %.1f%%%%\n' ...
                           'x_{CP} = %.1f%%%%   x_{QP} = %.1f%%%%'], ...
                           U(jU), fh, ft, 100*zh, 100*zt, ...
                           f(1,jU), 100*z(1,jU), f(3,jU), 100*z(3,jU), ...
                           100*CPratio, 100*QPratio);
            th = title(ttl); th.FontSize = 11; th.FontWeight = 'normal';
        
            %% Add velocity feedback to control flutter
            H = [0 0 Kdh Kdt]; % FB matrix
        
            %% ================= state space matrices with FB =================
            AA_CL = AA - BB*H;              % state matrix AA with FB
            CC_CL = CC - DD*H;              % equals CC since DD=0 (kept for clarity)
            sys_CL = ss(AA_CL, BB, CC_CL, DD);
        
            %% Extract poles, frequency, damping of FB model
            [~,zz_CL,poles_CL] = damp(sys_CL);
            s_CL(:,jU) = poles_CL;                      % poles
            f_CL(:,jU) = abs(imag(poles_CL))/(2*pi);    % frequencies
            z_CL(:,jU) = zz_CL.*(abs(zz_CL)>tol);       % damping
        
            %% Plot impulse response with FB (closed-loop)
            subplot(2,1,2);
            impulse(sys_CL,t);
        
            ttl = sprintf(['Aileron Velocity FB — U = %.3f m/s   (Kdh = %g, Kdt = %g)\n' ...
                           'fh = %.1f Hz   ft = %.1f Hz   |   zh = %.1f%%%%   zt = %.1f%%%%\n' ...
                           'Closed-loop:  f1 = %.1f Hz  z1 = %.1f%%%%   |   f2 = %.1f Hz  z2 = %.1f%%%%\n' ...
                           'x_{CP} = %.1f%%%%   x_{QP} = %.1f%%%%'], ...
                           U(jU), Kdh, Kdt, ...
                           fh, ft, 100*zh, 100*zt, ...
                           f_CL(1,jU), 100*z_CL(1,jU), f_CL(3,jU), 100*z_CL(3,jU), ...
                           100*CPratio, 100*QPratio);
            th = title(ttl); th.FontSize = 11; th.FontWeight = 'normal';
        
        end % jU loop ends here
        
        %% Reorder closed-loop data for display (smallest-frequency pair in rows 2 & 3)
        for jU = 1:NU
            [~, idx] = sort(f_CL(:,jU), 'ascend');
            if numel(idx) >= 4
                reorderIdx = [idx(3); idx(1); idx(2); idx(4)];
                f_CL(:,jU) = f_CL(reorderIdx,jU);
                z_CL(:,jU) = z_CL(reorderIdx,jU);
                s_CL(:,jU) = s_CL(reorderIdx,jU);
            end
        end



        
        
        %% Display results
        display('E.3 Flutter control through aileron feedback')
        display(' (a) poles, freq, damping of original system')
        ff = zeros(4,NU); 
        zz = zeros(4,NU); 
        poles = zeros(4,NU);
        
        for i = 1:4
            for jU = 1:NU
                poles(i,jU) = s(i,jU); 
                ff(i,jU) = f(i,jU); 
                zz(i,jU) = z(i,jU);
            end
        end
        
        display(U,' U, m/s');
        display(s,' poles of ss_sys');
        display([f],' f, Hz')
        display([z*100],' z%')
        
        %% Display FB results
        display(' (b) velocity FB aileron control results')
        display([Kdh Kdt],' Kdh, Kdt aileron FB gains by trail-and-error ')
        display(' (c) CL poles, freq., damping')
        display(U,' U, m/s');
        display(s_CL,' poles of ss_sys_CL');
        display([f_CL],' f_CL, Hz')
        display([z_CL*100],' z_CL %')
        display(' (d) please see plots')
        display(' (e) Students should write their own discussion')
    end % if UFdamped>=UD ends here
end % ifSectionE ends here
%% Section F. Challenge problems
if ifSectionF
    display('Section F. GVT negative damping suppression')
    close all
    
    %% (a) input data
    zh = -zh; % negative plunge damping
    zt = -zt; % negative pitch damping
    zhCL = zhCLratio*abs(zh); % desired +ve damping for plunge zhCL
    ztCL = ztCLratio*abs(zt); % desired +ve damping for pitch ztCL
    zh_ratio = zhCL/zh; % zh_ratio defined as zhCL/zh
    zt_ratio = ztCL/zt; % zt_ratio defined as ztCL/zt
    Kh_cr = -2*zh/wh; 
    Kt_cr = -2*zt/wt; % critical FB gains
    
    display(' (a) input data')
    fprintf(' c=%2.1fm, m=%2.1fkg/m I0=%5.4f kg*m^2/m \n',c,m,I0)
    fprintf(' uncoupled frequencies fh=%2.1f Hz, ft=%2.1f Hz \n',fh, ft)
    fprintf(' damping ratios zh=%2.0f%%, zt=%2.0f%%, \n',[zh, zt]*100)
    fprintf(' static offset xCP=%2.1f%%, %5.4f m \n',CPratio*100,xCP)
    fprintf(' %0.2f times desired |zh| damping increase by FB \n', zhCLratio)
    fprintf(' %0.2f times desired |zt| damping increase by FB\n', ztCLratio)
    
    %% (b) POLES, FREQUENCIES, DAMPING OF ss_sys MODEL
    % CALCULATE MIMO STATE SPACE GVT MODEL
    % ----- aeroelastic mass, damping, stiffness, Omega matrices
    MS = [1 -xCP ;
          -m*xCP/I0 Ip/I0 ];
    CS = [2*zh*wh 0 ;
          0 2*zt*wt ];
    KS = [wh^2 0 ;
          0 wt^2 ];
    Omega = [wh^2 0 ;
             0 wt^2 ];
    %-----------------------------------
    AA = [zeros(2,2) eye(2) ;
          -MS\KS -MS\CS ];
    BB = [zeros(2,2);
          MS\Omega ];
    CC = [eye(2) zeros(2,2)];
    DD = zeros(2,2);
    ss_sys = ss(AA,BB,CC,DD);
    [omeg,zz,poles] = damp(ss_sys);
    s = poles; % poles
    f_raw = abs(imag(s))/(2*pi); % frequencies
    z_raw = zz.*(abs(zz)>tol); % damping
    f = f_raw; 
    z = z_raw;
    display(' (b) poles, freq, damping of original system')
    display(s,' poles of ss_sys');
    display([f z*100],' f, Hz z %')
    
    %% (c) ADD VELOCITY FEEDBACK TO IMPROVE DAMPING
    % ===== calculate critical gain K_ratio for h and t ===========
    Kh_ratio = 1 - zh_ratio; 
    Kt_ratio = 1 - zt_ratio;
    Kh = Kh_ratio*Kh_cr; 
    Kt = Kt_ratio*Kt_cr; % FB gains
    
    display(' (c) add velocity FB to improve damping')
    display([zhCL*100 zh_ratio Kh_ratio Kh], ' zhCL% aim zh_ratio Kh_ratio Kh')
    display([ztCL*100 zt_ratio Kt_ratio Kt], ' ztCL% aim zt_ratio Kt_ratio Kt')
    Khh = Kh; 
    Kht = 0; 
    Kth = 0; 
    Ktt = Kt;
    
    H = [0 0 Khh Kht;
         0 0 Kth Ktt]; % FB matrix
    %====================================
    AA_CL = AA - BB*H; % state matrix AA with FB
    sys_CL = ss(AA_CL, BB, CC, DD);
    
    %% (d) EXTRACT POLES, FREQUENCIES, DAMPING OF ss_sys_CL MODEL
    [omeg_CL,zz_CL,poles_CL] = damp(sys_CL);
    s_CL = poles_CL; % poles
    f_CL = abs(imag(poles_CL))/(2*pi); % frequencies
    z_CL = zz_CL.*(abs(zz_CL)>tol); % damping
    display(' (d) poles, freq, damping of ss_sys_CL system')
    display(s_CL,' poles of ss_sys_CL');
    display([f_CL z_CL*100],' f_CL, Hz z_CL %')
    display(' (e) please see plots')
    display(' (f) Students should write their own discussion')
    
    %% DEFINE TIME RANGE
    fmin = min([fh,ft]); 
    T = 1/fmin; % time scale
    tmax = 50*T; 
    Nt = 1000; 
    t = linspace(0,tmax,Nt);
    
    %% PLOT IMPULSE RESPONSE
    % 2x2 MIMO impulse response
    % figure(nfig); nfig=nfig+1;
    figure; 
    subplot(2,1,1); 
    impulse(ss_sys,t);
    T1 = ['-ve damping GVT'];
    T2a = [' f1=' num2str(f(1),'%0.1f') 'Hz'];
    T2b = [' z1= ' num2str(z(1)*100,'%0.1f') '%'];
    T3a = [' f2=' num2str(f(3),'%0.1f') 'Hz'];
    T3b = [' z2= ' num2str(z(3)*100,'%0.1f') '%'];
    T5 = [' xCP= ' num2str(CPratio*100) '%'] ;
    T6 = [' fh=' num2str(fh) 'Hz ft=' num2str(ft) 'Hz'];
    T7 = [' zh= ' num2str(zh*100) '% zt= ' num2str(zt*100) '%'];
    line1 = [T1 T2a T3a T2b T3b]; 
    line2 = [T5 T6 T7];
    % Open-loop title (two clean lines, TeX subscripts)
    ax = gca;
    ttl_ol = sprintf([ ...
        'GVT (negative damping)  —  f_1 = %.1f Hz, z_1 = %.1f%%%%  |  f_2 = %.1f Hz, z_2 = %.1f%%%%\n' ...
        'f_h = %.1f Hz, f_t = %.1f Hz   |   z_h = %.1f%%%%, z_t = %.1f%%%%   |   x_{CP} = %.1f%%%%, x_{QP} = %.1f%%%%' ], ...
        f(1), 100*z(1),  f(3), 100*z(3), ...
        fh, ft, 100*zh, 100*zt, 100*CPratio, 100*QPratio);
    title(ax, ttl_ol, 'FontSize', 11, 'FontWeight', 'normal', 'Interpreter','tex');

    
    %% PLOT IMPULSE RESPONSE WITH FB
    % 2x2 MIMO impulse response with feedback
    subplot(2,1,2); 
    impulse(sys_CL,t)
    T1 = ['FB GVT'];
    Th_CL = [' Khh=' num2str(Kh_ratio) '*Khcrt' ' Kht=' num2str(Kht) ];
    Tt_CL = [ ' Kth=' num2str(Kth) ' Ktt=' num2str(Kt_ratio) '*Ktcrt'];
    T2a = [' f1CL=' num2str(f_CL(1),'%0.1f') 'Hz'];
    T2b = [' z1CL=' num2str(z_CL(1)*100,'%0.1f') '%'];
    T3a = [' f2CL=' num2str(f_CL(3),'%0.1f') 'Hz'];
    T3b = [' z2CL=' num2str(z_CL(3)*100,'%0.1f') '%'];
    T5 = [' xCP= ' num2str(CPratio*100) '%'] ;
    T6 = [' fh=' num2str(fh) 'Hz ft=' num2str(ft) 'Hz'];
    T7 = [' zh= ' num2str(zh*100) '% zt= ' num2str(zt*100) '%'];
    line1 = [T1 Th_CL Tt_CL];
    line2 = [T2a T3a T2b T3b];
    line3 = [T5 T6 T7];
    % Closed-loop title (two lines, compact gain info)
    ax = gca;
    ttl_cl = sprintf([ ...
        'FB GVT  —  K_{hh} = %.3g*K_{h,cr},  K_{ht} = %.3g,  K_{th} = %.3g,  K_{tt} = %.3g*K_{t,cr}\n' ...
        'f_1^{CL} = %.1f Hz, z_1^{CL} = %.1f%%%%  |  f_2^{CL} = %.1f Hz, z_2^{CL} = %.1f%%%%   |   x_{CP} = %.1f%%%%, x_{QP} = %.1f%%%%' ], ...
        Kh_ratio, Kht, Kth, Kt_ratio, ...
        f_CL(1), 100*z_CL(1),  f_CL(3), 100*z_CL(3), 100*CPratio, 100*QPratio);
    title(ax, ttl_cl, 'FontSize', 11, 'FontWeight', 'normal', 'Interpreter','tex');

end % ifSectionF ends here


%% finish
display(' ---------------')
display (['success! ' mfilename ' finished successfully'])
