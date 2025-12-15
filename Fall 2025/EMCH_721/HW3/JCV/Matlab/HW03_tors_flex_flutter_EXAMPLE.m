%{
HW03 EXAMPLE
Torsion-flexure flutter of fixed-free wing
%}

%% Magic numbers overview (edit here first)
% Initialization: mm=1e-3 (m/mm), deg=180/pi (rad->deg), tol=1e-10 (zero cut)
% Aerodynamics: rho=1.225 (kg/m^3), a1=2*pi (lift-curve slope)
% Geometry/structure: c=0.4 m, m=3 kg, I0=0.0288 kg*m^2, fh=2 Hz, ft=5 Hz,
%   CPratio=-0.10, QPratio=0.30, L=2 m, scale=8, NW=4, NPhi=3
% Speed sweep: Ustart=0 m/s, Uend=12 m/s, UFrigid=8.244 m/s, UFread=8.34 m/s
% Discretization/animation: Nz=100, NU=1001, Nx=1e2, Nc=5, Nt=1e2, zmax=1.2,
%   VideoWriter FrameRate=10, Quality=100
% Feature toggles: ifA1flexure, ifA2torsion, ifGVT, ifFlutter, ifZoom,
%   ifFlutterModes, ifdisplayfV, ifanimation

%% initialization
clc                            % clear command window
clear                          % clear workspace
close all                      % close all plots
format compact
set(0,'DefaultFigureWindowStyle','docked')

nfig = 1;
mm   = 1e-3; deg = 180/pi;
tol  = 1e-10;                 % tolerance for discarding machine zero

%% DEFINE AERODYNAMIC PARAMETERS
rho = 1.225;                   % air density, 1.225 kg/m3
a1  = 2*pi;                    % ideal lift curve slope value

%% INPUT DATA
% ----- data for EXAMPLE -----
c       = 0.45;                 % airfoil chord, m
m       = 3.2;                   % mass, kg
I0      = 0.055;              % moment of inertia about the center of mass, kg*m^2
fh      = 1.8;                   % plunge frequency, Hz
ft      = 5.3;                   % pitch frequency, Hz
CPratio = -10e-2;              % static offset as % of chord
QPratio = 35e-2;               % aerodynamic offset ratio as % of chord
L       = 2.5;                   % span, m
scale   = 8;                   % scale up factor for plunge displ
NW      = 4;                   % number of flexural modes
NPhi    = 3;                   % number of torsional modes 
Ustart  = 0; 
Uend    = 12;                  % flutter range
UFrigid = 10.654;               % flutter speed of rigid airfoil model from HW01
UFread  = 10.788;                % flutter speed of structural dynamics wing model read on the plot
 
%% CALCULATED DATA
xCP     = CPratio*c;           % static offset value
xQP     = QPratio*c;           % aerodynamic offset calculated with % of chord
Ip      = I0+m*xCP^2;          % moment of inertia about the elastic center, kg*m^2/m

% DISPLAY GIVEN DATA
display(' HW03 structural dynamics flutter analysis -- JC Vaught')
display(' input data')
fprintf(' air density rho=%4.3fkg/m^3 \n',rho)
fprintf(' c=%2.1fm, m=%2.1fkg/m, I0=%5.4fkg*m^2/m, L=%2.1fm \n',c,m,I0,L)
fprintf(' static offset xCP=%2.1f%%, %5.4fm \n',CPratio*100,xCP)
fprintf(' aerodynamic offset xQP=%2.1f%%, %5.4fm \n',QPratio*100,xQP)
fprintf(' rigid body frequencies fh=%2.1fHz, ft=%2.1fHz \n',fh,ft)
fprintf(' wing span L=%0.1f m \n', L)

%% choose what to do, to plot, and to display
% ifA1flexure = 0; % do not plot W modeshapes
ifA1flexure  = 0; % plot W modeshapes
ifA2torsion  = 0; % do not plot Phi modeshapes

ifGVT        = 1; % perform GVT analysis - Part C

ifFlutter    = 0; % perform flutter analysis - Part D.a

ifZoom       = 0; % provide calcuaotionjs/table - Part D.b

ifFlutterModes = 0; % plot flutter modes - Part D.c

ifdisplayfV  = 0; % do NOT display freq. and modeshapes

ifanimation  = 1; % do NOT animate GVT and flutter modeshapes


%% CALCULATE UNCOUPLED ANGULAR FREQUENCIES wt, wh
wt = 2*pi*ft; 
wh = 2*pi*fh;

%% discretize beam length
Nz = 100; 
zL = linspace(0,L,Nz);
%% Section A1: FLEXURAL FREQUENCIES AND MODESHAPES 
% calculate flexural eigenvalues 
gL_guess = zeros(NW,1); 
gL       = zeros(NW,1); 
beta     = zeros(NW,1);

D = @(x)(cos(x)+1/cosh(x));      % D=0 equation to solve 
for jW = 1:NW
    gL_guess(jW) = (2*jW-1)*pi/2;                % initial guess
    zW           = fzero(D,gL_guess(jW));        % solve equation
    gL(jW)       = zW;                           % store gL=gamma*L
end

% calculate wave number, angular frequency in rad/s, freq. in Hz 
gW = gL/L;                        % flexural wave number
aW = sqrt(wh)/gW(1);              % flex const aW to match first freq fW(1)=fh
EI = m*aW^4;                      % flexural stiffness EI of the wing, N*m^2/m
wW = gW.^2*aW^2;                  % angular frequency, rad/sec
fW = wW/2/pi;                     % frequency in Hz

% Calculate and plot modeshapes
W    = zeros(Nz,NW); 
AW   = zeros(1,NW);
beta = zeros(1,NW);
for jW = 1:NW
    AW(jW)   = 1/sqrt(L); 
    beta(jW) = (sinh(gL(jW))-sin(gL(jW)))/(cosh(gL(jW))+cos(gL(jW))); 
    W(:,jW)  = AW(jW)*(cosh(gW(jW)*zL)-cos(gW(jW)*zL)...
    -beta(jW)*(sinh(gW(jW)*zL)-sin(gW(jW)*zL))); 
end

if ifA1flexure
    display(' ')
    display('Section A1: flexural vibration of a fixed-free beam')
    display(' (a) students should recall relevant formulae from')
    display(' in-class instruction and class notes')
    fprintf(' (b) NW=%1.0f \n',NW)
    display(gL',' roots of flexural characteristic equation')
    fprintf(' (c) flexural stiffness EI =%4.0f N*m^2/m \n',EI)
    display(' (d) flexural wavenumbers, natural freq. in rad/s and Hz')
    display([gW,wW,fW], ' gW,rad/m wW,rad/s fW,Hz')
    display(' (e) please see plot')
    figure; plot(zL,W); grid; 
    title('Flexural modes of fixed-free beam', 'FontWeight', 'normal')
    xlabel('length, m'); ylabel('normalized modeshape')
end % ifplotW ends here

%% Section A2: TORSIONAL FREQUENCIES AND MODESHAPES
% torsional frequencies and modeshapes
gL  = zeros(NPhi,1);
cPhi = 2*L/pi*wt;                       % torsional wave speed
Phi = zeros(Nz,NPhi); gPhi = zeros(NPhi,1); B = zeros(NPhi,1);
for jPhi = 1:NPhi
    gL(jPhi)   = (2*jPhi-1)*pi/2;       % roots of torsional characteristic equation
    gPhi(jPhi) = gL(jPhi)/L;            % torsional wavenumber
    APhi(jPhi) = sqrt(2/L);             % mode amplitude, torsion
    Phi(:,jPhi)= APhi(jPhi)*sin(gPhi(jPhi)*zL); % modeshapes, torsion
    wPhi(jPhi) = cPhi*gPhi(jPhi);       % angular frequencies rad/s
end
GJ  = I0*cPhi^2;                        % torsional stiffness GJ of the wing, N*m^2/m
fPhi= wPhi/(2*pi);                      % freq. in Hz
if ifA2torsion
    display(' ')
    display('Section A2: torsional vibration of a fixed-free beam')
    display(' (a) students should recall relevant formulae from')
    display(' in-class instruction and class notes')
    fprintf(' (b) NPhi=%1.0f \n',NPhi)
    display(gL',' roots of torsional characteristic equation')
    fprintf(' (c) torsional stiffness GJ =%4.1f N*m^2/m \n',GJ)
    display(' (d) torsional wavenumbers, natural freq. in rad/s and Hz')
    display([gPhi,wPhi',fPhi'], ' gPhi,rad/m wPhi,rad/s fPhi,Hz')
    display(' (e) please see plot')
    figure ; plot(zL,Phi);grid; 
    title ('Torsional modes of fixed-free beam', 'FontWeight', 'normal')
    xlabel('length, m'); ylabel('normalized modeshape')
end % ifplotPhi ends here

%% Calculate modal matrices
N        = NW+NPhi;               % total number of modes
wW2      = wW.^2; 
mWW      = m*diag(ones(NW,1)); 
kS_WW    = diag(wW2)*m;
wPhi2     = wPhi.^2; 
mPhiPhi  = Ip*diag(ones(NPhi,1)); 
kS_PhiPhi= diag(wPhi2)*I0;
mWPhi    = zeros(NW,NPhi);
kS_WPhi  = zeros(NW,NPhi); 
kS_PhiW  = zeros(NPhi,NW);
for pPhi = 1:NPhi
    for qW = 1:NW
        modePhi = @(x) APhi(pPhi)*sin(gPhi(pPhi)*x); 
        modeW   = @(x) AW(qW)*((-cos(gW(qW)*x)+beta(qW)*sin(gW(qW)*x)...
                    +(1-beta(qW))/2*exp(gW(qW)*x)+(1+beta(qW))/2*exp(-gW(qW)*x))); 
        Int     = @(x) modePhi(x).*modeW(x);
        mWPhi(qW,pPhi) = -m*xCP*integral(Int,0,L);
    end
end
mPhiW = mWPhi';

%% DEFINE STRUCTURAL MATRICES
% structural mass matrix
MS=[mWW mWPhi ;
mPhiW mPhiPhi]; 
% structural stiffness matrix
KS=[kS_WW kS_WPhi ; 
kS_PhiW kS_PhiPhi]; 

%% Section C: GVT
if ifGVT
    display(' ')
    display(' Section C: GVT analysis')
    fprintf(' (a) NW=%1.0f, NPhi=%1.0f, N=%1.0f \n',NW,NPhi,N)
    %% CALCULATE EIGENVALUES: 
    % use polyeig to get eigenvectors V and eigenvalues s
    [V_raw,s_raw] = polyeig(KS,0,MS);
    V_raw(1:NW,:)=V_raw(1:NW,:)*scale; % scale up plunge displ
    [V,s]=sort_norm_eig(V_raw,s_raw);
    %% EXTRACT FREQ. IMAG PART OF s
    f=abs(imag(s))/(2*pi); % frequencies
    %% DISPLAY FREQUENCY
    display(f,' (b) coupled GVT frequencies f, Hz')
    %% DISPLAY EIGENVECTORS
    display(real(V),' GVT eigenvectors')
    display(' students should write their own discussion')
    display(' (c) please see plots')
    %% 3D plotting of the GVT coupled modes v(x,z)
    Nx=1e2; x=linspace(c/2,-c/2,Nx); % define x range
    % select mode to plot
    N=NW+NPhi;
    Nmax=2*N; % max number of modes to plot
    % Nmax=3; % for debugging 
    for mode=1:2:Nmax
        titleModeGVT=['GVT Mode ' num2str(mode) ', f=' num2str(f(mode),'%0.2f') ' Hz' ];
        Vxz=zeros(Nx,Nz);
        for i=1:Nx
            Vxz(i,:)=W*V(1:NW,mode)-x(i)*Phi*V(NW+1:NW+NPhi,mode);
        end
        Vxz = real(Vxz); % eigenvectors are complex; use physical (real) part for plotting
        figure;
        surf(zL,x,Vxz); % surf plot
        % view(0,90) % top view
        % view(45,60) % rotated view
        view(16,84) % rotated view VG
        zlim([-2 2])
        set(gca,'Ydir','reverse')
        % set(gca,'Ydir','normal')
        shading interp
        axis equal
        xlim([0 L]); 
        % ylim([-c/2 c/2]);
        xlabel('z, m'); ylabel('x, m');
        set(gca, 'FontSize', 12);
        tl=title({'GVT Coupled Modeshapes'; titleModeGVT});
        tl.FontWeight='normal'; tl.FontSize=12;
        %% 3D animation of the GVT coupled modes v(x,z)
        if ifanimation
            Nc=5; Nt=1e2; t=linspace(0,Nc/f(mode),Nt); % define time range over 5 cycles
            animation = VideoWriter(titleModeGVT);
            animation.FrameRate = 10; %% time interval between two frame
            animation.Quality =100; open(animation);
            Vxz=zeros(Nx,Nz);
            zmax=1.2;
            for k=1:Nt
                for i=1:Nx
                    Vxz(i,:)=(W*V(1:NW,mode)-x(i)*Phi*V(NW+1:NW+NPhi,mode))...
                    *exp(1i*2*pi*f(mode)*t(k));
                end
                figure(100) % figure(100) is used to generate the animation
                surf(zL,x,real(Vxz)); % surf plot
                % view(45,60) % rotated view
                view(16,84) % rotated view VG
                set(gca,'Ydir','reverse')
                shading interp
                axis equal
                xlim([0 L]); ylim([-c/2 c/2]); zlim([-zmax zmax]); 
                xlabel('z, m'); ylabel('x, m');
                set(gca, 'FontSize', 12);
                tl=title({'GVT Coupled Modeshapes'; titleModeGVT});
                tl.FontWeight='normal'; tl.FontSize=12;
                thisFrame = getframe(gcf);
                writeVideo(animation, thisFrame);
            end
            close(animation);
        end % ifanimation ends here
    end % mode loop ends here
end % ifGVT ends here

%% FLUTTER ANALYSIS section
if ifFlutter
    ifplot = 1;                             % plot flutter diagram

    %% DEFINE AERODYNAMIC LIFT FUNCTION
    a1 = 2*pi;                              % ideal lift curve slope value
    L0 = @(UU) rho*UU^2/2*c*a1;             % Lift function for a generic speed UU

    %% DEFINE AIRSPEED RANGE
    NU = 1001; 
    U  = linspace(Ustart, Uend, NU);        % airspeed range
    UF = UFread;
    if ifZoom
        eps = 1e-2; 
        U   = [1-eps 1 1+eps]*UF;           % zoom around UF
    end
    if ifFlutterModes
        U = UF;                             % plot flutter modes at flutter speed
    end
    NU = length(U); 
    if NU < 10
        ifplot = 0;
    end

    %% LOOP OVER ALL AIR SPEEDS
    r     = zeros(2*N,NU); 
    v     = zeros(N,2*N,NU); 
    f     = zeros(2*N,NU); 
    z     = zeros(2*N,NU);
    sigma = zeros(2*N,NU); 
    roots = zeros(2*N,NU);

    for jU = 1:NU
        %% DEFINE FLUTTER MATRICES
        MA      = zeros(N,N);                    % aerodynamic mass matrix MA=0 
        kA_WW   = zeros(NW,NW); 
        kA_PhiW = zeros(NPhi,NW);
        for pPhi = 1:NPhi
            for qW = 1:NW
                modePhi = @(x) APhi(pPhi)*sin(gPhi(pPhi)*x); 
                modeW   = @(x) AW(qW)*((-cos(gW(qW)*x)+beta(qW)*sin(gW(qW)*x)...
                        +(1-beta(qW))/2*exp(gW(qW)*x)+(1+beta(qW))/2*exp(-gW(qW)*x))); 
                Int     = @(x) modePhi(x).*modeW(x);
                kA_WPhi(qW,pPhi) = L0(U(jU))*integral(Int,0,L); 
            end
        end
        for pPhi = 1:NPhi
            for qPhi = 1:NPhi
                modePhi = @(x,j) APhi(j)*sin(gPhi(j)*x); 
                Int     = @(x) modePhi(x,pPhi).*modePhi(x,qPhi);
                kA_PhiPhi(qPhi,pPhi) = -L0(U(jU))*xQP*integral(Int,0,L); 
            end
        end

        % aerodynamic stiffness matrix
        KA = [kA_WW kA_WPhi ; 
              kA_PhiW kA_PhiPhi]; 
        M  = MS+MA;                      % system mass matrix
        K  = KS+KA;                      % system stiffness matrix

        %% CALCULATE EIGENVALUES: 
        % use polyeig to get eigenvectors V and eigenvalues s
        [V_raw,s_raw] = polyeig(K,0,M);
        V_raw(1:NW,:) = V_raw(1:NW,:)*scale; % scale up plunge displ
        [V,s] = sort_norm_eig(V_raw,s_raw);

        %% EXTRACT DAMPING AND FREQ. FROM REAL AND IMAG PARTS OF s
        ff  = abs(imag(s))/(2*pi);           % frequencies
        zz  = -real(s)./abs(s); zz=zz.*(abs(zz)>tol); % damping
        sig = real(s); sig=sig.*(abs(sig)>tol); 

        %% STORE EIGENVALUES AND EIGENVECTOR
        r(:,jU)      = s; 
        v(:,:,jU)    = V;
        f(:,jU)      = ff(:); 
        z(:,jU)      = zz(:);
        sigma(:,jU)  = sig(:);
    end

    %% DISPLAY FREQ, DAMPING AND MODESHAPES
    if ifZoom 
        for jU = 1:NU
            display(' ')
            display([' U=' num2str(U(jU)) 'm/s']);
            display(f(:,jU)',' f, Hz')
            display(z(:,jU)'*100,' z %')
            display(v(:,:,jU),' eigenvector V'); 
        end
    end

    %% PLOT FREQUENCY AND DAMPING VS AIRSPEED
    if ifplot
        figure
        subplot(2,1,1); 
        plot(U,f,'.r'); 
        title(['xCP=' num2str(CPratio*1e2) '% ' ...
               'xQP=' num2str(QPratio*1e2) '%'],'FontSize', 10, 'FontWeight', 'normal')
        xlabel('U, m/s'); ylabel('f, Hz'); 
        fmax=ceil(max(max(f))); ylim([0 fmax]);
        xlim([U(1) U(NU)]); 
        hold on
        subplot(2,1,2); 
        plot(U,z*1e2,'.g'); 
        xlim([U(1) U(NU)]); 
        xlabel('U, m/s'); ylabel('\zeta, %');
        ymax=15; ylim([-ymax ymax]); 
        grid on
        hold on
    end

    %% coupled flutter mode plotting v(x,z)
    if ifFlutterModes
        Nx=1e2; x=linspace(c/2,-c/2,Nx); % define x range
        N=NW+NPhi;
        Nmax=2*N; % max number of modes to plot
        for mode=1:2:Nmax
            titleModeFlutter=['Flutter Mode ' num2str(mode) ];
            Vxz=zeros(Nx,Nz);
            for i=1:Nx
                Vxz(i,:)=W*V(1:NW,mode)-x(i)*Phi*V(NW+1:NW+NPhi,mode);
            end
            Vxz = real(Vxz); % keep only real part for visualization
            figure;
            surf(zL,x,Vxz); % surf plot
            view(16,84) % rotated view VG
            zlim([-2 2])
            set(gca,'Ydir','reverse')
            shading interp
            axis equal
            xlim([0 L]); 
            xlabel('z, m'); ylabel('x, m');
            set(gca, 'FontSize', 12);
            tl=title({['Flutter Modeshapes at UF= ' num2str(UF,'%0.3f') ' m/s']; titleModeFlutter});
            tl.FontWeight='normal'; tl.FontSize=12;

            %% 3D animation of the coupled modes v(x,z)
            if ifanimation
                Nc=5; Nt=1e2; t=linspace(0,Nc/f(mode),Nt); % define time range over 5 cycles
                animation = VideoWriter(titleModeFlutter);
                animation.FrameRate = 10; %% time interval between two frame
                animation.Quality =100; open(animation);
                Vxz=zeros(Nx,Nz);
                zmax=1.2;
                for k=1:Nt
                    for i=1:Nx
                        Vxz(i,:)=(W*V(1:NW,mode)-x(i)*Phi*V(NW+1:NW+NPhi,mode))...
                            *exp(1i*2*pi*f(mode)*t(k));
                    end
                    figure(100) % figure(100) is used to generate the animation
                    surf(zL,x,real(Vxz)); % surf plot
                    view(16,84) % rotated view VG
                    set(gca,'Ydir','reverse')
                    shading interp
                    axis equal
                    xlim([0 L]); ylim([-c/2 c/2]); zlim([-zmax zmax]); 
                    xlabel('z, m'); ylabel('x, m');
                    set(gca, 'FontSize', 12);
                    tl=title({['Flutter Modeshapes at UF= ' num2str(UF)]; titleModeFlutter});
                    tl.FontWeight='normal'; tl.FontSize=12;
                    thisFrame = getframe(gcf);
                    writeVideo(animation, thisFrame);
                end
                close(animation);
            end % ifanimation ends here
        end % mode loop ends here
    end % ifFlutterModes loop ends here
end % ifFlutter ends here

%% finish
display(' ')
display (['success! ' mfilename ' finished successfully'])
